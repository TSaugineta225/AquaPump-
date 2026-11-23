"""Modelação computacional de bombas centrífugas.

Unidades internas (SI):
    Q      [m³/s]   vazão volumétrica
    H      [m]      altura manométrica
    P      [W]      potência no eixo
    η      [-]      rendimento (fração, NÃO %)
    NPSHr  [m]      NPSH requerido
    N      [rpm]    rotação
    D      [mm]     diâmetro do rotor

Interface pública (partilhada com AssociacaoBombas):
    definir_dados, ajustar_curvas
    H_de_Q, P_de_Q, eta_de_Q, npsh_de_Q, Q_de_H
    Q_min, Q_max, H_shutoff, curva
    com_rotacao, com_diametro  (leis de afinidade)
    ponto_operacao              (cruza com H_sistema(Q))
    to_dict, from_dict, salvar_json, carregar_json
"""

from __future__ import annotations

import json
from typing import Callable, Optional

import numpy as np
from CoolProp.CoolProp import PropsSI
from scipy.constants import g as G_CONST
from scipy.optimize import brentq

__all__ = [
    "Bomba", "BombaError",
    "encontrar_ponto_operacao", "para_plot",
]

FLUIDO_PADRAO = "Water"
T_PADRAO = 293.15        # K   (20 °C)
P_PADRAO = 101325.0      # Pa  (1 atm)
GRAUS_PADRAO = {"H": 2, "P": 3, "eta": 3, "npsh": 2}


class BombaError(ValueError):
    """Erro de domínio no modelo de bombas."""


# =====================================================================
# Bomba individual
# =====================================================================
class Bomba:
    """Modelo completo de uma bomba centrífuga."""

    # ------------------------------------------------------------------ #
    # Construção
    # ------------------------------------------------------------------ #
    def __init__(
        self,
        nome: str = "Bomba",
        fluido: str = FLUIDO_PADRAO,
        T: float = T_PADRAO,
        P: float = P_PADRAO,
        rpm: Optional[float] = None,
        diametro_rotor_mm: Optional[float] = None,
    ):
        self.nome = nome
        self.fluido = fluido
        self.T = float(T)
        self.P = float(P)
        self.rpm = None if rpm is None else float(rpm)
        self.diametro_rotor_mm = (
            None if diametro_rotor_mm is None else float(diametro_rotor_mm)
        )

        # Propriedades do fluido
        self.rho = float(PropsSI("D", "T", T, "P", P, fluido))
        self.mu = float(PropsSI("V", "T", T, "P", P, fluido))
        self.P_vapor = float(PropsSI("P", "T", T, "Q", 0, fluido))
        self.g = float(G_CONST)

        # Dados experimentais
        self._Q: Optional[np.ndarray] = None
        self._H: Optional[np.ndarray] = None
        self._P: Optional[np.ndarray] = None
        self._eta: Optional[np.ndarray] = None
        self._npsh_r: Optional[np.ndarray] = None

        # Coeficientes polinomiais
        self._coef = {"H": None, "P": None, "eta": None, "npsh": None}
        self._graus = dict(GRAUS_PADRAO)

    # ------------------------------------------------------------------ #
    # Entrada de dados
    # ------------------------------------------------------------------ #
    def definir_dados(
        self,
        Q,
        H=None,
        P=None,
        eta=None,
        npsh_r=None,
        ajustar: bool = True,
    ) -> "Bomba":
        """Define os pontos da curva do fabricante.

        Q e H são obrigatórios. Se for fornecida apenas uma das duplas
        (P, eta), a outra é deduzida via `P = ρ g Q H / η`.

        η pode vir em % (max > 1.5) ou em fração — é normalizada para fração.
        """
        Q = np.asarray(Q, dtype=float)
        if Q.ndim != 1 or Q.size < 2:
            raise BombaError("Q deve ser vetor 1-D com pelo menos 2 pontos.")
        if np.any(Q < 0):
            raise BombaError("Q não pode ter valores negativos.")
        if np.any(np.diff(Q) <= 0):
            raise BombaError("Q deve ser estritamente crescente.")

        self._Q = Q
        self._H = None if H is None else np.asarray(H, dtype=float)
        self._P = None if P is None else np.asarray(P, dtype=float)
        self._eta = None if eta is None else np.asarray(eta, dtype=float)
        self._npsh_r = None if npsh_r is None else np.asarray(npsh_r, dtype=float)

        for nome, arr in (
            ("H", self._H), ("P", self._P),
            ("eta", self._eta), ("npsh_r", self._npsh_r),
        ):
            if arr is not None and arr.shape != Q.shape:
                raise BombaError(f"Array '{nome}' com forma diferente de Q.")

        self._completar_grandezas()
        if ajustar:
            self.ajustar_curvas()
        return self

    def _completar_grandezas(self) -> None:
        """Deduz P a partir de η (ou vice‑versa) quando só uma está presente."""
        if self._H is None:
            return
        P_hid = self.rho * self.g * self._Q * self._H  # potência hidráulica

        if self._eta is not None and np.nanmax(self._eta) > 1.5:
            self._eta = self._eta / 100.0  # veio em %

        if self._eta is not None and self._P is None:
            with np.errstate(divide="ignore", invalid="ignore"):
                self._P = np.where(self._eta > 0, P_hid / self._eta, np.nan)
        elif self._P is not None and self._eta is None:
            with np.errstate(divide="ignore", invalid="ignore"):
                self._eta = np.where(self._P > 0, P_hid / self._P, np.nan)

    # ------------------------------------------------------------------ #
    # Ajuste de curvas
    # ------------------------------------------------------------------ #
    def ajustar_curvas(self, graus: Optional[dict] = None) -> None:
        """Ajusta polinómios a cada grandeza disponível."""
        if graus:
            self._graus.update(graus)
        if self._Q is None:
            return

        for nome, dados in (
            ("H", self._H), ("P", self._P),
            ("eta", self._eta), ("npsh", self._npsh_r),
        ):
            if dados is None:
                self._coef[nome] = None
                continue
            mask = np.isfinite(dados)
            if mask.sum() < 2:
                self._coef[nome] = None
                continue
            grau = min(self._graus[nome], int(mask.sum()) - 1)
            self._coef[nome] = np.polyfit(self._Q[mask], dados[mask], grau)

    # ------------------------------------------------------------------ #
    # Consulta de valores
    # ------------------------------------------------------------------ #
    def _avaliar(self, grandeza: str, Q) -> np.ndarray:
        coef = self._coef[grandeza]
        if coef is None:
            nome_attr = "npsh_r" if grandeza == "npsh" else grandeza.upper()
            raise BombaError(f"Curva '{nome_attr}' não disponível.")
        return np.polyval(coef, Q)

    def H_de_Q(self, Q):      return self._avaliar("H", Q)
    def P_de_Q(self, Q):      return self._avaliar("P", Q)
    def eta_de_Q(self, Q):    return self._avaliar("eta", Q)
    def npsh_de_Q(self, Q):   return self._avaliar("npsh", Q)

    def Q_de_H(self, H_alvo):
        """Inverte H(Q). Devolve Q=0 quando H ≥ H_shutoff."""
        if self._Q is None:
            raise BombaError("Bomba sem dados definidos.")

        escalar = np.ndim(H_alvo) == 0
        H_alvo_arr = np.atleast_1d(np.asarray(H_alvo, dtype=float))

        Q_dense = np.linspace(0.0, float(self._Q.max()), 1000)
        H_dense = self.H_de_Q(Q_dense)

        ordem = np.argsort(H_dense)
        H_sorted, Q_sorted = H_dense[ordem], Q_dense[ordem]

        Q = np.interp(H_alvo_arr, H_sorted, Q_sorted)
        Q = np.where(H_alvo_arr >= H_sorted[-1], 0.0, Q)

        return float(Q[0]) if escalar else Q

    # ------------------------------------------------------------------ #
    # Metadados
    # ------------------------------------------------------------------ #
    def Q_min(self) -> float:
        if self._Q is None:
            raise BombaError("Bomba sem dados definidos.")
        return float(self._Q.min())

    def Q_max(self) -> float:
        if self._Q is None:
            raise BombaError("Bomba sem dados definidos.")
        return float(self._Q.max())

    def H_shutoff(self) -> float:
        return float(self.H_de_Q(0.0))

    def Q_bep(self) -> Optional[float]:
        """Vazão no ponto de melhor eficiência (se η disponível)."""
        if self._eta is None:
            return None
        idx = int(np.nanargmax(self._eta))
        return float(self._Q[idx])

    def curva(self, n_pontos: int = 200) -> dict:
        """Devolve um dict {Q, H, [P], [eta], [npsh_r]} pronto para plot."""
        Q = np.linspace(self.Q_min(), self.Q_max(), n_pontos)
        out = {"Q": Q, "H": self.H_de_Q(Q)}
        if self._coef["P"]    is not None: out["P"]       = self.P_de_Q(Q)
        if self._coef["eta"]  is not None: out["eta"]     = self.eta_de_Q(Q)
        if self._coef["npsh"] is not None: out["npsh_r"]  = self.npsh_de_Q(Q)
        return out

    # ------------------------------------------------------------------ #
    # Leis de afinidade
    # ------------------------------------------------------------------ #
    def com_rotacao(self, nova_rpm: float) -> "Bomba":
        """Aplica as leis de afinidade para mudança de rotação.

            Q₂/Q₁ = N₂/N₁     H₂/H₁ = (N₂/N₁)²     P₂/P₁ = (N₂/N₁)³
            NPSHr₂/NPSHr₁ = (N₂/N₁)²              η (pontos homólogos) ≈ const
        """
        if self.rpm is None or self.rpm <= 0:
            raise BombaError("Rotação original não definida (rpm).")
        if nova_rpm <= 0:
            raise BombaError("Nova rotação deve ser positiva.")
        r = nova_rpm / self.rpm
        return self._replicar_afinidade(
            r, rotulo=f"{self.nome} @ {nova_rpm:.0f} rpm", rpm=nova_rpm
        )

    def com_diametro(self, novo_D_mm: float) -> "Bomba":
        """Aplica as leis de afinidade por trim do rotor (válidas ~ 0.8–1.0·D)."""
        if self.diametro_rotor_mm is None or self.diametro_rotor_mm <= 0:
            raise BombaError("Diâmetro do rotor original não definido.")
        if novo_D_mm <= 0:
            raise BombaError("Novo diâmetro deve ser positivo.")
        razao = novo_D_mm / self.diametro_rotor_mm
        if not (0.75 <= razao <= 1.0):
            # Não é erro fatal, mas as leis perdem precisão
            print(
                f"[Bomba] Aviso: trim {razao:.2f} fora do recomendado "
                "(0.8–1.0) — resultados aproximados."
            )
        return self._replicar_afinidade(
            razao, rotulo=f"{self.nome} @ Ø{novo_D_mm:.0f} mm",
            diametro_rotor_mm=novo_D_mm,
        )

    def _replicar_afinidade(self, r: float, rotulo: str, **kwargs) -> "Bomba":
        nova = Bomba(
            nome=rotulo, fluido=self.fluido, T=self.T, P=self.P,
            rpm=kwargs.get("rpm", self.rpm),
            diametro_rotor_mm=kwargs.get("diametro_rotor_mm",
                                         self.diametro_rotor_mm),
        )
        Q2 = self._Q * r
        H2 = self._H * r ** 2 if self._H is not None else None
        P2 = self._P * r ** 3 if self._P is not None else None
        eta2 = self._eta.copy() if self._eta is not None else None
        npsh2 = self._npsh_r * r ** 2 if self._npsh_r is not None else None

        nova.definir_dados(Q2, H2, P=P2, eta=eta2, npsh_r=npsh2)
        return nova

    # ------------------------------------------------------------------ #
    # NPSH disponível
    # ------------------------------------------------------------------ #
    def npsh_disponivel(
        self,
        P_entrada_Pa: Optional[float] = None,
        H_succao_m: float = 0.0,
        perdas_succao_m: float = 0.0,
    ) -> float:
        """NPSHa = (P_entrada - P_vapor)/(ρ g) + H_succao - h_perdas_succao."""
        P_ent = self.P if P_entrada_Pa is None else float(P_entrada_Pa)
        return (
            (P_ent - self.P_vapor) / (self.rho * self.g)
            + H_succao_m - perdas_succao_m
        )

    # ------------------------------------------------------------------ #
    # Ponto de operação (delega ao utilitário genérico)
    # ------------------------------------------------------------------ #
    def ponto_operacao(
        self, H_sistema_fn: Callable[[float], float],
        Q_intervalo: Optional[tuple[float, float]] = None,
    ) -> dict:
        return encontrar_ponto_operacao(self, H_sistema_fn, Q_intervalo)

    # ------------------------------------------------------------------ #
    # Serialização
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        d = {
            "tipo": "Bomba",
            "nome": self.nome,
            "fluido": self.fluido,
            "T": self.T, "P": self.P,
            "rpm": self.rpm,
            "diametro_rotor_mm": self.diametro_rotor_mm,
        }
        if self._Q is not None:
            d["Q"] = self._Q.tolist()
            d["H"] = None if self._H is None else self._H.tolist()
            d["P_shaft"] = None if self._P is None else self._P.tolist()
            d["eta"] = None if self._eta is None else self._eta.tolist()
            d["npsh_r"] = (
                None if self._npsh_r is None else self._npsh_r.tolist()
            )
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Bomba":
        b = cls(
            nome=d.get("nome", "Bomba"),
            fluido=d.get("fluido", FLUIDO_PADRAO),
            T=d.get("T", T_PADRAO), P=d.get("P", P_PADRAO),
            rpm=d.get("rpm"),
            diametro_rotor_mm=d.get("diametro_rotor_mm"),
        )
        if "Q" in d and d["Q"] is not None:
            b.definir_dados(
                d["Q"], d.get("H"),
                P=d.get("P_shaft"),
                eta=d.get("eta"),
                npsh_r=d.get("npsh_r"),
            )
        return b

    def salvar_json(self, caminho: str) -> None:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def carregar_json(cls, caminho: str) -> "Bomba":
        with open(caminho, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:
        return (
            f"Bomba(nome={self.nome!r}, "
            f"Q=[{self.Q_min():.3g}, {self.Q_max():.3g}] m³/s)"
        )


# =====================================================================
# Utilitários de ponto de operação (funcionam para Bomba E AssociacaoBombas)
# =====================================================================
def encontrar_ponto_operacao(
    elemento, H_sistema_fn: Callable[[float], float],
    Q_intervalo: Optional[tuple[float, float]] = None,
) -> dict:
    """Interseção entre a curva H(Q) do elemento e a curva do sistema.

    Parameters
    ----------
    elemento : Bomba | AssociacaoBombas
        Objeto com `Q_min()`, `Q_max()`, `H_de_Q`, opcionalmente
        `P_de_Q`, `eta_de_Q`, `npsh_de_Q`.
    H_sistema_fn : Callable[[float], float]
        Curva do sistema `H = H_sist(Q)`.
    Q_intervalo : (float, float), opcional
        Restrição adicional ao intervalo de busca.

    Returns
    -------
    dict com chaves:
        Q, H           — coordenadas do ponto de operação
        P              — potência no eixo (W)        [se disponível]
        eta            — rendimento (-)               [se disponível]
        npsh_r         — NPSH requerido (m)           [se disponível]
        Q_min, Q_max   — limites da curva do elemento
        avisos         — lista de strings
    """
    q_lo = elemento.Q_min()
    q_hi = elemento.Q_max()
    if Q_intervalo is not None:
        q_lo = max(q_lo, Q_intervalo[0])
        q_hi = min(q_hi, Q_intervalo[1])
    if q_lo >= q_hi:
        raise BombaError("Intervalo de busca vazio.")

    Q_grid = np.linspace(q_lo, q_hi, 400)
    H_b = np.atleast_1d(elemento.H_de_Q(Q_grid))
    H_s = np.array([float(H_sistema_fn(q)) for q in Q_grid], dtype=float)
    dif = H_b - H_s

    Q_op = None
    for i in range(len(dif) - 1):
        if dif[i] == 0.0:
            Q_op = float(Q_grid[i]); break
        if dif[i] * dif[i + 1] < 0.0:
            Q_op = float(brentq(
                lambda q: float(elemento.H_de_Q(q)) - H_sistema_fn(q),
                Q_grid[i], Q_grid[i + 1],
            ))
            break
    if Q_op is None:
        raise BombaError(
            "Sem interseção no intervalo — bomba e sistema não se cruzam."
        )

    H_op = float(elemento.H_de_Q(Q_op))

    resultado = {
        "Q": Q_op,
        "H": H_op,
        "Q_min": elemento.Q_min(),
        "Q_max": elemento.Q_max(),
        "avisos": [],
    }
    for grandeza in ("P", "eta", "npsh"):
        try:
            resultado[grandeza if grandeza != "npsh" else "npsh_r"] = float(
                elemento._avaliar(grandeza, Q_op)
            )
        except (BombaError, AttributeError):
            pass

    # Aviso BEP (só para Bomba individual)
    if isinstance(elemento, Bomba) and elemento._eta is not None:
        Q_bep = elemento.Q_bep()
        if Q_bep is not None:
            if Q_op < 0.5 * Q_bep:
                resultado["avisos"].append(
                    f"Operação < 50% do BEP ({Q_bep*3600:.1f} m³/h)"
                )
            elif Q_op > 1.2 * Q_bep:
                resultado["avisos"].append(
                    f"Operação > 120% do BEP ({Q_bep*3600:.1f} m³/h)"
                )
    return resultado


# =====================================================================
# Adaptador para curvas_bomba.plotar_dados
# =====================================================================
def para_plot(
    elemento, grandeza: str = "H",
    label: Optional[str] = None, cor: Optional[str] = None,
    n_pontos: int = 200,
) -> dict:
    """Devolve {'x', 'y', 'label', 'cor'} compatível com `Grafico.plotar_dados`."""
    c = elemento.curva(n_pontos)
    chave = "npsh_r" if grandeza == "npsh" else grandeza
    if chave not in c:
        raise BombaError(f"Grandeza '{grandeza}' não disponível.")
    return {
        "x": c["Q"], "y": c[chave],
        "label": label or getattr(elemento, "nome", grandeza),
        "cor": cor or "#1f77b4",
    }


# =====================================================================
# Smoke test
# =====================================================================
if __name__ == "__main__":
    # Curva típica de bomba (30 m³/h nominal)
    Q = np.array([0, 5, 10, 15, 20]) / 3600.0     # m³/h → m³/s
    H = np.array([45, 43, 38, 30, 15])
    eta = np.array([0, 35, 55, 60, 40]) / 100.0
    NPSH = np.array([1.5, 2.0, 2.5, 3.5, 5.0])

    b = Bomba("Demo", rpm=3500)
    b.definir_dados(Q, H, eta=eta, npsh_r=NPSH)

    print(b)
    print(f"  H_shutoff  = {b.H_shutoff():.2f} m")
    print(f"  Q_BEP      = {b.Q_bep()*3600:.2f} m³/h")
    print(f"  NPSHa@20°C = {b.npsh_disponivel():.2f} m")

    # Lei de afinidade
    b2 = b.com_rotacao(2900)
    print(b2)
    print(f"  H_shutoff  = {b2.H_shutoff():.2f} m  "
          f"(esperado ≈ {b.H_shutoff()*(2900/3500)**2:.2f})")

    # Curva do sistema: H = 10 + K·Q² com K = 5e5
    H_sist = lambda q: 10.0 + 5e5 * q * q
    op = b.ponto_operacao(H_sist)
    print(f"Ponto de operação: Q = {op['Q']*3600:.2f} m³/h  "
          f"H = {op['H']:.2f} m  η = {op.get('eta', 0)*100:.1f}%")
    if op["avisos"]:
        print("  Avisos:", op["avisos"])