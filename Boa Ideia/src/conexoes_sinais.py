from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import webbrowser

class ConexoesUI():
    def __init__(self, parent=None, menu=None, animacoes=None, configuracoes=None):
        self.parent = parent
        self.menu = menu
        self.animacoes = animacoes
        self.config = configuracoes
        
        # Inicializa todas as conexões
        self._conectar_principais_dados()
        self._conectar_configuracoes()
        self._conectar_entradas_calculo()
        self._conectar_js_e_mapa()
        self._conectar_menus()
        self._conectar_abas_frames()
        self._conectar_botoes_sair()
        self._conectar_pesquisa()
        self._perda_carga_dinamica()
        self._conectar_actualizao_graph()
        self._connectar_actualizacao_unidades()
        self._connectar_actualizacao_unidades_graficos()
        self._conectar_geracao_pdf() 
        self._connectar_arquivo()   
        self._conectar_ocultacoes()
        self._connectar_voltar_menu_principal()
        self._connectar_janelas_responsivas()
        self._connectar_janela_relatorio()
        self._connectar_versao_pro()

    def _conectar_configuracoes(self):
        """Restaura as configurações da sessão anterior."""
        self.parent.restaurar_configuracoes()

    def _conectar_principais_dados(self):
        """Conecta os principais dados de entrada do usuário."""
        self.parent.Vazao.textChanged.connect(self.parent.calculo_diametro_tubulacao)
        self.parent.Vazao_2.textChanged.connect(self.parent.calculo_diametro_tubulacao)
    
    def _conectar_entradas_calculo(self):
        """Conecta todas as entradas do usuário que afetam os cálculos hidráulicos."""
        # Vazão e Tempo de funcionamento
        self.parent.Vazao_2.textChanged.connect(self.parent.atualizar_parametros_entrada)
        self.parent.Vazao.textChanged.connect(self.parent.atualizar_parametros_entrada)
        
         # Sinais da UI para seleção de fórmula e material
        self.parent.radioButton_11.toggled.connect(self.parent.recalcular_sistema_completo)
        self.parent.radioButton_12.toggled.connect(self.parent.recalcular_sistema_completo)
        self.parent.darcy.currentIndexChanged.connect(self.parent.recalcular_sistema_completo)
        self.parent.hazen_will.currentIndexChanged.connect(self.parent.recalcular_sistema_completo)

        # Unidade de vazão
        self.parent.icone_2.currentIndexChanged.connect(self.parent.actualizar_vazao)

    def _conectar_js_e_mapa(self):
        """Conecta os sinais vindos do QWebChannel (JavaScript)."""
        # Envio de dados para o JS
        self.parent.Vazao_2.textChanged.connect(self.parent.enviar_js)
        self.parent.Vazao.textChanged.connect(self.parent.enviar_js)
                
        # Recebimento de dados do JS para cálculos
        self.parent.acessorios_channel.lista.connect(self.parent.definir_acessorios)
        self.parent.altura_geometrica_channel.altura_recebido.connect(self.parent.receber_altura)
        self.parent.comprimento_tubulacao_channel.comprimento_recebido.connect(self.parent.receber_comprimento)

    def _conectar_menus(self):
        """Conecta os botões da barra de título aos seus respectivos menus."""
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

    def _conectar_abas_frames(self):
        """Conecta os botões para animações de painéis laterais."""
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

    def _conectar_botoes_sair(self):
        """Conecta os botões de fechar a aplicação."""
        self.parent.sair_2.clicked.connect(self.parent.close)
        self.parent.sair_3.clicked.connect(self.parent.close)

    def _conectar_pesquisa(self):
        """Conecta a barra de pesquisa de localização."""
        self.parent.pesquisar_2.clicked.connect(self.parent.pesquisa_mapa)
        self.parent.pesquisa_line.returnPressed.connect(self.parent.pesquisa_mapa)

    def _perda_carga_dinamica(self):
        """Recalcula as perdas de carga quando o comprimento ou acessórios mudam."""
        self.parent.radioButton_11.toggled.connect(self.parent.mudanca_dinamica_perdas_carga)
        self.parent.radioButton_12.toggled.connect(self.parent.mudanca_dinamica_perdas_carga)

    def _conectar_actualizao_graph(self):
        self.parent.actualizar_grafico.clicked.connect(self.parent.atualizar_graficos_curvas)

    def _connectar_actualizacao_unidades(self):
        self.parent.icone_2.currentTextChanged.connect(self.parent.atualizar_parametros_entrada)
        self.parent.Vazao_2.textChanged.connect(self.parent.atualizar_parametros_entrada)
        self.parent.Vazao.textChanged.connect(self.parent.atualizar_parametros_entrada)

    def _connectar_actualizacao_unidades_graficos(self):
        self.parent.caudal_box_2.currentTextChanged.connect(self.parent.atualizar_unidades_graficos)
        self.parent.altura_box_2.currentTextChanged.connect(self.parent.atualizar_unidades_graficos)
        self.parent.potencia_box_2.currentTextChanged.connect(self.parent.atualizar_unidades_graficos)

    def _conectar_geracao_pdf(self):
        self.parent.exportar_pdf.clicked.connect(self.parent.gerar_pdf)

    def _conectar_ocultacoes(self):
        """Conecta os botões para ocultar/mostrar elementos da UI."""
        self.parent.banco_dados.setHidden(True)

    def _connectar_voltar_menu_principal(self):
        self.parent.voltar_2.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(0))

    def _connectar_arquivo(self):
        self.parent.novo_arquivo.clicked.connect(self.parent.novo_projecto)
        self.parent.salvar_projecto.clicked.connect(self.parent.salvar_historico)
        self.parent.abrir_arquivo.clicked.connect(self.parent.carregar_historico)

    def _connectar_janelas_responsivas(self):
        self.parent.parametros.clicked.connect(lambda: self.animacoes.altura(self.parent.exportar, altura=400))
        self.parent.projecto_2.clicked.connect(lambda: self.animacoes.altura(self.parent.projecto, altura=100))
    
    def _connectar_janela_relatorio(self):
        self.parent.relatorio_3.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(2))
        self.parent.relatorio_3.clicked.connect(self.parent.selecionar_melhor_bomba)
        self.parent.Vazao_2.textChanged.connect(self.parent.selecionar_melhor_bomba)

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