import sys
import os
import json
import img.img_rc

# ================== Qt Imports ==================
from PySide6.QtCore import (
    Qt, QUrl, QEvent, QSize, QPoint, QTimer, Signal, Slot, QSettings, QStringListModel,
    QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import (
    QIcon, QAction, QDoubleValidator, QSurfaceFormat
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMenu, QCompleter, QToolButton,
    QMessageBox, QFileDialog, QVBoxLayout, QSizePolicy
)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile

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
from src.web_channel import (
    Dados, Altura_Geometrica, Dimensao_Tubulacao, Acessorios_sistema
)

# ================== Importacoes Locais (Calculos) ==================
from calculos.perdas_cargas import Perdas
from calculos.curvas_bomba import Grafico
from calculos.unidades import ConversorUnidades
from calculos.dimensionamento_tubulação import Tubulacao

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

        # Remove layouts antigos antes de adicionar novos
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
                'Vazão': (f"{self.vazao:.4f}", 'm³/s'),
                'Tempo de funcionamento': (f"{self.tempo:.2f}", 'horas'),
                'Diâmetro da tubulação': (f"{self.diametro_tubulacao:.4f}", 'm'),
                'Altura geométrica': (f"{self.altura_geometrica_val:.2f}", 'm'),
                'Perdas totais': (f"{self.perdas_totais:.4f}", 'm'),
                'Altura manométrica': (f"{self.altura_manometrica:.2f}", 'm'),
                'Material da Tubulação': (material, None),
            }
            
            # Configurar e gerar PDF
            self.relatorio_pdf.adicionar_titulos("Relatório do Sistema de Bombeamento - AquaPump")
            self.relatorio_pdf.adicionar_secao("Dados do Sistema")
            self.relatorio_pdf.adicionar_conteudo(dados_relatorio)
            
            # Gerar PDF
            self.relatorio_pdf.gravar_pdf()
            
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
            
            # ---------- Reset dos gráficos ----------
            self.inicializar_graficos_curvas()
            
            # ---------- Atualizar status ----------
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