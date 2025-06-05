from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Slot, Signal, QUrl

class Dados():
    def __init__(self):
        pass

    def enviar_dados(self, vazão, tempo, pagina):
        self.valor_1 = float(vazão.text())
        self.valor_2 = float(tempo.text())

        pagina.page().runJavaScript(f"receber_dados({self.valor_1}, {self.valor_2})")

class Outros_dados():
    @Slot(str)
    def mensagem_recebida(self, msg):
        QMessageBox.Error(None, "Erro", msg)



