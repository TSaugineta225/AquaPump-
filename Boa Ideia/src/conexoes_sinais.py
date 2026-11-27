"""Liga os controlos da interface aos métodos da MainWindow.

As ligações do QWebChannel são propriedade de MainWindow._configurar_webengine.
Este módulo não as volta a ligar, evitando sinais inexistentes e recálculos duplicados.
"""
from __future__ import annotations

import logging
import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


class ConexoesUI:
    def __init__(self, parent=None, menu=None, animacoes=None, configuracoes=None):
        self.parent = parent
        self.menu = menu
        self.animacoes = animacoes
        self.config = configuracoes

        self._conectar_configuracoes()
        self._conectar_entradas_calculo()
        self._conectar_js_dados()
        self._conectar_js_unidades()
        self._conectar_mapa()  # deliberadamente sem ligações duplicadas
        self._conectar_menus()
        self._conectar_abas_frames()
        self._conectar_botoes_sair()
        self._conectar_pesquisa()
        self._perda_carga_dinamica()
        self._connectar_selecao_bombas()
        self._connectar_abrir_graph()
        self._conectar_geracao_relatorio()
        self._connectar_arquivo()
        self._conectar_ocultacoes()
        self._connectar_janelas_responsivas()
        self._connectar_widgets_desativadas()
        self._connectar_versao_pro()

    def _connect(self, object_name, signal_name, slot, required=True):
        widget = getattr(self.parent, object_name, None)
        signal = getattr(widget, signal_name, None) if widget is not None else None
        if signal is None or not hasattr(signal, "connect"):
            msg = f"Não foi possível ligar {object_name}.{signal_name}."
            if required:
                logger.warning(msg)
            return False
        signal.connect(slot)
        return True

    def _conectar_configuracoes(self):
        """Restaura as configurações antes de ligar os sinais de entrada."""
        self.parent.restaurar_configuracoes()

    def _conectar_entradas_calculo(self):
        """Cada alteração de entrada provoca apenas um recálculo completo."""
        self._connect("Vazao_2", "textChanged", self.parent.atualizar_parametros_entrada)
        self._connect("Vazao", "textChanged", self.parent.atualizar_parametros_entrada)
        self._connect("icone_2", "currentTextChanged", self.parent.atualizar_parametros_entrada)
        self._connect("radioButton_10", "toggled", self.parent.recalcular_sistema_completo)
        self._connect("radioButton_9", "toggled", self.parent.recalcular_sistema_completo)
        self._connect("darcy", "currentIndexChanged", self.parent.recalcular_sistema_completo)
        self._connect("hazen_will", "currentIndexChanged", self.parent.recalcular_sistema_completo)

    def _conectar_js_dados(self):
        for name in ("Vazao_2", "Vazao"):
            self._connect(name, "editingFinished", self.parent.enviar_js)
        for name in ("grafico_icon", "grafico"):
            self._connect(name, "clicked", self.parent.enviar_js)
        for name in (
            "darcy", "hazen_will", "icone_2", "altura_box", "diametro_box",
            "potencia_box", "comprimento_box",
        ):
            self._connect(name, "currentIndexChanged", self.parent.enviar_js)

    def _conectar_js_unidades(self):
        for name in ("Vazao_2", "Vazao"):
            self._connect(name, "editingFinished", self.parent.enviar_unidades_js)
        for name in ("grafico_icon", "grafico"):
            self._connect(name, "clicked", self.parent.enviar_unidades_js)
        for name in (
            "darcy", "hazen_will", "icone_2", "altura_box", "diametro_box",
            "potencia_box", "comprimento_box",
        ):
            self._connect(name, "currentIndexChanged", self.parent.enviar_unidades_js)

    def _conectar_mapa(self):
        """QWebChannel já foi ligado em MainWindow._configurar_webengine.

        Não voltar a ligar aqui: o código anterior tentava aceder a .lista,
        que não existia na classe actual, e ligava novamente altura/comprimento.
        """
        return

    def _conectar_menus(self):
        self._connect("definicoes_direita_3", "clicked", lambda: self.menu.menu_selecao_graficos().popup(
            self.parent.definicoes_direita_3.mapToGlobal(
                self.parent.definicoes_direita_3.rect().bottomRight()
            )
        ))
        self._connect("arquivo_2", "clicked", lambda: self.menu.menu_principal().popup(
            self.parent.arquivo_2.mapToGlobal(self.parent.arquivo_2.rect().bottomLeft())
        ))
        self._connect("config_2", "clicked", lambda: self.menu.menu_editar().popup(
            self.parent.config_2.mapToGlobal(self.parent.config_2.rect().bottomLeft())
        ))
        self._connect("relatorio_2", "clicked", lambda: self.menu.menu_relatorio().popup(
            self.parent.relatorio_2.mapToGlobal(self.parent.relatorio_2.rect().bottomLeft())
        ))
        self._connect("ajuda_2", "clicked", lambda: self.menu.menu_ajuda().popup(
            self.parent.ajuda_2.mapToGlobal(self.parent.ajuda_2.rect().bottomLeft())
        ))

    def _conectar_abas_frames(self):
        pairs = (
            ("fechar_lateral_2", lambda: self.animacoes.largura(self.parent.janel_direita, largura_alvo=300)),
            ("abrir_layout_3", lambda: self.animacoes.largura(self.parent.frame_4, self.parent.frame_6, largura_alvo=300)),
            ("pesquisar_3", lambda: self.animacoes.largura(self.parent.frame_4, self.parent.frame_6, largura_alvo=300)),
            ("projeto", lambda: self.animacoes.largura_altura(self.parent.frame_4, self.parent.projecto, self.parent.frame_6)),
            ("exportar_2", lambda: self.animacoes.largura_altura(self.parent.frame_4, self.parent.exportar, self.parent.frame_6, altura=100)),
            ("abrir_layout_2", lambda: self.animacoes.largura(self.parent.frame_4, self.parent.frame_6)),
        )
        for name, callback in pairs:
            self._connect(name, "clicked", callback)

    def _conectar_botoes_sair(self):
        self._connect("sair_2", "clicked", self.parent.close)
        self._connect("sair_3", "clicked", self.parent.close)

    def _conectar_pesquisa(self):
        self._connect("pesquisar_2", "clicked", self.parent.pesquisa_mapa)
        self._connect("pesquisa_line", "returnPressed", self.parent.pesquisa_mapa)

    def _perda_carga_dinamica(self):
        self._connect("radioButton_10", "toggled", self.parent.mudanca_dinamica_perdas_carga)
        self._connect("radioButton_9", "toggled", self.parent.mudanca_dinamica_perdas_carga)

    def _connectar_selecao_bombas(self):
        for name in ("rel", "relatorio_3"):
            self._connect(name, "clicked", lambda checked=False: self.parent.stackedWidget.setCurrentIndex(2))
            self._connect(name, "clicked", self.parent.selecionar_melhor_bomba)
        self._connect("voltar_2", "clicked", lambda: self.parent.stackedWidget.setCurrentIndex(0))

    def _connectar_abrir_graph(self):
        for name in ("grafico_icon", "grafico"):
            self._connect(name, "clicked", lambda: self.animacoes.largura(self.parent.janel_direita, largura_alvo=500))
        self._connect("calculos", "clicked", lambda: self.animacoes.altura(self.parent.scrollArea_5, altura=200))
        self._connect("graficos", "clicked", lambda: self.animacoes.altura(self.parent.janela_graficos, altura=800))

    def _conectar_geracao_relatorio(self):
        self._connect("exportar_pdf", "clicked", self.parent.gerar_pdf)
        self._connect("exportar_csv", "clicked", self.parent.gerar_csv)

    def _connectar_arquivo(self):
        self._connect("novo_arquivo", "clicked", lambda checked=False: self.parent.novo_projecto())
        self._connect("salvar_projecto", "clicked", lambda checked=False: self.parent.salvar_historico())
        self._connect("abrir_arquivo", "clicked", lambda checked=False: self.parent.carregar_historico())

    def _conectar_ocultacoes(self):
        widget = getattr(self.parent, "banco_dados", None)
        if widget is not None:
            widget.setHidden(True)

    def _connectar_janelas_responsivas(self):
        self._connect("parametros", "clicked", lambda: self.animacoes.altura(self.parent.exportar, altura=400))
        self._connect("projecto_2", "clicked", lambda: self.animacoes.altura(self.parent.projecto, altura=400))

    def _connectar_widgets_desativadas(self):
        states = {
            "groupBox_2": False, "npsh": False, "npsh_box": False,
            "groupBox_8": False, "groupBox": True, "label_8": False,
            "anterior": True, "proxima": False,
        }
        for name, visible in states.items():
            widget = getattr(self.parent, name, None)
            if widget is not None:
                widget.setVisible(visible)

    def _conectar_Observacoes(self):
        signal = getattr(self.parent, "bomba_encontrada", None)
        slot = getattr(self.parent, "iniciar_consulta", None)
        if signal is not None and slot is not None:
            signal.connect(slot)

    def _connectar_versao_pro(self):
        self._connect("pushButton_3", "clicked", self._mostrar_versao_pro)

    def _mostrar_versao_pro(self):
        QMessageBox.information(
            self.parent,
            "Versão Pro",
            "A versão Pro ainda está em preparação. Para informações, contacte "
            "tenerifenhalicale@outlook.com ou +258 86 843 9510.",
        )
