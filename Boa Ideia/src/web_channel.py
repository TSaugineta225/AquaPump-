"""Objectos QWebChannel usados pelo editor hidráulico do AquaPump."""
from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot


class Dados(QObject):
    """Envia valores e unidades da aplicação para as funções JS existentes."""

    def enviar_dados(self, vazao, tempo, altura, potencia, view):
        valores = [float(vazao), float(tempo), float(altura), float(potencia)]
        import json
        payload = json.dumps(valores, allow_nan=False)
        view.page().runJavaScript(
            "(function(v){ if(window.receber_dados) window.receber_dados.apply(window,v); })(" + payload + ");"
        )

    def enviar_unidades(self, unidade_vazao, unidade_diametro, unidade_altura, unidade_potencia, view):
        import json
        valores = [str(unidade_vazao), str(unidade_diametro), str(unidade_altura), str(unidade_potencia)]
        payload = json.dumps(valores, ensure_ascii=False)
        view.page().runJavaScript(
            "(function(v){ if(window.receber_unidades) window.receber_unidades.apply(window,v); })(" + payload + ");"
        )


class Altura_Geometrica(QObject):
    altura_recebida = Signal(float)

    @Slot(float)
    def altura_(self, valor):
        self.altura_recebida.emit(float(valor))


class Dimensao_Tubulacao(QObject):
    comprimento_recebido = Signal(float)

    @Slot(float)
    def comprimento_(self, valor):
        self.comprimento_recebido.emit(float(valor))


class Acessorios_sistema(QObject):
    """Recebe o modelo integral enviado por publishAccessories() no JavaScript."""
    modelo = Signal(object)

    @Slot('QVariant')
    def modelo_hidraulico(self, modelo):
        if isinstance(modelo, dict):
            self.modelo.emit(modelo)

    # Compatibilidade com a assinatura antiga do editor.
    @Slot('QVariant')
    def lista_acessorios(self, lista):
        if isinstance(lista, list):
            self.modelo.emit({"pipes": [], "components": lista})
