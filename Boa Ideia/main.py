import sys
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QToolButton
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QPoint, QEvent, Qt, QSize
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from gui.Ui_main import Ui_Form
from gui.Loses_main import Dialog_main
import gui.img_rc

class MainWindow(FramelessWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
        # Menus
        #self.arquivo.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
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

        self.abrir_layout_2.clicked.connect(self.layout_lateral)
        self.fechar_layout_2.clicked.connect(self.layout_lateral) 

        self.pushButton_5.clicked.connect(self.projecto_aba)
        self.parametros.clicked.connect(self.exportar_aba)

        self.pushButton_3.clicked.connect(self.janela_perdas) 
        self.comboBox.setHidden(True)

    def layout_lateral(self):
        width = self.frame_3.width()

        if width == 0:
            newWidth = 280
            self.fechar_layout_2.setHidden(True)
        else:
            newWidth = 0
            self.fechar_layout_2.setHidden(False)
        
        self.animacao = QPropertyAnimation(self.frame_3, b"maximumWidth")
        self.animacao.setDuration(300) 
        self.animacao.setStartValue(width)
        self.animacao.setEndValue(newWidth)
        self.animacao.setEasingCurve(QEasingCurve.OutCubic)
        self.animacao.start()

    def exportar_aba(self):
        height = self.exportar.height()
        
        if height == 0:
            newHeight = 100

        else:
            newHeight = 0
        
        self.animacao_2 = QPropertyAnimation(self.exportar, b"maximumHeight")
        self.animacao_2.setDuration(300) 
        self.animacao_2.setStartValue(height)
        self.animacao_2.setEndValue(newHeight)
        self.animacao_2.setEasingCurve(QEasingCurve.OutCubic)
        self.animacao_2.start()

    def projecto_aba(self):
        height = self.projecto.height()

        if height == 0:
            newHeight = 140
        else:
            newHeight = 0
        
        self.animacao_1 = QPropertyAnimation(self.projecto, b"maximumHeight")
        self.animacao_1.setDuration(300) 
        self.animacao_1.setStartValue(height)
        self.animacao_1.setEndValue(newHeight)
        self.animacao_1.setEasingCurve(QEasingCurve.OutCubic)
        self.animacao_1.start()

    def janela_perdas(self):
        janela = Dialog_main()
        janela.exec()


if __name__ == "__main__": 
    QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

