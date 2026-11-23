"""gestor_bombas.py — Orquestração entre a UI (Ui_main), os modelos
(Bomba/AssociacaoBombas) e os gráficos (curvas_bomba.Grafico).

Responsabilidades:
    • Ler entradas dos widgets (Vazao_2, icone_2, darcy, hazen_will, ...)
    • Manter a lista de bombas + associações série/paralelo
    • Construir a curva do sistema a partir de perdas_cargas.Perdas
    • Disparar atualizações nos 6 gráficos (altura/potência/rendimento/
      npsh/série/paralelo) e nos labels do painel de cálculos
    • Persistência: salvar/abrir projecto JSON
    • Exportação: PDF/CSV do gráfico actualmente visível

Uso (na main window):
    self.gestor = GestorBombas(self.ui, parent=self)
"""

from __future__ import annotations

import importlib
import json
import math
import traceback
from pathlib import Path
from typing import Optional

import numpy as np
from PySide6.QtCore import QObject
from PySide6.QtWidgets import (
    QFileDialog, QMessageBox, QVBoxLayout, QWidget,
)

# ---- Modelos ----------------------------------------------------------
from bomba import Bomba, BombaError
from associacao_bombas import (
    AssociacaoBombas, curva_sistema_de_perdas,
)
from curvas_bomba import Grafico
from perdas_cargas import Perdas
from unidades import ConversorUnidades

# Tubulacao pode ter nome com acento — tenta ambos
try:
    from dimensionamento_tubulacao import Tubulacao
except ImportError:
    try:
        Tubulacao = importlib.import_module(
            "dimensionamento_tubulação"
        ).Tubulacao
    except (ImportError, ModuleNotFoundError):
        Tubulacao = None
        print(
            "[Gestor] Aviso: Tubulacao indisponível. "
            "Renomeie 'dimensionamento_tubulação.py' → "
            "'dimensionamento_tubulacao.py'."
        )


# =====================================================================
class GestorBombas(QObject):
    """Maestro central do programa AquaPump."""

    #: mapeamento nome-lógico → índice no `stackedWidget_3`
    PAGINAS = {
        "altura":     0,
        "potencia":   1,
        "rendimento": 2,
        "npsh":       3,
        "serie":      4,
        "paralelo":   5,
    }

    #: unidades de vazão oferecidas no combo `icone_2`
    UNIDADES_VAZAO = ["m³/h", "m³/s", "L/s", "L/min", "L/h", "gal/min"]

    #: unidades de comprimento para o diâmetro (futuro)
    UNIDADES_COMPRIMENTO = ["m", "mm", "cm", "in"]

    # =================================================================
    #  Construção
    # =================================================================
    def __init__(self, ui, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = ui
        self.parent_widget = parent

        # ---------------- Estado interno (SI) ----------------
        self.bombas: list[Bomba] = []
        self.associacao_serie:    Optional[AssociacaoBombas] = None
        self.associacao_paralelo: Optional[AssociacaoBombas] = None

        self.perdas = Perdas(
            diametro_m=0.05, area=math.pi * 0.025 ** 2,
        )
        self.tubulacao = Tubulacao() if Tubulacao else None
        self.conversor = ConversorUnidades()

        self.H_geometrico = 15.0     # m
        self.comprimento_m = 100.0   # m
        self.material_darcy = "Aço comercial novo"

        # ---------------- Gráficos ----------------
        self.graficos: dict[str, Grafico] = {}

        # ---------------- Setup ----------------
        try:
            self._criar_graficos()
            self._popular_combos()
            self._conectar_sinais()
            self._carregar_demo()
            self.atualizar_tudo()
        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(
                parent, "Erro de inicialização",
                f"Falha ao inicializar o gestor:\n{e}",
            )

    # =================================================================
    #  Setup: gráficos
    # =================================================================
    def _criar_graficos(self) -> None:
        """Encaixa um Grafico em cada container vazio do Ui_main."""
        containers = {
            "altura":     getattr(self.ui, "altura",     None),
            "potencia":   getattr(self.ui, "potencia",   None),
            "rendimento": getattr(self.ui, "rendimento", None),
            "npsh":       getattr(self.ui, "npsh_2",     None),
            "serie":      getattr(self.ui, "serie",      None),
            "paralelo":   getattr(self.ui, "paralelo",   None),
        }
        for nome, container in containers.items():
            if container is None:
                continue
            try:
                g = Grafico(figsize=(7.0, 4.4), dpi=100)
                g.setMinimumSize(320, 220)
                lay = container.layout()
                if lay is None:
                    lay = QVBoxLayout(container)
                    lay.setContentsMargins(0, 0, 0, 0)
                    lay.setSpacing(0)
                    container.setLayout(lay)
                lay.addWidget(g)
                self.graficos[nome] = g
            except Exception as e:
                print(f"[Gestor] Falha ao criar gráfico '{nome}': {e}")

    # =================================================================
    #  Setup: combos
    # =================================================================
    def _popular_combos(self) -> None:
        if hasattr(self.ui, "icone_2"):
            self.ui.icone_2.clear()
            self.ui.icone_2.addItems(self.UNIDADES_VAZAO)
            self.ui.icone_2.setCurrentText("m³/h")

        if hasattr(self.ui, "darcy"):
            self.ui.darcy.clear()
            self.ui.darcy.addItems(Perdas.get_lista_materiais_darcy())

        if hasattr(self.ui, "hazen_will"):
            self.ui.hazen_will.clear()
            self.ui.hazen_will.addItems(Perdas.get_lista_materiais_hazen())

    # =================================================================
    #  Setup: sinais
    # =================================================================
    def _conectar_sinais(self) -> None:
        # Botões de exportação
        for nome_botao, slot in (
            ("exportar_pdf", self.exportar_pdf),
            ("exportar_csv", self.exportar_csv),
        ):
            b = getattr(self.ui, nome_botao, None)
            if b is not None:
                b.clicked.connect(slot)

        # Botões de projecto
        for nome_botao, slot in (
            ("novo_arquivo",   self.novo_projecto),
            ("salvar_projecto", self.salvar_projecto),
            ("abrir_arquivo",  self.abrir_projecto),
        ):
            b = getattr(self.ui, nome_botao, None)
            if b is not None:
                b.clicked.connect(slot)

        # Entradas reativas
        if hasattr(self.ui, "Vazao_2"):
            self.ui.Vazao_2.textChanged.connect(self.atualizar_resultados)
        if hasattr(self.ui, "icone_2"):
            self.ui.icone_2.currentTextChanged.connect(
                self.atualizar_resultados
            )
        if hasattr(self.ui, "darcy"):
            self.ui.darcy.currentTextChanged.connect(self._on_material_changed)

        # Navegação para o painel de gráficos
        if hasattr(self.ui, "grafico"):
            self.ui.grafico.clicked.connect(
                lambda: self.ui.stackedWidget_3.setCurrentIndex(0)
            )

    def _on_material_changed(self, material: str) -> None:
        if material:
            self.material_darcy = material
            self.atualizar_graficos()

    # =================================================================
    #  Bombas demo (substituir quando existir tabela de entrada)
    # =================================================================
    def _carregar_demo(self) -> None:
        Q_h = np.array([0, 6, 12, 18, 24, 30], dtype=float)      # m³/h
        H   = np.array([42, 40, 37, 32, 24, 12], dtype=float)
        eta = np.array([0, 35, 55, 68, 65, 45], dtype=float) / 100.0
        npsh = np.array([1.8, 2.0, 2.4, 3.2, 4.5, 6.5])

        b1 = Bomba("Bomba A", rpm=3500, diametro_rotor_mm=170)
        b1.definir_dados(Q_h / 3600.0, H, eta=eta, npsh_r=npsh)

        Q_h2 = np.array([0, 5, 10, 15, 20, 25], dtype=float)
        H2   = np.array([40, 38, 35, 30, 22, 10], dtype=float)
        eta2 = np.array([0, 32, 52, 65, 60, 40], dtype=float) / 100.0
        npsh2 = np.array([1.5, 1.8, 2.2, 3.0, 4.2, 6.0])

        b2 = Bomba("Bomba B", rpm=3500, diametro_rotor_mm=165)
        b2.definir_dados(Q_h2 / 3600.0, H2, eta=eta2, npsh_r=npsh2)

        self.bombas = [b1, b2]

    # =================================================================
    #  API pública — gestão de bombas
    # =================================================================
    def adicionar_bomba(self, bomba: Bomba) -> None:
        self.bombas.append(bomba)
        self.atualizar_tudo()

    def remover_bomba(self, indice: int) -> None:
        if 0 <= indice < len(self.bombas):
            self.bombas.pop(indice)
            self.atualizar_tudo()

    def limpar_bombas(self) -> None:
        self.bombas.clear()
        self.atualizar_tudo()

    def carregar_bombas(self, bombas: list[Bomba]) -> None:
        self.bombas = list(bombas)
        self.atualizar_tudo()

    # =================================================================
    #  API pública — configuração do sistema
    # =================================================================
    def configurar_sistema(
        self,
        H_geometrico: Optional[float] = None,
        diametro_m: Optional[float] = None,
        comprimento_m: Optional[float] = None,
        material: Optional[str] = None,
        acessorios: Optional[list] = None,
    ) -> None:
        if H_geometrico is not None:
            self.H_geometrico = float(H_geometrico)
        if diametro_m is not None and diametro_m > 0:
            self.perdas.atualizar_parametros(
                diametro_m=float(diametro_m),
                area=math.pi * float(diametro_m) ** 2 / 4.0,
            )
        if comprimento_m is not None:
            self.comprimento_m = float(comprimento_m)
        if material is not None:
            self.material_darcy = material
            self.perdas.definir_material_darcy(material)
        if acessorios is not None:
            self.perdas.definir_acessorios_lista(acessorios)
        self.atualizar_tudo()

    # =================================================================
    #  Reconstrução das associações
    # =================================================================
    def _reconstruir_associacoes(self) -> None:
        self.associacao_serie = None
        self.associacao_paralelo = None
        if not self.bombas:
            return
        try:
            self.associacao_serie = AssociacaoBombas(
                self.bombas, "serie", nome="Série"
            )
        except BombaError as e:
            print(f"[Gestor] Série indisponível: {e}")
        try:
            self.associacao_paralelo = AssociacaoBombas(
                self.bombas, "paralelo", nome="Paralelo"
            )
        except BombaError as e:
            print(f"[Gestor] Paralelo indisponível: {e}")

    # =================================================================
    #  Curva do sistema
    # =================================================================
    def _H_sistema_fn(self):
        """Devolve o callable H_sist(Q) construído a partir de perdas."""
        return curva_sistema_de_perdas(
            H_geometrico=self.H_geometrico,
            perdas_obj=self.perdas,
            comprimento_m=self.comprimento_m,
            material=self.material_darcy,
            incluir_localizadas=True,
        )

    # =================================================================
    #  Atualização total
    # =================================================================
    def atualizar_tudo(self) -> None:
        try:
            self._reconstruir_associacoes()
            self.atualizar_resultados()
            self.atualizar_graficos()
        except Exception as e:
            traceback.print_exc()
            print(f"[Gestor] Erro em atualizar_tudo: {e}")

    # =================================================================
    #  Painel de cálculos (labels inferiores)
    # =================================================================
    def _ler_vazao_m3s(self) -> Optional[float]:
        """Lê Vazao_2 + icone_2 → m³/s. Fallback: Vazao (assume SI)."""
        txt = self.ui.Vazao_2.text().strip().replace(",", ".") \
            if hasattr(self.ui, "Vazao_2") else ""
        if txt:
            try:
                valor = float(txt)
                unidade = (
                    self.ui.icone_2.currentText()
                    if hasattr(self.ui, "icone_2") else "m³/s"
                ) or "m³/s"
                return float(
                    self.conversor.converter_vazao(valor, unidade, "m³/s")
                )
            except Exception:
                pass

        txt = self.ui.Vazao.text().strip().replace(",", ".") \
            if hasattr(self.ui, "Vazao") else ""
        if txt:
            try:
                return float(txt)
            except ValueError:
                pass
        return None

    def atualizar_resultados(self) -> None:
        q = self._ler_vazao_m3s()

        # Vazão
        if hasattr(self.ui, "vazao_resul"):
            if q is None or q <= 0:
                self.ui.vazao_resul.setText("—")
            else:
                self.ui.vazao_resul.setText(f"{q * 3600:.2f} m³/h")

        if q is None or q <= 0:
            for attr in ("diametro_resul", "seccao_resul",
                         "velocidade_resul", "perdas_resul"):
                w = getattr(self.ui, attr, None)
                if w is not None:
                    w.setText("—")
            return

        # Diâmetro + área + velocidade (via Tubulacao)
        if self.tubulacao is not None:
            try:
                D = self.tubulacao.calcular_diametro(q, tempo=24)
                area = self.tubulacao.area_seccao()
                v = q / area if area > 0 else 0.0
                if hasattr(self.ui, "diametro_resul"):
                    self.ui.diametro_resul.setText(f"{D * 1000:.1f} mm")
                if hasattr(self.ui, "seccao_resul"):
                    self.ui.seccao_resul.setText(f"{area * 1e4:.2f} cm²")
                if hasattr(self.ui, "velocidade_resul"):
                    self.ui.velocidade_resul.setText(f"{v:.2f} m/s")
                # Actualiza objecto Perdas para coerência
                self.perdas.atualizar_parametros(
                    diametro_m=D, area=area,
                )
            except Exception as e:
                print(f"[Gestor] Cálculo tubulação: {e}")

        # Perda de carga total
        try:
            self.perdas.atualizar_parametros(vazao_m3s=q)
            h_darcy = self.perdas.calcular_perda_carga_darcy(
                self.comprimento_m
            )
            h_loc = self.perdas.calcular_perdas_localizadas()
            if hasattr(self.ui, "perdas_resul"):
                self.ui.perdas_resul.setText(
                    f"{h_darcy + h_loc:.2f} m  "
                    f"(Darcy {h_darcy:.2f} + loc. {h_loc:.2f})"
                )
        except Exception as e:
            print(f"[Gestor] Cálculo perdas: {e}")

    # =================================================================
    #  Gráficos
    # =================================================================
    def _elementos_para_grafico(self) -> list:
        """Lista base: bombas individuais + associações disponíveis."""
        elementos = list(self.bombas)
        if self.associacao_serie is not None:
            elementos.append(self.associacao_serie)
        if self.associacao_paralelo is not None:
            elementos.append(self.associacao_paralelo)
        return elementos

    def _plotar_seguro(
        self, nome_pagina: str, elementos, grandeza: str,
        H_sistema_fn=None, titulo: Optional[str] = None,
    ) -> None:
        g = self.graficos.get(nome_pagina)
        if g is None or not elementos:
            return
        try:
            g.plotar_bombas(
                elementos, grandeza=grandeza,
                H_sistema_fn=H_sistema_fn,
                titulo=titulo or f"Curvas — {grandeza}",
            )
        except Exception as e:
            print(f"[Gestor] Erro gráfico '{nome_pagina}': {e}")

    def atualizar_graficos(self) -> None:
        if not self.bombas:
            for g in self.graficos.values():
                g.limpar()
            return

        H_sist = self._H_sistema_fn()
        todos = self._elementos_para_grafico()

        # Página Altura: todos + curva do sistema + op points
        self._plotar_seguro(
            "altura", todos, "H", H_sistema_fn=H_sist,
            titulo="Curvas H(Q) — bombas & associações",
        )

        # Página Potência
        self._plotar_seguro(
            "potencia", todos, "P", H_sistema_fn=H_sist,
            titulo="Potência no eixo (kW)",
        )

        # Página Rendimento
        self._plotar_seguro(
            "rendimento", todos, "eta",
            titulo="Rendimento (%)",
        )

        # Página NPSH
        self._plotar_seguro(
            "npsh", todos, "npsh_r",
            titulo="NPSH requerido (m)",
        )

        # Página Série: individuais + associação série
        serie_els = list(self.bombas)
        if self.associacao_serie is not None:
            serie_els.append(self.associacao_serie)
        self._plotar_seguro(
            "serie", serie_els, "H", H_sistema_fn=H_sist,
            titulo="Associação em série",
        )

        # Página Paralelo
        par_els = list(self.bombas)
        if self.associacao_paralelo is not None:
            par_els.append(self.associacao_paralelo)
        self._plotar_seguro(
            "paralelo", par_els, "H", H_sistema_fn=H_sist,
            titulo="Associação em paralelo",
        )

    # =================================================================
    #  Exportação
    # =================================================================
    def _grafico_visivel(self) -> Optional[Grafico]:
        idx = self.ui.stackedWidget_3.currentIndex()
        for nome, i in self.PAGINAS.items():
            if i == idx:
                return self.graficos.get(nome)
        return None

    def exportar_pdf(self) -> None:
        g = self._grafico_visivel()
        if g is None:
            QMessageBox.information(
                self.parent_widget, "Exportar",
                "Nenhum gráfico visível.",
            )
            return
        caminho, _ = QFileDialog.getSaveFileName(
            self.parent_widget, "Exportar PDF", "grafico.pdf", "*.pdf"
        )
        if not caminho:
            return
        try:
            g.salvar_pdf(caminho)
            QMessageBox.information(
                self.parent_widget, "Exportar",
                f"PDF guardado em:\n{caminho}",
            )
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Erro", str(e))

    def exportar_csv(self) -> None:
        g = self._grafico_visivel()
        if g is None:
            QMessageBox.information(
                self.parent_widget, "Exportar",
                "Nenhum gráfico visível.",
            )
            return
        caminho, _ = QFileDialog.getSaveFileName(
            self.parent_widget, "Exportar CSV", "grafico.csv", "*.csv"
        )
        if not caminho:
            return
        try:
            g.exportar_csv(caminho)
            QMessageBox.information(
                self.parent_widget, "Exportar",
                f"CSV guardado em:\n{caminho}",
            )
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Erro", str(e))

    # =================================================================
    #  Persistência do projecto
    # =================================================================
    def to_dict(self) -> dict:
        return {
            "versao": "1.0",
            "sistema": {
                "H_geometrico":  self.H_geometrico,
                "comprimento_m": self.comprimento_m,
                "material_darcy": self.material_darcy,
                "diametro_m": self.perdas.diametro_m,
                "area_m2":    self.perdas.area,
            },
            "bombas": [b.to_dict() for b in self.bombas],
        }

    def from_dict(self, d: dict) -> None:
        sis = d.get("sistema", {})
        self.H_geometrico   = sis.get("H_geometrico", 15.0)
        self.comprimento_m  = sis.get("comprimento_m", 100.0)
        self.material_darcy = sis.get("material_darcy", "Aço comercial novo")
        D = sis.get("diametro_m", 0.05)
        A = sis.get("area_m2", math.pi * D ** 2 / 4.0)
        self.perdas.atualizar_parametros(diametro_m=D, area=A)
        self.perdas.definir_material_darcy(self.material_darcy)

        self.bombas = [
            Bomba.from_dict(bd) for bd in d.get("bombas", [])
        ]

    def salvar_projecto(self) -> None:
        caminho, _ = QFileDialog.getSaveFileName(
            self.parent_widget, "Guardar projecto",
            "projecto_aquapump.json", "*.json",
        )
        if not caminho:
            return
        try:
            Path(caminho).write_text(
                json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            QMessageBox.information(
                self.parent_widget, "Guardar",
                f"Projecto guardado em:\n{caminho}",
            )
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Erro", str(e))

    def abrir_projecto(self) -> None:
        caminho, _ = QFileDialog.getOpenFileName(
            self.parent_widget, "Abrir projecto", "", "*.json",
        )
        if not caminho:
            return
        try:
            d = json.loads(Path(caminho).read_text(encoding="utf-8"))
            self.from_dict(d)
            self.atualizar_tudo()
            QMessageBox.information(
                self.parent_widget, "Abrir",
                f"Projecto carregado ({len(self.bombas)} bombas).",
            )
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Erro", str(e))

    def novo_projecto(self) -> None:
        resp = QMessageBox.question(
            self.parent_widget, "Novo projecto",
            "Limpar tudo e recomeçar com as bombas demo?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )
        if resp != QMessageBox.StandardButton.Yes:
            return
        self.H_geometrico = 15.0
        self.comprimento_m = 100.0
        self.material_darcy = "Aço comercial novo"
        self.perdas = Perdas(diametro_m=0.05, area=math.pi * 0.025 ** 2)
        self._carregar_demo()
        self.atualizar_tudo()

    # =================================================================
    #  Conveniência
    # =================================================================
    def info(self) -> str:
        """Resumo do estado actual (útil para debug)."""
        linhas = [
            f"Bombas: {len(self.bombas)}",
            *[f"  • {b}" for b in self.bombas],
            f"Sistema: H_geo={self.H_geometrico:.1f} m  "
            f"L={self.comprimento_m:.0f} m  "
            f"D={self.perdas.diametro_m*1000:.0f} mm  "
            f"({self.material_darcy})",
        ]
        if self.associacao_serie:
            linhas.append(f"Série:    {self.associacao_serie}")
        if self.associacao_paralelo:
            linhas.append(f"Paralelo: {self.associacao_paralelo}")
        return "\n".join(linhas)


# =====================================================================
#  Demonstração headless (sem UI) — sanity check
# =====================================================================
if __name__ == "__main__":
    class _FakeUI:
        """Mock mínimo para correr o gestor sem PySide6."""
        pass

    g = GestorBombas.__new__(GestorBombas)
    QObject.__init__(g)
    g.bombas = []
    g.associacao_serie = None
    g.associacao_paralelo = None
    g.perdas = Perdas(diametro_m=0.05, area=math.pi * 0.025 ** 2)
    g.tubulacao = Tubulacao() if Tubulacao else None
    g.conversor = ConversorUnidades()
    g.H_geometrico = 15.0
    g.comprimento_m = 100.0
    g.material_darcy = "Aço comercial novo"
    g.graficos = {}
    g.ui = _FakeUI()
    g.parent_widget = None

    GestorBombas._carregar_demo(g)
    GestorBombas._reconstruir_associacoes(g)

    print(g.info())
    H_sist = GestorBombas._H_sistema_fn(g)
    print(f"H_sistema(10 m³/h) = {H_sist(10/3600):.2f} m")
    for b in g.bombas:
        op = b.ponto_operacao(H_sist)
        print(f"  {b.nome}: Q={op['Q']*3600:.2f} m³/h  "
              f"H={op['H']:.2f} m  η={op.get('eta', 0)*100:.1f}%")