import sys
import os, json
import img.img_rc

from pint import UnitRegistry

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl, QEvent, QSize, QPoint, QTimer, Signal, Slot, QSettings, QStringListModel
from PySide6.QtGui import QAction, QDoubleValidator, QSurfaceFormat
from PySide6.QtWidgets import (
    QApplication, QLabel, QMenu, QCompleter, QToolButton,
    QMessageBox, QFileDialog, QVBoxLayout, QSizePolicy
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile

from qframelesswindow import FramelessWindow, StandardTitleBar

from gui.Ui_main import Ui_AquaPump

from scripts.pdf_gen import PDF
from scripts.menus import Menus
from scripts.arquivos import Arquivos
from scripts.definicoes import Definicoes
from scripts.requisicoes import Pesquisa
from scripts.conexoes_sinais import ConexoesUI
from scripts.configurações import Configuracoes
from scripts.JavaScript import Mapa
from scripts.animações import Animações
from scripts.web_channel import (
    Dados, Altura_Geometrica, Dimensao_Tubulacao, Acessorios_sistema
)

from calculos.perdas_cargas import Perdas
from calculos.curvas_bomba import Grafico
from calculos.dimensionamento_tubulação import Tubulacao

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu-vsync --disable-frame-rate-limit"

class MainWindow(FramelessWindow, Ui_AquaPump):
    sincronizar = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # ___________ Expoentes ______________________
        self.ex_3 = chr(0x00B3)

        # ____________ Captura de LineEdit Vazao e Tempo _____________
        texto = self.Vazao_2.text().strip()
        self.vazao = float(texto) if texto else 0.0

        tempo = self.Vazao.text().strip()
        self.tempo = float(tempo) if tempo else 0.0

        # === Inicialização de Classes Internas ===
        self.animações = Animações()
        self.relatorio_pdf = PDF()
        self.arquivos = Arquivos(self.view)
        self.definicoes = Definicoes(parent=self)
        self.menu = Menus(parent=self, arquivos=self.arquivos, config=Configuracoes())
        self.config = Configuracoes()

        #  ______________Inicializacao de Classes de Calculo _____________
        self.grafico = Grafico()
        self._diametro = Tubulacao()

        #  _____________ Inicializacao de Classes de WebEngine _____________
        self.altura_geometrica = Altura_Geometrica()
        self.comprimento_tubulacao = Dimensao_Tubulacao()
        self.acessorios = Acessorios_sistema()
        self.dados = Dados()

        # ===_______ WebEngine + WebChannel _____________===
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)
        self._canal.registerObject("altura", self.altura_geometrica)
        self._canal.registerObject("comprimento", self.comprimento_tubulacao)
        self._canal.registerObject("acessorios", self.acessorios)


        # === ComboBox ===
        self.hazen_will.addItems(Perdas.get_lista_materiais_hazen())
        self.hazen_will.setHidden(True)
        self.darcy.addItems(Perdas.get_lista_materiais_darcy())

        # === Validação de Entrada ===
        validator = QDoubleValidator(0.0, 1000.0, 3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

        # === Autocompletar Pesquisa ===
        self.completador = QCompleter()
        self.completador.setCaseSensitivity(Qt.CaseInsensitive)
        self.pesquisa_line.setCompleter(self.completador)
        self.pesquisa_line.setPlaceholderText("Pesquisar")

        # === WebEngine + Mapa ===
        self.mapinha = Mapa()
        mapa = self.mapinha.html_code
        self.page.setHtml(mapa)

        self.icone_2.view().setMinimumWidth(60)

        # ____________________PlaceHolderText ________________________________
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")
        self.Vazao.setPlaceholderText("Tempo em horas")

        # =========== Status e Threads ==================
        self.worker = None
        self.status_label = QLabel()

        #  _________________ Conexões e Configurações (vai para ConexoesUI) _________________
        self.conexoes = ConexoesUI(parent=self, menu=self.menu, animacoes=self.animações, configuracoes=self.config)
        
    def actualizar_vazao(self):
        return self.icone_2.currentText()
    
    def calculo_diametro_tubulacao(self):
        self.diametro_tubulacao = self._diametro.calcular_diametro(self.vazao, self.tempo)
        print(self.diametro_tubulacao)
    
    def perdas_carga(self):
        self.perdas = Perdas(self.vazao, self.diametro_tubulacao, self._diametro.area_seccao())

    def definir_acessorios(self, lista):
        self.perdas_carga()
        self.perdas.definir_acessorios_lista(lista)
        self.localizadas = self.perdas.calcular_perdas_localizadas()
        print(self.localizadas)

    def perdas_carga_totais(self, comprimento):
        self.perdas_carga()
        if self.radioButton_7.isChecked():
            self.perdas_totais = self.perdas.calcular_perda_carga_darcy(comprimento) + self.localizadas()
        elif self.radioButton_8.isChecked():
            self.perdas_totais = self.perdas.calcular_perda_carga_hazen_williams(comprimento) + self.localizadas()
        return self.perdas_totais
        
    def calcular_altura_manometrica(self, altura):
        self.altura_geometrica = altura
        self.altura_manometrica = self.altura_geometrica + self.perdas_totais if hasattr(self, 'perdas_totais') else self.altura_geometrica
        return self.altura_manometrica

    def inicializar_graficos_curvas(self):
        """ Inicializa os gráficos de curvas com os dados da bomba. """
        

        for widget, tipo in [(self.altura, 'altura'), 
                             (self.potencia, 'potencia'), 
                             (self.rendimento, 'rendimento')]:
            layout = QVBoxLayout()
            grafico = Grafico(tipo=tipo)
            grafico.H_geometrico = self.altura_manometrica if hasattr(self, 'altura_manometrica') else 0
            grafico.perda_carga = self.perdas_totais if hasattr(self, 'perdas_totais') else 0
            grafico.gerar_dados()
            grafico.plotar()
            layout.addWidget(grafico)
            widget.setLayout(layout)

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

