import sys
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QToolButton, QMessageBox, QFileDialog, QCompleter, QLabel, QVBoxLayout
from PySide6.QtGui import QAction, QIcon,QDoubleValidator, QSurfaceFormat
from PySide6.QtCore import QPoint, QEvent, Qt, QSize, Slot, QStringListModel
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QUrl, Qt, QTimer, Signal, QSettings
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebChannel import QWebChannel
from pint import UnitRegistry
from gui.Ui_main import Ui_AquaPump
from gui.Loses_main import Dialog_main
from gui.config_main import Config_main
from scripts.animações import Animações
from scripts.JavaScript import Mapa
from scripts.web_channel import Dados, Relatório
from scripts.pdf_gen import PDF
from calculos.curvas_bomba import Grafico
from calculos.perdas_cargas import Perdas 
from scripts.arquivos import Arquivos
from scripts.requisicoes import Pesquisa
from scripts.configurações import Configuracoes
from scripts.menus import Menus
from scripts.definicoes import Definicoes
import os, json
import img.img_rc

os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_OPENGL"] = "software"

class MainWindow(FramelessWindow, Ui_AquaPump):
    sincronizar = Signal(int)


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # ___________ Expoentes ______________________
        self.ex_3 = chr(0x00B3)

        # === Inicialização de Classes Internas ===
        self.animações = Animações()
        self.dados_bomba = Relatório()
        self.dados = Dados()
        self.relatorio_pdf = PDF()
        self.arquivos = Arquivos(self.view)
        self.definicoes = Definicoes(parent=self)
        self.menu = Menus(parent=self, arquivos=self.arquivos, config=Configuracoes())

        # === WebEngine + WebChannel ===
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)
        self._canal.registerObject("dados_bomba", self.dados_bomba)
        
        # ______________Dados Recebidos________________
        self.altura_geometrica = 0
        self.distancia = 0
        self.diametro = 0

        self.dados_bomba.valor_recebido.connect(self.processamento_dados_recebidos)

        # === Settings ===
        self.config = Configuracoes()
        self.restaurar_configuracoes()

        # === Conexões JS ===
        self.Vazao_2.textChanged.connect(self.enviar_js)
        self.Vazao.textChanged.connect(self.enviar_js)
        self.page.featurePermissionRequested.connect(self.permissao)

        # === Botões de Menu Superior ===
        self.grafico_icon.clicked.connect(lambda: self.menu.menu_graficos().popup(self.grafico_icon.mapToGlobal(self.grafico_icon.rect().topRight())))
        self.definicoes_direita_2.clicked.connect(lambda: self.menu.menu_selecao_graficos().popup(self.definicoes_direita_2.mapToGlobal(self.definicoes_direita_2.rect().bottomRight())))
        self.arquivo_2.clicked.connect(lambda: self.menu.menu_principal().popup(self.arquivo_2.mapToGlobal(self.arquivo_2.rect().bottomLeft())))
        self.config_2.clicked.connect(lambda: self.menu.menu_editar().popup(self.config_2.mapToGlobal(self.config_2.rect().bottomLeft())))
        self.relatorio_2.clicked.connect(lambda: self.menu.menu_relatorio().popup(self.relatorio_2.mapToGlobal(self.relatorio_2.rect().bottomLeft())))
        self.ajuda_2.clicked.connect(lambda: self.menu.menu_ajuda().popup(self.ajuda_2.mapToGlobal(self.ajuda_2.rect().bottomLeft())))

        # === Aba Lateral e Frames ===
        self.fechar_lateral_2.clicked.connect(lambda: self.animações.largura(self.frame_4, largura_alvo=300))
        self.abrir_layout_3.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6, largura_alvo=300))
        self.pesquisar_3.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6, largura_alvo=300))
        self.projeto.clicked.connect(lambda: self.animações.largura_altura(self.frame_4, self.projecto, self.frame_6))
        self.exportar_2.clicked.connect(lambda: self.animações.largura_altura(self.frame_4, self.exportar, self.frame_6, altura=100))
        self.abrir_layout_2.clicked.connect(lambda: self.animações.largura(self.frame_4, self.frame_6)) 
        self.sair_2.clicked.connect(lambda: app.quit())
        self.sair_3.clicked.connect(lambda: app.quit())

        # === Seções Projeto e Exportar ===
        self.projecto_2.clicked.connect(lambda: self.animações.altura(self.projecto, altura=400))
        self.parametros.clicked.connect(lambda: self.animações.altura(self.exportar, altura=100))
        self.exportar_pdf.clicked.connect(self.gerar_pdf)

        # === Botões Arquivos ===
        self.pushButton.clicked.connect(self.arquivos.carregar_kml)
        self.pushButton_2.clicked.connect(self.arquivos.carregar_csv)
        self.pushButton_4.clicked.connect(self.arquivos.carregar_shapefile)

        # === ComboBox ===
        self.hazen_will.addItems(Perdas.get_lista_materiais_hazen())        
        self.hazen_will.setHidden(True)
        self.darcy.addItems(Perdas.get_lista_materiais_darcy())
        
        # === LineEdit ===
        texto = self.Vazao_2.text().strip()
        self.vazao = float(texto) if texto else 0.0

        # === Validação de Entrada ===
        validator = QDoubleValidator(0.0, 1000.0, 3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

        # === Autocompletar Pesquisa ===
        self.completador = QCompleter()
        self.completador.setCaseSensitivity(Qt.CaseInsensitive)
        self.pesquisa_line.setCompleter(self.completador)
        self.pesquisar_2.clicked.connect(self.pesquisa_mapa)
        self.pesquisa_line.returnPressed.connect(self.pesquisa_mapa)
        self.pesquisa_line.setPlaceholderText("Pesquisar")

        # === WebEngine + Mapa ===
        self.mapinha = Mapa()
        mapa = self.mapinha.html_code
        self.page.setHtml(mapa) 

        self.icone_2.currentIndexChanged.connect(self.actualizar_vazao)
        self.icone_2.view().setMinimumWidth(60)
  
        # ____________________PlaceHolderText ________________________________
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")
        self.Vazao.setPlaceholderText("Tempo em horas")

         # =========== Status e Threads ==================
        self.worker = None
        self.status_label = QLabel()

        # _______________ Inicialização de Gráficos _______________
        self.inicializar_graficos_curvas()

    def actualizar_vazao(self):
        return self.icone_2.currentText()

    def inicializar_graficos_curvas(self):
        """ Inicializa os gráficos de curvas com os dados da bomba. """
        
        vazao = self.actualizar_vazao()
        #perda = self.calcular_perda_carga()

        for widget, tipo in [(self.altura, 'altura'), 
                             (self.potencia, 'potencia'), 
                             (self.rendimento, 'rendimento')]:
            layout = QVBoxLayout()
            grafico = Grafico(tipo=tipo)
            grafico.H_geometrico = self.altura_geometrica
            #grafico.perda_carga = perda
            grafico.gerar_dados()
            grafico.plotar()
            layout.addWidget(grafico)
            widget.setLayout(layout)

    
    @Slot(float, float, float)
    def processamento_dados_recebidos(self, altura, distancia, diametro):
        """ Processa os dados recebidos do JavaScript. """
        self.altura_geometrica = altura
        self.distancia = distancia
        self.diametro = diametro                         

        perda = self.calcular_perda_carga()

        for widget, tipo in [(self.altura, 'altura'), 
                            (self.potencia, 'potencia'), 
                            (self.rendimento, 'rendimento')]:
            layout = widget.layout()
            if layout and layout.count() > 0:
                grafico_widget = layout.itemAt(0)
                if grafico_widget:
                    grafico = grafico_widget.widget()
                    if isinstance(grafico, Grafico):
                        grafico.actualizar_dados(self.altura_geometrica, perda)
  
    def calcular_perda_carga(self):
        p = Perdas(self.diametro, self.distancia, self.vazao)
        perda = 0
        if self.darcy.isVisible():
            p.definir_material_darcy(self.darcy.currentText())
            p.calcular_velocidade()
            return p.calcular_perda_carga_darcy()
        
        elif self.hazen_will.isVisible():
            p.definir_material_hazen(self.hazen_will.currentText())
            p.calcular_velocidade()
            return p.calcular_perda_carga_hazen_williams() 
        
        return 0
    
    def emitir_sinal_sincro(self, index):
        if self._sincronizar:
            return
        
        self.sincronizar.emit(index)
    
    def actualizar_espaco(self, index):
        self._sincronizar = True
        self.icone_2.setCurrentIndex(index)
        self._sincronizar = False

    def enviar_js(self):
        self.dados.enviar_dados(self.Vazao_2, self.Vazao, self.view)

    def pesquisa_mapa(self):
        texto = self.pesquisa_line.text()
        pesquisa = f"pesquisar_lugar('{texto}')"
        self.view.page().runJavaScript(pesquisa)

    @Slot(str)
    def buscar_sugestoes(self, texto):
        if len(texto) >= 3:
            self.status_label.setText("Buscando sugestões...")
            if self.worker and self.worker.isRunning():
                self.worker.terminate()

            self.worker = Pesquisa(texto)
            self.worker.resultado.connect(self.atualizar_completer)
            self.worker.start()

    @Slot(list)
    def atualizar_completer(self, sugestoes):
        self.status_label.setText("")
        modelo = QStringListModel(sugestoes)
        self.completador.setModel(modelo)

    def gerar_pdf(self):
        try:
            self.relatorio_pdf.adicionar_titulos()
            self.relatorio_pdf.adicionar_conteudo(self.dados_bomba.vazão, self.dados_bomba.tempo, self.dados_bomba.diametro)
            self.relatorio_pdf.gravar_pdf()
        except Exception as e:
            QMessageBox.critical(self, 'ERRO', f'Erro ao gerar pdf devido a {e}')
    
    def permissao(self, url, feature):
        if feature == QWebEnginePage.Feature.Geolocation:
            resposta = QMessageBox.question(
                self,
                "Permissão de Localização",
                "Este site deseja acessar sua localização. Permitir?",
                QMessageBox.Yes | QMessageBox.No
            )

            if resposta == QMessageBox.Yes:
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
            else:
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)
  
    def salvar_configuracoes(self):
        """ Salva todas as configurações da aplicação ao fechar. """
        self.config.salvar_geometria_janela(self)
        self.config.salvar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.salvar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.salvar_texto_lineedit(self.Vazao_2, "vazao_valor")
        self.config.salvar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.salvar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.salvar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def restaurar_configuracoes(self):
        """ Restaura todas as configurações da aplicação no arranque. """
        self.config.restaurar_geometria_janela(self)
        self.config.restaurar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.restaurar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.restaurar_texto_lineedit(self.Vazao_2, "vazao_valor")
        self.config.restaurar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.restaurar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.restaurar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def closeEvent(self, event):
        """ Chamado quando a janela está prestes a ser fechada. """
        self.salvar_configuracoes()
        super().closeEvent(event)


    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(r"estilos\estilos.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    app.exec()

