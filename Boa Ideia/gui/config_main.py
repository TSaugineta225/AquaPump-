from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QHeaderView
from PySide6.QtCore import Qt, Signal
from gui.Ui_config import Ui_Dialog
import gui.img_rc


class Config_main(QDialog):
    unidades = Signal(str, str)
    formula_mudada = Signal(bool)
    formula_mudada_2 = Signal(bool)
    sincronizar = Signal(int)
    itens_combo = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ex_3 = chr(0x00B3)

        self.ui.geral.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.unidades.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        self.ui.avancado.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
    
        self.ui.radioButton.toggled.connect(self.actualizar_unidades)
        self.ui.radioButton_2.toggled.connect(self.actualizar_unidades)

        self.ui.radioButton_7.toggled.connect(self.enviar_formulas_hazen)
        self.ui.radioButton_8.toggled.connect(self.enviar_formula_darcy)

        self.ui.caudal_box.addItems([
            f'm{self.ex_3}/s', 
            f'm{self.ex_3}/min', 
            f'm{self.ex_3}/h', 
            f'L/s', ])
        self.ui.altura_box.addItem('m')
        self.ui.comprimento_box.addItem('m')
        self.ui.diametro_box.addItems([
            'mm',
            'm'
        ])
        self.ui.potencia_box.addItems([
            'KW',
            'W',
            'CV'
        ])
        self.ui.npsh_box.addItem('m') 

        self._sincronizar = False 
        self.ui.caudal_box.currentIndexChanged.connect(self.emitir_sinal_sincro)

    def actualizar_unidades(self):
        itens = []
        itens.clear()
        self.ui.caudal_box.clear()
        self.ui.altura_box.clear()
        self.ui.comprimento_box.clear()
        self.ui.diametro_box.clear()
        self.ui.comprimento.clear()
        self.ui.potencia.clear()
        self.ex_3 = chr(0x00B3)
        if self.ui.radioButton.isChecked():
            self.ui.caudal_box.addItems([
                f'm{self.ex_3}/s', 
                f'm{self.ex_3}/min', 
                f'm{self.ex_3}/h', 
                f'L/s', ])
            self.ui.altura_box.addItem('m')
            self.ui.comprimento_box.addItem('m')
            self.ui.diametro_box.addItems([
                'mm',
                'm'
            ])
            self.ui.potencia_box.addItems([
                'KW',
                'W',
                'CV'
            ])
            self.ui.npsh_box.addItem('m')

            for item in range (self.ui.caudal_box.count()):
                itens.append(self.ui.caudal_box.itemText(item))

            self.itens_combo.emit(itens)

        elif self.ui.radioButton_2.isChecked():
            self.ui.caudal_box.addItems(['GPM', 'MGD', 'GPH'])
            self.ui.altura_box.addItem('ft')
            self.ui.comprimento_box.addItem('ft')
            self.ui.diametro_box.addItem('in')
            self.ui.potencia_box.addItem('hp')
            self.ui.npsh_box.addItem('ft')

            for item in range (self.ui.caudal_box.count()):
                itens.append(self.ui.caudal_box.itemText(item))

            self.itens_combo.emit(itens)

    def enviar_formulas_hazen(self):
        self.formula_mudada.emit(self.ui.radioButton_7.isChecked())
    
    def enviar_formula_darcy(self):
        self.formula_mudada_2.emit(self.ui.radioButton_8.isChecked())

    def enviar_unidades(self):
        caudal = self.ui.caudal_box.currentText()
        altura = self.ui.altura_box.currentText()
        comprimento = self.ui.comprimento_box.currentText()
        diametro = self.ui.diametro_box.currentText()
        potencia = self.ui.potencia_box.currentText()

        self.unidades.emit(caudal, altura)
    
    def emitir_sinal_sincro(self, index):
        if self._sincronizar:
            return
        
        self.sincronizar.emit(index)
    
    def actualizar_espaco(self, index):
        self._sincronizar = True
        self.ui.caudal_box.setCurrentIndex(index)
        self._sincronizar = False
