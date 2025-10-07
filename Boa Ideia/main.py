import sys
import os
import json
import logging
import img.img_rc

# ================== Qt Imports ==================
from PySide6.QtCore import (
    Qt, QUrl, QEvent, QSize, QPoint, QTimer, Signal, Slot, QSettings, QStringListModel,
    QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import (
    QIcon, QAction, QDoubleValidator, QSurfaceFormat, QPixmap
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMenu, QCompleter, QToolButton,
    QMessageBox, QFileDialog, QVBoxLayout, QSizePolicy
)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

# ================== Bibliotecas Externas ==================
from qframelesswindow import FramelessWindow
import fluids.piping as piping
from matplotlib import pyplot as plt
import numpy as np
import CoolProp.CoolProp as CP
from scipy.constants import g
import qdarkstyle

# ================== Importacoes Locais (GUI) ==================
from gui.Ui_main import Ui_AquaPump
from gui.main_about import Dialog

# ================== Importacoes Locais (Scripts) ==================
from src.pdf_gen import PDF
from src.csv_gen import CSV
from src.menus import Menus
from src.definicoes import Definicoes
from src.requisicoes import Pesquisa
from src.conexoes_sinais import ConexoesUI
from src.configurações import Configuracoes
from src.JavaScript import Mapa
from src.animações import Animações
from src.historico import HistoricoManager
from src.gestor_database import GestorDatabase
from src.Observações import Observacoes
from src.web_channel import (
    Dados, Altura_Geometrica, Dimensao_Tubulacao, Acessorios_sistema
)

# ================== Importacoes Locais (Calculos) ==================
from calculos.perdas_cargas import Perdas
from calculos.curvas_bomba import Grafico
from calculos.unidades import ConversorUnidades
from calculos.dimensionamento_tubulação import Tubulacao

# ================== Logging Configuration ==================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== WebEngine Configurations ==================
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = ("--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy")
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = ("--disable-gpu-vsync --disable-frame-rate-limit")


# ==========================================================
#                       MAIN WINDOW
# ==========================================================
class MainWindow(FramelessWindow, Ui_AquaPump):
    """
    Classe principal da aplicação AquaPump para dimensionamento de sistemas de bombeamento.
    """

    def __init__(self, parent=None):
        """Inicializa a janela principal e todos os seus componentes."""
        super().__init__(parent)
        self.setupUi(self)

        # ================== INICIALIZAÇÃO DE ATRIBUTOS ==================
        
        # ---------- Configurações da Janela ----------
        self.setWindowTitle("AquaPump")
        self.setWindowIcon(QIcon(u":/img/logo_principal.png"))
        self.ex_3 = chr(0x00B3)   # Expoente para m³

        # ---------- Atributos de Cálculo do Sistema ----------
        self.vazao = 0.0
        self.tempo = 0.0
        self.diametro_tubulacao = 0.0
        self.comprimento_tubulacao_val = 0.0
        self.altura_geometrica_val = 0.0
        self.localizadas = 0.0
        self.perdas_totais = 0.0
        self.altura_manometrica = 0.0
        self.potencia_requerida = 0.0

        self.modelo.setText(f"Grundfos CM 15-2 - Centrifuga")
        self.vazao_label.setText("Caudal nominal: 17 m³/h")
        self.altura_3.setText("Altura manométrica nominal: 29.7 m  ")
        self.potencia_3.setText("Potência nominal: 1.9 kW ")
        self.label_10.setPixmap(QPixmap(r"H:\O meu disco\Base de Dados\Grunfos\CM 15-3").scaled(250, 250, Qt.KeepAspectRatio))

        # ---------- Inicialização de Classes Auxiliares ----------
        self._inicializar_classes_auxiliares()
        
        # ---------- Configurações de Interface ----------
        self._configurar_validadores()
        self._configurar_combobox()
        self._configurar_placeholders()
        
        # ---------- WebEngine + Mapa ----------
        self._configurar_webengine()
        
        # ---------- Configurações de Rede ----------
        self._configurar_rede()
        
        # ---------- Conexões de Sinais ----------
        self._configurar_conexoes()
        
        # ---------- Inicialização de Gráficos ----------
        self._inicializar_graficos()
        self.atualizar_graficos_curvas()
        self.mudanca_dinamica_perdas_carga()

    # ================== MÉTODOS DE INICIALIZAÇÃO ==================

    def _inicializar_classes_auxiliares(self):
        """Inicializa todas as classes auxiliares utilizadas na aplicação."""
        self.animações = Animações()
        self.relatorio_pdf = PDF()
        self.definicoes = Definicoes(parent=self)
        self.config = Configuracoes()
        self.menu = Menus(parent=self, config=self.config)
        self.conversor = ConversorUnidades()
        self._diametro = Tubulacao()
        self.historico_manager = HistoricoManager(self)
        self.janela_sobre = Dialog()
        
        # Carregar base de dados
        db_caminho = self.caminho_dados(r'data/aquapump.db')
        try:
            self.gestor_db = GestorDatabase(db_caminho)
            logger.info('Base de dados Carregada com sucesso')
        except Exception as e:
            logger.warning(f"Erro ao carregar base de dados devido a {e}")

        # Atualizar parâmetros iniciais
        self.atualizar_parametros_entrada()

    def _configurar_validadores(self):
        """Configura validadores para campos de entrada numéricos."""
        validator = QDoubleValidator(0.0, 10000.0, 6)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

    def _configurar_combobox(self):
        """Configura os combobox com valores iniciais."""
        self.hazen_will.addItems(Perdas.get_lista_materiais_hazen())
        self.hazen_will.setHidden(True)
        self.darcy.addItems(Perdas.get_lista_materiais_darcy())

    def _configurar_placeholders(self):
        """Configura textos de placeholder para campos de entrada."""
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")
        self.Vazao.setPlaceholderText("Tempo em horas")

    def _configurar_webengine(self):
        """Configura o WebEngine, WebChannel e integração com JavaScript."""
        # Canais de comunicação com JavaScript
        self.altura_geometrica_channel = Altura_Geometrica()
        self.comprimento_tubulacao_channel = Dimensao_Tubulacao()
        self.acessorios_channel = Acessorios_sistema()
        self.dados = Dados()

        # Configuração do WebChannel
        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)

        # Registro de objetos no canal
        self._canal.registerObject("altura", self.altura_geometrica_channel)
        self._canal.registerObject("comprimento", self.comprimento_tubulacao_channel)
        self._canal.registerObject("acessorios", self.acessorios_channel)

        # Configuração do mapa
        self.mapinha = Mapa()
        self.page.setHtml(self.mapinha.html_code)
        self.icone_2.view().setMinimumWidth(60)

    def _configurar_rede(self):
        """Configura o gerenciador de rede para download de imagens."""
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self._on_image_downloaded)
        self._imagem_request_label = None

    def _configurar_conexoes(self):
        """Configura todas as conexões de sinais da interface."""
        self.conexoes = ConexoesUI(
            parent=self, menu=self.menu, animacoes=self.animações, configuracoes=self.config
        )

    def _inicializar_graficos(self):
        """Inicializa e configura todos os gráficos da aplicação."""
        self.grafico_altura = Grafico()
        self.grafico_potencia = Grafico()
        self.grafico_rendimento = Grafico()
        self.grafico_npsh = Grafico()

        # Limpar layouts existentes
        for layout in [self.altura.layout(), self.potencia.layout(), self.rendimento.layout()]:
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
        
        # Adicionar gráficos aos layouts
        QVBoxLayout(self.altura).addWidget(self.grafico_altura)
        QVBoxLayout(self.potencia).addWidget(self.grafico_potencia)
        QVBoxLayout(self.rendimento).addWidget(self.grafico_rendimento)
        QVBoxLayout(self.npsh_2).addWidget(self.grafico_npsh)

    # ================== MÉTODOS DE CARREGAMENTO DE ARQUIVOS ==================

    def caminho_dados(self, caminho_relactivo):
        """
        Garante que os arquivos sejam carregados tanto nos testes de Python como no .exe.
        
        Args:
            caminho_relactivo: Caminho relativo do arquivo
            
        Returns:
            str: Caminho absoluto do arquivo
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, caminho_relactivo)
        return os.path.join(os.path.abspath("."), caminho_relactivo)

    # ================== MÉTODOS DE CÁLCULO DO SISTEMA ==================

    def actualizar_vazao(self):
        """Retorna a unidade de vazão selecionada."""
        return self.icone_2.currentText()

    def atualizar_parametros_entrada(self):
        """Lê os valores de entrada (vazão, tempo) e recalcula o sistema."""
        texto_vazao = self.Vazao_2.text().strip().replace(',', '.')
        self.vazao_geral = float(texto_vazao) if texto_vazao else 0.0
        self.vazao = self.conversor.converter_vazao(self.vazao_geral, self.icone_2.currentText(), 'm³/s')
        print("Vazão atualizada:", self.vazao, "m³/s")
        self.vazao_resul.setText(f"{self.vazao_geral} {self.icone_2.currentText()}")

        texto_tempo = self.Vazao.text().strip().replace(',', '.')
        self.tempo = float(texto_tempo) if texto_tempo else 0.0

        self.calculo_diametro_tubulacao()
        self.perdas_carga()
        self.recalcular_sistema_completo()

    def calculo_diametro_tubulacao(self):
        """Calcula o diâmetro da tubulação."""
        self.diametro_tubulacao = self._diametro.calcular_diametro(
            self.vazao, self.tempo
        )
        self.diametro_resul.setText(f"{self.diametro_tubulacao:.3f} {self.comprimento_box.currentText()}")
        self.seccao_resul.setText(f"{self._diametro.area_seccao():.3f} m²")

        print(f"Diâmetro da tubulação calculado: {self.diametro_tubulacao} m ")
        print(f"Área da seção calculada: {self._diametro.area_seccao():.6f}")
        
    def perdas_carga(self):
        """Instancia a classe de Perdas com os parâmetros atuais."""
        vazao_m3s = self.vazao
        self.perdas = Perdas(
            vazao_m3s,
            self.diametro_tubulacao,
            self._diametro.area_seccao(),
            self.darcy.currentText(),
            self.hazen_will.currentText()
        )

    def calcular_potencia(self):
        """Calcula a potencia em KW."""
        self.potencia_requerida = self._diametro.calcular_potencia(self.altura_manometrica, self.vazao)
        self.label_19.setText(f"{self.potencia_requerida:.3f} {self.potencia_box.currentText()}")
        print("Potência calculada:", self.potencia_requerida, "KW")

    def calcular_altura_manometrica(self):
        """Calcula a altura manométrica."""
        self.altura_manometrica = self.altura_geometrica_val + self.perdas_totais
        self.label_18.setText(f"{self.altura_manometrica:.3f} {self.comprimento_box.currentText()}")
        print("Altura manométrica calculada:", self.altura_manometrica)

    @Slot()
    def recalcular_sistema_completo(self):
        """Função central que recalcula perdas, altura manométrica e gráficos."""
        if not hasattr(self, 'perdas') or not self.diametro_tubulacao > 0:
            return

        # 1. Calcular perdas distribuídas
        perda_distribuida = 0.0
        if self.comprimento_tubulacao_val > 0:
            try:
                if self.radioButton_10.isChecked():  # Darcy-Weisbach
                    self.perdas.definir_material_darcy(self.darcy.currentText())
                    perda_distribuida = self.perdas.calcular_perda_carga_darcy(
                        self.comprimento_tubulacao_val
                    )
                elif self.radioButton_9.isChecked():  # Hazen-Williams
                    self.perdas.definir_material_hazen(self.hazen_will.currentText())
                    perda_distribuida = self.perdas.calcular_perda_carga_hazen_williams(
                        self.comprimento_tubulacao_val
                    )
            except (ValueError, AttributeError):
                perda_distribuida = 0.0

        # 2. Calcular perdas totais e altura manométrica
        self.perdas_totais = perda_distribuida + self.localizadas
        self.calcular_potencia()
        self.perdas_resul.setText(f"{self.perdas_totais:.3f} {self.comprimento_box.currentText()}")
        print(f"Perdas totais: {self.perdas_totais:.8f} m")
        self.calcular_altura_manometrica()

        # 3. Atualizar gráficos
        self.atualizar_graficos_curvas()

    # ================== MÉTODOS DE COMUNICAÇÃO COM JAVASCRIPT ==================

    @Slot(list)
    def definir_acessorios(self, lista):
        """Recebe a lista de acessórios do JS e recalcula o sistema."""
        if not hasattr(self, 'perdas'):
            return
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

    def enviar_js(self):
        """Envia dados de entrada (vazão, tempo) para o JavaScript."""
        self.exibir_dados_calculados()
        self.dados.enviar_dados(self.vazao, self.tempo, self.altura_manometrica_ex, self.potencia_exe, self.view)
    
    def enviar_unidades_js(self):
        """Envia unidades selecionadas para o JavaScript."""
        self.unidades_exibicao()
        self.dados.enviar_unidades(self.unidade_vazao, self.unidade_diametro, self.unidade_altura, self.unidade_potencia, self.view)

    # ================== MÉTODOS DE GRÁFICOS ==================

    def atualizar_graficos_curvas(self):
        """
        Atualiza TODOS os gráficos de SIMULAÇÃO, garantindo cálculos estáveis e consistentes.
        """
        try:
            # ==============================
            # 1. PARÂMETROS DE ENTRADA
            # ==============================
            vazao_sistema_m3s = self.vazao if self.vazao > 1e-9 else 0.001
            altura_manometrica_m = self.altura_manometrica if self.altura_manometrica > 1e-9 else 0.1
            altura_geometrica_m = self.altura_geometrica_val

            # ==============================
            # 2. GERAR PONTOS PARA O EIXO DA VAZÃO
            # ==============================
            q_max_m3s = vazao_sistema_m3s * 1.5
            q_plot_m3s = np.linspace(1e-9, q_max_m3s, 200)

            # ==============================
            # 3. CÁLCULO DAS CURVAS
            # ==============================
            # A. Curva do Sistema (H = H_geom + K * Q²)
            coef_perda = (altura_manometrica_m - altura_geometrica_m) / (vazao_sistema_m3s ** 2)
            H_sistema_m = altura_geometrica_m + coef_perda * q_plot_m3s ** 2

            # B. Curva da Bomba Simulada (Parábola H = H0 - A*Q²)
            H0_bomba_m = altura_manometrica_m * 1.3  # Altura de shutoff (Q=0) um pouco acima
            A_bomba = (H0_bomba_m - altura_manometrica_m) / (vazao_sistema_m3s ** 2)
            H_bomba_m = np.clip(H0_bomba_m - A_bomba * q_plot_m3s ** 2, 0, None)

            # C. Curva de Rendimento Simulada (η)
            eta_max = 0.75 # Ponto de melhor eficiência
            k_rendimento = (eta_max - 0.1) / (vazao_sistema_m3s ** 2)
            eta_plot = np.clip(eta_max - k_rendimento * (q_plot_m3s - vazao_sistema_m3s)**2, 0.1, eta_max)

            # D. Curva de Potência (P = ρ*g*Q*H / η)
            self.rho = CP.PropsSI("D", "T", 293.15, "P", 101325, "Water")
            self.peso_especifico = self.rho * g  # kg/m³ * m/s² = N/m³
            potencia_plot_watt = (self.peso_especifico * q_plot_m3s * H_bomba_m) / eta_plot
            
            # E. Curva de NPSH Requerido (NPSHr) Simulada
            npsh_min = 1.5 # m
            npsh_max = 5.0 # m
            npsh_plot_m = npsh_min + (npsh_max - npsh_min) * (q_plot_m3s / q_max_m3s)**2

            # ==============================
            # 4. PONTO DE OPERAÇÃO
            # ==============================
            q_op_m3s = vazao_sistema_m3s
            h_op_m = altura_manometrica_m
            p_op_watt = np.interp(q_op_m3s, q_plot_m3s, potencia_plot_watt)
            eta_op = np.interp(q_op_m3s, q_plot_m3s, eta_plot)
            npsh_op_m = np.interp(q_op_m3s, q_plot_m3s, npsh_plot_m)

            # ==============================
            # 5. CONVERSÕES DE UNIDADES PARA EXIBIÇÃO
            # ==============================
            u_q = self.caudal_box.currentText()
            u_h = self.altura_box.currentText()
            u_p = self.potencia_box.currentText()

            q_plot_exibir = self.conversor.converter_vazao(q_plot_m3s, "m³/s", u_q)
            H_bomba_exibir = self.conversor.converter_comprimento(H_bomba_m, "m", u_h)
            H_sistema_exibir = self.conversor.converter_comprimento(H_sistema_m, "m", u_h)
            potencia_exibir = self.conversor.converter_potencia(potencia_plot_watt, "watt", u_p)
            rendimento_exibir = eta_plot * 100
            npsh_exibir = self.conversor.converter_comprimento(npsh_plot_m, "m", u_h)

            q_op_exibir = self.conversor.converter_vazao(q_op_m3s, "m³/s", u_q)
            h_op_exibir = self.conversor.converter_comprimento(h_op_m, "m", u_h)
            p_op_exibir = self.conversor.converter_potencia(p_op_watt, "watt", u_p)
            eta_op_exibir = eta_op * 100
            npsh_op_exibir = self.conversor.converter_comprimento(npsh_op_m, "m", u_h)

            # ==============================
            # 6. PLOTAGEM
            # ============================== 
            self.grafico_altura.plotar_dados(
                tipo_grafico="Altura",
                dados_curva1={"label": "Curva Bomba (Simulada)", "x": q_plot_exibir, "y": H_bomba_exibir},
                dados_curva2={"label": "Curva Sistema", "x": q_plot_exibir, "y": H_sistema_exibir},
                ponto_operacao={"x": q_op_exibir, "y": h_op_exibir},
                unidade_vazao=u_q, unidade_y=u_h,
                titulo="Altura vs. Vazão"
            )

            self.grafico_potencia.plotar_dados(
                tipo_grafico="Potência",
                dados_curva1={"label": "Potência Consumida", "x": q_plot_exibir, "y": potencia_exibir, "cor": "#2ca02c"},
                ponto_operacao={"x": q_op_exibir, "y": p_op_exibir},
                unidade_vazao=u_q, unidade_y=u_p,
                titulo="Potência vs. Vazão"
            )

            self.grafico_rendimento.plotar_dados(
                tipo_grafico="Rendimento",
                dados_curva1={"label": "Rendimento", "x": q_plot_exibir, "y": rendimento_exibir, "cor": "#d62728"},
                ponto_operacao={"x": q_op_exibir, "y": eta_op_exibir},
                unidade_vazao=u_q, unidade_y="%",
                titulo="Rendimento vs. Vazão"
            )
            
            # Plotagem do NPSH
            self.grafico_npsh.plotar_dados(
                tipo_grafico="NPSH",
                dados_curva1={"label": "NPSH Requerido (Simulado)", "x": q_plot_exibir, "y": npsh_exibir, "cor": "#9467bd"},
                ponto_operacao={"x": q_op_exibir, "y": npsh_op_exibir},
                unidade_vazao=u_q, unidade_y=u_h,
                titulo="NPSH Requerido vs. Vazão"
            )

        except Exception as e:
            logger.error(f"Erro ao atualizar gráficos de simulação: {e}", exc_info=True)

    # ================== MÉTODOS DE EXIBIÇÃO DE DADOS ==================

    def exibir_dados_calculados(self):
        """Atualiza os resultados em SI para outras unidades."""
        try:
            self.vazao_ex = self.conversor.converter_vazao(self.vazao, 'm³/s', self.icone_2.currentText())
            
            self.diametro_t = self.conversor.converter_comprimento(
                self.diametro_tubulacao, 'm', self.diametro_box.currentText()
            )
            self.compr = self.conversor.converter_comprimento(
                self.comprimento_tubulacao_val, 'm', self.comprimento_box.currentText()
            )
            self.potencia_exe = self.conversor.converter_potencia(
                self.potencia_requerida, 'kilowatt', self.potencia_box.currentText()
            )
            self.altura_geometrica_ex = self.conversor.converter_comprimento(
                self.altura_geometrica_val, 'm', self.altura_box.currentText()
            )
            self.altura_manometrica_ex = self.conversor.converter_comprimento(
                self.altura_manometrica, 'm', self.altura_box.currentText()
            )

        except Exception as e:
            pass

    def unidades_exibicao(self):
        """Retorna as unidades atualmente selecionadas."""
        self.unidade_vazao = self.icone_2.currentText()
        self.unidade_diametro = self.diametro_box.currentText()
        self.unidade_altura = self.altura_box.currentText()
        self.unidade_potencia = self.potencia_box.currentText()

    # ================== MÉTODOS DE MAPA E PESQUISA ==================

    def pesquisa_mapa(self):
        """Executa pesquisa no mapa via JS."""
        texto = self.pesquisa_line.text()
        pesquisa = f"pesquisar_lugar('{texto}')"
        self.view.page().runJavaScript(pesquisa)

    # ================== MÉTODOS DE EXPORTAÇÃO ==================

    def gerar_pdf(self):
        """Gera o relatório em PDF com os dados atuais."""
        try:
            self.exibir_dados_calculados()
            material = self.darcy.currentText() if self.radioButton_10.isChecked() else self.hazen_will.currentText()
            dados_relatorio = {
                'Vazão': (f"{self.vazao_ex:.3f}", f'{self.icone_2.currentText()}'),
                'Tempo de funcionamento': (f"{self.tempo:.1f}", 'horas'),
                'Comprimento da tubulação': (f"{self.compr:.3f}", f'{self.comprimento_box.currentText()}'),
                'Diâmetro da tubulação': (f"{self.diametro_t:.3f}", f'{self.diametro_box.currentText()}'),
                'Potência requerida': (f"{self.potencia_exe:.3f}", f'{self.potencia_box.currentText()}'),
                'Altura geométrica': (f"{self.altura_geometrica_ex:.3f}", f'{self.altura_box.currentText()}'),
                'Perdas totais': (f"{self.perdas_totais:.3f}", f'{self.altura_box.currentText()}'),
                'Altura manométrica': (f"{self.altura_manometrica_ex:.3f}", f'{self.altura_box.currentText()}'),
                'Material da Tubulação': (material, None),
            }

            self.atualizar_graficos_curvas()

            self.relatorio_pdf.adicionar_titulos("Relatório do Sistema de Bombeamento")
            self.relatorio_pdf.adicionar_secao("Dados do Dimensionamento")
            self.relatorio_pdf.adicionar_conteudo(dados_relatorio)
            
            # Adicionar gráficos
            self.relatorio_pdf.adicionar_secao("Gráficos de Curvas da Bomba - Simulação")
            self.relatorio_pdf.adicionar_grafico(self.grafico_altura.figure, self.grafico_potencia.figure, self.grafico_rendimento.figure)

            self.relatorio_pdf.gravar_pdf()
            
        except Exception as e:
            QMessageBox.critical(self, 'ERRO', f'Erro ao gerar PDF devido a {e}')

    def gerar_csv(self):
        """Gera relatório em formato CSV com os dados atuais."""
        try:
            material = self.darcy.currentText() if self.radioButton_10.isChecked() else self.hazen_will.currentText()
            
            dados_relatorio = {
                'Vazão': (f"{self.vazao_ex:.3f}", f'{self.icone_2.currentText()}'),
                'Tempo de funcionamento': (f"{self.tempo:.1f}", 'horas'),
                'Comprimento da tubulação': (f"{self.compr:.3f}", f'{self.comprimento_box.currentText()}'),
                'Diâmetro da tubulação': (f"{self.diametro_t:.3f}", f'{self.diametro_box.currentText()}'),
                'Potência requerida': (f"{self.potencia_exe:.3f}", f'{self.potencia_box.currentText()}'),
                'Altura geométrica': (f"{self.altura_geometrica_ex:.3f}", f'{self.altura_box.currentText()}'),
                'Perdas totais': (f"{self.perdas_totais:.3f}", f'{self.altura_box.currentText()}'),
                'Altura manométrica': (f"{self.altura_manometrica_ex:.3f}", f'{self.altura_box.currentText()}'),
                'Material da Tubulação': (material, None),
            }
            
            csv_exporter = CSV()
            
            # Adicionar metadados
            csv_exporter.adicionar_metadados(
                "Relatório do Sistema de Bombeamento - AquaPump",
                "1.0",
                "Relatório gerado automaticamente pelo sistema AquaPump"
            )
            
            csv_exporter.adicionar_secao("DADOS DO SISTEMA DE BOMBEAMENTO")
            csv_exporter.adicionar_conjunto_dados(dados_relatorio)
            csv_exporter.adicionar_secao("GRÁFICOS DE CURVAS DA BOMBA - SIMULAÇÃO")
            
            # Gerar CSV
            sucesso = csv_exporter.exportar("relatorio_bombeamento.csv")        
            if sucesso:
                QMessageBox.information(self, "Sucesso", "Relatório .xlsv gerado com sucesso!")
            else:
                QMessageBox.warning(self, "Aviso", "Não foi possível gerar o relatório .xlsv.")
                
            return sucesso
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o .xlsv: {str(e)}")
            return False

    # ================== MÉTODOS DE HISTÓRICO ==================

    def salvar_historico(self):
        """Salva o estado atual do cálculo no histórico."""
        dados_calculo = {
            "Vazao_total": self.vazao,
            "Diametro": self.diametro_tubulacao,
            "Perdas_de_Carga": self.perdas_totais,
            "Altura_Manometrica": self.altura_manometrica,
            "Tempo": self.tempo,
            "Material_Tubulacao": self.darcy.currentText() if self.radioButton_10.isChecked() else self.hazen_will.currentText(),
            "Formula_Utilizada": "Darcy-Weisbach" if self.radioButton_10.isChecked() else "Hazen-Williams"
        }
        
        if self.historico_manager.salvar_historico(dados_calculo):
            QMessageBox.information(self, "Sucesso", "Histórico salvo com sucesso!")

    def carregar_historico(self):
        """Carrega um estado anterior de cálculo do histórico."""
        dados = self.historico_manager.carregar_historico()
        if dados:
            # Atualiza os valores na interface
            self.vazao = dados.get("Vazao_total", 0.0)
            self.diametro_tubulacao = dados.get("Diametro", 0.0)
            self.perdas_totais = dados.get("Perdas_de_Carga", 0.0)
            self.altura_manometrica = dados.get("Altura_Manometrica", 0.0)
            self.tempo = dados.get("Tempo", 0.0)
            
            # Atualiza a UI
            self.Vazao_2.setText(f"{self.vazao:.4f}")
            self.Vazao.setText(f"{self.tempo:.2f}")
            
            # Atualiza material e fórmula se disponível nos dados
            material = dados.get("Material_Tubulacao", "")
            formula = dados.get("Formula_Utilizada", "")
            
            if formula == "Darcy-Weisbach":
                self.radioButton_10.setChecked(True)
                index = self.darcy.findText(material)
                if index >= 0:
                    self.darcy.setCurrentIndex(index)
            else:
                self.radioButton_9.setChecked(True)
                index = self.hazen_will.findText(material)
                if index >= 0:
                    self.hazen_will.setCurrentIndex(index)

            self.recalcular_sistema_completo()
            
            QMessageBox.information(self, "Sucesso", "Histórico carregado com sucesso!")

    # ================== MÉTODOS DE SELEÇÃO DE BOMBA ==================

    def selecionar_melhor_bomba(self):
        """
        Seleciona e exibe a melhor bomba para os parâmetros atuais do sistema.
        """
        if not hasattr(self, 'gestor_db') or not self.gestor_db:
            self._nenhuma_bomba_encontrada("Base de dados não disponível.")
            return

        try:
            # Converter para unidades usadas no banco de dados
            vazao_m3h = self.conversor.converter_vazao(self.vazao_geral, self.icone_2.currentText(), 'm³/h')
            altura_m = self.altura_manometrica
            logger.info(f"A vazao nominal e de {vazao_m3h} e a altura manometrica e de {altura_m}")

            # Buscar a melhor bomba
            bomba = self.gestor_db.selecionar_melhor_bomba(vazao_m3h, altura_m)

            if not bomba:
                self._nenhuma_bomba_encontrada("Nenhuma bomba compatível encontrada nos critérios de busca.")
                return

            # Exibir a bomba encontrada
            self._exibir_bomba(bomba)

        except Exception as e:
            logger.error(f"Erro no processo de seleção de bomba: {e}", exc_info=True)
            self._nenhuma_bomba_encontrada("Ocorreu um erro inesperado.")

    def _exibir_bomba(self, bomba: dict):
        """
        Exibe os dados de uma única bomba na interface.
        """
        self.label_12.setText("Melhor Bomba Encontrada")

        self.modelo.setText(f"<b>{bomba['fabricante']}</b> - {bomba['modelo']}")
        self.potencia_3.setText(f"<b>Potência:</b> {bomba['potencia_nominal_kW']} kW")
        self.vazao_label.setText(f"<b>Vazão Nominal:</b> {bomba['caudal_nominal_m3h']} m³/h")
        self.altura_3.setText(f"<b>Altura Nominal:</b> {bomba['altura_nominal_m']} m")

        # Carregar imagem
        caminho_imagem = bomba.get('caminho_imagem', '')
        self.label_10.setText("A carregar imagem...") 

        if caminho_imagem and caminho_imagem.startswith("http"):
            if "drive.google.com" in caminho_imagem:
                try:
                    file_id = caminho_imagem.split('/d/')[1].split('/')[0]
                    url_direto = f"https://drive.google.com/uc?export=view&id={file_id}"
                    request = QNetworkRequest(QUrl(url_direto))
                    self._imagem_request_label = self.label_10
                    self.network_manager.get(request)
                except IndexError:
                    logger.warning("URL do Google Drive mal formatado.")
                    self.label_10.setPixmap(QPixmap(u":/img/infeliz.png").scaled(250, 250, Qt.KeepAspectRatio))
            else:
                request = QNetworkRequest(QUrl(caminho_imagem))
                self._imagem_request_label = self.label_10
                self.network_manager.get(request)
        else:
            logger.warning("Caminho da imagem não é um URL válido.")
            self.label_10.setPixmap(QPixmap(u":/img/infeliz.png").scaled(250, 250, Qt.KeepAspectRatio))

    def _nenhuma_bomba_encontrada(self, motivo: str):
        """Mostra estado quando nenhuma bomba é encontrada"""
        logger.info(motivo)
        self.label_12.setText("Sugestão de Bomba")
        self.modelo.setText("Nenhuma bomba encontrada")
        self.vazao_label.setText("--")
        self.altura_3.setText("--")
        self.potencia_3.setText("--")
        self.label_10.setPixmap(QPixmap(u":/img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))

    def _on_image_downloaded(self, reply):
        """Callback quando o QNetworkAccessManager termina o download da imagem."""
        if self._imagem_request_label is None:
            return

        if reply.error():
            logger.warning(f"Erro ao baixar imagem: {reply.errorString()}")
            self._imagem_request_label.setPixmap(QPixmap(u":/img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))
        else:
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                self._imagem_request_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
            else:
                self._imagem_request_label.setPixmap(QPixmap(u":/img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))

        self._imagem_request_label = None
        reply.deleteLater()

    # ================== MÉTODOS DE INTERFACE ==================

    def mudanca_dinamica_perdas_carga(self):
        """Alterna entre lista de materiais Darcy e Hazen conforme opção selecionada."""
        self.darcy.setVisible(self.radioButton_10.isChecked())
        self.hazen_will.setVisible(self.radioButton_9.isChecked())

    def novo_projecto(self):
        """Reseta a aplicação para um novo projeto, limpando todos os dados."""
        reply = QMessageBox.question(
            self, 
            "Novo Projeto",
            "Tem certeza que deseja iniciar um novo projeto? Todos os dados não salvos serão perdidos.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            # ---------- Reset dos campos de entrada ----------
            self.Vazao_2.clear()
            self.Vazao.clear()
            self.pesquisa_line.clear()
            
            # ---------- Reset dos parâmetros de cálculo ----------
            self.vazao = 0.0
            self.tempo = 0.0
            self.diametro_tubulacao = 0.0
            self.comprimento_tubulacao_val = 0.0
            self.altura_geometrica_val = 0.0
            self.localizadas = 0.0
            self.perdas_totais = 0.0
            self.altura_manometrica = 0.0
            
            # ---------- Reset das seleções ----------
            self.icone_2.setCurrentIndex(0)  # Primeira unidade de vazão
            self.darcy.setCurrentIndex(0)    # Primeiro material Darcy
            self.hazen_will.setCurrentIndex(0)  # Primeiro material Hazen
            self.radioButton_10.setChecked(True)  # Darcy selecionado por padrão
            
            # ---------- Reset do mapa (via JavaScript) ----------
            self.view.page().runJavaScript("limpar_mapa();")
            self.inicializar_graficos()
            self.status_label.setText("Novo projeto iniciado")

            self.atualizar_parametros_entrada()
            QMessageBox.information(self, "Novo Projeto", "Projeto reiniciado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar novo projeto: {str(e)}")

    # ================== MÉTODOS DE CONFIGURAÇÕES ==================

    def salvar_configuracoes(self):
        """Salva estado da janela e widgets."""
        self.config.salvar_geometria_janela(self)
        self.config.salvar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.salvar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.salvar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.salvar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.salvar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def restaurar_configuracoes(self):
        """Restaura estado salvo da janela e widgets."""
        self.config.restaurar_geometria_janela(self)
        self.config.restaurar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.restaurar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.restaurar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.restaurar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.restaurar_texto_combobox(self.hazen_will, "hazen_material_texto")

    # ================== EVENTOS ==================

    def closeEvent(self, event):
        """Salva configurações antes de fechar a janela."""
        self.salvar_configuracoes()
        if hasattr(self, 'gestor_db'):
            self.gestor_db.fechar()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())