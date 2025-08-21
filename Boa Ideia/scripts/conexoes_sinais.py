
class ConexoesUI():
    def __init__(self, parent=None, menu=None, animacoes=None, configuracoes=None):
        self.parent = parent
        self.menu = menu
        self.animacoes = animacoes
        self.config = configuracoes

        # Inicializa as conexões organizadas
        self._conectar_configuracoes()
        #self._conectar_diametro()
        self._conectar_js()
        self._conectar_menus()
        self._conectar_abas_frames()
        self._conectar_botoes_sair()
        self._conectar_pesquisa()
        self._conectar_graficos()
        self._conectar_perdas()
        self._conectar_combo_icone()

    # ===================== CONFIG =====================
    def _conectar_configuracoes(self):
        self.parent.restaurar_configuracoes()

    # ===================== DIÂMETRO =====================
    def _conectar_diametro(self):
        self.parent.Vazao_2.textChanged.connect(self.parent.diametro)
        self.parent.Vazao.textChanged.connect(self.parent.diametro)

    # ===================== CONEXÕES JS =====================
    def _conectar_js(self):
        self.parent.Vazao_2.textChanged.connect(self.parent.enviar_js)
        self.parent.Vazao.textChanged.connect(self.parent.enviar_js)
        self.parent.page.featurePermissionRequested.connect(self.parent.permissao)

    # ===================== MENUS SUPERIORES =====================
    def _conectar_menus(self):
        self.parent.grafico_icon.clicked.connect(
            lambda: self.menu.menu_graficos().popup(
                self.parent.grafico_icon.mapToGlobal(self.parent.grafico_icon.rect().topRight())
            )
        )
        self.parent.definicoes_direita_2.clicked.connect(
            lambda: self.menu.menu_selecao_graficos().popup(
                self.parent.definicoes_direita_2.mapToGlobal(self.parent.definicoes_direita_2.rect().bottomRight())
            )
        )
        self.parent.arquivo_2.clicked.connect(
            lambda: self.menu.menu_principal().popup(
                self.parent.arquivo_2.mapToGlobal(self.parent.arquivo_2.rect().bottomLeft())
            )
        )
        self.parent.config_2.clicked.connect(
            lambda: self.menu.menu_editar().popup(
                self.parent.config_2.mapToGlobal(self.parent.config_2.rect().bottomLeft())
            )
        )
        self.parent.relatorio_2.clicked.connect(
            lambda: self.menu.menu_relatorio().popup(
                self.parent.relatorio_2.mapToGlobal(self.parent.relatorio_2.rect().bottomLeft())
            )
        )
        self.parent.ajuda_2.clicked.connect(
            lambda: self.menu.menu_ajuda().popup(
                self.parent.ajuda_2.mapToGlobal(self.parent.ajuda_2.rect().bottomLeft())
            )
        )

    # ===================== FRAMES E ABAS LATERAIS =====================
    def _conectar_abas_frames(self):
        self.parent.fechar_lateral_2.clicked.connect(
            lambda: self.animacoes.largura(self.parent.frame_4, largura_alvo=300)
        )
        self.parent.abrir_layout_3.clicked.connect(
            lambda: self.animacoes.largura(self.parent.frame_4, self.parent.frame_6, largura_alvo=300)
        )
        self.parent.pesquisar_3.clicked.connect(
            lambda: self.animacoes.largura(self.parent.frame_4, self.parent.frame_6, largura_alvo=300)
        )
        self.parent.projeto.clicked.connect(
            lambda: self.animacoes.largura_altura(self.parent.frame_4, self.parent.projecto, self.parent.frame_6)
        )
        self.parent.exportar_2.clicked.connect(
            lambda: self.animacoes.largura_altura(self.parent.frame_4, self.parent.exportar, self.parent.frame_6, altura=100)
        )
        self.parent.abrir_layout_2.clicked.connect(
            lambda: self.animacoes.largura(self.parent.frame_4, self.parent.frame_6)
        )

    # ===================== BOTÕES DE SAÍDA =====================
    def _conectar_botoes_sair(self):
        self.parent.sair_2.clicked.connect(lambda: self.app.quit())
        self.parent.sair_3.clicked.connect(lambda: self.app.quit())

    # ===================== PESQUISA =====================
    def _conectar_pesquisa(self):
        self.parent.pesquisar_2.clicked.connect(self.parent.pesquisa_mapa)
        self.parent.pesquisa_line.returnPressed.connect(self.parent.pesquisa_mapa)

    # ===================== GRÁFICOS =====================
    def _conectar_graficos(self):
        self.parent.Vazao_2.textChanged.connect(self.parent.inicializar_graficos_curvas)
        self.parent.Vazao.textChanged.connect(self.parent.inicializar_graficos_curvas)

    # ===================== PERDAS =====================
    def _conectar_perdas(self):
        self.parent.acessorios.lista.connect(self.parent.calcular_perda_carga)
        self.parent.Vazao_2.textChanged.connect(self.parent.calculo_diametro_tubulacao)

    # ===================== COMBO ICONE =====================
    def _conectar_combo_icone(self):
        self.parent.icone_2.currentIndexChanged.connect(self.parent.actualizar_vazao)
