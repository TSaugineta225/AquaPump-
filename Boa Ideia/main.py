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
        self.setWindowTitle("AquaPump")
        
        # =========== System Calculation Attributes ===========
        self.vazao = 0.0
        self.tempo = 0.0
        self.diametro_tubulacao = 0.0
        self.comprimento_tubulacao_val = 0.0
        self.altura_geometrica_val = 0.0
        self.localizadas = 0.0
        self.perdas_totais = 0.0
        self.altura_manometrica = 0.0

        # === Inicialização de Classes Internas ===
        self.animações = Animações()
        self.relatorio_pdf = PDF()
        self.arquivos = Arquivos(self.view)
        self.definicoes = Definicoes(parent=self)
        self.menu = Menus(parent=self, arquivos=self.arquivos, config=Configuracoes())
        self.config = Configuracoes()

        #  ______________Inicializacao de Classes de Calculo _____________
        self._diametro = Tubulacao()
        
        #  _____________ Inicializacao de Classes de WebEngine _____________
        self.altura_geometrica_channel = Altura_Geometrica()
        self.comprimento_tubulacao_channel = Dimensao_Tubulacao()
        self.acessorios_channel = Acessorios_sistema()
        self.dados = Dados()

        # ===_______ WebEngine + WebChannel _____________===
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)
        self._canal.registerObject("altura", self.altura_geometrica_channel)
        self._canal.registerObject("comprimento", self.comprimento_tubulacao_channel)
        self._canal.registerObject("acessorios", self.acessorios_channel)

        # === ComboBox ===
        self.hazen_will.addItems(Perdas.get_lista_materiais_hazen())
        self.hazen_will.setHidden(True)
        self.darcy.addItems(Perdas.get_lista_materiais_darcy())

        # === Validação de Entrada ===
        validator = QDoubleValidator(0.0, 10000.0, 3)
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
        self.page.setHtml(self.mapinha.html_code)
        self.icone_2.view().setMinimumWidth(60)

        # ____________________PlaceHolderText ________________________________
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")
        self.Vazao.setPlaceholderText("Tempo em horas")

        # =========== Status e Threads ==================
        self.worker = None
        self.status_label = QLabel()

        # =========== Initialize Graphs ==================
        self.inicializar_graficos_curvas()

        #  _________________ Conexões e Configurações _________________
        self.conexoes = ConexoesUI(parent=self, menu=self.menu, animacoes=self.animações, configuracoes=self.config)
        self.atualizar_parametros_entrada() 
        
    def actualizar_vazao(self):
        return self.icone_2.currentText()

    @Slot()
    def atualizar_parametros_entrada(self):
        """Lê os valores de vazão e tempo e inicia a cascata de cálculos."""
        texto_vazao = self.Vazao_2.text().strip().replace(',', '.')
        self.vazao = float(texto_vazao) if texto_vazao else 0.0
        
        texto_tempo = self.Vazao.text().strip().replace(',', '.')
        self.tempo = float(texto_tempo) if texto_tempo else 0.0

        self.calculo_diametro_tubulacao()
        self.perdas_carga()
        self.recalcular_sistema_completo()

    def calculo_diametro_tubulacao(self):
        self.diametro_tubulacao = self._diametro.calcular_diametro(self.vazao, self.tempo)
    
    def perdas_carga(self):
        vazao_m3s = self.vazao 
        self.perdas = Perdas(vazao_m3s, self.diametro_tubulacao, self._diametro.area_seccao(), self.darcy.currentText(), self.hazen_will.currentText())


    @Slot(list)
    def definir_acessorios(self, lista):
        """Recebe a lista de acessórios do JS e recalcula o sistema."""
        if not hasattr(self, 'perdas'): return
        self.perdas.definir_acessorios_lista(lista)
        try:
            self.localizadas = self.perdas.calcular_perdas_localizadas()
        except (ValueError, AttributeError):
            self.localizadas = 0.0
        self.recalcular_sistema_completo()

    @Slot(float)
    def receber_comprimento(self, comprimento):
        """Recebe o comprimento da tubulação do JS e recalcula o sistema."""
        self.comprimento_tubulacao_val = comprimento
        print("Comprimento da tubulação recebido:", comprimento)
        self.recalcular_sistema_completo()

    @Slot(float)
    def receber_altura(self, altura):
        """Recebe a altura geométrica do JS e recalcula o sistema."""
        self.altura_geometrica_val = altura
        print("Altura geométrica recebida:", altura)
        self.recalcular_sistema_completo()

    @Slot()
    def recalcular_sistema_completo(self):
        """Função central que recalcula perdas, altura manométrica e atualiza os gráficos."""
        if not hasattr(self, 'perdas') or not self.diametro_tubulacao > 0:
            return

        perda_distribuida = 0.0
        if self.comprimento_tubulacao_val > 0:
            try:
                if self.radioButton_7.isChecked():  # Darcy-Weisbach
                    self.perdas.definir_material_darcy(self.darcy.currentText())
                    perda_distribuida = self.perdas.calcular_perda_carga_darcy(self.comprimento_tubulacao_val)
                elif self.radioButton_8.isChecked():  
                    self.perdas.definir_material_hazen(self.hazen_will.currentText())
                    perda_distribuida = self.perdas.calcular_perda_carga_hazen_williams(self.comprimento_tubulacao_val)
            except (ValueError, AttributeError):
                 perda_distribuida = 0.0

        self.perdas_totais = perda_distribuida + self.localizadas
        print(f"Perdas totais: {self.perdas_totais:.8f} m")

        # 2. Calcular altura manométrica
        self.altura_manometrica = self.altura_geometrica_val + self.perdas_totais
        print("Altura manométrica calculada:", self.altura_manometrica)
        print(f"Altura geométrica: {self.altura_geometrica_val} m, Perdas distribuídas: {perda_distribuida} m, Perdas localizadas: {self.localizadas} m")
        print(f"Area da seção: {self._diametro.area_seccao():.6f} m²")
        print(f"Vazão: {self.vazao} m³/s, Diâmetro: {self.diametro_tubulacao} m")
        print(f"{self.darcy.currentText()} - {self.hazen_will.currentText()}")

        # 3. Atualizar gráficos
        self.atualizar_graficos_curvas()

    def inicializar_graficos_curvas(self):
        """Cria as instâncias dos gráficos uma única vez."""
        self.grafico_altura = Grafico(tipo='altura')
        self.grafico_potencia = Grafico(tipo='potencia')
        self.grafico_rendimento = Grafico(tipo='rendimento')
        
        # Limpa layouts antigos se existirem
        for widget in [self.altura, self.potencia, self.rendimento]:
            if widget.layout():
                while widget.layout().count():
                    child = widget.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
        
        layout_altura = QVBoxLayout(self.altura)
        layout_altura.addWidget(self.grafico_altura)
        
        layout_potencia = QVBoxLayout(self.potencia)
        layout_potencia.addWidget(self.grafico_potencia)
        
        layout_rendimento = QVBoxLayout(self.rendimento)
        layout_rendimento.addWidget(self.grafico_rendimento)

    def atualizar_graficos_curvas(self):
        """Atualiza os gráficos com os dados mais recentes."""

        vazao_m3h_quadrado = self.vazao ** 2
        coeficiente_perda = self.perdas_totais / vazao_m3h_quadrado if vazao_m3h_quadrado > 1e-9 else 0.0

        self.grafico_altura.actualizar_dados(self.altura_geometrica_val, coeficiente_perda)
        self.grafico_potencia.actualizar_dados(self.altura_geometrica_val, coeficiente_perda)
        self.grafico_rendimento.actualizar_dados(self.altura_geometrica_val, coeficiente_perda)

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
                self, "Permissão de Localização",
                "Este site deseja acessar sua localização. Permitir?",
                QMessageBox.Yes | QMessageBox.No
            )
            permission = QWebEnginePage.PermissionGrantedByUser if resposta == QMessageBox.Yes else QWebEnginePage.PermissionDeniedByUser
            self.page.setFeaturePermission(url, feature, permission)
  
    def salvar_configuracoes(self):
        self.config.salvar_geometria_janela(self)
        self.config.salvar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.salvar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.salvar_texto_lineedit(self.Vazao_2, "vazao_valor")
        self.config.salvar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.salvar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.salvar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def restaurar_configuracoes(self):
        self.config.restaurar_geometria_janela(self)
        self.config.restaurar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.restaurar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.restaurar_texto_lineedit(self.Vazao_2, "vazao_valor")
        self.config.restaurar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.restaurar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.restaurar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def closeEvent(self, event):
        self.salvar_configuracoes()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Apply stylesheet if it exists
    try:
        with open(r"estilos\estilos.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet not found.")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())