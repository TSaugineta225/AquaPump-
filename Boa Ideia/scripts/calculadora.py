import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QGridLayout, QMessageBox
)
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtCore import Qt

class ConversorVolume(QWidget):
    """
    Uma janela de aplicação para converter unidades de volume.
    Migrado de customtkinter e refatorado para PySide6.
    """
    def __init__(self):
        super().__init__()
        
        # Dicionário central para todas as unidades, fatores e símbolos.
        # A unidade base para conversão é 'Litros'.
        # O fator representa quantos litros existem em uma unidade da chave.
        self.UNIDADES = {
            'Litros':                   {'fator': 1.0, 'simbolo': 'L'},
            'Metros Cúbicos':           {'fator': 1000.0, 'simbolo': 'm³'},
            'Decímetros Cúbicos':       {'fator': 1.0, 'simbolo': 'dm³'},
            'Centímetros Cúbicos':      {'fator': 0.001, 'simbolo': 'cm³'},
            'Milímetros Cúbicos':       {'fator': 1e-6, 'simbolo': 'mm³'},
            'Polegadas Cúbicas':        {'fator': 0.0163871, 'simbolo': 'in³'},
            'Pés Cúbicos':              {'fator': 28.3168, 'simbolo': 'ft³'},
            'Barris (Petróleo)':        {'fator': 158.987, 'simbolo': 'bbl'},
            'Galões (EUA)':             {'fator': 3.78541, 'simbolo': 'gal'},
        }
        
        self._configurar_ui()

    def _configurar_ui(self):
        """Inicializa e configura a interface do usuário."""
        self.setWindowTitle('Conversor de Unidades de Volume')
        
        # Layout
        layout = QGridLayout(self)

        # Widgets
        titulo_label = QLabel('Conversor de Unidades de Volume')
        titulo_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))

        valor_label = QLabel('Valor:')
        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Insira o valor a converter")
        # Adicionar um validador para aceitar apenas números
        self.valor_input.setValidator(QDoubleValidator())
        
        unidade_inicial_label = QLabel('De:')
        self.combo_inicial = QComboBox()
        self.combo_inicial.addItems(self.UNIDADES.keys())

        unidade_final_label = QLabel('Para:')
        self.combo_final = QComboBox()
        self.combo_final.addItems(self.UNIDADES.keys())
        self.combo_final.setCurrentText('Metros Cúbicos')

        self.botao_converter = QPushButton('Converter')
        self.resultado_label = QLabel("Resultado aparecerá aqui")
        self.resultado_label.setFont(QFont('Arial', 12))
        self.resultado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultado_label.setStyleSheet("border: 1px solid gray; padding: 10px;")

        # Adicionar widgets ao layout
        layout.addWidget(titulo_label, 0, 0, 1, 2)
        layout.addWidget(valor_label, 1, 0)
        layout.addWidget(self.valor_input, 1, 1)
        layout.addWidget(unidade_inicial_label, 2, 0)
        layout.addWidget(self.combo_inicial, 2, 1)
        layout.addWidget(unidade_final_label, 3, 0)
        layout.addWidget(self.combo_final, 3, 1)
        layout.addWidget(self.botao_converter, 4, 0, 1, 2)
        layout.addWidget(self.resultado_label, 5, 0, 1, 2)

        # Conectar o sinal do botão ao slot (método de conversão)
        self.botao_converter.clicked.connect(self._realizar_conversao)

    def _realizar_conversao(self):
        """
        Executa a lógica de conversão de unidades.
        Este método substitui a complexa estrutura de if/elif.
        """
        try:
            valor_str = self.valor_input.text().replace(',', '.')
            if not valor_str:
                raise ValueError("Nenhum valor inserido.")
            
            valor_inicial = float(valor_str)
            unidade_origem = self.combo_inicial.currentText()
            unidade_destino = self.combo_final.currentText()
            
            # Se as unidades forem as mesmas, não há necessidade de calcular
            if unidade_origem == unidade_destino:
                resultado = valor_inicial
            else:
                # Fatores de conversão
                fator_origem = self.UNIDADES[unidade_origem]['fator']
                fator_destino = self.UNIDADES[unidade_destino]['fator']

                # 1. Converter o valor de entrada para a unidade base (Litros)
                valor_em_litros = valor_inicial * fator_origem
                
                # 2. Converter da unidade base para a unidade de destino
                resultado = valor_em_litros / fator_destino

            # Obter símbolos para exibição
            simbolo_origem = self.UNIDADES[unidade_origem]['simbolo']
            simbolo_destino = self.UNIDADES[unidade_destino]['simbolo']

            # Formatar e exibir o resultado
            # Usamos :.4g para formatação inteligente de casas decimais
            texto_resultado = f"{valor_inicial} {simbolo_origem} = {resultado:.4g} {simbolo_destino}"
            self.resultado_label.setText(texto_resultado)

        except ValueError as e:
            # Exibe uma caixa de diálogo de erro se a entrada for inválida
            QMessageBox.critical(self, 'Erro de Entrada', f"Por favor, insira um número válido. ({e})")
            self.resultado_label.setText("Erro!")
        except Exception as e:
            QMessageBox.critical(self, 'Erro Inesperado', f"Ocorreu um erro: {e}")
            self.resultado_label.setText("Erro!")

# --- Ponto de entrada da aplicação ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    conversor = ConversorVolume()
    conversor.show()
    sys.exit(app.exec())