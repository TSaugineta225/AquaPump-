from PySide6.QtWidgets import QDialog
from gui.Ui_about import Ui_Dialog
import webbrowser


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.git.linkActivated.connect(lambda:self.abrir_link("https://github.com/TSaugineta225"))
        self.ui.link.linkActivated.connect(lambda:self.abrir_link("https://www.linkedin.com/in/tenerife-saugineta/"))

    def abrir_link(self, link):
        webbrowser.open(link)