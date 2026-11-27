"""Objectos QWebChannel usados pelo editor hidráulico do AquaPump."""
from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot


class Dados(QObject):
    """Envia valores e unidades da aplicação para funções JavaScript existentes."""

    def enviar_dados(self, vazao, tempo, altura, potencia, view):
        import json

        valores = [float(vazao), float(tempo), float(altura), float(potencia)]
        payload = json.dumps(valores, allow_nan=False)
        view.page().runJavaScript(
            "(function(v){ if(window.receber_dados) window.receber_dados.apply(window,v); })("
            + payload + ");"
        )

    def enviar_unidades(
        self, unidade_vazao, unidade_diametro, unidade_altura, unidade_potencia, view
    ):
        import json

        valores = [
            str(unidade_vazao), str(unidade_diametro),
            str(unidade_altura), str(unidade_potencia),
        ]
        payload = json.dumps(valores, ensure_ascii=False)
        view.page().runJavaScript(
            "(function(v){ if(window.receber_unidades) window.receber_unidades.apply(window,v); })("
            + payload + ");"
        )


class Altura_Geometrica(QObject):
    altura_recebida = Signal(float)

    @Slot(float)
    def altura_(self, valor):
        self.altura_recebida.emit(float(valor))

    @Slot(float)
    def altura_recebido(self, valor):
        """Alias para a versão antiga do JavaScript (nome no masculino)."""
        self.altura_recebida.emit(float(valor))


class Dimensao_Tubulacao(QObject):
    comprimento_recebido = Signal(float)

    @Slot(float)
    def comprimento_(self, valor):
        self.comprimento_recebido.emit(float(valor))


class Acessorios_sistema(QObject):
    """Recebe o modelo integral do esquema e mantém compatibilidade com listas antigas."""
    modelo = Signal(object)
    lista = Signal(list)  # compatibilidade com versões antigas de conexoes_sinais.py

    @Slot('QVariant')
    def modelo_hidraulico(self, modelo):
        if not isinstance(modelo, dict):
            return
        pipes = modelo.get("pipes", modelo.get("tubulacoes", []))
        components = modelo.get("components", modelo.get("acessorios", []))
        if not isinstance(pipes, list) or not isinstance(components, list):
            return
        self.modelo.emit(modelo)

    @Slot('QVariant')
    def lista_acessorios(self, lista):
        """Recebe a lista antiga e a transforma num modelo hidráulico mínimo."""
        if not isinstance(lista, list):
            return
        payload = list(lista)
        self.lista.emit(payload)
        self.modelo.emit({"pipes": [], "components": payload})
