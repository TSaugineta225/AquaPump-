import sys
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QToolButton, QMessageBox, QFileDialog, QCompleter, QLabel
from PySide6.QtGui import QAction, QIcon,QDoubleValidator, QSurfaceFormat
from PySide6.QtCore import QPoint, QEvent, Qt, QSize, Slot, QStringListModel
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QUrl, Qt, QTimer
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebChannel import QWebChannel
from gui.Ui_main import Ui_AquaPump
from gui.Loses_main import Dialog_main
from gui.config_main import Config_main
from scripts.animações import Animações
from scripts.JavaScript import Mapa
from scripts.web_channel import Dados, Relatório
from scripts.pdf_gen import PDF
from scripts.graficos import Graficos
from scripts.arquivos import Arquivos
from scripts.requisicoes import Pesquisa
import os, json
import gui.img_rc

os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_OPENGL"] = "software"

class MainWindow(FramelessWindow, Ui_AquaPump):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


        self.animações = Animações()
        self.dados_bomba = Relatório()
        self.dados = Dados()
        self.relatorio_pdf = PDF()
       
       # WebChannel e Permissões
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)
        self._canal.registerObject("dados_bomba", self.dados_bomba)
        
        self.Vazao_2.textChanged.connect(self.enviar_js)
        self.Vazao.textChanged.connect(self.enviar_js)
        self.page.featurePermissionRequested.connect(self.permissao)
        self.arquivos = Arquivos(self.view)

        self.menu = QMenu(self)
        acao_novo = QAction("Novo", self)
        acao_novo.setShortcut("Ctrl+N")

        acao_abrir = QAction("Abrir", self)
        acao_abrir.setShortcut("Ctrl+O")

        acao_salvar = QAction("Salvar", self)
        acao_salvar.setShortcut("Ctrl+S")

        acao_salvar_como = QAction("Salvar Como", self)
        acao_salvar_como.setShortcut("Ctrl+Shift+S")

        acao_fechar = QAction("Fechar Projeto", self)
        acao_fechar.setShortcut("Ctrl+W")

        acao_sair = QAction("Sair", self)
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.setShortcutContext(Qt.ApplicationShortcut)
        self.addAction(acao_sair)
        acao_sair.triggered.connect(lambda: app.quit())

        accao_coor =  QAction(QIcon(u":/img/kml.png"), "Carregar KML", self)
        self.addAction(accao_coor)
        accao_coor.triggered.connect(self.arquivos.carregar_kml)

        accao_coor_1 =  QAction(QIcon(u":/img/arquivo.png"), "Carregar camada shapefile", self)
        self.addAction(accao_coor_1)
        accao_coor_1.triggered.connect(self.arquivos.carregar_shapefile)

        accao_coor_2 =  QAction(QIcon(u":/img/arquivo-csv.png"), "Carregar coordenadas CSV", self)
        self.addAction(accao_coor_2)
        accao_coor_2.triggered.connect(self.arquivos.carregar_csv)

        # Adicionar ações ao menu
        self.menu.addAction(acao_novo)
        self.menu.addAction(acao_abrir)
        self.menu.addAction(acao_salvar)
        self.menu.addAction(acao_salvar_como)
        self.menu.addAction(acao_fechar)
        self.menu.addSeparator()
        self.menu.addAction(accao_coor)
        self.menu.addAction(accao_coor_1)
        self.menu.addAction(accao_coor_2)
        self.menu.addSeparator()
        self.menu.addAction(acao_sair)

        self.editar = QMenu(self)
        accao_config = QAction("Configurações", self)
        accao_config.setShortcut("Ctrl+E")
        accao_config.setShortcutContext(Qt.ApplicationShortcut)
        self.addAction(accao_config)
        accao_config.triggered.connect(self.janela_config)


        acao_parametros = QAction("Parâmetros do Projecto", self)
        acao_parametros.setShortcut("Ctrl+P")
        self.editar.addAction(accao_config)
        self.editar.addAction(acao_parametros)

        self.rel = QMenu(self)
        acao_relatorio = QAction("Relatório", self)
        acao_relatorio.setShortcut("Ctrl+R")

        acao_exportar = QAction("Exportar", self)
        acao_exportar.setShortcut("Ctrl+E")
        self.rel.addAction(acao_relatorio)
        self.rel.addAction(acao_exportar)

        self.help =QMenu(self)
        acao_manual = QAction("Manual do Usuário", self)
        acao_manual.setShortcut("Ctrl+M")

        acao_dicas = QAction("Dicas de Uso", self)
        acao_dicas.setShortcut("Ctrl+D")

        acao_sobre = QAction("Sobre o Programa", self)
        acao_sobre.setShortcut("Ctrl+I")

        acao_suporte = QAction("Suporte Técnico", self)
        acao_suporte.setShortcut("Ctrl+T")
        self.help.addAction(acao_manual)
        self.help.addAction(acao_dicas)
        self.help.addAction(acao_sobre)
        self.help.addAction(acao_suporte)

        self.arquivo_2.clicked.connect(lambda:self.menu.popup(self.arquivo_2.mapToGlobal(self.arquivo_2.rect().bottomLeft())))
        self.config_2.clicked.connect(lambda:self.editar.popup(self.config_2.mapToGlobal(self.config_2.rect().bottomLeft())))
        self.relatorio_2.clicked.connect(lambda:self.rel.popup(self.relatorio_2.mapToGlobal(self.relatorio_2.rect().bottomLeft())))
        self.ajuda_2.clicked.connect(lambda:self.help.popup(self.ajuda_2.mapToGlobal(self.ajuda_2.rect().bottomLeft())))
        
        # Aba Lateral
        self.abrir_layout_3.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6, largura_alvo=300))
        self.pesquisar_3.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6, largura_alvo=300))
        self.projeto.clicked.connect(lambda: self.animações.largura_altura(self.frame_4, self.projecto, self.frame_6))
        self.exportar_2.clicked.connect(lambda: self.animações.largura_altura(self.frame_4, self.exportar, self.frame_6, altura=100))
        self.abrir_layout_2.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6)) 
        self.sair_2.clicked.connect(lambda: app.quit())
        self.sair_3.clicked.connect(lambda: app.quit())

        self.projecto_2.clicked.connect(lambda: self.animações.altura(self.projecto, altura=400))
        self.parametros.clicked.connect(lambda: self.animações.altura(self.exportar, altura=100))
        self.configuracoes.clicked.connect(self.janela_config)
        self.configuracoes_2.clicked.connect(self.janela_config)
        self.exportar_pdf.clicked.connect(self.gerar_pdf)

        self.pushButton.clicked.connect(self.arquivos.carregar_kml)
        self.pushButton_2.clicked.connect(self.arquivos.carregar_csv)
        self.pushButton_4.clicked.connect(self.arquivos.carregar_shapefile)
        #self.mapa_2.clicked.connect(self.carregar_arquivo)

        #self.pushButton_3.clicked.connect(self.janela_perdas) 
        self.comboBox.setHidden(True)

        # Validadores
        validator = QDoubleValidator(0.0, 1000.0, 3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

        #Completadores
        self.completador = QCompleter()
        self.completador.setCaseSensitivity(Qt.CaseInsensitive)
        self.pesquisa_line.setCompleter(self.completador)

        self.pesquisa_line.textEdited.connect(self.pesquisa_mapa)
        self.pesquisa_line.returnPressed.connect(self.pesquisa_mapa)

        self.worker = None
        self.status_label = QLabel()

        # HTML, MAPA
        self.mapinha = Mapa()
        mapa = self.mapinha.html_code 
        self.page.setHtml(mapa)    

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

        self.chart_view.setChart(self.grafico.chart())

    def janela_perdas(self):
        janela = Dialog_main()
        janela.exec()

    def janela_config(self):
        janela = Config_main()
        janela.exec()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(r"estilos\estilos.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    app.exec()

