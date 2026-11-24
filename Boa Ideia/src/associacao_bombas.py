"""Associação de bombas centrífugas em série, paralelo e forma aninhada.

Mantém a interface pública da versão anterior do AquaPump. As curvas
combinadas são armazenadas com vazão crescente, para garantir interpolação
numérica consistente. O NPSHr agregado é um indicador conservador (máximo
entre os elementos); a validação de NPSH deve continuar a ser feita por bomba.
"""
from __future__ import annotations

import json
from typing import Callable, Iterable, Optional

import numpy as np

try:
    from .bomba import Bomba, BombaError, encontrar_ponto_operacao
except ImportError:
    from bomba import Bomba, BombaError, encontrar_ponto_operacao

__all__ = [
    "AssociacaoBombas", "curva_sistema_simples", "curva_sistema_de_perdas",
    "encontrar_ponto_operacao_associacao",
]


class AssociacaoBombas:
    """Combina duas ou mais bombas/associações em série ou paralelo."""

    TIPOS_VALIDOS = ("serie", "paralelo")

    def __init__(self, elementos: Iterable, tipo: str = "serie", nome: Optional[str] = None):
        self.elementos = list(elementos)
        if len(self.elementos) < 2:
            raise BombaError("Uma associação requer pelo menos dois elementos.")
        tipo = str(tipo).strip().lower()
        if tipo not in self.TIPOS_VALIDOS:
            raise BombaError(f"Tipo de associação inválido: {tipo!r}.")
        for elemento in self.elementos:
            if not isinstance(elemento, (Bomba, AssociacaoBombas)):
                raise BombaError("Cada elemento deve ser uma Bomba ou AssociacaoBombas.")
        self.tipo = tipo
        self.nome = nome or f"Associação ({tipo}, {len(self.elementos)} elementos)"
        self._validar_coerencia()
        primeiro = self.elementos[0]
        for attr in ("fluido", "T", "P", "rho", "g", "P_vapor"):
            setattr(self, attr, getattr(primeiro, attr))
        self._Q = self._H = self._P = self._eta = self._npsh_r = None
        self._Q_por_elemento: dict[str, np.ndarray] = {}
        self._calcular_curva_combinada()

    def _validar_coerencia(self) -> None:
        primeiro = self.elementos[0]
        for elemento in self.elementos[1:]:
            if elemento.fluido != primeiro.fluido:
                raise BombaError("Todos os elementos devem utilizar o mesmo fluido.")
            for attr, rotulo in (("T", "temperatura"), ("P", "pressão")):
                if not np.isclose(getattr(elemento, attr), getattr(primeiro, attr), rtol=1e-8, atol=1e-10):
                    raise BombaError(f"Elementos com {rotulo} diferentes não podem ser associados nesta versão.")

    @staticmethod
    def _tem(elemento, grandeza: str) -> bool:
        try:
            return bool(elemento.tem_grandeza(grandeza))
        except AttributeError:
            try:
                elemento._avaliar(grandeza, elemento.Q_min())
                return True
            except Exception:
                return False

    def _todos_tem(self, grandeza: str) -> bool:
        return all(self._tem(e, grandeza) for e in self.elementos)

    def _calcular_curva_combinada(self, n: int = 600) -> None:
        if self.tipo == "serie":
            self._curva_serie(n)
        else:
            self._curva_paralelo(n)
        self._eta = self._calcular_rendimento(self._Q, self._H, self._P)

    def _calcular_rendimento(self, q, h, p):
        if p is None:
            return None
        p_hid = self.rho * self.g * np.asarray(q) * np.asarray(h)
        p = np.asarray(p, dtype=float)
        return np.divide(p_hid, p, out=np.full_like(p_hid, np.nan, dtype=float), where=p > 1e-12)

    def _curva_serie(self, n: int) -> None:
        q_min = max(float(e.Q_min()) for e in self.elementos)
        q_max = min(float(e.Q_max()) for e in self.elementos)
        if not q_min < q_max:
            raise BombaError("As bombas em série não têm uma faixa de vazão comum.")
        q = np.linspace(q_min, q_max, n)
        h = np.zeros_like(q)
        p = np.zeros_like(q) if self._todos_tem("P") else None
        npsh = np.zeros_like(q) if self._todos_tem("npsh") else None
        self._Q_por_elemento = {}
        for i, elemento in enumerate(self.elementos, start=1):
            h += np.asarray(elemento.H_de_Q(q), dtype=float)
            self._Q_por_elemento[f"{getattr(elemento, 'nome', f'Elemento {i}')}"] = q.copy()
            if p is not None:
                p += np.asarray(elemento.P_de_Q(q), dtype=float)
            if npsh is not None:
                # NPSHr não se soma em série: guarda-se o pior requisito
                # individual como indicador agregado, não como NPSHa do conjunto.
                npsh = np.maximum(npsh, np.asarray(elemento.npsh_de_Q(q), dtype=float))
        self._Q, self._H, self._P, self._npsh_r = q, h, p, npsh

    def _curva_paralelo(self, n: int) -> None:
        h_shutoff = []
        for elemento in self.elementos:
            h0 = float(elemento.H_de_Q(elemento.Q_min()))
            if not np.isfinite(h0) or h0 < 0:
                raise BombaError(f"Curva de altura inválida em '{getattr(elemento, 'nome', 'elemento')}'.")
            h_shutoff.append(h0)
        h_max = max(h_shutoff)
        if h_max <= 0:
            raise BombaError("A altura de fecho das bombas deve ser positiva.")
        h_grid = np.linspace(0.0, h_max, n)
        q_total = np.zeros_like(h_grid)
        p_total = np.zeros_like(h_grid) if self._todos_tem("P") else None
        npsh_max = np.zeros_like(h_grid) if self._todos_tem("npsh") else None
        q_components: dict[str, np.ndarray] = {}

        for i, (elemento, h_stop) in enumerate(zip(self.elementos, h_shutoff), start=1):
            nome = getattr(elemento, "nome", f"Elemento {i}")
            q_i = np.asarray(elemento.Q_de_H(h_grid), dtype=float)
            # Acima da altura de fecho o ramo não fornece vazão.
            inativo = h_grid > h_stop + max(1e-10, h_max * 1e-10)
            q_i = np.where(inativo, 0.0, q_i)
            q_i = np.maximum(q_i, 0.0)
            q_components[nome] = q_i
            q_total += q_i
            if p_total is not None:
                p_i = np.asarray(elemento.P_de_Q(np.clip(q_i, elemento.Q_min(), elemento.Q_max())), dtype=float)
                p_total += np.where(inativo, 0.0, p_i)
            if npsh_max is not None:
                n_i = np.asarray(elemento.npsh_de_Q(np.clip(q_i, elemento.Q_min(), elemento.Q_max())), dtype=float)
                npsh_max = np.maximum(npsh_max, np.where(inativo, 0.0, n_i))

        # Converter H crescente / Q decrescente para Q crescente.
        order = np.argsort(q_total, kind="mergesort")
        q_sorted = q_total[order]
        h_sorted = h_grid[order]
        p_sorted = None if p_total is None else p_total[order]
        n_sorted = None if npsh_max is None else npsh_max[order]
        unique_q = np.unique(q_sorted)
        h_unique = np.empty_like(unique_q)
        p_unique = None if p_sorted is None else np.empty_like(unique_q)
        n_unique = None if n_sorted is None else np.empty_like(unique_q)
        for j, q_value in enumerate(unique_q):
            idxs = np.flatnonzero(np.isclose(q_sorted, q_value, rtol=1e-10, atol=1e-13))
            # Em caso de vazão repetida, manter a maior altura correspondente.
            idx = idxs[int(np.argmax(h_sorted[idxs]))]
            h_unique[j] = h_sorted[idx]
            if p_unique is not None:
                p_unique[j] = p_sorted[idx]
            if n_unique is not None:
                n_unique[j] = n_sorted[idx]

        if unique_q.size < 2 or np.any(np.diff(unique_q) <= 0):
            raise BombaError("Não foi possível construir uma curva paralela válida.")
        self._Q, self._H, self._P, self._npsh_r = unique_q, h_unique, p_unique, n_unique
        self._Q_por_elemento = {k: v for k, v in q_components.items()}

    def tem_grandeza(self, grandeza: str) -> bool:
        key = "npsh" if grandeza in ("npsh", "npsh_r") else grandeza
        return {"H": self._H, "P": self._P, "eta": self._eta, "npsh": self._npsh_r}.get(key) is not None

    def _avaliar(self, grandeza: str, Q_alvo):
        key = "npsh" if grandeza == "npsh_r" else grandeza
        arr = {"H": self._H, "P": self._P, "eta": self._eta, "npsh": self._npsh_r}.get(key)
        if arr is None:
            rotulo = "NPSHr" if key == "npsh" else key.upper()
            raise BombaError(f"Curva '{rotulo}' não disponível na associação.")
        q = np.asarray(Q_alvo, dtype=float)
        if not np.all(np.isfinite(q)):
            raise BombaError("A vazão de consulta deve ser finita.")
        tol = max(1e-12, (self._Q[-1] - self._Q[0]) * 1e-10)
        if np.any(q < self._Q[0] - tol) or np.any(q > self._Q[-1] + tol):
            raise BombaError(
                f"Vazão fora da curva da associação: [{self._Q[0]:.6g}, {self._Q[-1]:.6g}] m³/s."
            )
        # Potência/rendimento/NPSH podem não ter dados válidos no ponto Q=0
        # (por exemplo, quando P é inferida de eta=0). Não interpolar NaN:
        # devolver NaN apenas na região sem dados e preservar o resto da curva.
        mask = np.isfinite(arr)
        if int(mask.sum()) < 2:
            result = np.full_like(q, np.nan, dtype=float)
            if int(mask.sum()) == 1:
                result = np.where(np.isclose(q, self._Q[mask][0]), arr[mask][0], result)
        else:
            xp, fp = self._Q[mask], np.asarray(arr)[mask]
            result = np.interp(q, xp, fp)
            result = np.where((q < xp[0] - tol) | (q > xp[-1] + tol), np.nan, result)
        return float(result) if np.ndim(result) == 0 else result

    def _validar_vazao(self, Q):
        q = np.asarray(Q, dtype=float)
        if not np.all(np.isfinite(q)):
            raise BombaError("A vazão de consulta deve ser finita.")
        tol = max(1e-12, (self._Q[-1] - self._Q[0]) * 1e-10)
        if np.any(q < self._Q[0] - tol) or np.any(q > self._Q[-1] + tol):
            raise BombaError(
                f"Vazão fora da curva da associação: [{self._Q[0]:.6g}, {self._Q[-1]:.6g}] m³/s."
            )
        return np.clip(q, self._Q[0], self._Q[-1])

    def H_de_Q(self, Q):
        q = self._validar_vazao(Q)
        if self.tipo == "serie":
            values = sum(np.asarray(e.H_de_Q(q), dtype=float) for e in self.elementos)
            return float(values) if np.ndim(values) == 0 else values
        return self._avaliar("H", q)

    def P_de_Q(self, Q):
        q = self._validar_vazao(Q)
        if self.tipo == "serie":
            if not self._todos_tem("P"):
                raise BombaError("A potência no eixo não está disponível em todas as bombas.")
            values = sum(np.asarray(e.P_de_Q(q), dtype=float) for e in self.elementos)
            return float(values) if np.ndim(values) == 0 else values
        return self._avaliar("P", q)

    def eta_de_Q(self, Q):
        q = self._validar_vazao(Q)
        if self.tipo == "serie":
            p = np.asarray(self.P_de_Q(q), dtype=float)
            h = np.asarray(self.H_de_Q(q), dtype=float)
            hydraulic = self.rho * self.g * q * h
            values = np.divide(hydraulic, p, out=np.full_like(np.asarray(hydraulic), np.nan, dtype=float), where=p > 1e-12)
            return float(values) if np.ndim(values) == 0 else values
        return self._avaliar("eta", q)

    def npsh_de_Q(self, Q):
        q = self._validar_vazao(Q)
        if self.tipo == "serie":
            if not self._todos_tem("npsh"):
                raise BombaError("NPSHr não está disponível em todas as bombas.")
            values = np.maximum.reduce([np.asarray(e.npsh_de_Q(q), dtype=float) for e in self.elementos])
            return float(values) if np.ndim(values) == 0 else values
        return self._avaliar("npsh", q)

    def npsh_por_elemento(self, Q_total: float) -> dict[str, float]:
        """Devolve NPSHr de cada bomba na condição de vazão correspondente.

        Em paralelo, a vazão de cada ramo é estimada à altura comum da
        associação. Em série, todas as bombas recebem a mesma vazão.
        """
        if not self._todos_tem("npsh"):
            raise BombaError("Uma ou mais bombas não têm curva NPSHr.")
        q_total = float(Q_total)
        h_total = float(self.H_de_Q(q_total))
        resultado = {}
        if self.tipo == "serie":
            for i, elemento in enumerate(self.elementos, start=1):
                nome = getattr(elemento, "nome", f"Elemento {i}")
                resultado[nome] = float(elemento.npsh_de_Q(q_total))
        else:
            for i, elemento in enumerate(self.elementos, start=1):
                nome = getattr(elemento, "nome", f"Elemento {i}")
                q_i = float(elemento.Q_de_H(h_total))
                if h_total > float(elemento.H_de_Q(elemento.Q_min())) + 1e-10:
                    resultado[nome] = float("nan")  # ramo sem escoamento
                    continue
                q_i = float(np.clip(q_i, elemento.Q_min(), elemento.Q_max()))
                resultado[nome] = float(elemento.npsh_de_Q(q_i))
        return resultado

    def Q_de_H(self, H_alvo):
        scalar = np.ndim(H_alvo) == 0
        h_targets = np.atleast_1d(np.asarray(H_alvo, dtype=float))
        if not np.all(np.isfinite(h_targets)):
            raise BombaError("A altura de consulta deve ser finita.")
        # A curva H(Q) de uma associação convencional deve ser decrescente.
        order = np.argsort(self._H, kind="mergesort")
        h_sorted, q_sorted = self._H[order], self._Q[order]
        scale = max(1.0, float(np.max(np.abs(h_sorted))))
        if np.any(np.diff(self._H) > scale * 1e-7):
            raise BombaError(
                "A curva H(Q) da associação não é monotonicamente decrescente; "
                "a inversão H para Q é ambígua."
            )
        h_unique, first = np.unique(h_sorted, return_index=True)
        q_unique = q_sorted[first]
        q = np.interp(h_targets, h_unique, q_unique)
        q = np.where(h_targets >= h_unique[-1], q_unique[-1], q)
        q = np.where(h_targets <= h_unique[0], q_unique[0], q)
        return float(q[0]) if scalar else q

    def Q_min(self) -> float:
        return float(self._Q.min())

    def Q_max(self) -> float:
        return float(self._Q.max())

    def H_shutoff(self) -> float:
        if not np.isclose(self.Q_min(), 0.0, atol=1e-12):
            raise BombaError("A associação não tem ponto de vazão zero na faixa validada.")
        return float(self._H[0])

    def Q_bep(self) -> Optional[float]:
        if self._eta is None:
            return None
        eta = np.asarray(self._eta, dtype=float)
        valid = np.isfinite(eta)
        if not np.any(valid):
            return None
        return float(self._Q[np.flatnonzero(valid)[np.argmax(eta[valid])]])

    def curva(self, n_pontos: int = 200) -> dict:
        if not isinstance(n_pontos, int) or n_pontos < 2:
            raise BombaError("n_pontos deve ser um inteiro igual ou superior a 2.")
        q = np.linspace(self.Q_min(), self.Q_max(), n_pontos)
        out = {"Q": q, "H": self.H_de_Q(q)}
        if self._P is not None:
            out["P"] = self.P_de_Q(q)
        if self._eta is not None:
            out["eta"] = self.eta_de_Q(q)
        if self._npsh_r is not None:
            out["npsh_r"] = self.npsh_de_Q(q)
        return out

    def ponto_operacao(
        self, H_sistema_fn: Callable[[float], float],
        Q_intervalo: Optional[tuple[float, float]] = None,
    ) -> dict:
        return encontrar_ponto_operacao_associacao(self, H_sistema_fn, Q_intervalo)

    def to_dict(self) -> dict:
        return {
            "tipo": "AssociacaoBombas", "subtipo": self.tipo, "nome": self.nome,
            "elementos": [e.to_dict() for e in self.elementos],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AssociacaoBombas":
        if not isinstance(data, dict) or data.get("subtipo") not in cls.TIPOS_VALIDOS:
            raise BombaError("Dados de associação inválidos.")
        elementos = []
        for item in data.get("elementos", []):
            if item.get("tipo") == "Bomba":
                elementos.append(Bomba.from_dict(item))
            elif item.get("tipo") == "AssociacaoBombas":
                elementos.append(cls.from_dict(item))
            else:
                raise BombaError(f"Tipo de elemento desconhecido: {item.get('tipo')!r}.")
        return cls(elementos, data["subtipo"], nome=data.get("nome"))

    def salvar_json(self, caminho: str) -> None:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def carregar_json(cls, caminho: str) -> "AssociacaoBombas":
        with open(caminho, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def __repr__(self) -> str:
        return (
            f"AssociacaoBombas({self.tipo}, Q=[{self.Q_min():.3g}, "
            f"{self.Q_max():.3g}] m³/s, n={len(self.elementos)})"
        )


def curva_sistema_simples(
    H_geometrico: float, K: float = 0.0, Q_offset: float = 0.0,
) -> Callable[[float], float]:
    """Curva simplificada H(Q) = H_geo + K*(Q-Q_offset)^2."""
    h_geo, k, q_off = map(float, (H_geometrico, K, Q_offset))
    if not all(np.isfinite(v) for v in (h_geo, k, q_off)) or h_geo < 0 or k < 0:
        raise BombaError("Parâmetros inválidos para a curva simplificada do sistema.")
    def h_sistema(q: float) -> float:
        q = float(q)
        if not np.isfinite(q) or q < 0:
            raise BombaError("A vazão deve ser finita e não negativa.")
        return h_geo + k * (q - q_off) ** 2
    return h_sistema


def curva_sistema_de_perdas(
    H_geometrico: float,
    perdas_obj,
    comprimento_m: float,
    material: str,
    incluir_localizadas: bool = True,
    incluir_hazen: bool = False,
) -> Callable[[float], float]:
    """Constrói a curva do sistema usando Darcy-Weisbach ou Hazen-Williams.

    Os métodos Darcy-Weisbach e Hazen-Williams são alternativos para as
    perdas distribuídas; não são somados entre si. As perdas localizadas
    podem ser adicionadas a qualquer um dos métodos.
    """
    h_geo, comprimento = float(H_geometrico), float(comprimento_m)
    if not np.isfinite(h_geo) or h_geo < 0:
        raise BombaError("Altura geométrica inválida.")
    if not np.isfinite(comprimento) or comprimento < 0:
        raise BombaError("Comprimento de tubulação inválido.")
    def h_sistema(q: float) -> float:
        q = float(q)
        if not np.isfinite(q) or q < 0:
            raise BombaError("A vazão deve ser finita e não negativa.")
        if q <= 1e-12:
            return h_geo
        perdas_obj.atualizar_parametros(vazao_m3s=q)
        if incluir_hazen:
            perdas_obj.definir_material_hazen(material)
            h_distribuida = perdas_obj.calcular_perda_carga_hazen_williams(comprimento)
        else:
            perdas_obj.definir_material_darcy(material)
            h_distribuida = perdas_obj.calcular_perda_carga_darcy(comprimento)
        h_localizada = perdas_obj.calcular_perdas_localizadas() if incluir_localizadas else 0.0
        total = h_geo + float(h_distribuida) + float(h_localizada)
        if not np.isfinite(total) or total < 0:
            raise BombaError("O cálculo da curva do sistema produziu um resultado inválido.")
        return total
    return h_sistema


def encontrar_ponto_operacao_associacao(
    associacao, H_sistema_fn, Q_intervalo=None,
) -> dict:
    """Wrapper de compatibilidade para o solver de ponto de operação."""
    resultado = encontrar_ponto_operacao(associacao, H_sistema_fn, Q_intervalo)
    if resultado["Q"] > 0.95 * associacao.Q_max():
        resultado["avisos"].append("Operação próxima do limite superior da curva combinada.")
    return resultado
