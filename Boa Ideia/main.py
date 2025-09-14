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
from qframelesswindow import FramelessWindow, StandardTitleBar

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
from src. gestor_database import GestorDatabase
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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # ---------- Configurações da Janela ----------
        self.setWindowTitle("AquaPump")
        self.setWindowIcon(QIcon(r"img\logo_principal.png"))
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

        # ---------- Inicialização de Classes Internas ----------
        self.animações = Animações()
        self.relatorio_pdf = PDF()
        self.definicoes = Definicoes(parent=self)
        self.config = Configuracoes()
        self.menu = Menus(parent=self, config=self.config)
        self.conversor = ConversorUnidades()
        self._diametro = Tubulacao()
        self.historico_manager = HistoricoManager(self)
        self.janela_sobre = Dialog()
        self.atualizar_parametros_entrada()
        try:
            self.gestor_db = GestorDatabase(db_path=r'data/aquapump.db')
            if self.gestor_db.is_fallback_db():
                logger.warning("Usando banco de dados em memória (fallback)")
                
        except Exception as e:
            logger.error(f"Falha crítica ao inicializar banco de dados: {e}")
            


        # ---------- WebEngine + WebChannel ----------
        self.altura_geometrica_channel = Altura_Geometrica()
        self.comprimento_tubulacao_channel = Dimensao_Tubulacao()
        self.acessorios_channel = Acessorios_sistema()
        self.dados = Dados()

        self._canal = QWebChannel()
        self.page = QWebEnginePage(self)
        self.view.setPage(self.page)
        self.page.setWebChannel(self._canal)

        self._canal.registerObject("altura", self.altura_geometrica_channel)
        self._canal.registerObject("comprimento", self.comprimento_tubulacao_channel)
        self._canal.registerObject("acessorios", self.acessorios_channel)

        # ---------------Network Manager----------------
        self._internet = QNetworkAccessManager()
        self._internet.finished.connect(self._on_image_downloaded)

        # ---------- Conexões e Configurações ----------
        self.conexoes = ConexoesUI(
            parent=self, menu=self.menu, animacoes=self.animações, configuracoes=self.config
        )

        # ---------- ComboBox ----------
        self.hazen_will.addItems(Perdas.get_lista_materiais_hazen())
        self.hazen_will.setHidden(True)
        self.darcy.addItems(Perdas.get_lista_materiais_darcy())

        # ---------- Validação de Entrada ----------
        validator = QDoubleValidator(0.0, 10000.0, 3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

        # ---------- Autocompletar Pesquisa ----------
        self.completador = QCompleter()
        self.completador.setCaseSensitivity(Qt.CaseInsensitive)
        self.pesquisa_line.setCompleter(self.completador)
        self.pesquisa_line.setPlaceholderText("Pesquisar")

        # ---------- WebEngine + Mapa ----------
        self.mapinha = Mapa()
        self.page.setHtml(self.mapinha.html_code)
        self.icone_2.view().setMinimumWidth(60)

        # ---------- PlaceholderText ----------
        self.Vazao_2.setPlaceholderText(f"Vazão em {self.icone_2.currentText()}")
        self.Vazao.setPlaceholderText("Tempo em horas")

        # ---------- Status e Threads ----------
        self.worker = None
        self.status_label = QLabel()

        # ---------- Inicialização de Gráficos ----------
        self.inicializar_graficos_curvas()
        self.mudanca_dinamica_perdas_carga()

    # ==========================================================
    #                 MÉTODOS DE CÁLCULO
    # ==========================================================
    def actualizar_vazao(self):
        """Retorna a unidade de vazão selecionada."""
        return self.icone_2.currentText()

    def atualizar_parametros_entrada(self):
        """Lê os valores de entrada (vazão, tempo) e recalcula o sistema."""
        texto_vazao = self.Vazao_2.text().strip().replace(',', '.')
        self.vazao = float(texto_vazao) if texto_vazao else 0.0

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

    @Slot()
    def recalcular_sistema_completo(self):
        """Função central que recalcula perdas, altura manométrica e gráficos."""
        if not hasattr(self, 'perdas') or not self.diametro_tubulacao > 0:
            return

        # --- 1. Perdas distribuídas ---
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

        # --- 2. Perdas totais e altura manométrica ---
        self.perdas_totais = perda_distribuida + self.localizadas
        self.altura_manometrica = self.altura_geometrica_val + self.perdas_totais

        print(f"Perdas totais: {self.perdas_totais:.8f} m")
        print("Altura manométrica calculada:", self.altura_manometrica)

        # --- 3. Atualização dos gráficos ---
        self.atualizar_graficos_curvas()

    # ==========================================================
    #                 GRÁFICOS
    # ==========================================================
    def inicializar_graficos_curvas(self):
        """Inicializa os gráficos de altura, potência e rendimento."""

        self.grafico_altura = Grafico(
            tipo='altura',
            potencia=self.potencia_box.currentText(),
            altura=self.altura_box.currentText(),
            v=self.caudal_box.currentText()
        )
        self.grafico_potencia = Grafico(
            tipo='potencia',
            potencia=self.potencia_box.currentText(),
            altura=self.altura_box.currentText(),
            v=self.caudal_box.currentText()
        )
        self.grafico_rendimento = Grafico(
            tipo='rendimento',
            potencia=self.potencia_box.currentText(),
            altura=self.altura_box.currentText(),
            v=self.caudal_box.currentText()
        )

        if not hasattr(self, "layout_altura"):
            self.layout_altura = QVBoxLayout(self.altura)
        if not hasattr(self, "layout_potencia"):
            self.layout_potencia = QVBoxLayout(self.potencia)
        if not hasattr(self, "layout_rendimento"):
            self.layout_rendimento = QVBoxLayout(self.rendimento)

        for layout in [self.layout_altura, self.layout_potencia, self.layout_rendimento]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        self.layout_altura.addWidget(self.grafico_altura)
        self.layout_potencia.addWidget(self.grafico_potencia)
        self.layout_rendimento.addWidget(self.grafico_rendimento)

    
    def estilo_grafico(self):
        """Aplica estilo consistente aos gráficos."""
        
        self.janel_direita.setStyleSheet("""
            background-color: #ffffff;
        """)

    def atualizar_graficos_curvas(self):
        """Atualiza os gráficos com os dados calculados mais recentes."""
        vazao_m3h_quadrado = self.vazao ** 2
        coef_perda = self.perdas_totais / vazao_m3h_quadrado if vazao_m3h_quadrado > 1e-9 else 0.0

        self.grafico_altura.actualizar_dados(self.altura_geometrica_val, coef_perda)
        self.grafico_potencia.actualizar_dados(self.altura_geometrica_val, coef_perda)
        self.grafico_rendimento.actualizar_dados(self.altura_geometrica_val, coef_perda)

    def atualizar_unidades_graficos(self):
        """Atualiza os gráficos quando as unidades são alteradas"""
        if hasattr(self, 'grafico_altura') and hasattr(self, 'grafico_potencia') and hasattr(self, 'grafico_rendimento'):
            self.inicializar_graficos_curvas()
            self.atualizar_graficos_curvas()
    # ==========================================================
    #                 INTEGRAÇÃO COM JAVASCRIPT
    # ==========================================================
    def enviar_js(self):
        """Envia dados de entrada (vazão, tempo) para o JavaScript."""
        texto_vazao = self.Vazao_2.text().strip().replace(',', '.')
        self.vazao = float(texto_vazao) if texto_vazao else 0.0

        texto_tempo = self.Vazao.text().strip().replace(',', '.')
        self.tempo = float(texto_tempo) if texto_tempo else 0.0

        self.dados.enviar_dados(self.vazao, self.tempo, self.view)

    def mudanca_dinamica_perdas_carga(self):
        """Alterna entre lista de materiais Darcy e Hazen conforme opção selecionada."""
        self.darcy.setVisible(self.radioButton_10.isChecked())
        self.hazen_will.setVisible(self.radioButton_9.isChecked())

    # ==========================================================
    #                 PESQUISA (MAPA + AUTOCOMPLETAR)
    # ==========================================================
    def pesquisa_mapa(self):
        """Executa pesquisa no mapa via JS."""
        texto = self.pesquisa_line.text()
        pesquisa = f"pesquisar_lugar('{texto}')"
        self.view.page().runJavaScript(pesquisa)

    @Slot(str)
    def buscar_sugestoes(self, texto):
        """Busca sugestões de local em background (mínimo 3 letras)."""
        if len(texto) >= 3:
            self.status_label.setText("Buscando sugestões...")
            if self.worker and self.worker.isRunning():
                self.worker.terminate()
            self.worker = Pesquisa(texto)
            self.worker.resultado.connect(self.atualizar_completer)
            self.worker.start()

    @Slot(list)
    def atualizar_completer(self, sugestoes):
        """Atualiza o autocompleter com novas sugestões."""
        self.status_label.setText("")
        modelo = QStringListModel(sugestoes)
        self.completador.setModel(modelo)

    # ==========================================================
    #                EXPORTAÇÃO PARA PDF
    # ==========================================================
    def gerar_pdf(self):
        try:
            material = self.darcy.currentText() if self.radioButton_10.isChecked() else self.hazen_will.currentText()
            dados_relatorio = {
                'Vazão': (f"{self.vazao:.4f}", f'{self.icone_2.currentText()}'),
                'Tempo de funcionamento': (f"{self.tempo:.2f}", 'horas'),
                'Comprimento da tubulação': (f"{self.comprimento_tubulacao_val:.2f}", 'm'),
                'Diâmetro da tubulação': (f"{self.diametro_tubulacao:.4f}", f'{self.diametro_box.currentText()}'),
                'Altura geométrica': (f"{self.altura_geometrica_val:.2f}", f'{self.altura_box.currentText()}'),
                'Perdas totais': (f"{self.perdas_totais:.4f}", f'{self.altura_box.currentText()}'),
                'Altura manométrica': (f"{self.altura_manometrica:.2f}", f'{self.altura_box.currentText()}'),
                'Material da Tubulação': (material, None),
            }

            self.atualizar_graficos_curvas()

            # Configurar e gerar PDF
            self.relatorio_pdf.adicionar_titulos("Relatório do Sistema de Bombeamento")
            self.relatorio_pdf.adicionar_secao("Dados do Dimensionamento")
            self.relatorio_pdf.adicionar_conteudo(dados_relatorio)
            
            # Adicionar gráficos
            self.relatorio_pdf.adicionar_secao("Gráficos de Curvas da Bomba - Simulação")
            self.relatorio_pdf.adicionar_grafico(self.grafico_altura.figure, self.grafico_potencia.figure, self.grafico_rendimento.figure)

            self.relatorio_pdf.gravar_pdf()
            QMessageBox.information(self, "Sucesso", "Relatório PDF gerado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, 'ERRO', f'Erro ao gerar PDF devido a {e}')

    def gerar_csv(self):
        try:
            material = self.darcy.currentText() if self.radioButton_10.isChecked() else self.hazen_will.currentText()
            
            # Coletar os mesmos dados que seriam usados no PDF
            dados_relatorio = {
                'Vazão': (f"{self.vazao:.4f}", 'm³/s'),
                'Tempo de funcionamento': (f"{self.tempo:.2f}", 'horas'),
                'Diâmetro da tubulação': (f"{self.diametro_tubulacao:.4f}", 'm'),
                'Altura geométrica': (f"{self.altura_geometrica_val:.2f}", 'm'),
                'Perdas totais': (f"{self.perdas_totais:.4f}", 'm'),
                'Altura manométrica': (f"{self.altura_manometrica:.2f}", 'm'),
                'Material da Tubulação': (material, None),
            }
            

            csv_exporter = CSV()
            
            # Adicionar metadados
            csv_exporter.adicionar_metadados(
                "Relatório do Sistema de Bombeamento - AquaPump",
                "1.0",
                "Relatório gerado automaticamente pelo sistema AquaPump"
            )
            
            # Adicionar seção principal
            csv_exporter.adicionar_secao("DADOS DO SISTEMA")
            
            # Adicionar todos os dados do relatório
            csv_exporter.adicionar_conjunto_dados(dados_relatorio, "Cálculos do Sistema")
            
            # Gerar CSV
            sucesso = csv_exporter.exportar("relatorio_bombeamento.csv")        
            if sucesso:
                QMessageBox.information(self, "Sucesso", "Relatório CSV gerado com sucesso!")
            else:
                QMessageBox.warning(self, "Aviso", "Não foi possível gerar o relatório CSV.")
                
            return sucesso
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Ocorreu um erro ao gerar o CSV: {str(e)}")
            return False
        
    # =========================================================
    #               Histórico de Cálculos
    # =========================================================
    def salvar_historico(self):
        """Salva o estado atual do cálculo"""
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
        """Carrega um estado anterior de cálculo"""
        dados = self.historico_manager.carregar_historico()
        if dados:
            # Atualiza os valores da interface
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

    def selecionar_melhor_bomba(self):
        """Seleciona e exibe a melhor bomba para o sistema"""
        try:
            if not hasattr(self, 'vazao') or not hasattr(self, 'altura_manometrica'):
                self._nenhuma_bomba_encontrada()
                return

            if self.vazao <= 0 or self.altura_manometrica <= 0:
                self._nenhuma_bomba_encontrada()
                return

            bombas_candidatas = self.selecionar_bombas_candidatas()
            if not bombas_candidatas:
                self._nenhuma_bomba_encontrada()
                return

            melhor_bomba = bombas_candidatas[0]

            modelo = melhor_bomba['modelo']
            fabricante = melhor_bomba['fabricante']
            tipo_bomba = melhor_bomba['tipo_bomba']
            potencia = melhor_bomba['potencia_nominal_kW']
            vazao = melhor_bomba['caudal_nominal_m3h']
            altura = melhor_bomba['altura_nominal_m']
            material = melhor_bomba['material_corpo']
            caminho_imagem = melhor_bomba['caminho_imagem']

            self.modelo.setText(f"{fabricante} - {modelo} ({tipo_bomba})")
            self.potencia_3.setText(f"Potência: {potencia} kW")
            self.vazao_label.setText(f"Vazão: {vazao} m³/h")
            self.altura_3.setText(f"Altura: {altura} m")
            self.material.setText(f"Material (Corpo Bomba): {material}")

            if caminho_imagem:
                if caminho_imagem.startswith("http"):  
                    request = QNetworkRequest(QUrl(caminho_imagem))
                    self._imagem_request_label = self.label_10
                    self.manager.get(request)
                elif os.path.exists(caminho_imagem):
                    self.label_10.setPixmap(QPixmap(caminho_imagem).scaled(150, 150, Qt.KeepAspectRatio))
                else:
                    self.label_10.setPixmap(QPixmap("img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))
            else:
                self.label_10.setPixmap(QPixmap("img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))

        except Exception as e:
            logger.error(f"Erro ao selecionar melhor bomba: {e}")
            self._nenhuma_bomba_encontrada()

    def _on_image_downloaded(self, reply):
        """Callback quando o QNetworkAccessManager termina o download"""
        if self._imagem_request_label is None:
            return

        if reply.error():
            logger.warning(f"Erro ao baixar imagem: {reply.errorString()}")
            self._imagem_request_label.setPixmap(QPixmap("img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))
        else:
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                self._imagem_request_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
            else:
                self._imagem_request_label.setPixmap(QPixmap("img/infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))

        self._imagem_request_label = None
        reply.deleteLater()
   
    def _nenhuma_bomba_encontrada(self):
        """Mostra estado quando nenhuma bomba é encontrada"""
        self.modelo.clear()
        self.material.clear()
        self.vazao_label.clear()
        self.altura_3.clear()
        self.potencia_3.clear()
        self.label_10.clear()

        self.modelo.setText("Nenhuma bomba encontrada")
        self.vazao_label.setText("--")
        self.altura_3.setText("--")
        self.potencia_3.setText("--")
        self.material.setText("--")
        self.label_10.setPixmap(QPixmap(r"img\infeliz.png").scaled(150, 150, Qt.KeepAspectRatio))
        logger.info("Nenhuma bomba candidata encontrada mas tem um pequeno problema com o banco de dados")
        return
    
    def selecionar_bombas_candidatas(self):
        """
        Seleciona e retorna todas as bombas candidatas ordenadas por score,
        permitindo acesso individual a cada bomba.
        """
        try:
            if not hasattr(self, 'vazao') or not hasattr(self, 'altura_manometrica'):
                logger.warning("Parâmetros de cálculo não disponíveis")
                return []
                
            if self.vazao <= 0 or self.altura_manometrica <= 0:
                logger.warning("Vazão ou altura manométrica com valores inválidos")
                return []
            vazao_necessaria_m3h = self.vazao
            altura_necessaria_m = self.altura_manometrica

            if not hasattr(self, 'gestor_db') or not self.gestor_db.verificar_conexao():
                logger.error("Conexão com banco de dados não disponível")
                QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar ao banco de dados de bombas.")
                return []

            bombas_candidatas = self.gestor_db.pesquisar_bombas_candidatas(vazao_necessaria_m3h, altura_necessaria_m)

            if not bombas_candidatas:
                QMessageBox.information(self, "Nenhuma Bomba Encontrada", 
                                    "Não encontramos bombas com essas características. "
                                    "Tente ajustar os parâmetros do sistema.")
                return []

            #Processar resultados
            resultados_finais = []
            
            for bomba in bombas_candidatas:
                try:
                    # Extrair dados da bomba
                    id_bomba = bomba['id']
                    modelo = bomba['modelo']
                    fabricante = bomba['fabricante']
                    tipo_bomba = bomba['tipo_bomba']
                    caudal_nominal_m3h = bomba['caudal_nominal_m3h']
                    altura_nominal_m = bomba['altura_nominal_m']
                    potencia_nominal_kW = bomba['potencia_nominal_kW']
                    velocidade_rpm = bomba['velocidade_rpm']
                    material_corpo = bomba['material_corpo']
                    pressao_max_bar = bomba['pressao_max_bar']
                    caminho_imagem = bomba['caminho_imagem']
                    fator_vazao = bomba['fator_vazao']
                    fator_altura = bomba['fator_altura']
                    score_adequacao = bomba['score_adequacao']

                    if any([valor is None for valor in [modelo, fabricante, caudal_nominal_m3h, altura_nominal_m]]):
                        logger.warning(f"Dados incompletos para bomba {id_bomba}, ignorando")
                        continue
                        
                    # Calcular fatores de operação
                    fator_carga = altura_necessaria_m / altura_nominal_m if altura_nominal_m > 0 else float('inf')
                    fator_vazao_operacao = vazao_necessaria_m3h / caudal_nominal_m3h if caudal_nominal_m3h > 0 else float('inf')

                    if fator_carga > 2.0 or fator_vazao_operacao > 2.0 or fator_carga < 0.5 or fator_vazao_operacao < 0.5:
                        continue
                        
                    # Estimativa de rendimento (aproximação)
                    diferenca_ideal = abs(1 - fator_carga) + abs(1 - fator_vazao_operacao)
                    rendimento_estimado = max(0.4, 0.8 - (diferenca_ideal * 0.3))  # Mínimo de 40%, máximo de 80%
                    
                    # Calcular potência estimada
                    # Densidade da água assumida como 1000 kg/m³
                    potencia_hidraulica = (1000 * 9.81 * vazao_necessaria_m3h * altura_necessaria_m) / 3600
                    potencia_eletrica_estimada = potencia_hidraulica / rendimento_estimado if rendimento_estimado > 0 else 0
                    
                    # Verificar se a potência nominal é suficiente
                    potencia_suficiente = potencia_nominal_kW >= potencia_eletrica_estimada * 1.2  # Margem de 20%
                    
                    # Score de adequação baseado em múltiplos fatores
                    score_final = self.calcular_score_adequacao_simplificado(
                        rendimento_estimado,
                        fator_vazao_operacao,
                        fator_carga,
                        potencia_suficiente,
                        potencia_nominal_kW,
                        potencia_eletrica_estimada
                    )
                    
                    # Organizar todos os dados em um dicionário estruturado
                    dados_bomba = {
                        # Identificação
                        "id_bomba": id_bomba,
                        "modelo": modelo,
                        "fabricante": fabricante,
                        "tipo_bomba": tipo_bomba,
                        
                        # Especificações nominais
                        "caudal_nominal_m3h": caudal_nominal_m3h,
                        "altura_nominal_m": altura_nominal_m,
                        "potencia_nominal_kW": potencia_nominal_kW,
                        "velocidade_rpm": velocidade_rpm,
                        "material_corpo": material_corpo,
                        "pressao_max_bar": pressao_max_bar,
                        "caminho_imagem": caminho_imagem,
                        
                        # Fatores de adequação
                        "fator_vazao": fator_vazao,
                        "fator_altura": fator_altura,
                        "score_adequacao_db": score_adequacao,
                        
                        # Análise de operação
                        "fator_carga_operacao": fator_carga,
                        "fator_vazao_operacao": fator_vazao_operacao,
                        "rendimento_estimado": rendimento_estimado,
                        "potencia_hidraulica_kW": potencia_hidraulica,
                        "potencia_eletrica_estimada_kW": potencia_eletrica_estimada,
                        "potencia_suficiente": potencia_suficiente,
                        "score_final": score_final,
                        
                        # Posição/classificação (será preenchida após ordenação)
                        "posicao_classificacao": 0
                    }
                    
                    resultados_finais.append(dados_bomba)
                    
                except Exception as e:
                    logger.error(f"Erro processando bomba {bomba.get('id_bomba', 'N/A')}: {e}")
                    continue

            # 6. Ordenar resultados
            if not resultados_finais:
                return []
                
            resultados_ordenados = sorted(resultados_finais, key=lambda x: x['score_final'], reverse=True)
            for i, bomba in enumerate(resultados_ordenados):
                bomba['posicao_classificacao'] = i + 1

            return resultados_ordenados

        except Exception as e:
            logger.error(f"Erro inesperado na seleção de bombas: {e}")
            return []

    def calcular_score_adequacao_simplificado(self, rendimento, fator_vazao, fator_altura, 
                                        potencia_suficiente, potencia_nominal, potencia_estimada):
        """
        Calcula um score de adequação simplificado para classificar as bombas.
        """
        PESO_RENDIMENTO = 0.30
        PESO_PROXIMIDADE = 0.40  # Proximidade aos valores nominais
        PESO_POTENCIA = 0.30
        fator_rendimento = rendimento
        
        # Proximidade ideal é quando ambos os fatores estão próximos de 1
        fator_proximidade = 1 - (abs(1 - fator_vazao) + abs(1 - fator_altura)) / 2
        
        # Fator de potência (penaliza se não for suficiente, recompensa se for eficiente)
        if not potencia_suficiente:
            fator_potencia = 0.1  
        else:
            # Quanto mais próxima a potência nominal da estimada (sem excesso), melhor
            excesso_potencia = (potencia_nominal - potencia_estimada) / potencia_estimada
            fator_potencia = 1.0 if excesso_potencia <= 0.3 else 1.0 - (excesso_potencia - 0.3) / 2

        score = (PESO_RENDIMENTO * fator_rendimento +
                PESO_PROXIMIDADE * fator_proximidade +
                PESO_POTENCIA * fator_potencia)
        
        return score
    
    def novo_projecto(self):
        """Reseta a aplicação para um novo projeto, limpando todos os dados"""
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
            self.inicializar_graficos_curvas()
            self.status_label.setText("Novo projeto iniciado")
            
            # ---------- Emitir sinal para atualizar a interface se necessário ----------
            self.atualizar_parametros_entrada()
            QMessageBox.information(self, "Novo Projeto", "Projeto reiniciado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar novo projeto: {str(e)}")
    
    
    # ==========================================================
    #                 CONFIGURAÇÕES
    # ==========================================================
    def salvar_configuracoes(self):
        """Salva estado da janela e widgets."""
        self.config.salvar_geometria_janela(self)
        self.config.salvar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.salvar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.salvar_texto_lineedit(self.Vazao_2, "vazao_valor")
        self.config.salvar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.salvar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.salvar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def restaurar_configuracoes(self):
        """Restaura estado salvo da janela e widgets."""
        self.config.restaurar_geometria_janela(self)
        self.config.restaurar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.restaurar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.restaurar_texto_lineedit(self.Vazao_2, "vazao_valor")
        self.config.restaurar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "vazao_unidade_indice")
        self.config.restaurar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.restaurar_texto_combobox(self.hazen_will, "hazen_material_texto")

    # ==========================================================
    #                 EVENTOS
    # ==========================================================
    def closeEvent(self, event):
        """Salva configurações antes de fechar a janela."""
        self.salvar_configuracoes()
        if hasattr(self, 'gestor_db'):
            self.gestor_db.fechar_conexao()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())