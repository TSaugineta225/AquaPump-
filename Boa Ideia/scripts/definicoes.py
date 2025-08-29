class Definicoes:
    def __init__(self, parent=None):
        self.parent = parent
        self.ex_3 = chr(0x00B3)

        self.unidades_metricas = {
            'caudal': [f'm{self.ex_3}/s', f'm{self.ex_3}/min', f'm{self.ex_3}/h', 'L/s'],
            'altura': ['m'],
            'comprimento': ['m'],
            'diametro': ['mm', 'm'],
            'potencia': ['KW', 'W', 'CV'],
            'npsh': ['m']
        }

        self.unidades_imperiais = {
            'caudal': ['GPM', 'MGD', 'GPH'],
            'altura': ['ft'],
            'comprimento': ['ft'],
            'diametro': ['in'],
            'potencia': ['hp'],
            'npsh': ['ft']
        }
        self.sincronizando = False  # Evita loop infinito

        self.parent.icone_2.currentIndexChanged.connect(self.sincronizar_com_caudal_box)
        self.parent.icone_2.currentIndexChanged.connect(self.mudanca_dinamica_Textholder)
        self.parent.caudal_box.currentIndexChanged.connect(self.sincronizar_com_icone_2)

        self.conectar_sinais()
        self.carregar_unidades_iniciais()

    def conectar_sinais(self):
        """Conecta os botões aos métodos correspondentes."""
        self.parent.radioButton.toggled.connect(self.actualizar_unidades)
        self.parent.radioButton_2.toggled.connect(self.actualizar_unidades)
        self.parent.configuracoes.clicked.connect(self.mostrar_janela_definicoes)
        self.parent.configuracoes_2.clicked.connect(self.mostrar_janela_definicoes)
        self.parent.voltar.clicked.connect(self.voltar_a_menu_principal)
        self.parent.geral.clicked.connect(lambda: self.mudanca_widget(0))
        self.parent.unidades.clicked.connect(lambda: self.mudanca_widget(3))
        self.parent.banco_dados.clicked.connect(lambda: self.mudanca_widget(1))

    def carregar_unidades_iniciais(self):
        """Carrega as unidades métricas por padrão."""
        self.adicionar_unidades(self.unidades_metricas)

    def adicionar_unidades(self, unidades):
        """Adiciona as unidades aos respetivos comboboxes."""
        self.parent.caudal_box.clear()
        self.parent.altura_box.clear()
        self.parent.comprimento_box.clear()
        self.parent.diametro_box.clear()
        self.parent.potencia_box.clear()
        self.parent.npsh_box.clear()
        self.parent.icone_2.clear()

        self.parent.caudal_box.addItems(unidades['caudal'])
        self.parent.icone_2.addItems(unidades['caudal'])
        self.parent.altura_box.addItems(unidades['altura'])
        self.parent.comprimento_box.addItems(unidades['comprimento'])
        self.parent.diametro_box.addItems(unidades['diametro'])
        self.parent.potencia_box.addItems(unidades['potencia'])
        self.parent.npsh_box.addItems(unidades['npsh'])

    def actualizar_unidades(self):
        """Atualiza as unidades com base no botão selecionado."""
        if self.parent.radioButton.isChecked():
            self.adicionar_unidades(self.unidades_metricas)
        elif self.parent.radioButton_2.isChecked():
            self.adicionar_unidades(self.unidades_imperiais)

    def mostrar_janela_definicoes(self):
        """Mostra a janela de definições."""
        if self.parent:
            if self.parent.frame_4.width() != 0:
                self.parent.frame_4.setFixedWidth(0)
            self.parent.frame_6.setHidden(True)
            self.parent.stackedWidget.setCurrentIndex(1)

    def voltar_a_menu_principal(self):
        """Volta ao menu principal."""
        if self.parent:
            self.parent.stackedWidget.setCurrentIndex(0)
            self.parent.frame_6.setVisible(True)

    
    def mudanca_widget(self, index=int):
        self.parent.janela_definicoes.setCurrentIndex(index)

    def sincronizar_com_caudal_box(self, index):
        if self.sincronizando:
            return
        self.sincronizando = True
        self.parent.caudal_box.setCurrentIndex(index)
        self.sincronizando = False

    def sincronizar_com_icone_2(self, index):
        if self.sincronizando:
            return
        self.sincronizando = True
        self.parent.icone_2.setCurrentIndex(index)
        self.sincronizando = False

    def formula_hazen_recebida(self, mostrar):
        self.hazen_will.setVisible(mostrar)

    def formula_darcy_recebida(self, mostrar):
        self.darcy.setVisible(mostrar)
    
    def mudanca_dinamica_Textholder(self):
        self.parent.Vazao_2.setPlaceholderText(f"Vazão em {self.parent.icone_2.currentText()}")

