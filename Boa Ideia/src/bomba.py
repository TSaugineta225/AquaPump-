"""Modelo de bombas centrífugas para o AquaPump.

Unidades internas SI:
    Q [m³/s], H [m], P_shaft [W], eta [-], NPSHr [m].

A API pública da versão anterior é mantida. As curvas passam a usar
interpolação PCHIP (shape-preserving), sem extrapolação silenciosa.
"""
from __future__ import annotations

import json
from typing import Callable, Optional

import numpy as np
from CoolProp.CoolProp import PropsSI
from scipy.constants import g as G_CONST
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

__all__ = ["Bomba", "BombaError", "encontrar_ponto_operacao", "para_plot"]

FLUIDO_PADRAO = "Water"
T_PADRAO = 293.15
P_PADRAO = 101325.0


class BombaError(ValueError):
    """Erro de domínio ou de dados no modelo da bomba."""


def _array_1d(
    nome: str, valores, tamanho: int | None = None, allow_nan: bool = False
) -> np.ndarray:
    try:
        arr = np.asarray(valores, dtype=float)
    except (TypeError, ValueError) as exc:
        raise BombaError(f"'{nome}' deve conter valores numéricos.") from exc
    if arr.ndim != 1 or arr.size < 2:
        raise BombaError(f"'{nome}' deve ser um vector 1-D com pelo menos 2 pontos.")
    if tamanho is not None and arr.size != tamanho:
        raise BombaError(f"'{nome}' deve ter {tamanho} valores, mas tem {arr.size}.")
    if np.any(np.isinf(arr)) or (not allow_nan and np.any(np.isnan(arr))):
        raise BombaError(f"'{nome}' contém valores NaN ou infinitos.")
    return arr.copy()


class Bomba:
    """Representa uma bomba centrífuga através das curvas do fabricante."""

    def __init__(
        self,
        nome: str = "Bomba",
        fluido: str = FLUIDO_PADRAO,
        T: float = T_PADRAO,
        P: float = P_PADRAO,
        rpm: Optional[float] = None,
        diametro_rotor_mm: Optional[float] = None,
    ):
        self.nome = str(nome)
        self.fluido = str(fluido)
        self.T = float(T)
        self.P = float(P)
        if not np.isfinite(self.T) or self.T <= 0:
            raise BombaError("A temperatura absoluta deve ser positiva e finita.")
        if not np.isfinite(self.P) or self.P <= 0:
            raise BombaError("A pressão absoluta deve ser positiva e finita.")
        self.rpm = None if rpm is None else float(rpm)
        self.diametro_rotor_mm = (
            None if diametro_rotor_mm is None else float(diametro_rotor_mm)
        )
        if self.rpm is not None and (not np.isfinite(self.rpm) or self.rpm <= 0):
            raise BombaError("A rotação deve ser positiva e finita.")
        if self.diametro_rotor_mm is not None and (
            not np.isfinite(self.diametro_rotor_mm) or self.diametro_rotor_mm <= 0
        ):
            raise BombaError("O diâmetro do rotor deve ser positivo e finito.")

        try:
            self.rho = float(PropsSI("D", "T", self.T, "P", self.P, self.fluido))
            self.mu = float(PropsSI("V", "T", self.T, "P", self.P, self.fluido))
            self.P_vapor = float(PropsSI("P", "T", self.T, "Q", 0, self.fluido))
        except Exception as exc:
            raise BombaError(
                f"Não foi possível obter as propriedades do fluido '{self.fluido}': {exc}"
            ) from exc
        if not all(np.isfinite(v) and v > 0 for v in (self.rho, self.mu)):
            raise BombaError("As propriedades calculadas do fluido são inválidas.")
        self.g = float(G_CONST)

        self._Q: Optional[np.ndarray] = None
        self._H: Optional[np.ndarray] = None
        self._P: Optional[np.ndarray] = None
        self._eta: Optional[np.ndarray] = None
        self._npsh_r: Optional[np.ndarray] = None
        # Mantém-se o nome _coef para reduzir o impacto nas integrações antigas.
        # Os valores são agora interpoladores PCHIP, não coeficientes polinomiais.
        self._coef = {"H": None, "P": None, "eta": None, "npsh": None}

    def definir_dados(
        self, Q, H=None, P=None, eta=None, npsh_r=None, ajustar: bool = True
    ) -> "Bomba":
        """Define os pontos das curvas do fabricante.

        ``P`` representa potência no eixo [W]. ``eta`` pode ser fornecido em
        fracção ou percentagem. Se apenas P ou eta for fornecido, a outra
        grandeza é estimada a partir de rho*g*Q*H.
        """
        q = _array_1d("Q", Q)
        if np.any(q < 0):
            raise BombaError("A vazão não pode ser negativa.")
        if np.any(np.diff(q) <= 0):
            raise BombaError("Q deve ser estritamente crescente e sem duplicados.")
        if H is None:
            raise BombaError("A curva de altura manométrica H(Q) é obrigatória.")
        h = _array_1d("H", H, q.size)
        if np.any(h < 0):
            raise BombaError("A altura manométrica não pode ser negativa.")

        p = None if P is None else _array_1d("P", P, q.size, allow_nan=True)
        e = None if eta is None else _array_1d("eta", eta, q.size, allow_nan=True)
        n = None if npsh_r is None else _array_1d("NPSHr", npsh_r, q.size, allow_nan=True)
        if p is not None and np.any(p[np.isfinite(p)] < 0):
            raise BombaError("A potência no eixo não pode ser negativa.")
        if n is not None and np.any(n[np.isfinite(n)] < 0):
            raise BombaError("O NPSH requerido não pode ser negativo.")
        if e is not None:
            # Mantém compatibilidade com a detecção automática anterior.
            finite_eta = e[np.isfinite(e)]
            if finite_eta.size == 0:
                raise BombaError("A curva de rendimento não contém valores válidos.")
            if np.max(finite_eta) > 1.5:
                e = e / 100.0
            finite_eta = e[np.isfinite(e)]
            if np.any(finite_eta < 0) or np.any(finite_eta > 1.02):
                raise BombaError("O rendimento deve estar entre 0 e 1 (ou 0 e 100%).")
            e = np.where(np.isfinite(e), np.minimum(e, 1.0), np.nan)

        self._Q, self._H = q, h
        self._P, self._eta, self._npsh_r = p, e, n
        self._completar_grandezas()
        if ajustar:
            self.ajustar_curvas()
        return self

    def _completar_grandezas(self) -> None:
        if self._Q is None or self._H is None:
            return
        p_hid = self.rho * self.g * self._Q * self._H
        if self._eta is not None and self._P is None:
            valid = np.isfinite(self._eta) & (self._eta > 1e-12)
            self._P = np.divide(
                p_hid, self._eta,
                out=np.full_like(p_hid, np.nan, dtype=float),
                where=valid,
            )
        elif self._P is not None and self._eta is None:
            valid = np.isfinite(self._P) & (self._P > 1e-12)
            self._eta = np.divide(
                p_hid, self._P,
                out=np.full_like(p_hid, np.nan, dtype=float),
                where=valid,
            )
            finite_eta = self._eta[np.isfinite(self._eta)]
            if finite_eta.size and np.any(finite_eta > 1.02):
                raise BombaError(
                    "Os dados de potência implicam rendimento superior a 100%; "
                    "verifique a curva de potência no eixo."
                )

    def ajustar_curvas(self, graus: Optional[dict] = None) -> None:
        """Cria interpoladores PCHIP sem oscilações artificiais de polinómios globais.

        ``graus`` é aceite por compatibilidade com chamadas antigas, mas não
        altera o grau: PCHIP é uma interpolação local por troços.
        """
        if self._Q is None or self._H is None:
            return
        dados = {
            "H": self._H,
            "P": self._P,
            "eta": self._eta,
            "npsh": self._npsh_r,
        }
        self._coef = {k: None for k in dados}
        for nome, valores in dados.items():
            if valores is None:
                continue
            mask = np.isfinite(valores)
            if int(mask.sum()) < 2:
                continue
            self._coef[nome] = PchipInterpolator(
                self._Q[mask], valores[mask], extrapolate=False
            )

    def tem_grandeza(self, grandeza: str) -> bool:
        chave = "npsh" if grandeza in ("npsh", "npsh_r") else grandeza
        return self._coef.get(chave) is not None

    def _avaliar(self, grandeza: str, Q):
        chave = "npsh" if grandeza == "npsh_r" else grandeza
        interpolador = self._coef.get(chave)
        if interpolador is None:
            rotulo = "NPSHr" if chave == "npsh" else chave.upper()
            raise BombaError(f"Curva '{rotulo}' não disponível.")
        if self._Q is None:
            raise BombaError("A bomba ainda não tem dados definidos.")
        q = np.asarray(Q, dtype=float)
        if not np.all(np.isfinite(q)):
            raise BombaError("A vazão de consulta deve ser finita.")
        tol = max(1e-12, (self._Q[-1] - self._Q[0]) * 1e-10)
        if np.any(q < self._Q[0] - tol) or np.any(q > self._Q[-1] + tol):
            raise BombaError(
                f"Vazão fora da curva de '{self.nome}': intervalo válido "
                f"[{self._Q[0]:.6g}, {self._Q[-1]:.6g}] m³/s."
            )
        q = np.clip(q, self._Q[0], self._Q[-1])
        result = np.asarray(interpolador(q), dtype=float)
        return float(result) if result.ndim == 0 else result

    def H_de_Q(self, Q):
        return self._avaliar("H", Q)

    def P_de_Q(self, Q):
        return self._avaliar("P", Q)

    def eta_de_Q(self, Q):
        return self._avaliar("eta", Q)

    def npsh_de_Q(self, Q):
        return self._avaliar("npsh", Q)

    def Q_de_H(self, H_alvo):
        """Inverte H(Q); exige uma curva de altura monotonicamente decrescente.

        Fora da faixa de altura medida, devolve o caudal de extremidade mais
        próximo, sem extrapolar a curva do fabricante.
        """
        if self._Q is None:
            raise BombaError("Bomba sem dados definidos.")
        scalar = np.ndim(H_alvo) == 0
        h_targets = np.atleast_1d(np.asarray(H_alvo, dtype=float))
        if not np.all(np.isfinite(h_targets)):
            raise BombaError("A altura de consulta deve ser finita.")
        q_dense = np.linspace(self.Q_min(), self.Q_max(), 1000)
        h_dense = np.asarray(self.H_de_Q(q_dense), dtype=float)
        scale = max(1.0, float(np.max(np.abs(h_dense))))
        if np.any(np.diff(h_dense) > scale * 1e-7):
            raise BombaError(
                "A curva H(Q) não é monotonicamente decrescente; "
                "não é possível inverter H para Q sem ambiguidade."
            )
        # np.interp requer abcissas crescentes. Inverter Q e H e retirar
        # alturas repetidas de patamares.
        h_up = h_dense[::-1]
        q_up = q_dense[::-1]
        h_unique, first = np.unique(h_up, return_index=True)
        q_unique = q_up[first]
        result = np.interp(h_targets, h_unique, q_unique)
        result = np.where(h_targets >= h_unique[-1], self.Q_min(), result)
        result = np.where(h_targets <= h_unique[0], self.Q_max(), result)
        return float(result[0]) if scalar else result

    def Q_min(self) -> float:
        if self._Q is None:
            raise BombaError("Bomba sem dados definidos.")
        return float(self._Q.min())

    def Q_max(self) -> float:
        if self._Q is None:
            raise BombaError("Bomba sem dados definidos.")
        return float(self._Q.max())

    def H_shutoff(self) -> float:
        if not np.isclose(self.Q_min(), 0.0, atol=1e-12):
            raise BombaError(
                "A curva do fabricante não inclui Q=0; não é possível "
                "determinar H de fecho sem extrapolar."
            )
        return float(self.H_de_Q(0.0))

    def Q_bep(self) -> Optional[float]:
        if not self.tem_grandeza("eta"):
            return None
        q = np.linspace(self.Q_min(), self.Q_max(), 2000)
        eta = np.asarray(self.eta_de_Q(q), dtype=float)
        valid = np.isfinite(eta)
        if not np.any(valid):
            return None
        return float(q[np.flatnonzero(valid)[np.argmax(eta[valid])]])

    def curva(self, n_pontos: int = 200) -> dict:
        if not isinstance(n_pontos, int) or n_pontos < 2:
            raise BombaError("n_pontos deve ser um inteiro igual ou superior a 2.")
        q = np.linspace(self.Q_min(), self.Q_max(), n_pontos)
        out = {"Q": q, "H": self.H_de_Q(q)}
        if self.tem_grandeza("P"):
            out["P"] = self.P_de_Q(q)
        if self.tem_grandeza("eta"):
            out["eta"] = self.eta_de_Q(q)
        if self.tem_grandeza("npsh"):
            out["npsh_r"] = self.npsh_de_Q(q)
        return out

    def com_rotacao(self, nova_rpm: float) -> "Bomba":
        if self.rpm is None or self.rpm <= 0:
            raise BombaError("Rotação original não definida (rpm).")
        if not np.isfinite(nova_rpm) or nova_rpm <= 0:
            raise BombaError("Nova rotação deve ser positiva e finita.")
        r = float(nova_rpm) / self.rpm
        return self._replicar_afinidade(
            r, rotulo=f"{self.nome} @ {nova_rpm:.0f} rpm", rpm=float(nova_rpm)
        )

    def com_diametro(self, novo_D_mm: float) -> "Bomba":
        if self.diametro_rotor_mm is None or self.diametro_rotor_mm <= 0:
            raise BombaError("Diâmetro do rotor original não definido.")
        if not np.isfinite(novo_D_mm) or novo_D_mm <= 0:
            raise BombaError("Novo diâmetro deve ser positivo e finito.")
        razao = float(novo_D_mm) / self.diametro_rotor_mm
        if not (0.75 <= razao <= 1.0):
            # Mantém-se o aviso: as leis para corte do rotor são aproximações.
            import warnings
            warnings.warn(
                f"Trim de rotor {razao:.2f} fora do intervalo recomendado "
                "(0.75–1.00); resultados aproximados.", RuntimeWarning,
            )
        return self._replicar_afinidade(
            razao, rotulo=f"{self.nome} @ Ø{novo_D_mm:.0f} mm",
            diametro_rotor_mm=float(novo_D_mm),
        )

    def _replicar_afinidade(self, r: float, rotulo: str, **kwargs) -> "Bomba":
        if self._Q is None or self._H is None:
            raise BombaError("Defina primeiro as curvas da bomba.")
        nova = Bomba(
            nome=rotulo, fluido=self.fluido, T=self.T, P=self.P,
            rpm=kwargs.get("rpm", self.rpm),
            diametro_rotor_mm=kwargs.get("diametro_rotor_mm", self.diametro_rotor_mm),
        )
        q2 = self._Q * r
        h2 = self._H * r**2
        p2 = None if self._P is None else self._P * r**3
        eta2 = None if self._eta is None else self._eta.copy()
        npsh2 = None if self._npsh_r is None else self._npsh_r * r**2
        nova.definir_dados(q2, h2, P=p2, eta=eta2, npsh_r=npsh2)
        return nova

    def npsh_disponivel(
        self,
        P_entrada_Pa: Optional[float] = None,
        H_succao_m: float = 0.0,
        perdas_succao_m: float = 0.0,
    ) -> float:
        """Calcula NPSHa, usando pressão absoluta na entrada da bomba."""
        p_in = self.P if P_entrada_Pa is None else float(P_entrada_Pa)
        hs = float(H_succao_m)
        hl = float(perdas_succao_m)
        if not all(np.isfinite(v) for v in (p_in, hs, hl)) or p_in <= 0 or hl < 0:
            raise BombaError("Dados inválidos para o cálculo de NPSHa.")
        return float((p_in - self.P_vapor) / (self.rho * self.g) + hs - hl)

    def ponto_operacao(
        self, H_sistema_fn: Callable[[float], float],
        Q_intervalo: Optional[tuple[float, float]] = None,
    ) -> dict:
        return encontrar_ponto_operacao(self, H_sistema_fn, Q_intervalo)

    def to_dict(self) -> dict:
        data = {
            "tipo": "Bomba", "nome": self.nome, "fluido": self.fluido,
            "T": self.T, "P": self.P, "rpm": self.rpm,
            "diametro_rotor_mm": self.diametro_rotor_mm,
        }
        if self._Q is not None:
            def serializar(arr):
                if arr is None:
                    return None
                return [float(v) if np.isfinite(v) else None for v in arr]
            data.update({
                "Q": serializar(self._Q),
                "H": serializar(self._H),
                "P_shaft": serializar(self._P),
                "eta": serializar(self._eta),
                "npsh_r": serializar(self._npsh_r),
            })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Bomba":
        if not isinstance(data, dict):
            raise BombaError("Os dados da bomba devem ser um objecto/dicionário.")
        bomba = cls(
            nome=data.get("nome", "Bomba"), fluido=data.get("fluido", FLUIDO_PADRAO),
            T=data.get("T", T_PADRAO), P=data.get("P", P_PADRAO),
            rpm=data.get("rpm"), diametro_rotor_mm=data.get("diametro_rotor_mm"),
        )
        if data.get("Q") is not None:
            bomba.definir_dados(
                data["Q"], data.get("H"), P=data.get("P_shaft"),
                eta=data.get("eta"), npsh_r=data.get("npsh_r"),
            )
        return bomba

    def salvar_json(self, caminho: str) -> None:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def carregar_json(cls, caminho: str) -> "Bomba":
        with open(caminho, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def __repr__(self) -> str:
        return f"Bomba(nome={self.nome!r}, Q=[{self.Q_min():.3g}, {self.Q_max():.3g}] m³/s)"


def encontrar_ponto_operacao(
    elemento, H_sistema_fn: Callable[[float], float],
    Q_intervalo: Optional[tuple[float, float]] = None,
) -> dict:
    """Determina a intersecção entre H_bomba(Q) e H_sistema(Q).

    Para o caso normal (curva da bomba decrescente e curva do sistema
    crescente) existe uma única raiz. Se houver várias, é escolhida a
    primeira intersecção estável, com a diferença H_bomba-H_sistema a
    passar de positiva para negativa.
    """
    if not callable(H_sistema_fn):
        raise BombaError("H_sistema_fn deve ser uma função chamada com Q.")
    q_lo, q_hi = float(elemento.Q_min()), float(elemento.Q_max())
    if Q_intervalo is not None:
        if len(Q_intervalo) != 2:
            raise BombaError("Q_intervalo deve conter (Q_min, Q_max).")
        a, b = map(float, Q_intervalo)
        if not np.isfinite(a) or not np.isfinite(b) or a >= b:
            raise BombaError("Q_intervalo inválido.")
        q_lo, q_hi = max(q_lo, a), min(q_hi, b)
    if not np.isfinite(q_lo + q_hi) or q_lo >= q_hi:
        raise BombaError("Intervalo de procura vazio ou inválido.")

    q_grid = np.linspace(q_lo, q_hi, 1201)
    try:
        h_pump = np.asarray(elemento.H_de_Q(q_grid), dtype=float)
        h_system = np.asarray([float(H_sistema_fn(float(q))) for q in q_grid])
    except Exception as exc:
        raise BombaError(f"Falha ao avaliar a curva do sistema ou da bomba: {exc}") from exc
    if h_pump.shape != q_grid.shape or not np.all(np.isfinite(h_pump)) or not np.all(np.isfinite(h_system)):
        raise BombaError("As curvas contêm resultados inválidos ou não finitos.")
    diff = h_pump - h_system
    scale = max(1.0, float(np.max(np.abs(h_pump))), float(np.max(np.abs(h_system))))
    tol = scale * 1e-9

    roots: list[tuple[float, bool]] = []
    for i in range(len(q_grid) - 1):
        if abs(diff[i]) <= tol:
            stable = i == 0 or diff[i - 1] >= diff[i + 1]
            roots.append((float(q_grid[i]), stable))
        elif diff[i] > 0 and diff[i + 1] < 0:
            root = brentq(
                lambda q: float(elemento.H_de_Q(q)) - float(H_sistema_fn(q)),
                float(q_grid[i]), float(q_grid[i + 1]), xtol=1e-12, rtol=1e-10,
            )
            roots.append((float(root), True))
        elif diff[i] < 0 and diff[i + 1] > 0:
            root = brentq(
                lambda q: float(elemento.H_de_Q(q)) - float(H_sistema_fn(q)),
                float(q_grid[i]), float(q_grid[i + 1]), xtol=1e-12, rtol=1e-10,
            )
            roots.append((float(root), False))
    if abs(diff[-1]) <= tol:
        roots.append((float(q_grid[-1]), False))

    # Remove raízes duplicadas detectadas em pontos consecutivos da grelha.
    roots_unique: list[tuple[float, bool]] = []
    for root, stable in roots:
        if not roots_unique or abs(root - roots_unique[-1][0]) > max(1e-10, (q_hi - q_lo) * 1e-7):
            roots_unique.append((root, stable))
        elif stable and not roots_unique[-1][1]:
            roots_unique[-1] = (root, stable)
    stable_roots = [r for r in roots_unique if r[1]]
    if stable_roots:
        q_op = stable_roots[0][0]
    elif roots_unique:
        q_op = roots_unique[0][0]
    else:
        # Verifica se existe tangência muito próxima, sem mudança de sinal.
        idx = int(np.argmin(np.abs(diff)))
        if abs(diff[idx]) <= scale * 1e-6:
            q_op = float(q_grid[idx])
        else:
            raise BombaError(
                "Não foi encontrada intersecção entre a curva da bomba e a "
                "curva do sistema no intervalo de vazão válido."
            )

    h_op = float(elemento.H_de_Q(q_op))
    result = {
        "Q": q_op, "H": h_op, "Q_min": elemento.Q_min(),
        "Q_max": elemento.Q_max(), "avisos": [],
    }
    getters = {"P": "P_de_Q", "eta": "eta_de_Q", "npsh": "npsh_de_Q"}
    for grandeza, chave in (("P", "P"), ("eta", "eta"), ("npsh", "npsh_r")):
        try:
            if hasattr(elemento, "tem_grandeza") and not elemento.tem_grandeza(grandeza):
                continue
            getter = getattr(elemento, getters[grandeza])
            value = float(getter(q_op))
            if np.isfinite(value):
                result[chave] = value
        except (BombaError, AttributeError, TypeError, ValueError):
            pass

    if hasattr(elemento, "Q_bep"):
        q_bep = elemento.Q_bep()
        if q_bep is not None and q_bep > 0:
            if q_op < 0.5 * q_bep:
                result["avisos"].append(f"Operação abaixo de 50% do BEP ({q_bep * 3600:.2f} m³/h).")
            elif q_op > 1.2 * q_bep:
                result["avisos"].append(f"Operação acima de 120% do BEP ({q_bep * 3600:.2f} m³/h).")
    if np.isclose(q_op, q_lo, rtol=0, atol=1e-10) or np.isclose(q_op, q_hi, rtol=0, atol=1e-10):
        result["avisos"].append("Ponto de operação no limite da faixa de dados da curva.")
    return result


def para_plot(
    elemento, grandeza: str = "H", label: Optional[str] = None,
    cor: Optional[str] = None, n_pontos: int = 200,
) -> dict:
    """Adapta uma curva ao formato esperado por ``Grafico.plotar_dados``."""
    curva = elemento.curva(n_pontos)
    chave = "npsh_r" if grandeza in ("npsh", "npsh_r") else grandeza
    if chave not in curva:
        raise BombaError(f"Grandeza '{grandeza}' não disponível.")
    return {
        "x": curva["Q"], "y": curva[chave],
        "label": label or getattr(elemento, "nome", grandeza),
        "cor": cor or "#1f77b4",
    }
