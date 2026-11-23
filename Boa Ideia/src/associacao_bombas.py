"""Associação de bombas — série, paralelo e aninhamento arbitrário.

`AssociacaoBombas` implementa a MESMA interface de `Bomba`
(H_de_Q, Q_de_H, P_de_Q, eta_de_Q, npsh_de_Q, Q_min, Q_max, H_shutoff,
curva, ponto_operacao), o que permite:

    (B1 + B2 em série)  em paralelo com  B3
    ──────────────────────────────────────────
    AssociacaoBombas(
        [AssociacaoBombas([b1, b2], "serie"), b3],
        "paralelo",
    )

Unidades internas: idênticas a `Bomba` (SI).
"""

from __future__ import annotations

import json
from typing import Callable, Iterable, Optional, Union

import numpy as np
from scipy.optimize import brentq

try:                                     # pacote
    from .bomba import Bomba, BombaError
except ImportError:                      # execução direta
    from bomba import Bomba, BombaError

__all__ = [
    "AssociacaoBombas",
    "curva_sistema_simples",
    "curva_sistema_de_perdas",
    "encontrar_ponto_operacao_associacao",
]


# =====================================================================
# Associação
# =====================================================================
class AssociacaoBombas:
    """Combina N elementos (Bomba ou AssociacaoBombas) em série ou paralelo."""

    TIPOS_VALIDOS = ("serie", "paralelo")

    # ------------------------------------------------------------------ #
    def __init__(self, elementos: Iterable, tipo: str = "serie",
                 nome: Optional[str] = None):
        self.elementos = list(elementos)
        if not self.elementos:
            raise BombaError("Associação sem elementos.")
        if tipo not in self.TIPOS_VALIDOS:
            raise BombaError(f"Tipo inválido: {tipo!r}.")
        self.tipo = tipo
        self.nome = nome or f"Associação ({tipo}, {len(self.elementos)}×)"

        self._validar_coerencia()
        # Herda propriedades do fluido do primeiro elemento
        self.fluido = self.elementos[0].fluido
        self.T = self.elementos[0].T
        self.P = self.elementos[0].P
        self.rho = self.elementos[0].rho
        self.g = self.elementos[0].g
        self.P_vapor = self.elementos[0].P_vapor

        self._calcular_curva_combinada()

    # ------------------------------------------------------------------ #
    def _validar_coerencia(self) -> None:
        for attr, rotulo in (
            ("fluido", "fluido"), ("T", "temperatura"), ("P", "pressão"),
        ):
            valores = {getattr(e, attr) for e in self.elementos}
            if len(valores) > 1:
                raise BombaError(
                    f"Elementos com {rotulo} diferentes: {valores}"
                )

    # ------------------------------------------------------------------ #
    # Curva combinada
    # ------------------------------------------------------------------ #
    def _calcular_curva_combinada(self) -> None:
        if self.tipo == "serie":
            self._curva_serie()
        else:
            self._curva_paralelo()

        # Guardar disponibilidade de cada grandeza
        self._tem_P    = all(self._safe(e, "P",     0.0) is not None
                             for e in self.elementos)
        self._tem_eta  = all(self._safe(e, "eta",   0.0) is not None
                             for e in self.elementos)
        self._tem_npsh = all(self._safe(e, "npsh",  0.0) is not None
                             for e in self.elementos)

    @staticmethod
    def _safe(elemento, grandeza, q):
        try:
            return float(elemento._avaliar(grandeza, q))
        except (BombaError, AttributeError):
            return None

    def _curva_serie(self, n: int = 400) -> None:
        # Série: mesma Q, H soma → intervalo = interseção dos Q
        q_lo = max(e.Q_min() for e in self.elementos)
        q_hi = min(e.Q_max() for e in self.elementos)
        if q_lo >= q_hi:
            raise BombaError(
                "Bombas em série sem faixa de vazão comum."
            )
        Q = np.linspace(q_lo, q_hi, n)
        H = np.zeros_like(Q)
        P = np.zeros_like(Q) if self._all_have("P")   else None
        for e in self.elementos:
            H += e.H_de_Q(Q)
            if P is not None:
                P += e.P_de_Q(Q)

        self._Q = Q
        self._H = H
        self._P = P
        self._eta = self._derivar_eta(Q, H, P)
        self._npsh_r = self._combinar_npsh_serie(Q)

    def _curva_paralelo(self, n: int = 400) -> None:
        H_shut_max = max(
            float(np.max(e.H_de_Q(e.Q_min()))) for e in self.elementos
        )
        H = np.linspace(0.0, H_shut_max, n)
        Q = np.zeros_like(H)
        P = np.zeros_like(H) if self._all_have("P")   else None
        for e in self.elementos:
            Qe = np.atleast_1d(e.Q_de_H(H))
            H_shut_e = float(np.max(e.H_de_Q(e.Q_min())))
            Qe = np.where(H > H_shut_e, 0.0, Qe)
            Q += Qe
            if P is not None:
                Pe = np.atleast_1d(e.P_de_Q(Qe))
                Pe = np.where(H > H_shut_e, 0.0, Pe)
                P += Pe

        # Ordenar por H crescente (já está) → Q decrescente é OK
        self._Q = Q          # vazão total (diminui com H)
        self._H = H
        self._P = P
        self._eta = self._derivar_eta(Q, H, P)
        self._npsh_r = self._combinar_npsh_paralelo(H)

    def _all_have(self, grandeza: str) -> bool:
        for e in self.elementos:
            try:
                e._avaliar(grandeza, 0.0)
            except (BombaError, AttributeError):
                return False
        return True

    def _derivar_eta(self, Q, H, P):
        if P is None:
            return None
        P_hid = self.rho * self.g * Q * H
        with np.errstate(divide="ignore", invalid="ignore"):
            eta = np.where(P > 0, P_hid / P, 0.0)
        return eta

    def _combinar_npsh_serie(self, Q):
        if not self._all_have("npsh"):
            return None
        npsh = np.zeros_like(Q)
        for e in self.elementos:
            npsh += e.npsh_de_Q(Q)
        return npsh

    def _combinar_npsh_paralelo(self, H):
        if not self._all_have("npsh"):
            return None
        # Para cada H, o NPSHr da associação ≈ máximo dos NPSHr dos que operam
        npsh = np.zeros_like(H)
        for e in self.elementos:
            Qe = np.atleast_1d(e.Q_de_H(H))
            H_shut = float(np.max(e.H_de_Q(e.Q_min())))
            npsh_e = np.atleast_1d(e.npsh_de_Q(Qe))
            npsh_e = np.where(H > H_shut, 0.0, npsh_e)
            npsh = np.maximum(npsh, npsh_e)
        return npsh

    # ------------------------------------------------------------------ #
    # Interface pública (espelha Bomba)
    # ------------------------------------------------------------------ #
    def _avaliar(self, grandeza: str, Q_alvo):
        arr = {
            "H": self._H, "P": self._P,
            "eta": self._eta, "npsh": self._npsh_r,
        }[grandeza]
        if arr is None:
            nome_attr = "npsh_r" if grandeza == "npsh" else grandeza.upper()
            raise BombaError(f"Curva '{nome_attr}' não disponível na associação.")
        return np.interp(Q_alvo, self._Q, arr)

    def H_de_Q(self, Q):     return self._avaliar("H", Q)
    def P_de_Q(self, Q):     return self._avaliar("P", Q)
    def eta_de_Q(self, Q):   return self._avaliar("eta", Q)
    def npsh_de_Q(self, Q):  return self._avaliar("npsh", Q)

    def Q_de_H(self, H_alvo):
        escalar = np.ndim(H_alvo) == 0
        H_arr = np.atleast_1d(np.asarray(H_alvo, dtype=float))

        ordem = np.argsort(self._H)
        H_sorted, Q_sorted = self._H[ordem], self._Q[ordem]

        Q = np.interp(H_arr, H_sorted, Q_sorted)
        Q = np.where(H_arr >= H_sorted[-1], 0.0, Q)
        return float(Q[0]) if escalar else Q

    def Q_min(self) -> float: return float(self._Q.min())
    def Q_max(self) -> float: return float(self._Q.max())
    def H_shutoff(self) -> float:
        return float(np.interp(0.0, self._Q, self._H))

    def Q_bep(self) -> Optional[float]:
        if self._eta is None:
            return None
        return float(self._Q[int(np.nanargmax(self._eta))])

    def curva(self, n_pontos: int = 200) -> dict:
        if self.tipo == "serie":
            Q = np.linspace(self.Q_min(), self.Q_max(), n_pontos)
            out = {"Q": Q, "H": self.H_de_Q(Q)}
            if self._P    is not None: out["P"]      = self.P_de_Q(Q)
            if self._eta  is not None: out["eta"]    = self.eta_de_Q(Q)
            if self._npsh_r is not None: out["npsh_r"] = self.npsh_de_Q(Q)
        else:  # paralelo
            H = np.linspace(0.0, self._H.max(), n_pontos)
            Q = np.atleast_1d(self.Q_de_H(H))
            out = {"Q": Q, "H": H}
            if self._P is not None:
                out["P"] = np.interp(Q, self._Q, self._P)
            if self._eta is not None:
                out["eta"] = np.interp(Q, self._Q, self._eta)
            if self._npsh_r is not None:
                out["npsh_r"] = np.interp(Q, self._Q, self._npsh_r)
        return out

    # ------------------------------------------------------------------ #
    def ponto_operacao(
        self, H_sistema_fn: Callable[[float], float],
        Q_intervalo: Optional[tuple[float, float]] = None,
    ) -> dict:
        return encontrar_ponto_operacao_associacao(
            self, H_sistema_fn, Q_intervalo
        )

    # ------------------------------------------------------------------ #
    # Serialização recursiva
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        return {
            "tipo": "AssociacaoBombas",
            "subtipo": self.tipo,
            "nome": self.nome,
            "elementos": [e.to_dict() for e in self.elementos],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AssociacaoBombas":
        elementos = []
        for ed in d["elementos"]:
            if ed["tipo"] == "Bomba":
                elementos.append(Bomba.from_dict(ed))
            elif ed["tipo"] == "AssociacaoBombas":
                elementos.append(cls.from_dict(ed))
            else:
                raise BombaError(f"Tipo desconhecido: {ed['tipo']}")
        return cls(elementos, d["subtipo"], nome=d.get("nome"))

    def salvar_json(self, caminho: str) -> None:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def carregar_json(cls, caminho: str) -> "AssociacaoBombas":
        with open(caminho, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:
        return (
            f"AssociacaoBombas({self.tipo}, "
            f"Q=[{self.Q_min():.3g}, {self.Q_max():.3g}] m³/s, "
            f"n={len(self.elementos)})"
        )


# =====================================================================
# Construtores de curva do sistema
# =====================================================================
def curva_sistema_simples(
    H_geometrico: float, K: float = 0.0, Q_offset: float = 0.0,
) -> Callable[[float], float]:
    """H(Q) = H_geo + K·(Q - Q_offset)²  (regime turbulento simplificado)."""
    def H_sist(q: float) -> float:
        return H_geometrico + K * (q - Q_offset) ** 2
    return H_sist


def curva_sistema_de_perdas(
    H_geometrico: float,
    perdas_obj,
    comprimento_m: float,
    material: str,
    incluir_localizadas: bool = True,
    incluir_hazen: bool = False,
) -> Callable[[float], float]:
    """Curva do sistema construída a partir do módulo `perdas_cargas.Perdas`.

    Aceita `perdas_obj` já configurado (acessórios, etc.). O material é
    aplicado a Darcy (e opcionalmente Hazen‑Williams).
    """
    def H_sist(q: float) -> float:
        if q <= 1e-9:
            return H_geometrico
        perdas_obj.atualizar_parametros(vazao_m3s=q)
        perdas_obj.definir_material_darcy(material)
        h = perdas_obj.calcular_perda_carga_darcy(comprimento_m)
        if incluir_localizadas:
            h += perdas_obj.calcular_perdas_localizadas()
        if incluir_hazen:
            perdas_obj.definir_material_hazen(material)
            h += perdas_obj.calcular_perda_carga_hazen_williams(comprimento_m)
        return H_geometrico + h
    return H_sist


# =====================================================================
# Ponto de operação para associações
# =====================================================================
def encontrar_ponto_operacao_associacao(
    associacao, H_sistema_fn, Q_intervalo=None,
) -> dict:
    """Wrapper que reutiliza a lógica de `bomba.encontrar_ponto_operacao`."""
    try:
        from .bomba import encontrar_ponto_operacao
    except ImportError:
        from bomba import encontrar_ponto_operacao

    resultado = encontrar_ponto_operacao(
        associacao, H_sistema_fn, Q_intervalo
    )
    # Aviso adicional: operação fora da faixa recomendada da associação
    Qop = resultado["Q"]
    if Qop > 0.95 * associacao.Q_max():
        resultado["avisos"].append("Operação no limite superior da curva.")
    return resultado


# =====================================================================
# Smoke test
# =====================================================================
if __name__ == "__main__":
    Q = np.array([0, 5, 10, 15, 20]) / 3600.0
    H = np.array([45, 43, 38, 30, 15])
    eta = np.array([0, 35, 55, 60, 40]) / 100.0
    NPSH = np.array([1.5, 2.0, 2.5, 3.5, 5.0])

    b1 = Bomba("B1", rpm=3500); b1.definir_dados(Q, H, eta=eta, npsh_r=NPSH)
    b2 = Bomba("B2", rpm=3500); b2.definir_dados(Q, H * 0.95, eta=eta, npsh_r=NPSH)

    serie    = AssociacaoBombas([b1, b2], "serie")
    paralelo = AssociacaoBombas([b1, b2], "paralelo")

    print(serie)
    print(f"  H_shutoff(série)    = {serie.H_shutoff():.2f} m "
          f"(≈ {b1.H_shutoff() + b2.H_shutoff():.2f})")
    print(paralelo)
    print(f"  Q_max(paralelo)     = {paralelo.Q_max()*3600:.2f} m³/h "
          f"(≈ {(b1.Q_max() + b2.Q_max())*3600:.2f})")

    H_sist = curva_sistema_simples(10.0, K=5e5)
    op_s = serie.ponto_operacao(H_sist)
    op_p = paralelo.ponto_operacao(H_sist)
    print(f"Série    → Q={op_s['Q']*3600:6.2f} m³/h  H={op_s['H']:5.2f} m")
    print(f"Paralelo → Q={op_p['Q']*3600:6.2f} m³/h  H={op_p['H']:5.2f} m")

    # Aninhamento: (B1+B2 série) em paralelo com B1
    nested = AssociacaoBombas([serie, b1], "paralelo")
    print(nested)
    print(f"  Q_max(nested)       = {nested.Q_max()*3600:.2f} m³/h")

    # Round-trip JSON
    import tempfile, os
    p = os.path.join(tempfile.gettempdir(), "bombas.json")
    nested.salvar_json(p)
    reconstruida = AssociacaoBombas.carregar_json(p)
    print(f"  JSON round-trip OK  → {reconstruida}")