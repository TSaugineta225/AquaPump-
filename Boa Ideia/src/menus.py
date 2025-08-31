from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
import webbrowser
import img.img_rc


class Menus:
    def __init__(self, parent=None, config=None):
        self.parent = parent  
        self.config = config  # objeto com métodos de projetos recentes
        self.menu_recentes = QMenu("Projetos Recentes", self.parent)

    # ---------------- MENU PRINCIPAL ----------------
    def menu_principal(self):
        menu = QMenu(self.parent)

        # --- Ações ---
        acao_novo = QAction("Novo", self.parent)
        acao_abrir = QAction("Abrir", self.parent)
        acao_salvar = QAction("Salvar", self.parent)
        acao_salvar_como = QAction("Salvar Como", self.parent)
        acao_fechar = QAction("Fechar Projeto", self.parent)
        acao_sair = QAction("Sair", self.parent)

        # --- Atalhos ---
        acao_novo.setShortcut("Ctrl+N")
        acao_abrir.setShortcut("Ctrl+O")
        acao_salvar.setShortcut("Ctrl+S")
        acao_salvar_como.setShortcut("Ctrl+Shift+S")
        acao_fechar.setShortcut("Ctrl+W")
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.setShortcutContext(Qt.ApplicationShortcut)
        acao_abrir.setShortcutContext(Qt.ApplicationShortcut)
        acao_salvar.setShortcutContext(Qt.ApplicationShortcut)
        acao_novo.setShortcutContext(Qt.ApplicationShortcut)

        # --- Sinais ---
        if self.parent:
            acao_sair.triggered.connect(self.parent.close)
            acao_abrir.triggered.connect(self.parent.carregar_historico)
            acao_salvar.triggered.connect(self.parent.salvar_historico)
            acao_novo.triggered.connect(self.parent.novo_projecto)

        # --- Submenus ---
        self.atualizar_menu_recentes()

        # --- Adição ao menu ---
        menu.addActions([
            acao_novo, acao_abrir, self.menu_recentes.menuAction(),
            acao_salvar
        ])
        menu.addSeparator()
        menu.addAction(acao_sair)

        return menu

    # ---------------- MENU EDITAR ----------------
    def menu_editar(self):
        editar = QMenu("Editar", self.parent)

        # --- Ações ---
        acao_config = QAction("Configurações", self.parent)
        acao_parametros = QAction("Parâmetros do Projeto", self.parent)

        # --- Atalhos ---
        acao_config.setShortcut("Ctrl+E")
        acao_parametros.setShortcut("Ctrl+P")

        # --- Sinais ---
        if self.parent:
            acao_config.triggered.connect(lambda: self.parent.stackedWidget.setCurrentIndex(1))

        editar.addActions([acao_config])
        return editar

    # ---------------- MENU RELATÓRIOS ----------------
    def menu_relatorio(self):
        rel = QMenu("Relatórios", self.parent)

        # --- Ações principais ---

        acao_exportar = QAction("Exportar", self.parent)
        
        # --- Submenu Exportar ---
        submenu_exportar = QMenu("Exportar", rel)
        exportar_pdf = QAction(QIcon(":/img/pdf.png"), "Exportar para PDF", self.parent)
        exportar_csv = QAction(QIcon(":/img/arquivo-csv.png"), "Exportar para CSV", self.parent)

        exportar_csv.setShortcut("Ctrl+Shift+C")
        exportar_pdf.setShortcut("Ctrl+Shift+P")
        exportar_csv.setShortcutContext(Qt.ApplicationShortcut)
        exportar_pdf.setShortcutContext(Qt.ApplicationShortcut)

        # --- Sinais ---
        if self.parent:
            exportar_pdf.triggered.connect(self.parent.gerar_pdf)
            exportar_csv.triggered.connect(self.parent.gerar_csv)

        submenu_exportar.addActions([exportar_pdf, exportar_csv])
        acao_exportar.setMenu(submenu_exportar)

        # --- Adição ao menu ---
        rel.addActions( [acao_exportar])
        return rel

    # ---------------- MENU AJUDA ----------------
    def menu_ajuda(self):
        help_menu = QMenu("Ajuda", self.parent)

        # --- Ações ---
        acao_manual = QAction("Manual do Usuário", self.parent)
        acao_sobre = QAction("Sobre o Programa", self.parent)
        acao_suporte = QAction("Suporte Técnico", self.parent)

        # --- Atalhos ---
        acao_manual.setShortcut("Ctrl+M")
        acao_sobre.setShortcut("Ctrl+I")
        acao_suporte.setShortcut("Ctrl+T")

        # --- Sinais ---
        if self.parent:
            acao_suporte.triggered.connect(lambda: QMessageBox.information(
                self.parent, "Suporte Técnico",
                "Para suporte técnico, por favor contate:\nEmail: tenerifenhalicale@outlook.com\nTelefone: +258 86 843 9510"
            ))

            acao_sobre.triggered.connect(lambda: self.parent.janela_sobre.exec())
           

        help_menu.addActions([acao_manual,acao_suporte])
        help_menu.addSeparator()
        help_menu.addAction(acao_sobre)
        return help_menu

    # ---------------- MENU GRÁFICOS ----------------
    def menu_graficos(self):
        grafico_menu = QMenu(self.parent)

        # --- Ações ---
        perfil = QAction("Perfil de Elevação", self.parent)
        curva = QAction("Curvas de Bombas/Associação", self.parent)

        # --- Sinais ---
        if self.parent:
            perfil.triggered.connect(lambda: self.parent.animações.altura(self.parent.widget_2, altura=400))
            curva.triggered.connect(lambda: self.parent.animações.largura(self.parent.janel_direita, largura_alvo=500))

        grafico_menu.addActions([curva, perfil])
        return grafico_menu

    # ---------------- MENU SELEÇÃO DE GRÁFICOS ----------------
    def menu_selecao_graficos(self):
        selecao = QMenu(self.parent)

        # --- Ações ---
        self.principal = QAction("Curva H vs Q (Altura vs Vazão)", self.parent)
        self.potencia = QAction("Curva de Potência vs Vazão (P vs Q)", self.parent)
        self.rendimento = QAction("Curva de Eficiência vs Vazão (η vs Q)", self.parent)

        # --- Sinais ---
        if self.parent:
            self.principal.triggered.connect(lambda: self.sub_menus_selecao(self.principal, 0))
            self.potencia.triggered.connect(lambda: self.sub_menus_selecao(self.potencia, 1))
            self.rendimento.triggered.connect(lambda: self.sub_menus_selecao(self.rendimento, 2))

        selecao.addActions([self.principal, self.potencia, self.rendimento])
        return selecao

    # ---------------- FUNÇÕES AUXILIARES ----------------
    def atualizar_menu_recentes(self):
        self.menu_recentes.clear()

        if not self.config:
            return

        recentes = self.config.obter_projetos_recentes()
        if recentes:
            for caminho in recentes:
                acao = QAction(caminho, self.parent)
                acao.triggered.connect(lambda checked=False, path=caminho: self.abrir_projeto(path))
                self.menu_recentes.addAction(acao)
        else:
            self.menu_recentes.setEnabled(False)

    def abrir_projeto(self, caminho):
        QMessageBox.information(self.parent, "Abrir Projeto", f"A abrir o projeto:\n{caminho}")
        if self.config:
            self.config.adicionar_projeto_recente(caminho)
            self.atualizar_menu_recentes()

    def sub_menus_selecao(self, acao, index):
        self.parent.label_2.setText(acao.text())
        self.parent.stackedWidget_3.setCurrentIndex(index)
