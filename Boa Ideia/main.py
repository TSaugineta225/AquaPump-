import sys
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QToolButton, QMessageBox, QFileDialog, QCompleter, QLabel, QVBoxLayout
from PySide6.QtGui import QAction, QIcon,QDoubleValidator, QSurfaceFormat
from PySide6.QtCore import QPoint, QEvent, Qt, QSize, Slot, QStringListModel
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QUrl, Qt, QTimer, Signal
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebChannel import QWebChannel
from gui.Ui_main import Ui_AquaPump
from gui.Loses_main import Dialog_main
from gui.config_main import Config_main
from scripts.animações import Animações
from scripts.JavaScript import Mapa
from scripts.web_channel import Dados, Relatório
from scripts.pdf_gen import PDF
from calculos.graph import Grafico
from scripts.arquivos import Arquivos
from scripts.requisicoes import Pesquisa
import os, json
import gui.img_rc

os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_OPENGL"] = "software"

class MainWindow(FramelessWindow, Ui_AquaPump):
    sincronizar = Signal(int)


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ex_3 = chr(0x00B3)

        # === Inicialização de Classes Internas ===
        self.animações = Animações()
        self.dados_bomba = Relatório()
        self.dados = Dados()
        self.relatorio_pdf = PDF()
        self.arquivos = Arquivos(self.view)

        # === WebEngine + WebChannel ===
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)
        self._canal.registerObject("dados_bomba", self.dados_bomba)

        # === Conexões JS ===
        self.Vazao_2.textChanged.connect(self.enviar_js)
        self.Vazao.textChanged.connect(self.enviar_js)
        self.page.featurePermissionRequested.connect(self.permissao)

        # === Menu Arquivo ===
        self.menu = QMenu(self)
        acao_novo = QAction("Novo", self)
        acao_abrir = QAction("Abrir", self)
        acao_salvar = QAction("Salvar", self)
        acao_salvar_como = QAction("Salvar Como", self)
        acao_fechar = QAction("Fechar Projeto", self)
        acao_sair = QAction("Sair", self)

        acao_novo.setShortcut("Ctrl+N")
        acao_abrir.setShortcut("Ctrl+O")
        acao_salvar.setShortcut("Ctrl+S")
        acao_salvar_como.setShortcut("Ctrl+Shift+S")
        acao_fechar.setShortcut("Ctrl+W")
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.setShortcutContext(Qt.ApplicationShortcut)
        acao_sair.triggered.connect(lambda: app.quit())
        self.addAction(acao_sair)

        accao_coor = QAction(QIcon(":/img/kml.png"), "Carregar KML", self)
        accao_coor_1 = QAction(QIcon(":/img/arquivo.png"), "Carregar camada shapefile", self)
        accao_coor_2 = QAction(QIcon(":/img/arquivo-csv.png"), "Carregar coordenadas CSV", self)

        accao_coor.triggered.connect(self.arquivos.carregar_kml)
        accao_coor_1.triggered.connect(self.arquivos.carregar_shapefile)
        accao_coor_2.triggered.connect(self.arquivos.carregar_csv)

        self.addAction(accao_coor)
        self.addAction(accao_coor_1)
        self.addAction(accao_coor_2)

        self.menu.addActions([
            acao_novo, acao_abrir, acao_salvar, acao_salvar_como, acao_fechar,
        ])
        self.menu.addSeparator()
        self.menu.addActions([accao_coor, accao_coor_1, accao_coor_2])
        self.menu.addSeparator()
        self.menu.addAction(acao_sair)

        # === Menu Editar ===
        self.editar = QMenu(self)
        accao_config = QAction("Configurações", self)
        acao_parametros = QAction("Parâmetros do Projecto", self)

        accao_config.setShortcut("Ctrl+E")
        accao_config.setShortcutContext(Qt.ApplicationShortcut)
        acao_parametros.setShortcut("Ctrl+P")
        accao_config.triggered.connect(self.janela_config)

        self.addAction(accao_config)
        self.editar.addActions([accao_config, acao_parametros])

        # === Menu Relatório ===
        self.rel = QMenu(self)
        acao_relatorio = QAction("Relatório", self)
        acao_exportar = QAction("Exportar", self)
        acao_relatorio.setShortcut("Ctrl+R")
        acao_exportar.setShortcut("Ctrl+E")
        self.rel.addActions([acao_relatorio, acao_exportar])

        # === Menu Ajuda ===
        self.help = QMenu(self)
        acao_manual = QAction("Manual do Usuário", self)
        acao_dicas = QAction("Dicas de Uso", self)
        acao_sobre = QAction("Sobre o Programa", self)
        acao_suporte = QAction("Suporte Técnico", self)

        acao_manual.setShortcut("Ctrl+M")
        acao_dicas.setShortcut("Ctrl+D")
        acao_sobre.setShortcut("Ctrl+I")
        acao_suporte.setShortcut("Ctrl+T")
        self.help.addActions([acao_manual, acao_dicas, acao_sobre, acao_suporte])

        # === Menu Gráficos ===
        self.grafico = QMenu(self)
        self.perfil = QAction("Perfil de Elevação", self)
        self.curva = QAction("Curvas de Bombas/Associação")

        self.perfil.triggered.connect(lambda: self.animações.altura(self.widget_2, altura=400))
        self.curva.triggered.connect(lambda: self.animações.largura(self.widget, largura_alvo=500))
        #self.curva.triggered.connect(self.plotar_gráfico)
        self.grafico.addActions([self.perfil, self.curva])

        # === Botões de Menu Superior ===
        self.grafico_icon.clicked.connect(lambda: self.grafico.popup(self.grafico_icon.mapToGlobal(self.grafico_icon.rect().topRight())))
        self.arquivo_2.clicked.connect(lambda: self.menu.popup(self.arquivo_2.mapToGlobal(self.arquivo_2.rect().bottomLeft())))
        self.config_2.clicked.connect(lambda: self.editar.popup(self.config_2.mapToGlobal(self.config_2.rect().bottomLeft())))
        self.relatorio_2.clicked.connect(lambda: self.rel.popup(self.relatorio_2.mapToGlobal(self.relatorio_2.rect().bottomLeft())))
        self.ajuda_2.clicked.connect(lambda: self.help.popup(self.ajuda_2.mapToGlobal(self.ajuda_2.rect().bottomLeft())))

        # === Aba Lateral e Frames ===
        self.abrir_layout_3.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6, largura_alvo=300))
        self.pesquisar_3.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6, largura_alvo=300))
        self.projeto.clicked.connect(lambda: self.animações.largura_altura(self.frame_4, self.projecto, self.frame_6))
        self.exportar_2.clicked.connect(lambda: self.animações.largura_altura(self.frame_4, self.exportar, self.frame_6, altura=100))
        self.abrir_layout_2.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6)) 
        self.sair_2.clicked.connect(lambda: app.quit())
        self.sair_3.clicked.connect(lambda: app.quit())

        # === Seções Projeto e Exportar ===
        self.projecto_2.clicked.connect(lambda: self.animações.altura(self.projecto, altura=400))
        self.parametros.clicked.connect(lambda: self.animações.altura(self.exportar, altura=100))
        self.configuracoes.clicked.connect(self.janela_config)
        self.configuracoes_2.clicked.connect(self.janela_config)
        self.exportar_pdf.clicked.connect(self.gerar_pdf)

        # === Botões Arquivos ===
        self.pushButton.clicked.connect(self.arquivos.carregar_kml)
        self.pushButton_2.clicked.connect(self.arquivos.carregar_csv)
        self.pushButton_4.clicked.connect(self.arquivos.carregar_shapefile)
        #self.pushButton_3.clicked.connect(self.janela_perdas) 
        #self.mapa_2.clicked.connect(self.carregar_arquivo)

        # === ComboBox ===
        self.comboBox.setHidden(True)

        # === Validação de Entrada ===
        validator = QDoubleValidator(0.0, 1000.0, 3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

        # === Autocompletar Pesquisa ===
        self.completador = QCompleter()
        self.completador.setCaseSensitivity(Qt.CaseInsensitive)
        self.pesquisa_line.setCompleter(self.completador)
        self.pesquisar_2.clicked.connect(self.pesquisa_mapa)
        self.pesquisa_line.returnPressed.connect(self.pesquisa_mapa)
        self.pesquisa_line.setPlaceholderText("Pesquisar")

        # === WebEngine + Mapa ===
        self.mapinha = Mapa()
        mapa = self.mapinha.html_code
        self.page.setHtml(mapa) 

        # === Combobox com Unidades ===
        self.icone_2.addItems([
            f'm{self.ex_3}/s', 
            f'm{self.ex_3}/min', 
            f'm{self.ex_3}/h', 
            f'L/s',
        ])
        self.icone_2.currentIndexChanged.connect(self.emitir_sinal_sincro)
        self.icone_2.currentIndexChanged.connect(self.mudanca_dinamica_Textholder)
        self.icone_2.view().setMinimumWidth(60)
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")
        self.Vazao.setPlaceholderText("Tempo em horas")

        # === Gráfico Matplotlib ===
        self.matplot_grafico = Grafico()
        layout = QVBoxLayout(self.widget_3)
        self.widget_3.setLayout(layout)
        self.widget_3.layout().addWidget(self.matplot_grafico)

        # === Status e Threads ===
        self.worker = None
        self.status_label = QLabel()


    def mudanca_dinamica_Textholder(self):
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")

    def emitir_sinal_sincro(self, index):
        if self._sincronizar:
            return
        
        self.sincronizar.emit(index)
    
    def actualizar_espaco(self, index):
        self._sincronizar = True
        self.icone_2.setCurrentIndex(index)
        self._sincronizar = False

    def enviar_js(self):
        self.dados.enviar_dados(self.Vazao_2, self.Vazao, self.view)

    def pesquisa_mapa(self):
        texto = self.pesquisa_line.text()
        pesquisa = f"pesquisar_lugar('{texto}')"
        self.view.page().runJavaScript(pesquisa)

    @Slot(str)
    def buscar_sugestoes(self, texto):
        if len(texto) >= 3:
            self.status_label.setText("Buscando sugestões...")
            if self.worker and self.worker.isRunning():
                self.worker.terminate()

            self.worker = Pesquisa(texto)
            self.worker.resultado.connect(self.atualizar_completer)
            self.worker.start()

    @Slot(list)
    def atualizar_completer(self, sugestoes):
        self.status_label.setText("")
        modelo = QStringListModel(sugestoes)
        self.completador.setModel(modelo)

    def gerar_pdf(self):
        try:
            self.relatorio_pdf.adicionar_titulos()
            self.relatorio_pdf.adicionar_conteudo(self.dados_bomba.vazão, self.dados_bomba.tempo, self.dados_bomba.diâmetro)
            self.relatorio_pdf.gravar_pdf()
        except Exception as e:
            QMessageBox.critical(self, 'ERRO', f'Erro ao gerar pdf devido a {e}')
    
    def permissao(self, url, feature):
        if feature == QWebEnginePage.Feature.Geolocation:
            resposta = QMessageBox.question(
                self,
                "Permissão de Localização",
                "Este site deseja acessar sua localização. Permitir?",
                QMessageBox.Yes | QMessageBox.No
            )

            if resposta == QMessageBox.Yes:
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
            else:
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)

    def plotar_gráfico(self):
        self.gráfico = Graficos(self.dados_bomba.vazão)
        self.grafico.calculo_K()
        self.grafico.curva_car()
        self.grafico.configuracoes_grafico()
        self.grafico.plotar()

        self.graph_curve.setChart(self.grafico.chart())
    
    def formula_hazen_recebida(self, mostrar):
        self.comboBox_3.setVisible(mostrar)

    def formula_darcy_recebida(self, mostrar):
        self.comboBox.setVisible(mostrar)
    
    def receber_unidades(self, itens):
        self.icone_2.clear()
        for item in itens:
            self.icone_2.addItem(item)

    def janela_perdas(self):
        janela = Dialog_main()
        janela.exec()

    def janela_config(self):
        janela = Config_main()
        janela.itens_combo.connect(self.receber_unidades)
        janela.formula_mudada.connect(self.formula_hazen_recebida)
        janela.formula_mudada_2.connect(self.formula_darcy_recebida)
        janela.sincronizar.connect(self.actualizar_espaco)
        self.sincronizar.connect(janela.actualizar_espaco)

        janela.exec()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(r"estilos\estilos.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    app.exec()

