import sys
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QToolButton, QMessageBox, QFileDialog
from PySide6.QtGui import QAction, QIcon,QDoubleValidator, QSurfaceFormat
from PySide6.QtCore import QPoint, QEvent, Qt, QSize
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QUrl, Qt, QTimer
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebChannel import QWebChannel
from gui.Ui_main import Ui_Form
from gui.Loses_main import Dialog_main
from gui.config_main import Config_main
from scripts.animações import Animações
from scripts.JavaScript import Mapa
from scripts.web_channel import Dados, Relatório
from scripts.pdf_gen import PDF
from scripts.graficos import Graficos
from scripts.arquivos import Arquivos
import os, json
import gui.img_rc

os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_OPENGL"] = "software"

class MainWindow(FramelessWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


        self.animações = Animações()
        self.dados_bomba = Relatório()
        self.dados = Dados()
        self.relatorio_pdf = PDF()
        self.arquivos = Arquivos()
       
       # WebChannel e Permissões
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)
        self._canal.registerObject("dados_bomba", self.dados_bomba)
        self.lineEdit_2.textChanged.connect(self.enviar_js)
        self.lineEdit_3.textChanged.connect(self.enviar_js)
        self.page.featurePermissionRequested.connect(self.permissao)
        
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

        # Adicionar ações ao menu
        self.menu.addAction(acao_novo)
        self.menu.addAction(acao_abrir)
        self.menu.addAction(acao_salvar)
        self.menu.addAction(acao_salvar_como)
        self.menu.addAction(acao_fechar)
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

        self.arquivo.clicked.connect(lambda:self.menu.popup(self.arquivo.mapToGlobal(self.arquivo.rect().bottomLeft())))
        self.config.clicked.connect(lambda:self.editar.popup(self.config.mapToGlobal(self.config.rect().bottomLeft())))
        self.relatorio.clicked.connect(lambda:self.rel.popup(self.relatorio.mapToGlobal(self.relatorio.rect().bottomLeft())))
        self.ajuda.clicked.connect(lambda:self.help.popup(self.ajuda.mapToGlobal(self.ajuda.rect().bottomLeft())))
        self.sair_2.clicked.connect(lambda: app.quit())
        
        self.abrir_layout_2.clicked.connect(lambda: self.animações.largura(self.frame_3, self.fechar_layout_2))
        self.fechar_layout_2.clicked.connect(lambda: self.animações.largura(self.frame_3, self.fechar_layout_2)) 
        self.dimensionar_2.clicked.connect(lambda: self.animações.largura(self.janelas, largura_alvo=450))

        self.pushButton_5.clicked.connect(lambda: self.animações.altura(self.projecto))
        self.parametros.clicked.connect(lambda: self.animações.altura(self.exportar, altura=100))
        self.configuracoes.clicked.connect(self.janela_config)
        self.exportar_pdf.clicked.connect(self.gerar_pdf)
        #self.mapa_2.clicked.connect(self.carregar_arquivo)

        self.pushButton_3.clicked.connect(self.janela_perdas) 
        self.comboBox.setHidden(True)

        validator = QDoubleValidator(0.0, 1000.0, 3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.lineEdit_2.setValidator(validator)
        self.lineEdit_3.setValidator(validator)

        # HTML, MAPA
        self.mapinha = Mapa()
        mapa = self.mapinha.html_code 
        self.page.setHtml(mapa)    

    def enviar_js(self):
        self.dados.enviar_dados(self.lineEdit_2, self.lineEdit_3, self.view)

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

