from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
import img.img_rc 

class Menus:
    def __init__(self, parent=None, arquivos=None, config=None):
        self.parent = parent  
        self.arquivos = arquivos  # objeto com métodos de carregamento de arquivos
        self.config = config  # objeto com métodos de projetos recentes
        self.menu_recentes = QMenu("Projetos Recentes", self.parent)

    def menu_principal(self):
        menu = QMenu(self.parent)

        acao_novo = QAction("Novo", self.parent)
        acao_abrir = QAction("Abrir", self.parent)
        acao_salvar = QAction("Salvar", self.parent)
        acao_salvar_como = QAction("Salvar Como", self.parent)
        acao_fechar = QAction("Fechar Projeto", self.parent)
        acao_sair = QAction("Sair", self.parent)

        # Atalhos
        acao_novo.setShortcut("Ctrl+N")
        acao_abrir.setShortcut("Ctrl+O")
        acao_salvar.setShortcut("Ctrl+S")
        acao_salvar_como.setShortcut("Ctrl+Shift+S")
        acao_fechar.setShortcut("Ctrl+W")
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.setShortcutContext(Qt.ApplicationShortcut)

        # Sair do app
        if self.parent:
            acao_sair.triggered.connect(self.parent.close)

        # Ações de carregamento
        accao_coor = QAction(QIcon(":/img/kml.png"), "Carregar KML", self.parent)
        accao_coor_1 = QAction(QIcon(":/img/arquivo.png"), "Carregar camada shapefile", self.parent)
        accao_coor_2 = QAction(QIcon(":/img/arquivo-csv.png"), "Carregar coordenadas CSV", self.parent)

        if self.arquivos:
            accao_coor.triggered.connect(self.arquivos.carregar_kml)
            accao_coor_1.triggered.connect(self.arquivos.carregar_shapefile)
            accao_coor_2.triggered.connect(self.arquivos.carregar_csv)

        # Menu Recentes
        self.atualizar_menu_recentes()

        menu.addActions([
            acao_novo, acao_abrir, self.menu_recentes.menuAction(),
            acao_salvar, acao_salvar_como, acao_fechar
        ])
        menu.addSeparator()
        menu.addActions([accao_coor, accao_coor_1, accao_coor_2])
        menu.addSeparator()
        menu.addAction(acao_sair)

        return menu

    def menu_editar(self):
        editar = QMenu("Editar", self.parent)

        accao_config = QAction("Configurações", self.parent)
        acao_parametros = QAction("Parâmetros do Projeto", self.parent)

        accao_config.setShortcut("Ctrl+E")
        acao_parametros.setShortcut("Ctrl+P")
        if self.parent:
            accao_config.triggered.connect(lambda: self.parent.stackedWidget.setCurrentIndex(1))

        editar.addActions([accao_config, acao_parametros])
        return editar

    def menu_relatorio(self):
        rel = QMenu("Relatórios", self.parent)

        acao_relatorio = QAction("Relatório", self.parent)
        acao_exportar = QAction("Exportar", self.parent)

        acao_relatorio.setShortcut("Ctrl+R")
        acao_exportar.setShortcut("Ctrl+E")

        rel.addActions([acao_relatorio, acao_exportar])
        return rel

    def menu_ajuda(self):
        help_menu = QMenu("Ajuda", self.parent)

        acao_manual = QAction("Manual do Usuário", self.parent)
        acao_dicas = QAction("Dicas de Uso", self.parent)
        acao_sobre = QAction("Sobre o Programa", self.parent)
        acao_suporte = QAction("Suporte Técnico", self.parent)

        acao_manual.setShortcut("Ctrl+M")
        acao_dicas.setShortcut("Ctrl+D")
        acao_sobre.setShortcut("Ctrl+I")
        acao_suporte.setShortcut("Ctrl+T")

        help_menu.addActions([acao_manual, acao_dicas, acao_sobre, acao_suporte])
        return help_menu
    
    def menu_graficos(self):
        grafico_menu = QMenu(self.parent)
        perfil = QAction("Perfil de Elevação", self.parent)
        curva = QAction("Curvas de Bombas/Associação", self.parent)
        
        
        if self.parent:
            perfil.triggered.connect(lambda: self.parent.animações.altura(self.parent.widget_2, altura=400))
            curva.triggered.connect(lambda: self.parent.animações.largura(self.parent.janel_direita, largura_alvo=500))
         
        grafico_menu.addActions([curva, perfil])
        return grafico_menu
    
    def menu_selecao_graficos(self):
        selecao = QMenu(self.parent)
        self.principal =QAction("Curva H vs Q (Altura vs Vazão)", self.parent)
        self.potencia = QAction("Curva de Potência vs Vazão (P vs Q)", self.parent)
        self.rendimento = QAction("Curva de Eficiência vs Vazão (η vs Q)", self.parent)

        if self.parent:
            self.principal.triggered.connect(lambda: self.sub_menus_selecao(self.principal, 0))
            self.potencia.triggered.connect(lambda: self.sub_menus_selecao(self.potencia, 1))
            self.rendimento.triggered.connect(lambda: self.sub_menus_selecao(self.rendimento, 2))

        selecao.addActions([self.principal, self.potencia, self.rendimento])
        return selecao
    
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

    def sub_menus_selecao(self, accao, index):
        self.parent.label_2.setText(f"{accao.text()}")
        self.parent.stackedWidget_3.setCurrentIndex(index)

