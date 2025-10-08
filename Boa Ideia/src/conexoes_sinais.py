from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import webbrowser


class ConexoesUI:
    def __init__(self, parent=None, menu=None, animacoes=None, configuracoes=None):
        self.parent = parent
        self.menu = menu
        self.animacoes = animacoes
        self.config = configuracoes

        # ========== INICIALIZA TODAS AS CONEXÕES ==========
        # --- Configurações / Principais ---
        self._conectar_configuracoes()
        self._conectar_principais_dados()
        self._conectar_entradas_calculo()

        # --- Comunicação com JS / Mapa ---
        self._conectar_js_dados()
        self._conectar_js_unidades()
        self._conectar_mapa()

        # --- Menus / Abas / Botões / Pesquisa ---
        self._conectar_menus()
        self._conectar_abas_frames()
        self._conectar_botoes_sair()
        self._conectar_pesquisa()

        # --- Cálculos / Perdas de Carga / Unidades ---
        self._perda_carga_dinamica()
        self._connectar_actualizacao_unidades()
        # self._connectar_actualizacao_unidades_graficos()
        # self._conectar_actualizao_graph()

        # --- Seleção de bombas / gráficos / relatório ---
        self._connectar_selecao_bombas()
        self._connectar_abrir_graph()
        self._conectar_geracao_relatorio()

        # --- Arquivos / Ocultações / Widgets / Janelas ---
        self._connectar_arquivo()
        self._conectar_ocultacoes()
        self._connectar_janelas_responsivas()
        self._connectar_widgets_desativadas()

        # --- Versão Pro / Observações ---
        self._connectar_versao_pro()
        # self._conectar_Observacoes()
        # self._connectar_actualizacoes()

    # =================== CONFIGURAÇÕES ========================
    def _conectar_configuracoes(self):
        """Restaura as configurações da sessão anterior."""
        self.parent.restaurar_configuracoes()

    def _conectar_principais_dados(self):
        """Conecta os principais dados de entrada do usuário."""
        self.parent.Vazao.textChanged.connect(self.parent.calculo_diametro_tubulacao)
        self.parent.Vazao_2.textChanged.connect(self.parent.calculo_diametro_tubulacao)

    def _conectar_entradas_calculo(self):
        """Conecta todas as entradas do usuário que afetam os cálculos hidráulicos."""
        # Vazão e tempo de funcionamento
        self.parent.Vazao_2.textChanged.connect(self.parent.atualizar_parametros_entrada)
        self.parent.Vazao.textChanged.connect(self.parent.atualizar_parametros_entrada)

        # Seleção de fórmula e material
        self.parent.radioButton_10.toggled.connect(self.parent.recalcular_sistema_completo)
        self.parent.radioButton_9.toggled.connect(self.parent.recalcular_sistema_completo)
        self.parent.darcy.currentIndexChanged.connect(self.parent.recalcular_sistema_completo)
        self.parent.hazen_will.currentIndexChanged.connect(self.parent.recalcular_sistema_completo)

        # Unidade de vazão
        self.parent.icone_2.currentIndexChanged.connect(self.parent.actualizar_vazao)

    # =============== COMUNICAÇÃO COM JS / MAPA ================
    def _conectar_js_dados(self):
        """Conecta sinais para envio e recebimento de dados com o JavaScript."""
        self.parent.Vazao_2.editingFinished.connect(self.parent.enviar_js)
        self.parent.Vazao.editingFinished.connect(self.parent.enviar_js)

        self.parent.grafico_icon.clicked.connect(self.parent.enviar_js)
        self.parent.grafico.clicked.connect(self.parent.enviar_js)

        self.parent.darcy.currentIndexChanged.connect(self.parent.enviar_js)
        self.parent.hazen_will.currentIndexChanged.connect(self.parent.enviar_js)
        self.parent.icone_2.currentIndexChanged.connect(self.parent.enviar_js)
        self.parent.altura_box.currentIndexChanged.connect(self.parent.enviar_js)
        self.parent.diametro_box.currentIndexChanged.connect(self.parent.enviar_js)
        self.parent.potencia_box.currentIndexChanged.connect(self.parent.enviar_js)
        self.parent.comprimento_box.currentIndexChanged.connect(self.parent.enviar_js)

    def _conectar_js_unidades(self):
        """Conecta sinais para atualização das unidades (JavaScript)."""
        self.parent.Vazao_2.editingFinished.connect(self.parent.enviar_unidades_js)
        self.parent.Vazao.editingFinished.connect(self.parent.enviar_unidades_js)

        self.parent.grafico_icon.clicked.connect(self.parent.enviar_unidades_js)
        self.parent.grafico.clicked.connect(self.parent.enviar_unidades_js)

        self.parent.darcy.currentIndexChanged.connect(self.parent.enviar_unidades_js)
        self.parent.hazen_will.currentIndexChanged.connect(self.parent.enviar_unidades_js)

        self.parent.icone_2.currentIndexChanged.connect(self.parent.enviar_unidades_js)
        self.parent.altura_box.currentIndexChanged.connect(self.parent.enviar_unidades_js)
        self.parent.diametro_box.currentIndexChanged.connect(self.parent.enviar_unidades_js)
        self.parent.potencia_box.currentIndexChanged.connect(self.parent.enviar_unidades_js)
        self.parent.comprimento_box.currentIndexChanged.connect(self.parent.enviar_unidades_js)

    def _conectar_mapa(self):
        """Conecta sinais vindos do QWebChannel (JavaScript)."""
        self.parent.acessorios_channel.lista.connect(self.parent.definir_acessorios)
        self.parent.altura_geometrica_channel.altura_recebido.connect(self.parent.receber_altura)
        self.parent.comprimento_tubulacao_channel.comprimento_recebido.connect(self.parent.receber_comprimento)

    # ================= MENUS / ABAS / BOTÕES =================
    def _conectar_menus(self):
        """Conecta os botões da barra de título aos seus respectivos menus."""
        self.parent.definicoes_direita_3.clicked.connect(
            lambda: self.menu.menu_selecao_graficos().popup(
                self.parent.definicoes_direita_3.mapToGlobal(self.parent.definicoes_direita_3.rect().bottomRight())
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

    def _conectar_abas_frames(self):
        """Conecta botões para animações de painéis laterais."""
        self.parent.fechar_lateral_2.clicked.connect(
            lambda: self.animacoes.largura(self.parent.janel_direita, largura_alvo=300)
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
        self.parent.parametros.clicked.connect(
            lambda: self.animacoes.altura(self.parent.exportar, altura=100)
        )

    def _conectar_botoes_sair(self):
        """Conecta botões de fechar a aplicação."""
        self.parent.sair_2.clicked.connect(self.parent.close)
        self.parent.sair_3.clicked.connect(self.parent.close)

    def _conectar_pesquisa(self):
        """Conecta a barra de pesquisa de localização."""
        self.parent.pesquisar_2.clicked.connect(self.parent.pesquisa_mapa)
        self.parent.pesquisa_line.returnPressed.connect(self.parent.pesquisa_mapa)

    # ================= CÁLCULOS / UNIDADES ===================
    def _perda_carga_dinamica(self):
        """Recalcula as perdas de carga quando o comprimento ou acessórios mudam."""
        self.parent.radioButton_10.toggled.connect(self.parent.mudanca_dinamica_perdas_carga)
        self.parent.radioButton_9.toggled.connect(self.parent.mudanca_dinamica_perdas_carga)

    def _connectar_actualizacao_unidades(self):
        self.parent.icone_2.currentTextChanged.connect(self.parent.atualizar_parametros_entrada)
        self.parent.Vazao_2.textChanged.connect(self.parent.atualizar_parametros_entrada)
        self.parent.Vazao.textChanged.connect(self.parent.atualizar_parametros_entrada)

    def _connectar_actualizacao_unidades_graficos(self):
        self.parent.caudal_box.currentTextChanged.connect(self.parent.atualizar_unidades_graficos)
        self.parent.altura_box.currentTextChanged.connect(self.parent.atualizar_unidades_graficos)
        self.parent.potencia_box.currentTextChanged.connect(self.parent.atualizar_unidades_graficos)

    def _conectar_actualizao_graph(self):
        self.parent.actualizar_grafico.clicked.connect(self.parent.atualizar_graficos_curvas)

    # ========= SELEÇÃO DE BOMBAS / GRÁFICOS / RELATÓRIOS ======
    def _connectar_selecao_bombas(self):
        self.parent.rel.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(2))
        self.parent.relatorio_3.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(2))
        self.parent.rel.clicked.connect(self.parent.selecionar_melhor_bomba)
        self.parent.relatorio_3.clicked.connect(self.parent.selecionar_melhor_bomba)
        self.parent.voltar_2.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(0))

    def _connectar_abrir_graph(self):
        self.parent.grafico_icon.clicked.connect(
            lambda: self.animacoes.largura(self.parent.janel_direita, largura_alvo=500)
        )
        self.parent.grafico.clicked.connect(
            lambda: self.animacoes.largura(self.parent.janel_direita, largura_alvo=500)
        )
        self.parent.calculos.clicked.connect(
            lambda: self.animacoes.altura(self.parent.scrollArea_5, altura=200)
        )
        self.parent.graficos.clicked.connect(
            lambda: self.animacoes.altura(self.parent.janela_graficos, altura=800)
        )

    def _conectar_geracao_relatorio(self):
        self.parent.exportar_pdf.clicked.connect(self.parent.gerar_pdf)
        self.parent.exportar_csv.clicked.connect(self.parent.gerar_csv)

    # ======= ARQUIVOS / OCULTAÇÕES / JANELAS / WIDGETS ========
    def _connectar_arquivo(self):
        self.parent.novo_arquivo.clicked.connect(self.parent.novo_projecto)
        self.parent.salvar_projecto.clicked.connect(self.parent.salvar_historico)
        self.parent.abrir_arquivo.clicked.connect(self.parent.carregar_historico)

    def _conectar_ocultacoes(self):
        """Conecta botões para ocultar/mostrar elementos da UI."""
        self.parent.banco_dados.setHidden(True)

    def _connectar_janelas_responsivas(self):
        self.parent.parametros.clicked.connect(lambda: self.animacoes.altura(self.parent.exportar, altura=400))
        self.parent.projecto_2.clicked.connect(lambda: self.animacoes.altura(self.parent.projecto, altura=400))

    def _connectar_widgets_desativadas(self):
        self.parent.groupBox_2.setVisible(False)
        self.parent.npsh.setVisible(False)
        self.parent.npsh_box.setVisible(False)
        self.parent.groupBox_8.setVisible(False)
        self.parent.groupBox.setVisible(True)
        self.parent.label_8.setVisible(False)
        self.parent.anterior.setVisible(True)
        self.parent.proxima.setVisible(False)

    # ================== Observações =======================
    def _conectar_Observacoes(self):
        window.bomba_encontrada.connect(self.parent.iniciar_consulta)

    # =================== VERSÃO PRO =======================
    def _connectar_versao_pro(self):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Suporte Técnico")
        msg.setIcon(QMessageBox.Information)
        msg.setTextFormat(Qt.RichText)
        msg.setText(
            """
            <h3 style="margin-bottom: 8px;">Versão Pro - Em Breve</h3>
            <p>O lançamento oficial da versão Pro está agendado para breve. 
            Clique abaixo para se registar na lista de espera e receber um desconto de lançamento.</p>
            <p><b>Entre em contacto connosco:</b></p>
            <p>
                <b>Email:</b> <a href="mailto:tenerifenhalicale@outlook.com">
                tenerifenhalicale@outlook.com</a><br>
                <b>Telefone:</b> +258 86 843 9510
            </p>
            """
        )

        btn_pro = msg.addButton("Quero ser PRO", QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Close)

        if msg.clickedButton() == btn_pro:
            webbrowser.open("https://forms.gle/teu_link_lista_de_espera")
            msg.setStandardButtons(QMessageBox.Ok)

        self.parent.pushButton_3.clicked.connect(msg.exec)


