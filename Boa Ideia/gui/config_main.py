from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QHeaderView
from PySide6.QtCore import Qt
from gui.Ui_config import Ui_Dialog
import gui.img_rc


class Config_main(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))