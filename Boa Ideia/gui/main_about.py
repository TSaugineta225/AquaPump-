# -*- coding: utf-8 -*-
"""Controlador da janela "Sobre" do AquaPump."""

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from gui.Ui_about import Ui_Dialog


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # A interface redesenhada já trata os links na própria Ui_Dialog.
        # Estas ligações opcionais mantêm compatibilidade com a interface antiga,
        # caso ela ainda tenha os atributos "git" e "link".
        self._ligar_link_legado(
            "git", "https://github.com/TSaugineta225"
        )
        self._ligar_link_legado(
            "link", "https://www.linkedin.com/in/tenerife-saugineta/"
        )

    def _ligar_link_legado(self, atributo, url):
        widget = getattr(self.ui, atributo, None)
        if widget is None:
            return

        sinal = getattr(widget, "linkActivated", None)
        if sinal is not None:
            sinal.connect(lambda _texto=None, destino=url: self.abrir_link(destino))

    @staticmethod
    def abrir_link(link):
        QDesktopServices.openUrl(QUrl(link))
