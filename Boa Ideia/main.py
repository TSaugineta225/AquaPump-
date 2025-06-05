import sys
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QToolButton, QMessageBox
from PySide6.QtGui import QAction, QIcon,QDoubleValidator, QSurfaceFormat
from PySide6.QtCore import QPoint, QEvent, Qt, QSize
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QUrl, Qt, QTimer
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel
from gui.Ui_main import Ui_Form
from gui.Loses_main import Dialog_main
from gui.config_main import Config_main
from scripts.animações import Animações
#from scripts.mapa import Mapa
from scripts.JavaScript import Mapa
from scripts.web_channel import Dados
import os
from scripts.net_var import VerificadorConexaoInternet
import gui.img_rc

os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_OPENGL"] = "software"

class MainWindow(FramelessWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.animações = Animações()
        self.web_channel = Dados()
        self.verificar = VerificadorConexaoInternet()

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

        self.pushButton_5.clicked.connect(lambda: self.animações.altura(self.projecto))
        self.parametros.clicked.connect(lambda: self.animações.altura(self.exportar, altura=100))
        self.configuracoes.clicked.connect(self.janela_config)

        self.pushButton_3.clicked.connect(self.janela_perdas) 
        self.comboBox.setHidden(True)

        validator = QDoubleValidator(0.0, 1000.0, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.lineEdit_2.setValidator(validator)
        self.lineEdit_3.setValidator(validator)

        # HTML, MAPA
        self.mapinha = Mapa()
        mapa = self.mapinha.html_code
        self.view.setHtml(mapa)

        # Web Channel
        self.lineEdit_2.textChanged.connect(self.enviar_js)
        self.lineEdit_3.textChanged.connect(self.enviar_js)

        #self._canal = QWebChannel()
        #self._canal.registerObject()

        ## Conexão a internet
        self.timer = QTimer()
        self.timer.timeout.connect(self.verificar.verificar)
        self.timer.start(10000)
        self.verificar.conexao_finalizada.connect(self.net_var)
        self.estado_anterior = None 
        self.verificar.verificar()

    def net_var(self, conectado):
        if conectado != self.estado_anterior:
            if conectado:
                QMessageBox.information(self, "Informação", "Internet Reestabelecida")
            else:
                QMessageBox.critical(self, "Aviso", "Ligue-se a uma rede Wi-fi para prosseguir")
            self.estado_anterior = conectado

    def enviar_js(self):
        self.web_channel.enviar_dados(self.lineEdit_2, self.lineEdit_3, self.view)

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

