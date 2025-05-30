from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QHeaderView
from PySide6.QtCore import Qt
from gui.Ui_perdas import Ui_Dialog
import gui.img_rc


class Dialog_main(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
    
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        self.ui.botao_succao.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.botao_recalque.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.botao_metodo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

        self.ui.tabela_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabela_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.estilo_spin = """ QDoubleSpinBox {
    background-color: #FFFFFF;
    border: 2px solid #CCCCCC;
    border-radius: 1px;
    padding: 2px 6px;
    font-size: 14px;
    color: #333333;
}
QDoubleSpinBox:focus {
    border: 2px solid #5B9BD5;
    background-color: #F0F8FF;
}
QDoubleSpinBox::up-button{
    background-color: #F3F3F3;
    border-left: 1px solid #CCCCCC;
    width: 16px;
    image:url(:/img/arrow-up.png);
}
QDoubleSpinBox::down-button {
    background-color: #F3F3F3;
    border-left: 1px solid #CCCCCC;
    width: 16px;
    image:url(:/img/arrow-down-1.png);
}
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #E6F0FF;
}

QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
    width: 8px;
    height: 8px;
} """ 
        
        for row in range(self.ui.tabela_1.rowCount()):
            
            item2 = self.ui.tabela_1.item(row, 0)
            if item2:
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)

            valor_existente = self.ui.tabela_1.item(row, 1).text() if self.ui.tabela_1.item(row, 1) else "0"
            self.spin = QDoubleSpinBox()
            self.spin.setRange(0, 99999)
            self.spin.setValue(int(valor_existente))
            self.ui.tabela_1.setCellWidget(row, 1, self.spin)
            self.spin.setStyleSheet(self.estilo_spin)
        
        for row in range(self.ui.tabela_2.rowCount()):
            
            item2 = self.ui.tabela_2.item(row, 0)
            if item2:
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)

            valor_existente = self.ui.tabela_2.item(row, 1).text() if self.ui.tabela_2.item(row, 1) else "0"
            self.spin_1 = QDoubleSpinBox()
            self.spin_1.setRange(0, 99999)
            self.spin_1.setValue(int(valor_existente))
            self.ui.tabela_2.setCellWidget(row, 1, self.spin_1)
            self.spin_1.setStyleSheet(self.estilo_spin)

        
        self.ui.comboBox_2.setHidden(True)
        self.ui.comboBox.setHidden(True)

        self.ui.darcy.toggled.connect(self.actualizar_combobo)
        self.ui.wiliams.toggled.connect(self.actualizar_combobo)

    def actualizar_combobo(self):
        if self.ui.darcy.isChecked():
            self.ui.comboBox_2.setHidden(True)
            self.ui.comboBox.setHidden(True)
            self.ui.comboBox_3.setHidden(False)
            self.ui.comboBox_4.setHidden(False)
        
        elif self.ui.wiliams.isChecked():
            self.ui.comboBox_3.setHidden(True)
            self.ui.comboBox_4.setHidden(True)
            self.ui.comboBox_2.setHidden(False)
            self.ui.comboBox.setHidden(False)
        



        