from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Slot, Signal, QUrl

class Dados():
    def __init__(self):
        self.valor_1 = 0
        self.valor_2 = 0

    def enviar_dados(self, vazão, tempo, pagina):
        self.valor_1 = float(vazão.text())
        self.valor_2 = float(tempo.text())

        pagina.page().runJavaScript(f"receber_dados({self.valor_1}, {self.valor_2})")

class Outros_dados():
    @Slot(str)
    def mensagem_recebida(self, msg):
        QMessageBox.Error(None, "Erro", msg)

class Relatório (QObject):
    def __init__(self):
        super().__init__()
        self.vazão = 0
        self.tempo = 0
        self.potencia = 0
        self.diâmetro = 0
        self.latitude = 0
        self.longitude = 0
        self.altura = 0
        
    @Slot(float, float, float, float)
    def valores_recebidos(self, flow, tempo, altura, diametro):
        self.vazão = float(flow)
        self.tempo = float(tempo)
        self.altura = float(altura)
        self.diametro = float(diametro)



