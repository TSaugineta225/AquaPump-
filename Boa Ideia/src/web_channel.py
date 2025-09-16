from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Slot, Signal, QUrl
import json

class Dados():
    def __init__(self):
        self.valor_1 = 0
        self.valor_2 = 0
        self.valor_3 = 0
        self.valor_4 = 0

        self.unidade_1 = ''
        self.unidade_2 = ''
        self.unidade_3 = ''
        self.unidade_4 = ''

    def enviar_dados(self, vazão, diametro, altura, potencia, pagina):
        self.valor_1 = float(vazão)
        self.valor_2 = float(diametro)
        self.valor_3 = float(altura)
        self.valor_4 = float(potencia)

        pagina.page().runJavaScript(f"receber_dados({self.valor_1}, {self.valor_2}, {self.valor_3}, {self.valor_4})")
    
    def enviar_unidades(self, unidade_vazao, unidade_diametro, unidade_altura, unidade_potencia, pagina):
        self.unidade_1 = unidade_vazao
        self.unidade_2 = unidade_diametro
        self.unidade_3 = unidade_altura
        self.unidade_4 = unidade_potencia

        pagina.page().runJavaScript(
            f"receber_unidades({json.dumps(self.unidade_1)}, {json.dumps(self.unidade_2)}, {json.dumps(self.unidade_3)}, {json.dumps(self.unidade_4)})"
        )
        print(f"Unidades enviadas para a página web: {self.unidade_1}, {self.unidade_2}, {self.unidade_3}, {self.unidade_4}")

class Outros_dados():
    @Slot(str)
    def mensagem_recebida(self, msg):
        QMessageBox.Error(None, "Erro", msg)

class Altura_Geometrica (QObject):
    altura_recebido = Signal(float)
    def __init__(self):
        super().__init__()

        
    @Slot(float)
    def altura_(self, altura):
        self.altura_recebido.emit(altura)

class Dimensao_Tubulacao (QObject):
    comprimento_recebido = Signal(float)
    def __init__(self):
        super().__init__()

    @Slot(float)
    def comprimento_(self, comprimento):
        self.comprimento_recebido.emit(comprimento)


class Acessorios_sistema(QObject):
    lista = Signal(list)

    def __init__(self):
        super().__init__()
    
    @Slot(list)
    def lista_acessorios(self, lista):
        self.lista.emit(lista)

        

       



