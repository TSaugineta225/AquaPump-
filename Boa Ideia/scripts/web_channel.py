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

class Altura_Geometrica (QObject):
    altura_recebido = Signal(float)
    def __init__(self):
        super().__init__()

        
    @Slot(float)
    def valores_recebidos(self, altura):
        self.altura_recebido.emit(altura)

class Dimensao_Tubulacao (QObject):
    comprimento_recebido = Signal(float)
    def __init__(self):
        super().__init__()

    @Slot(float)
    def valores_recebidos(self, comprimento):
        self.comprimento_recebido.emit(comprimento)


class Acessorios_sistema(QObject):
    lista = Signal(list)

    def __init__(self):
        super().__init__()
    
    @Slot(list)
    def lista_acessorios(self, lista):
        self.lista.emit(lista)
        print("Lista de acessórios recebida:", lista)
        

       



