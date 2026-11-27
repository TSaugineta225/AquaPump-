"""Menus principais da aplicação AquaPump."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QMessageBox

import img.img_rc


class Menus:
    def __init__(self, parent=None, config=None):
        self.parent = parent
        self.config = config
        self.menu_recentes = QMenu("Projectos recentes", self.parent)

    def menu_principal(self):
        menu = QMenu(self.parent)
        novo = QAction("Novo projecto", self.parent)
        abrir = QAction("Abrir projecto…", self.parent)
        salvar = QAction("Guardar", self.parent)
        salvar_como = QAction("Guardar como…", self.parent)
        fechar = QAction("Fechar projecto", self.parent)
        sair = QAction("Sair", self.parent)

        novo.setShortcut("Ctrl+N")
        abrir.setShortcut("Ctrl+O")
        salvar.setShortcut("Ctrl+S")
        salvar_como.setShortcut("Ctrl+Shift+S")
        fechar.setShortcut("Ctrl+W")
        sair.setShortcut("Ctrl+Q")
        for action in (novo, abrir, salvar, salvar_como, fechar, sair):
            action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)

        novo.triggered.connect(lambda checked=False: self.parent.novo_projecto())
        abrir.triggered.connect(lambda checked=False: self.parent.carregar_historico())
        salvar.triggered.connect(lambda checked=False: self.parent.salvar_historico())
        salvar_como.triggered.connect(lambda checked=False: self.parent.salvar_historico(como=True))
        fechar.triggered.connect(lambda checked=False: self.parent.novo_projecto())
        sair.triggered.connect(self.parent.close)

        self.atualizar_menu_recentes()
        menu.addActions([novo, abrir])
        menu.addMenu(self.menu_recentes)
        menu.addSeparator()
        menu.addActions([salvar, salvar_como, fechar])
        menu.addSeparator()
        menu.addAction(sair)
        return menu

    def menu_editar(self):
        menu = QMenu("Editar", self.parent)
        configuracoes = QAction("Configurações", self.parent)
        configuracoes.setShortcut("Ctrl+E")
        configuracoes.triggered.connect(
            lambda checked=False: self.parent.stackedWidget.setCurrentIndex(1)
        )
        menu.addAction(configuracoes)
        return menu

    def menu_relatorio(self):
        menu = QMenu("Relatórios", self.parent)
        submenu = QMenu("Exportar", menu)
        pdf = QAction(QIcon(":/img/pdf.png"), "Exportar para PDF", self.parent)
        excel = QAction(QIcon(":/img/arquivo-csv.png"), "Exportar para Excel (.xlsx)", self.parent)
        pdf.setShortcut("Ctrl+Shift+P")
        excel.setShortcut("Ctrl+Shift+X")
        pdf.triggered.connect(lambda checked=False: self.parent.gerar_pdf())
        excel.triggered.connect(lambda checked=False: self.parent.gerar_csv())
        submenu.addActions([pdf, excel])
        menu.addMenu(submenu)
        return menu

    def menu_ajuda(self):
        menu = QMenu("Ajuda", self.parent)
        suporte = QAction("Suporte técnico", self.parent)
        sobre = QAction("Sobre o AquaPump", self.parent)
        suporte.triggered.connect(lambda checked=False: QMessageBox.information(
            self.parent, "Suporte técnico",
            "Para suporte técnico, contacte:\n"
            "tenerifenhalicale@outlook.com\n+258 86 843 9510",
        ))
        sobre.triggered.connect(lambda checked=False: self.parent.janela_sobre.exec())
        menu.addActions([suporte, sobre])
        return menu

    def menu_selecao_graficos(self):
        menu = QMenu(self.parent)
        pages = (
            ("Curva H vs Q (Altura vs Vazão)", 0),
            ("Curva de Potência vs Vazão", 1),
            ("Curva de Rendimento vs Vazão", 2),
        )
        for title, index in pages:
            action = QAction(title, self.parent)
            action.triggered.connect(
                lambda checked=False, i=index, t=title: self.sub_menus_selecao(t, i)
            )
            menu.addAction(action)
        return menu

    def atualizar_menu_recentes(self):
        self.menu_recentes.clear()
        recentes = self.config.obter_projetos_recentes() if self.config else []
        self.menu_recentes.setEnabled(bool(recentes))
        for caminho in recentes:
            action = QAction(str(caminho), self.parent)
            action.setToolTip(str(caminho))
            action.triggered.connect(
                lambda checked=False, path=str(caminho): self.abrir_projeto(path)
            )
            self.menu_recentes.addAction(action)

    def abrir_projeto(self, caminho):
        """Abre realmente o projecto, em vez de apenas mostrar o seu caminho."""
        return self.parent.carregar_historico(caminho)

    def sub_menus_selecao(self, titulo, index):
        self.parent.label_2.setText(titulo)
        self.parent.stackedWidget_3.setCurrentIndex(index)
