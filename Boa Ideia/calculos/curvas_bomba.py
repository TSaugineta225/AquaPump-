"""curvas_bomba.py — Plotador de curvas de bombas e associações.

Integra-se nativamente com:
    src/bomba.py            → Bomba, para_plot
    src/associacao_bombas.py → AssociacaoBombas, curva_sistema_simples,
                               curva_sistema_de_perdas

Uso típico dentro de um QWidget da UI:

    g = Grafico()
    g.plotar_bombas([b1, b2, associacao], grandeza="H",
                    H_sistema_fn=H_sist)

    g.plotar_comparacao_modos([b1, b2], H_sistema_fn=H_sist)
    g.plotar_curva_completa(b1, H_sistema_fn=H_sist)
    g.salvar_png("curvas.png"); g.exportar_csv("curvas.csv")
"""

from __future__ import annotations

from typing import Callable, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

# Estilo (silencioso se indisponível)
try:
    plt.style.use("seaborn-v0_8")
except Exception:
    try:
        plt.style.use("ggplot")
    except Exception:
        pass

__all__ = ["Grafico"]


# =====================================================================
#  Constantes
# =====================================================================
_CORES_PADRAO = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]

#: tipo -> (rótulo do eixo Y, unidade padrão, fator de escala, é_eficiência)
_GRANDEZAS = {
    "H":          ("Altura manométrica", "m",  1.0,   False),
    "Altura":     ("Altura manométrica", "m",  1.0,   False),
    "P":          ("Potência no eixo",   "kW", 1e-3,  False),
    "Potencia":   ("Potência no eixo",   "kW", 1e-3,  False),
    "Potência":   ("Potência no eixo",   "kW", 1e-3,  False),
    "eta":        ("Rendimento",         "%",  100.0, True),
    "Rendimento": ("Rendimento",         "%",  100.0, True),
    "npsh":       ("NPSH requerido",     "m",  1.0,   False),
    "npsh_r":     ("NPSH requerido",     "m",  1.0,   False),
    "NPSH":       ("NPSH requerido",     "m",  1.0,   False),
}

#: símbolo curto mostrado nas anotações de ponto de operação
_SIMBOLOS = {
    "H": "H", "Altura": "H",
    "P": "P", "Potencia": "P", "Potência": "P",
    "eta": "η", "Rendimento": "η",
    "npsh": "NPSHr", "npsh_r": "NPSHr", "NPSH": "NPSHr",
}


# =====================================================================
#  Classe principal
# =====================================================================
class Grafico(QWidget):
    """Widget Matplotlib embebido, pronto para curvas de bombas."""

    # -----------------------------------------------------------------
    # Construção
    # -----------------------------------------------------------------
    def __init__(self, parent=None, figsize=(7.5, 4.8), dpi=100):
        super().__init__(parent)
        self._figsize = figsize
        self._dpi = dpi

        self.figure = plt.figure(figsize=figsize, dpi=dpi)
        self.ax = self.figure.add_subplot(111)
        self.ax2 = None

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.toolbar = NavigationBar(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, 1)

        self._dados_ultima = None
        self._limpar_eixos()

    # -----------------------------------------------------------------
    # Utilitários
    # -----------------------------------------------------------------
    @staticmethod
    def paleta(n: int) -> list[str]:
        """Devolve n cores ciclando a paleta padrão."""
        if n <= len(_CORES_PADRAO):
            return list(_CORES_PADRAO[:n])
        return [_CORES_PADRAO[i % len(_CORES_PADRAO)] for i in range(n)]

    @staticmethod
    def _normalizar_chave(grandeza: str) -> str:
        g = str(grandeza).lower().strip()
        if g in ("npsh", "npshr", "npsh_r", "npsh-r"): return "npsh_r"
        if g in ("h", "altura", "head"):                return "H"
        if g in ("p", "potencia", "potência", "power"): return "P"
        if g in ("eta", "rendimento", "efficiency", "η"): return "eta"
        return grandeza

    @staticmethod
    def _resolver_grandeza(tipo, y_scale=None, unidade_y=None):
        meta = _GRANDEZAS.get(tipo)
        if meta is None:
            return (tipo, unidade_y or "", 
                    1.0 if y_scale is None else y_scale, False)
        rotulo, unid, fator, eh_eta = meta
        return (
            rotulo,
            unidade_y or unid,
            y_scale if y_scale is not None else fator,
            eh_eta,
        )

    def _limpar_eixos(self):
        """Reinicia a figura do zero (sem eixos fantasmas)."""
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax2 = None
        self.ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.6)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def limpar(self):
        """Apaga todo o conteúdo do gráfico."""
        self._limpar_eixos()
        self._dados_ultima = None

    # =================================================================
    #  Método de plotagem principal (aceita N curvas)
    # =================================================================
    def plotar_dados(
        self,
        tipo_gráfico: str,
        curvas: Union[dict, list[dict]],
        ponto_operacao: Optional[Union[dict, list[dict]]] = None,
        curva_sistema: Optional[dict] = None,
        unidade_vazao: Optional[str] = None,
        unidade_y: Optional[str] = None,
        fator_vazao: float = 1.0,
        y_scale: Optional[float] = None,
        titulo: Optional[str] = None,
        mostrar_legenda: bool = True,
        anotar_pontos_op: bool = True,
    ):
        """Plota N curvas + opcionalmente sistema e pontos de operação.

        Parameters
        ----------
        tipo_gráfico : str
            'H' / 'Altura', 'P' / 'Potência', 'eta' / 'Rendimento',
            'npsh' / 'NPSH'.
        curvas : dict ou list[dict]
            Cada dict: {'x', 'y', 'label'?, 'cor'?, 'linestyle'?,
            'linewidth'?, 'marker'?, 'alpha'?}.
        ponto_operacao : dict ou list[dict], opcional
            {'x', 'y', 'label'?, 'cor'?, 'texto'?, 'offset'?}.
        curva_sistema : dict, opcional
            {'x', 'y', 'label'?, 'cor'?, 'linestyle'?}.
        fator_vazao : float
            1.0 = manter SI (m³/s). 3600.0 → m³/h.
        y_scale : float, opcional
            Força o factor de escala do eixo Y (senão vem de `_GRANDEZAS`).
        """
        self._limpar_eixos()

        if isinstance(curvas, dict):
            curvas = [curvas]
        if isinstance(ponto_operacao, dict):
            ponto_operacao = [ponto_operacao]

        rotulo_y, unidade_y, fator_y, _ = self._resolver_grandeza(
            tipo_gráfico, y_scale=y_scale, unidade_y=unidade_y
        )
        unidade_vazao = unidade_vazao or "m³/h"
        simbolo_y = _SIMBOLOS.get(tipo_gráfico, rotulo_y)

        # ---------- Curvas ----------
        for i, c in enumerate(curvas):
            try:
                x = np.asarray(c["x"], dtype=float) * fator_vazao
                y = np.asarray(c["y"], dtype=float) * fator_y
            except (KeyError, TypeError) as e:
                print(f"[Grafico] Curva {i} inválida: {e}")
                continue
            self.ax.plot(
                x, y,
                label=c.get("label", f"Curva {i + 1}"),
                color=c.get("cor", _CORES_PADRAO[i % len(_CORES_PADRAO)]),
                linestyle=c.get("linestyle", "-"),
                linewidth=c.get("linewidth", 2.2),
                marker=c.get("marker"),
                markersize=c.get("markersize", 5) if c.get("marker") else 0,
                alpha=c.get("alpha", 1.0),
                zorder=2,
            )

        # ---------- Curva do sistema ----------
        if curva_sistema:
            try:
                x_s = np.asarray(curva_sistema["x"], dtype=float) * fator_vazao
                y_s = np.asarray(curva_sistema["y"], dtype=float) * fator_y
                self.ax.plot(
                    x_s, y_s,
                    label=curva_sistema.get("label", "Curva do sistema"),
                    color=curva_sistema.get("cor", "#444444"),
                    linestyle=curva_sistema.get("linestyle", "--"),
                    linewidth=curva_sistema.get("linewidth", 2.0),
                    zorder=1,
                )
            except (KeyError, TypeError) as e:
                print(f"[Grafico] Curva do sistema inválida: {e}")

        # ---------- Pontos de operação ----------
        if ponto_operacao:
            for i, p in enumerate(ponto_operacao):
                try:
                    px = float(p["x"]) * fator_vazao
                    py = float(p["y"]) * fator_y
                except (KeyError, TypeError, ValueError):
                    continue
                cor = p.get("cor", "black")
                self.ax.plot(
                    px, py, "o", markersize=9, color=cor,
                    markeredgecolor="white", markeredgewidth=1.2,
                    label=p.get("label", "Ponto de operação"),
                    zorder=5,
                )
                if anotar_pontos_op:
                    texto = p.get("texto") or (
                        f"Q = {px:.2f} {unidade_vazao}\n"
                        f"{simbolo_y} = {py:.2f} {unidade_y}"
                    )
                    self.ax.annotate(
                        texto, (px, py),
                        xytext=p.get("offset", (15, -30)),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.35",
                                  fc="#f5f5f5", ec="#888", alpha=0.92),
                        fontsize=8.5,
                        arrowprops=dict(arrowstyle="->",
                                        connectionstyle="arc3,rad=.2",
                                        color="#555"),
                        zorder=6,
                    )

        # ---------- Eixos ----------
        self.ax.set_title(titulo or f"Curva — {rotulo_y}",
                          fontsize=11, fontweight="bold")
        self.ax.set_xlabel(f"Vazão ({unidade_vazao})", fontsize=10)
        self.ax.set_ylabel(f"{rotulo_y} ({unidade_y})", fontsize=10)
        self.ax.tick_params(axis="both", which="major", labelsize=8.5)
        self.ax.set_xlim(left=0)
        if mostrar_legenda:
            self.ax.legend(frameon=True, loc="best", fontsize=9)

        self.figure.tight_layout()
        self.canvas.draw_idle()

        self._dados_ultima = {
            "tipo": tipo_gráfico,
            "curvas": curvas,
            "sistema": curva_sistema,
            "pontos": ponto_operacao,
            "unidade_vazao": unidade_vazao,
            "unidade_y": unidade_y,
            "fator_vazao": fator_vazao,
            "fator_y": fator_y,
        }

    # =================================================================
    #  Atalho de alto nível — recebe Bomba / AssociacaoBombas
    # =================================================================
    def plotar_bombas(
        self,
        elementos,
        grandeza: str = "H",
        H_sistema_fn: Optional[Callable[[float], float]] = None,
        mostrar_sistema: bool = True,
        fator_vazao: float = 3600.0,
        unidade_vazao: str = "m³/h",
        y_scale: Optional[float] = None,
        unidade_y: Optional[str] = None,
        titulo: Optional[str] = None,
        cores: Optional[list] = None,
        n_pontos: int = 200,
        **kwargs,
    ):
        """Plota N elementos (Bomba ou AssociacaoBombas) na mesma figura.

        Se `H_sistema_fn` for fornecido, calcula o ponto de operação de cada
        elemento e desenha também a curva do sistema.
        """
        if not elementos:
            raise ValueError("Lista de elementos vazia.")
        if not isinstance(elementos, (list, tuple)):
            elementos = [elementos]

        cores = cores or self.paleta(len(elementos))
        chave = self._normalizar_chave(grandeza)
        simbolo = _SIMBOLOS.get(grandeza, chave)

        # ---------- Curvas ----------
        curvas = []
        for el, cor in zip(elementos, cores):
            try:
                c = el.curva(n_pontos)
            except Exception as e:
                print(f"[Grafico] Falha na curva de {el}: {e}")
                continue
            if chave not in c:
                print(f"[Grafico] {getattr(el, 'nome', el)} sem '{chave}'.")
                continue
            curvas.append({
                "x": c["Q"], "y": c[chave],
                "label": getattr(el, "nome", f"Elemento {len(curvas)+1}"),
                "cor": cor,
            })
        if not curvas:
            raise RuntimeError("Nenhuma curva válida para plotar.")

        # ---------- Pontos de operação ----------
        pontos = []
        if H_sistema_fn is not None:
            for el, cor in zip(elementos, cores):
                try:
                    op = el.ponto_operacao(H_sistema_fn)
                except Exception:
                    continue
                y_val = op.get(chave)
                if y_val is None:
                    try:
                        y_val = float(el._avaliar(chave, op["Q"]))
                    except Exception:
                        continue
                pontos.append({
                    "x": op["Q"], "y": y_val, "cor": cor,
                    "label": f"Op. {getattr(el, 'nome', '')}".strip(),
                })

        # ---------- Curva do sistema ----------
        cs = None
        if (H_sistema_fn is not None and mostrar_sistema
                and chave == "H"):
            q_max = max(float(np.max(c["x"])) for c in curvas)
            Q_sis = np.linspace(0.0, q_max, n_pontos)
            H_sis = np.array([float(H_sistema_fn(q)) for q in Q_sis])
            cs = {"x": Q_sis, "y": H_sis, "label": "Curva do sistema"}

        self.plotar_dados(
            tipo_gráfico=grandeza,
            curvas=curvas,
            ponto_operacao=pontos or None,
            curva_sistema=cs,
            fator_vazao=fator_vazao,
            unidade_vazao=unidade_vazao,
            y_scale=y_scale,
            unidade_y=unidade_y,
            titulo=titulo,
            **kwargs,
        )

    # =================================================================
    #  Curva completa H + η (dois eixos)
    # =================================================================
    def plotar_curva_completa(
        self,
        elemento,
        H_sistema_fn: Optional[Callable[[float], float]] = None,
        fator_vazao: float = 3600.0,
        unidade_vazao: str = "m³/h",
        titulo: Optional[str] = None,
        n_pontos: int = 200,
    ):
        """Plota H (eixo esquerdo) e η (eixo direito) com ponto de operação."""
        self._limpar_eixos()
        c = elemento.curva(n_pontos)
        Q = c["Q"] * fator_vazao

        # H — eixo esquerdo
        self.ax.plot(Q, c["H"], color="#1f77b4", lw=2.4, label="H")
        self.ax.set_xlabel(f"Vazão ({unidade_vazao})", fontsize=10)
        self.ax.set_ylabel("Altura manométrica (m)", fontsize=10,
                           color="#1f77b4")
        self.ax.tick_params(axis="y", labelcolor="#1f77b4")
        self.ax.set_xlim(left=0)
        self.ax.grid(True, ls="--", lw=0.4, alpha=0.6)

        # η — eixo direito
        if "eta" in c:
            ax2 = self.ax.twinx()
            ax2.plot(Q, c["eta"] * 100.0, color="#d62728", lw=2.0,
                     label="η")
            ax2.set_ylabel("Rendimento (%)", fontsize=10, color="#d62728")
            ax2.tick_params(axis="y", labelcolor="#d62728")
            self.ax2 = ax2

        # Ponto de operação + curva do sistema
        if H_sistema_fn is not None:
            try:
                op = elemento.ponto_operacao(H_sistema_fn)
                q_op = op["Q"] * fator_vazao
                self.ax.plot(q_op, op["H"], "o", ms=9, color="black",
                             markeredgecolor="white", mew=1.2, zorder=5)
                self.ax.annotate(
                    f"Q = {q_op:.2f} {unidade_vazao}\n"
                    f"H = {op['H']:.2f} m",
                    (q_op, op["H"]),
                    xytext=(15, -30), textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.35", fc="#f5f5f5",
                              ec="#888"),
                    fontsize=8.5,
                    arrowprops=dict(arrowstyle="->", color="#555"),
                )
                Q_sis = np.linspace(0.0, Q.max(), n_pontos)
                H_sis = np.array([H_sistema_fn(q / fator_vazao)
                                  for q in Q_sis])
                self.ax.plot(Q_sis, H_sis, "--", color="#444", lw=1.8,
                             label="Sistema")
            except Exception as e:
                print(f"[Grafico] Sem ponto de operação: {e}")

        self.ax.set_title(
            titulo or f"Curva completa — {getattr(elemento, 'nome', '')}",
            fontsize=11, fontweight="bold",
        )

        # Legenda unificada (ax + ax2)
        linhas, labels = self.ax.get_legend_handles_labels()
        if self.ax2 is not None:
            l2, lb2 = self.ax2.get_legend_handles_labels()
            linhas += l2
            labels += lb2
        if linhas:
            self.ax.legend(linhas, labels, loc="best", fontsize=9)

        self.figure.tight_layout()
        self.canvas.draw_idle()

        self._dados_ultima = {
            "tipo": "completa",
            "curvas": [{"x": c["Q"], "y": c["H"], "label": "H"}],
            "sistema": None, "pontos": None,
            "unidade_vazao": unidade_vazao, "unidade_y": "m",
            "fator_vazao": fator_vazao, "fator_y": 1.0,
        }

    # =================================================================
    #  Comparação: individual × série × paralelo
    # =================================================================
    def plotar_comparacao_modos(
        self,
        bombas,
        H_sistema_fn: Optional[Callable[[float], float]] = None,
        fator_vazao: float = 3600.0,
        unidade_vazao: str = "m³/h",
        incluir_individual: bool = False,
        titulo: Optional[str] = None,
    ):
        """Coloca no mesmo gráfico: (opcional) cada bomba, série, paralelo."""
        try:
            from .associacao_bombas import AssociacaoBombas
        except ImportError:
            from associacao_bombas import AssociacaoBombas

        if not isinstance(bombas, (list, tuple)):
            bombas = [bombas]
        if not bombas:
            raise ValueError("Lista de bombas vazia.")

        pal = self.paleta(4)
        elementos, cores = [], []

        if incluir_individual:
            for i, b in enumerate(bombas):
                elementos.append(b)
                cores.append(pal[i % len(pal)])

        serie = AssociacaoBombas(bombas, "serie", nome="Série")
        paralelo = AssociacaoBombas(bombas, "paralelo", nome="Paralelo")
        elementos += [serie, paralelo]
        cores += [pal[2], pal[3]]

        self.plotar_bombas(
            elementos, grandeza="H", H_sistema_fn=H_sistema_fn,
            fator_vazao=fator_vazao, unidade_vazao=unidade_vazao,
            cores=cores,
            titulo=titulo or "Comparação: individual × série × paralelo",
        )

    # =================================================================
    #  Exportação
    # =================================================================
    def salvar_png(self, caminho: str, dpi: int = 150):
        self.figure.savefig(caminho, dpi=dpi, bbox_inches="tight")

    def salvar_pdf(self, caminho: str):
        self.figure.savefig(caminho, bbox_inches="tight", format="pdf")

    def exportar_csv(self, caminho: str):
        """Exporta curvas da última plotagem (dados em unidades de display)."""
        if not self._dados_ultima or not self._dados_ultima["curvas"]:
            raise RuntimeError("Nenhuma plotagem disponível para exportar.")
        import csv

        dados = self._dados_ultima
        fv, fy = dados["fator_vazao"], dados["fator_y"]
        curvas = dados["curvas"]

        with open(caminho, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            cab = [f"Q ({dados['unidade_vazao']})"] + [
                f"{c.get('label', f'Curva {i+1}')} ({dados['unidade_y']})"
                for i, c in enumerate(curvas)
            ]
            w.writerow(cab)

            Q = np.asarray(curvas[0]["x"]) * fv
            for i in range(len(Q)):
                row = [f"{Q[i]:.6g}"]
                for c in curvas:
                    y = np.asarray(c["y"]) * fy
                    row.append(f"{y[i]:.6g}" if i < len(y) else "")
                w.writerow(row)


# =====================================================================
#  Demo — correr directamente:  python -m src.curvas_bomba
# =====================================================================
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    try:
        from .bomba import Bomba
        from .associacao_bombas import curva_sistema_simples
    except ImportError:
        from bomba import Bomba
        from associacao_bombas import curva_sistema_simples

    # Bomba fictícia tipo 30 m³/h
    Q = np.array([0, 5, 10, 15, 20, 25]) / 3600.0
    H1 = np.array([45, 44, 42, 38, 30, 15])
    H2 = H1 * 0.92
    eta = np.array([0, 30, 55, 68, 62, 40]) / 100.0
    npsh = np.array([1.5, 1.8, 2.2, 3.0, 4.2, 6.0])

    b1 = Bomba("B1", rpm=3500); b1.definir_dados(Q, H1, eta=eta, npsh_r=npsh)
    b2 = Bomba("B2", rpm=3500); b2.definir_dados(Q, H2, eta=eta, npsh_r=npsh)
    H_sist = curva_sistema_simples(10.0, K=4e5)

    app = QApplication(sys.argv)
    win = QMainWindow()
    g = Grafico()

    # ① Uma bomba + sistema + ponto de operação
    g.plotar_bombas([b1, b2], grandeza="H", H_sistema_fn=H_sist)

    # ② Comparação de modos (descomenta para testar)
    # g.plotar_comparacao_modos([b1, b2], H_sistema_fn=H_sist,
    #                           incluir_individual=True)

    # ③ Curva completa H + η
    # g.plotar_curva_completa(b1, H_sistema_fn=H_sist)

    win.setCentralWidget(g)
    win.resize(950, 580)
    win.setWindowTitle("Teste — curvas_bomba")
    win.show()
    sys.exit(app.exec())