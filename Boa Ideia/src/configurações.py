from PySide6.QtCore import QSettings

class Configuracoes:
    def __init__(self):
        self.settings = QSettings('Bombas Hidraulicas', 'AquaPump')

    # ===== GEOMETRIA DA JANELA ========================
    def salvar_geometria_janela(self, janela):
        self.settings.setValue('geometry', janela.saveGeometry())
       # self.settings.setValue('windowState', janela.saveState())

    def restaurar_geometria_janela(self, janela):
        geometry = self.settings.value('geometry')
        if geometry:
            janela.restoreGeometry(geometry)
        
        state = self.settings.value('windowState')
        if state:
            janela.restoreState(state)

    # ===== ESTADO DO SPLITTER =========================
    def salvar_estado_splitter(self, splitter, chave):
        """ Salva o estado (posição das divisões) de um QSplitter. """
        self.settings.setValue(chave, splitter.saveState())

    def restaurar_estado_splitter(self, splitter, chave):
        """ Restaura o estado de um QSplitter. """
        state = self.settings.value(chave)
        if state:
            splitter.restoreState(state)

    # ===== COMBOBOX ===================================
    def salvar_indice_combobox(self, combobox, chave):
        """ Salva o índice atual de um QComboBox. """
        self.settings.setValue(chave, combobox.currentIndex())

    def restaurar_indice_combobox(self, combobox, chave, padrao=0):
        """ Restaura o índice de um QComboBox. """
        indice = self.settings.value(chave, padrao, type=int)
        combobox.setCurrentIndex(indice)

    def salvar_texto_combobox(self, combobox, chave):
        """ Salva o texto selecionado de um QComboBox. """
        self.settings.setValue(chave, combobox.currentText())

    def restaurar_texto_combobox(self, combobox, chave, padrao=""):
        """ Restaura um QComboBox para um texto específico. """
        texto = self.settings.value(chave, padrao, type=str)
        if texto:
            index = combobox.findText(texto)
            if index != -1:
                combobox.setCurrentIndex(index)

    # ===== QLINEEDIT ==================================
    def salvar_texto_lineedit(self, lineedit, chave):
        """ Salva o texto de um QLineEdit. """
        self.settings.setValue(chave, lineedit.text())
        
    def restaurar_texto_lineedit(self, lineedit, chave, padrao=""):
        """ Restaura o texto de um QLineEdit. """
        texto = self.settings.value(chave, padrao, type=str)
        lineedit.setText(texto)

    # ===== PROJETOS RECENTES ==========================
    def obter_projetos_recentes(self, max_items=5):
        return self.settings.value("recent_projects", [], type=list)[:max_items]

    def adicionar_projeto_recente(self, caminho_arquivo, max_items=5):
        recentes = self.obter_projetos_recentes(max_items)
        if caminho_arquivo in recentes:
            recentes.remove(caminho_arquivo)
        # Insere no início da lista
        recentes.insert(0, caminho_arquivo)
        # Garante que a lista não excede o tamanho máximo
        self.settings.setValue("recent_projects", recentes[:max_items])