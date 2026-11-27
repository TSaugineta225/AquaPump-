import os
import re
import sys
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
    QMessageBox, QFileDialog, QVBoxLayout, QSizePolicy,
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QComboBox,
    QListWidget, QListWidgetItem, QAbstractItemView, QPushButton
)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

# ================== Bibliotecas Externas ==================
from qframelesswindow import FramelessMainWindow as FramelessWindow
from matplotlib import pyplot as plt
import numpy as np
import CoolProp.CoolProp as CP
from scipy.constants import g

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
from src.modelo_hidraulico import ModeloHidraulico, ErroModeloHidraulico

# Os modelos de bombas são importados de forma diferida na inicialização do
# módulo de associações, para que a aplicação base continue a abrir mesmo
# quando esses ficheiros ainda não foram instalados.

# ================== Logging Configuration ==================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== WebEngine Configurations ==================
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu-vsync --disable-frame-rate-limit")


# ==========================================================
#                       MAIN WINDOW
# ==========================================================
class MainWindow(FramelessWindow, Ui_AquaPump):
    """
    Classe principal da aplicação AquaPump para dimensionamento de sistemas de bombeamento.
    """
    bomba_encontrada = Signal(dict)
    def __init__(self, parent=None):
        """Inicializa a janela principal e todos os seus componentes."""
        super().__init__(parent)
        # Ui_AquaPump foi gerada para QWidget, não para QMainWindow.
        # O conteúdo deve ficar no centralWidget do FramelessWindow.
        self._ui_container = QWidget(self)
        self.setupUi(self._ui_container)
        self.setCentralWidget(self._ui_container)
        self.exportar_csv.setText("Exportar Excel")
        self._historico_path = None
        self.modelo_hidraulico_dados = None
        self.modelo_hidraulico_resultado = None
        self.modelo_hidraulico_erro = None
        self.modelo_hidraulico_perfil = None

        # ================== INICIALIZAÇÃO DE ATRIBUTOS ==================
        
        # ---------- Configurações da Janela ----------
        self.setWindowTitle("AquaPump")
        # O ícone é definido na QApplication para contornar o crash no QtFrameless.setWindowIcon.
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

        # Estado inicial neutro: não apresentar dados de uma bomba fictícia.
        self.modelo.setText("Nenhuma bomba seleccionada")
        self.vazao_label.setText("Caudal nominal: —")
        self.altura_3.setText("Altura manométrica nominal: —")
        self.potencia_3.setText("Potência nominal: —")
        self.label_10.clear()

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
        
        # ---------- Inicialização de Gráficos e Associações ----------
        self._inicializar_graficos()
        self._inicializar_gestor_bombas()
        # Os parâmetros só podem ser recalculados depois de os gráficos existirem.
        self.atualizar_parametros_entrada()
        self.mudanca_dinamica_perdas_carga()

        # ---------- Inicialização de pequenos sinais ------
        self.pequeno_sinal()
        
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
            self.gestor_db = None
            logger.warning(f"Erro ao carregar base de dados devido a {e}")

        # Os parâmetros iniciais são calculados no __init__, depois de
        # _inicializar_graficos(), para evitar chamadas prematuras aos gráficos.
        
    def pequeno_sinal(self):
        self.bomba_encontrada.connect(self.iniciar_consulta)

    def _configurar_validadores(self):
        """Configura validadores para campos de entrada numéricos."""
        validator = QDoubleValidator(0.0, 10000.0, 6)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.Vazao_2.setValidator(validator)
        self.Vazao.setValidator(validator)

    def _configurar_combobox(self):
        """Preenche listas vazias e evita duplicar opções já definidas no Designer."""
        unidades = {
            "icone_2": ["m³/h", "m³/s", "L/s", "L/min", "L/h", "gal/min", "ft³/s"],
            "caudal_box": ["m³/h", "m³/s", "L/s", "L/min", "L/h"],
            "diametro_box": ["m", "cm", "mm", "in", "ft"],
            "comprimento_box": ["m", "cm", "mm", "km", "ft", "in"],
            "altura_box": ["m", "cm", "mm", "ft"],
            "potencia_box": ["kilowatt", "watt", "megawatt", "horsepower", "cv"],
        }
        for nome, opcoes in unidades.items():
            combo = getattr(self, nome, None)
            if combo is not None and combo.count() == 0:
                combo.addItems(opcoes)
                combo.setCurrentIndex(0)

        if self.hazen_will.count() == 0:
            self.hazen_will.addItems(Perdas.get_lista_materiais_hazen())
        self.hazen_will.setHidden(True)
        if self.darcy.count() == 0:
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
        self.acessorios_channel.modelo.connect(self.receber_modelo_hidraulico)
        self.altura_geometrica_channel.altura_recebida.connect(self.receber_altura)
        self.comprimento_tubulacao_channel.comprimento_recebido.connect(self.receber_comprimento)
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
        # O menu original expõe apenas os três primeiros gráficos, apesar de
        # a UI já possuir seis páginas no stackedWidget_3.
        # A substituição é feita no objecto de menu, sem editar o código gerado.
        self.menu.menu_selecao_graficos = self._menu_selecao_graficos_completo

    def _inicializar_graficos(self):
        """Inicializa os quatro gráficos actuais e os dois de associação."""
        self.grafico_altura = Grafico()
        self.grafico_potencia = Grafico()
        self.grafico_rendimento = Grafico()
        self.grafico_npsh = Grafico()
        self.grafico_serie = Grafico()
        self.grafico_paralelo = Grafico()

        destinos = (
            (self.altura, self.grafico_altura),
            (self.potencia, self.grafico_potencia),
            (self.rendimento, self.grafico_rendimento),
            (self.npsh_2, self.grafico_npsh),
            (self.serie, self.grafico_serie),
            (self.paralelo, self.grafico_paralelo),
        )

        for container, grafico in destinos:
            layout = container.layout()
            if layout is None:
                layout = QVBoxLayout(container)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(grafico)

    def _inicializar_gestor_bombas(self):
        """Liga o motor de associação aos dois espaços de gráfico existentes.

        O gestor recebe ui=None de propósito: os cálculos principais e os
        resultados apresentados no painel continuam sob responsabilidade do
        MainWindow. Assim evitamos duplicar sinais e sobrescrever resultados.
        """
        try:
            from src.bomba import Bomba as BombaModel
            from src.gestor_bombas import GestorBombas as GestorBombasModel

            self._BombaModel = BombaModel
            self.gestor_bombas = GestorBombasModel(
                ui=None,
                parent=self,
                carregar_demo=False,
                construir_graficos=False,
                conectar_sinais=False,
            )
            self.gestor_bombas.graficos = {
                "serie": self.grafico_serie,
                "paralelo": self.grafico_paralelo,
            }
            self.acessorios_lista = []
            self._acessorios_gestor_sincronizados = None
            self._criar_controlos_gestor_bombas()
            self._sincronizar_gestor_bombas()
        except Exception as exc:
            self.gestor_bombas = None
            self._BombaModel = None
            logger.exception("Não foi possível inicializar o gestor de associações: %s", exc)
            QMessageBox.warning(
                self,
                "Associação de bombas",
                "O módulo de associação não foi iniciado. Verifique os módulos "
                "src/bomba.py, src/associacao_bombas.py e src/gestor_bombas.py.\n\n"
                f"Detalhe: {exc}",
            )

    def _criar_controlos_gestor_bombas(self):
        """Acrescenta controlos ao cabeçalho já existente, sem alterar Ui_main.py."""
        layout = getattr(self, "horizontalLayout_31", None)
        if layout is None:
            logger.warning("Não foi encontrado o cabeçalho dos gráficos para inserir os controlos.")
            return

        self.btn_adicionar_bomba = QPushButton("Adicionar bomba", self.janela_graficos)
        self.btn_adicionar_bomba.setToolTip(
            "Introduzir os pontos das curvas fornecidas pelo fabricante"
        )
        self.btn_associar_bombas = QPushButton("Associar bombas", self.janela_graficos)
        self.btn_associar_bombas.setToolTip(
            "Seleccionar duas ou mais bombas e criar uma associação em série ou paralelo"
        )
        self.btn_adicionar_bomba.clicked.connect(self._adicionar_bomba_ui)
        self.btn_associar_bombas.clicked.connect(self._criar_associacao_ui)

        # O layout tem: título, espaçador e botão de selecção de gráficos.
        # Inserimos os novos controlos antes do espaçador.
        layout.insertWidget(1, self.btn_adicionar_bomba)
        layout.insertWidget(2, self.btn_associar_bombas)

    def _menu_selecao_graficos_completo(self):
        """Menu para as seis páginas que já existem em Ui_main.py."""
        menu = QMenu(self)
        paginas = (
            ("Curva H vs Q (Altura vs Vazão)", 0),
            ("Curva de Potência vs Vazão", 1),
            ("Curva de Rendimento vs Vazão", 2),
            ("NPSH requerido vs Vazão", 3),
            ("Associação em Série", 4),
            ("Associação em Paralelo", 5),
        )
        for titulo, indice in paginas:
            acao = QAction(titulo, self)
            acao.triggered.connect(
                lambda checked=False, i=indice, t=titulo: self._selecionar_pagina_grafico(i, t)
            )
            menu.addAction(acao)
        return menu

    def _selecionar_pagina_grafico(self, indice: int, titulo: str):
        self.label_2.setText(titulo)
        self.stackedWidget_3.setCurrentIndex(indice)

    @staticmethod
    def _ler_lista_numerica(texto: str, nome: str, obrigatoria: bool = True):
        """Lê números separados por ponto e vírgula ou espaços; aceita vírgula decimal."""
        texto = str(texto or "").strip()
        if not texto:
            if obrigatoria:
                raise ValueError(f"Preencha a lista de {nome}.")
            return None
        partes = [p for p in re.split(r"[;\s]+", texto) if p]
        try:
            valores = [float(p.replace(",", ".")) for p in partes]
        except ValueError as exc:
            raise ValueError(
                f"A lista de {nome} contém um valor não numérico. "
                "Use ponto e vírgula ou espaços para separar os valores."
            ) from exc
        if len(valores) < 2:
            raise ValueError(f"A lista de {nome} deve conter pelo menos dois pontos.")
        if not np.all(np.isfinite(valores)):
            raise ValueError(f"A lista de {nome} contém valores inválidos.")
        return np.asarray(valores, dtype=float)

    def _adicionar_bomba_ui(self):
        """Regista uma bomba a partir dos pontos das curvas do fabricante."""
        if self.gestor_bombas is None:
            QMessageBox.warning(self, "Associação", "O gestor de bombas não está disponível.")
            return

        dialogo = QDialog(self)
        dialogo.setWindowTitle("Adicionar curva de uma bomba")
        dialogo.setMinimumWidth(430)
        raiz = QVBoxLayout(dialogo)
        formulario = QFormLayout()

        campos = {
            "nome": QLineEdit(),
            "rpm": QLineEdit("3500"),
            "q": QLineEdit(),
            "h": QLineEdit(),
            "eta": QLineEdit(),
            "npsh": QLineEdit(),
        }
        campos["q"].setPlaceholderText("0; 5; 10; 15; 20  (m³/h)")
        campos["h"].setPlaceholderText("40; 38; 34; 27; 15  (m)")
        campos["eta"].setPlaceholderText("0; 35; 55; 68; 45  (%) — opcional")
        campos["npsh"].setPlaceholderText("1,5; 1,8; 2,4; 3,5; 5  (m) — opcional")
        campos["nome"].setPlaceholderText("Fabricante / modelo")

        formulario.addRow("Nome / modelo:", campos["nome"])
        formulario.addRow("Rotação (rpm):", campos["rpm"])
        formulario.addRow("Caudais (m³/h):", campos["q"])
        formulario.addRow("Alturas (m):", campos["h"])
        formulario.addRow("Rendimento (%):", campos["eta"])
        formulario.addRow("NPSH requerido (m):", campos["npsh"])
        raiz.addLayout(formulario)
        nota = QLabel(
            "Introduza os pontos na mesma ordem. Use ponto e vírgula ou espaços "
            "como separador. A vazão é convertida internamente para m³/s."
        )
        nota.setWordWrap(True)
        raiz.addWidget(nota)
        botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botoes.accepted.connect(dialogo.accept)
        botoes.rejected.connect(dialogo.reject)
        raiz.addWidget(botoes)

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            nome = campos["nome"].text().strip()
            if not nome:
                raise ValueError("Indique o nome ou modelo da bomba.")
            texto_rpm = campos["rpm"].text().strip()
            rpm = float(texto_rpm.replace(",", ".")) if texto_rpm else None
            caudais = self._ler_lista_numerica(campos["q"].text(), "caudais")
            alturas = self._ler_lista_numerica(campos["h"].text(), "alturas")
            rendimentos = self._ler_lista_numerica(
                campos["eta"].text(), "rendimentos", obrigatoria=False
            )
            npsh = self._ler_lista_numerica(
                campos["npsh"].text(), "NPSH", obrigatoria=False
            )

            bomba = self._BombaModel(nome=nome, rpm=rpm)
            bomba.definir_dados(
                Q=caudais / 3600.0,
                H=alturas,
                eta=rendimentos,
                npsh_r=npsh,
            )
            self.gestor_bombas.adicionar_bomba(bomba)
            QMessageBox.information(
                self, "Bomba adicionada", f"A curva de '{nome}' foi adicionada ao projecto."
            )
        except Exception as exc:
            QMessageBox.warning(self, "Dados da bomba inválidos", str(exc))

    def _criar_associacao_ui(self):
        """Cria uma associação simples a partir das bombas já introduzidas."""
        if self.gestor_bombas is None:
            QMessageBox.warning(self, "Associação", "O gestor de bombas não está disponível.")
            return
        if len(self.gestor_bombas.bombas) < 2:
            QMessageBox.information(
                self,
                "Associar bombas",
                "Introduza pelo menos duas bombas com as respectivas curvas antes de criar uma associação.",
            )
            return

        dialogo = QDialog(self)
        dialogo.setWindowTitle("Criar associação de bombas")
        dialogo.setMinimumWidth(380)
        raiz = QVBoxLayout(dialogo)
        formulario = QFormLayout()
        nome = QLineEdit("Associação personalizada")
        tipo = QComboBox()
        tipo.addItem("Série", "serie")
        tipo.addItem("Paralelo", "paralelo")
        formulario.addRow("Nome:", nome)
        formulario.addRow("Tipo:", tipo)
        raiz.addLayout(formulario)

        lista = QListWidget()
        lista.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        for indice, bomba in enumerate(self.gestor_bombas.bombas):
            item = QListWidgetItem(f"{indice + 1}. {bomba.nome}")
            item.setData(Qt.ItemDataRole.UserRole, indice)
            lista.addItem(item)
        raiz.addWidget(QLabel("Seleccione duas ou mais bombas:"))
        raiz.addWidget(lista)

        botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botoes.accepted.connect(dialogo.accept)
        botoes.rejected.connect(dialogo.reject)
        raiz.addWidget(botoes)

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            indices = [item.data(Qt.ItemDataRole.UserRole) for item in lista.selectedItems()]
            if len(indices) < 2:
                raise ValueError("Seleccione pelo menos duas bombas.")
            nome_associacao = nome.text().strip()
            if not nome_associacao:
                raise ValueError("Indique um nome para a associação.")
            tipo_associacao = tipo.currentData()
            self.gestor_bombas.criar_associacao(
                nome_associacao, tipo_associacao, indices
            )
            pagina = 4 if tipo_associacao == "serie" else 5
            titulo = "Associação em Série" if pagina == 4 else "Associação em Paralelo"
            self._selecionar_pagina_grafico(pagina, titulo)
            QMessageBox.information(
                self, "Associação criada", f"'{nome_associacao}' foi criada com sucesso."
            )
        except Exception as exc:
            QMessageBox.warning(self, "Não foi possível associar", str(exc))

    def _sincronizar_gestor_bombas(self):
        """Mantém a curva do sistema das associações alinhada com o dimensionamento.

        Não escreve nos labels da janela nem executa o cálculo principal; apenas
        actualiza os parâmetros usados pela curva do sistema nos gráficos de série
        e paralelo.
        """
        gestor = getattr(self, "gestor_bombas", None)
        if gestor is None:
            return
        # O gestor de curvas de bombas usa actualmente um único diâmetro e
        # comprimento equivalentes. Não o alimentar com uma rede de vários
        # troços evita apresentar uma curva do sistema tecnicamente enganadora.
        modelo = getattr(self, "modelo_hidraulico_dados", None)
        if isinstance(modelo, dict) and modelo.get("pipes"):
            logger.info(
                "Curva do sistema do gestor de bombas não sincronizada: "
                "falta ainda adaptar o solver de bombas ao modelo multi-troço."
            )
            return
        try:
            parametros = {}
            altura = max(0.0, float(self.altura_geometrica_val))
            comprimento = max(0.0, float(self.comprimento_tubulacao_val))
            if not np.isclose(gestor.H_geometrico, altura):
                parametros["H_geometrico"] = altura
            if not np.isclose(gestor.comprimento_m, comprimento):
                parametros["comprimento_m"] = comprimento

            diametro = float(self.diametro_tubulacao)
            if np.isfinite(diametro) and diametro > 0 and not np.isclose(
                gestor.perdas.diametro_m, diametro
            ):
                parametros["diametro_m"] = diametro

            material_darcy = self.darcy.currentText().strip()
            material_hazen = self.hazen_will.currentText().strip()
            if material_darcy and gestor.material_darcy != material_darcy:
                parametros["material"] = material_darcy
            if material_hazen and gestor.material_hazen != material_hazen:
                parametros["material_hazen"] = material_hazen

            metodo = "darcy" if self.radioButton_10.isChecked() else "hazen"
            if gestor.metodo_perdas != metodo:
                parametros["metodo_perdas"] = metodo

            tempo = float(self.tempo)
            if np.isfinite(tempo) and 0 < tempo <= 24 and not np.isclose(
                gestor.tempo_funcionamento_h, tempo
            ):
                parametros["tempo_funcionamento_h"] = tempo

            acessorios = list(getattr(self, "acessorios_lista", []))
            if self._acessorios_gestor_sincronizados != acessorios:
                parametros["acessorios"] = acessorios
                self._acessorios_gestor_sincronizados = list(acessorios)

            if parametros:
                gestor.configurar_sistema(**parametros)
        except Exception as exc:
            logger.warning("Não foi possível sincronizar a curva do sistema das associações: %s", exc)

    # ================== MÉTODOS DE CARREGAMENTO DE ARQUIVOS ==================

    def caminho_dados(self, caminho_relactivo):
        """
        Garante que os arquivos sejam carregados tanto nos testes de Python como no .exe.
        
        Args:
            caminho_relactivo: Caminho relativo do arquivo
            
        Returns:
            str: Caminho absoluto do arquivo
        """
        if hasattr(sys, "_MEIPASS"):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, caminho_relactivo)

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
        """Instancia a classe de Perdas com os parâmetros atuais de forma segura."""
        vazao_m3s = max(self.vazao, 1e-9)  # Garantir vazão mínima
        diametro_seguro = max(self.diametro_tubulacao, 0.001)  # Diâmetro mínimo de 1mm
        area_segura = max(self._diametro.area_seccao(), 1e-6)  # Área mínima
        
        try:
            self.perdas = Perdas(
                vazao_m3s,
                diametro_seguro,
                area_segura,
                self.darcy.currentText(),
                self.hazen_will.currentText()
            )
        except Exception as e:
            logger.error(f"Erro ao instanciar classe Perdas: {e}")
            # Fallback: criar instância com valores padrão seguros
            self.perdas = Perdas(0.001, 0.1, 0.007854, self.darcy.currentText(), self.hazen_will.currentText())

        # A classe Perdas é recriada quando caudal/tempo mudam. Reaplicar a
        # lista do editor evita perder acessórios e os K/DN definidos pelo utilizador.
        acessorios_guardados = getattr(self, "acessorios_lista", None)
        if acessorios_guardados is not None:
            try:
                self.perdas.definir_acessorios_lista(acessorios_guardados)
                self.localizadas = self.perdas.calcular_perdas_localizadas()
            except (TypeError, ValueError, AttributeError) as erro:
                logger.warning("Não foi possível restaurar acessórios após actualizar parâmetros: %s", erro)
                self.localizadas = 0.0

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

    def _enviar_perfil_hidraulico_js(self, resultado):
        """Gera HGL/EGL com condições de fronteira explícitas e envia ao SVG."""
        modelo = getattr(self, "modelo_hidraulico_dados", None)
        if not isinstance(modelo, dict) or not isinstance(resultado, dict):
            return

        # A cota piezométrica inicial é uma condição de fronteira; nunca é
        # inferida da altura geométrica ou da perda total.
        cota_inicial = modelo.get("cota_piezometrica_inicial_m")
        if cota_inicial is None:
            cota_inicial = getattr(self, "cota_piezometrica_inicial_m", None)
        if cota_inicial is None:
            self.page.runJavaScript("window.limpar_perfil_hidraulico && window.limpar_perfil_hidraulico();")
            return

        try:
            perfil = ModeloHidraulico.gerar_perfil_longitudinal(
                modelo=modelo,
                resultado=resultado,
                cota_piezometrica_inicial_m=float(cota_inicial),
            )
            payload = json.dumps(perfil, ensure_ascii=False, allow_nan=False)
            self.page.runJavaScript(
                "window.receber_perfil_hidraulico && window.receber_perfil_hidraulico(" + payload + ");"
            )
            self.modelo_hidraulico_perfil = perfil
        except (ErroModeloHidraulico, TypeError, ValueError, KeyError) as exc:
            self.modelo_hidraulico_perfil = None
            logger.info("Perfil hidráulico ainda não disponível: %s", exc)
            self.page.runJavaScript("window.limpar_perfil_hidraulico && window.limpar_perfil_hidraulico();")

    def _calcular_perdas_esquema_hidraulico(self):
        """Calcula a linha principal por troços com DN e material próprios.

        Devolve None quando o editor ainda não enviou troços, para manter o
        fluxo legado (mapa + parâmetros globais) sem alterações.
        """
        modelo = getattr(self, "modelo_hidraulico_dados", None)
        if not isinstance(modelo, dict) or not modelo.get("pipes"):
            return None

        metodo = "darcy" if self.radioButton_10.isChecked() else "hazen"
        resultado = ModeloHidraulico.calcular(
            modelo=modelo,
            vazao_m3s=self.vazao,
            metodo=metodo,
            material_darcy_padrao=self.darcy.currentText(),
            material_hazen_padrao=self.hazen_will.currentText(),
        )
        self.modelo_hidraulico_resultado = resultado
        self.modelo_hidraulico_erro = None
        self._enviar_perfil_hidraulico_js(resultado)
        return resultado

    @Slot()
    def recalcular_sistema_completo(self):
        """Recalcula o sistema; usa o modelo por troços quando existe esquema."""
        modelo_ativo = bool(
            isinstance(getattr(self, "modelo_hidraulico_dados", None), dict)
            and self.modelo_hidraulico_dados.get("pipes")
        )

        if self.vazao <= 1e-9 or (not modelo_ativo and self.diametro_tubulacao <= 1e-6):
            self.perdas_totais = 0.0
            self.localizadas = 0.0
            self.altura_manometrica = self.altura_geometrica_val
            self.potencia_requerida = 0.0
            self.perdas_resul.setText(f"0.000 {self.comprimento_box.currentText()}")
            self.label_18.setText(f"{self.altura_geometrica_val:.3f} {self.comprimento_box.currentText()}")
            self.label_19.setText(f"0.000 {self.potencia_box.currentText()}")
            try:
                self.atualizar_graficos_curvas()
            except Exception as exc:
                logger.warning("Erro ao actualizar gráficos com valores mínimos: %s", exc)
            self._sincronizar_gestor_bombas()
            return

        if not hasattr(self, "perdas") or (not modelo_ativo and self.diametro_tubulacao <= 1e-6):
            logger.warning("Parâmetros insuficientes para cálculo de perdas")
            self._sincronizar_gestor_bombas()
            return

        try:
            if modelo_ativo:
                resultado = self._calcular_perdas_esquema_hidraulico()
                perda_distribuida = resultado["perdas_distribuidas_m"]
                self.localizadas = resultado["perdas_localizadas_m"]
                self.comprimento_tubulacao_val = resultado["comprimento_total_m"]
                linhas_tooltip = ["Perdas por troço:"]
                for troco in resultado.get("trocos", []):
                    linhas_tooltip.append(
                        f"{troco['id']}: distribuída {troco['perda_distribuida_m']:.3f} m; "
                        f"localizada {troco['perda_localizada_m']:.3f} m; "
                        f"total {troco['perda_total_m']:.3f} m"
                    )
                linhas_tooltip.append(resultado.get("nota", ""))
                self.perdas_resul.setToolTip("\n".join(linhas_tooltip))
                for aviso in resultado.get("avisos", []):
                    logger.warning("Modelo hidráulico: %s", aviso)
            else:
                self.perdas_resul.setToolTip("")
                perda_distribuida = 0.0
                if self.comprimento_tubulacao_val > 1e-6:
                    if self.radioButton_10.isChecked():
                        self.perdas.definir_material_darcy(self.darcy.currentText())
                        perda_distribuida = self.perdas.calcular_perda_carga_darcy(
                            self.comprimento_tubulacao_val
                        )
                    elif self.radioButton_9.isChecked():
                        self.perdas.definir_material_hazen(self.hazen_will.currentText())
                        perda_distribuida = self.perdas.calcular_perda_carga_hazen_williams(
                            self.comprimento_tubulacao_val
                        )
                # Mantém o cálculo localizado do fluxo anterior.
                self.localizadas = self.perdas.calcular_perdas_localizadas()

            self.perdas_totais = max(0.0, perda_distribuida + self.localizadas)
            self.calcular_potencia()
            self.perdas_resul.setText(
                f"{self.perdas_totais:.3f} {self.comprimento_box.currentText()}"
            )
            logger.info("Perdas totais calculadas: %.6f m", self.perdas_totais)
            self.calcular_altura_manometrica()
            self.atualizar_graficos_curvas()

        except (ErroModeloHidraulico, ValueError, TypeError, AttributeError, ZeroDivisionError) as exc:
            self.modelo_hidraulico_erro = str(exc)
            self.modelo_hidraulico_resultado = None
            logger.error("Modelo hidráulico não calculado: %s", exc)
            # Não publicar um resultado hidráulico fictício. O utilizador vê
            # explicitamente que o esquema precisa de correcção.
            self.perdas_totais = 0.0
            self.localizadas = 0.0
            self.altura_manometrica = 0.0
            self.potencia_requerida = 0.0
            self.perdas_resul.setText("Verificar esquema")
            self.perdas_resul.setToolTip(f"Modelo hidráulico inválido: {exc}")
            self.label_18.setText("Modelo inválido")
            self.label_19.setText("—")
            return
        except Exception as exc:
            logger.error("Erro no cálculo do sistema hidráulico: %s", exc, exc_info=True)
            self.perdas_totais = 0.0
            self.altura_manometrica = self.altura_geometrica_val
            return

        self._sincronizar_gestor_bombas()

    # ================== MÉTODOS DE COMUNICAÇÃO COM JAVASCRIPT ==================

    @Slot('QVariant')
    def receber_modelo_hidraulico(self, modelo):
        """Recebe o esquema completo do editor SVG via QWebChannel."""
        if not isinstance(modelo, dict):
            logger.warning("O editor enviou um modelo hidráulico num formato inválido.")
            return
        pipes = modelo.get("pipes", [])
        components = modelo.get("components", [])
        if not isinstance(pipes, list) or not isinstance(components, list):
            logger.warning("O modelo hidráulico contém listas inválidas.")
            return
        self.modelo_hidraulico_dados = modelo
        self.acessorios_lista = list(components)
        if hasattr(self, "perdas"):
            try:
                self.perdas.definir_acessorios_lista(self.acessorios_lista)
            except Exception as exc:
                logger.warning("Não foi possível sincronizar acessórios no cálculo legado: %s", exc)
        self.recalcular_sistema_completo()

    @Slot(list)
    def definir_acessorios(self, lista):
        """Recebe a lista de acessórios do JS e recalcula o sistema."""
        if not hasattr(self, 'perdas'):
            return
        self.acessorios_lista = list(lista or [])
        self.perdas.definir_acessorios_lista(self.acessorios_lista)
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
        Atualiza TODOS os gráficos de SIMULAÇÃO com proteção contra erros numéricos.
        """
        # Pode ser chamado por um recálculo durante a inicialização. Nesse
        # momento, ignoramos a atualização até que os gráficos sejam criados.
        if not hasattr(self, "grafico_altura"):
            logger.debug("Gráficos ainda não inicializados; atualização adiada.")
            return
        try:
            # ==============================
            # 1. PARÂMETROS DE ENTRADA SEGUROS
            # ==============================
            vazao_sistema_m3s = max(self.vazao, 1e-6) if hasattr(self, 'vazao') else 0.001
            altura_manometrica_m = max(self.altura_manometrica, 0.1) if hasattr(self, 'altura_manometrica') else 1.0
            altura_geometrica_m = max(self.altura_geometrica_val, 0.0) if hasattr(self, 'altura_geometrica_val') else 0.0

            # Limitar valores extremos que podem causar instabilidade
            vazao_sistema_m3s = min(vazao_sistema_m3s, 100.0)  # Limite máximo de 100 m³/s
            altura_manometrica_m = min(altura_manometrica_m, 500.0)  # Limite máximo de 500 m

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
                tipo_gráfico="Altura",
                curvas=[
                    {"label": "Curva Bomba (Simulada)", "x": q_plot_exibir, "y": H_bomba_exibir},
                ],
                curva_sistema={
                    "label": "Curva Sistema", "x": q_plot_exibir, "y": H_sistema_exibir,
                },
                ponto_operacao={"x": q_op_exibir, "y": h_op_exibir},
                unidade_vazao=u_q, unidade_y=u_h, y_scale=1.0,
                titulo="Altura vs. Vazão",
            )

            self.grafico_potencia.plotar_dados(
                tipo_gráfico="Potência",
                curvas=[
                    {"label": "Potência Consumida", "x": q_plot_exibir, "y": potencia_exibir, "cor": "#2ca02c"},
                ],
                ponto_operacao={"x": q_op_exibir, "y": p_op_exibir},
                unidade_vazao=u_q, unidade_y=u_p, y_scale=1.0,
                titulo="Potência vs. Vazão",
            )

            self.grafico_rendimento.plotar_dados(
                tipo_gráfico="Rendimento",
                curvas=[
                    {"label": "Rendimento", "x": q_plot_exibir, "y": rendimento_exibir, "cor": "#d62728"},
                ],
                ponto_operacao={"x": q_op_exibir, "y": eta_op_exibir},
                unidade_vazao=u_q, unidade_y="%", y_scale=1.0,
                titulo="Rendimento vs. Vazão",
            )

            # Plotagem do NPSH
            self.grafico_npsh.plotar_dados(
                tipo_gráfico="NPSH",
                curvas=[
                    {"label": "NPSH Requerido (Simulado)", "x": q_plot_exibir, "y": npsh_exibir, "cor": "#9467bd"},
                ],
                ponto_operacao={"x": q_op_exibir, "y": npsh_op_exibir},
                unidade_vazao=u_q, unidade_y=u_h, y_scale=1.0,
                titulo="NPSH Requerido vs. Vazão",
            )

        except Exception as e:
            logger.error(f"Erro crítico ao atualizar gráficos: {e}", exc_info=True)
            # Fallback: gráficos vazios em caso de erro
            self._limpar_graficos_emergencia()

    def _limpar_graficos_emergencia(self):
        """Limpa todos os gráficos em caso de erro crítico."""
        try:
            for grafico in [self.grafico_altura, self.grafico_potencia, self.grafico_rendimento, self.grafico_npsh]:
                grafico.ax.clear()
                grafico.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
                grafico.ax.set_title("Gráfico temporariamente indisponível")
                grafico.canvas.draw()
        except Exception as e:
            logger.error(f"Erro ao limpar gráficos de emergência: {e}")

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
        texto = self.pesquisa_line.text().strip()
        # JSON encoding prevents quotes or special characters breaking JavaScript.
        argumento = json.dumps(texto, ensure_ascii=False)
        pesquisa = f"pesquisar_lugar({argumento})"
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
            sucesso = csv_exporter.exportar(parent=self)
            if sucesso:
                QMessageBox.information(self, "Sucesso", "Relatório Excel (.xlsx) gerado com sucesso!")
            else:
                QMessageBox.warning(self, "Aviso", "A exportação para Excel foi cancelada ou falhou.")
                
            return sucesso
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o relatório Excel: {str(e)}")
            return False
        
    # ================== MÉTODOS DE HISTÓRICO ==================

    def salvar_historico(self, caminho=None, como=False):
        """Guarda o estado actual em JSON; reutiliza o último caminho quando possível."""
        destino = None if como else (caminho or self._historico_path)
        dados_calculo = {
            # A vazão guardada é sempre SI. A unidade visual é guardada separadamente.
            "Vazao_total": float(self.vazao),
            "Vazao_total_m3s": float(self.vazao),
            "Unidade_vazao": self.icone_2.currentText(),
            "Diametro": float(self.diametro_tubulacao),
            "Perdas_de_Carga": float(self.perdas_totais),
            "Altura_Manometrica": float(self.altura_manometrica),
            "Altura_Geometrica": float(self.altura_geometrica_val),
            "Comprimento_Tubulacao": float(self.comprimento_tubulacao_val),
            "Tempo": float(self.tempo),
            "Material_Tubulacao": self.darcy.currentText() if self.radioButton_10.isChecked() else self.hazen_will.currentText(),
            "Formula_Utilizada": "Darcy-Weisbach" if self.radioButton_10.isChecked() else "Hazen-Williams",
        }
        if self.historico_manager.salvar_historico(dados_calculo, caminho=destino):
            # HistoricoManager devolve True por compatibilidade; o destino é mantido
            # pelo atributo quando foi escolhido pelo diálogo.
            caminho_final = getattr(self.historico_manager, "ultimo_caminho", None)
            if caminho_final:
                self._historico_path = caminho_final
                self.config.adicionar_projeto_recente(caminho_final)
                self.menu.atualizar_menu_recentes()
            QMessageBox.information(self, "Sucesso", "Projecto guardado com sucesso!")
            return True
        return False

    def carregar_historico(self, caminho=None):
        """Carrega um JSON e converte a vazão SI para a unidade actualmente escolhida."""
        dados = self.historico_manager.carregar_historico(caminho=caminho)
        if not isinstance(dados, dict):
            return False

        controlos = (
            self.Vazao_2, self.Vazao, self.icone_2,
            self.radioButton_10, self.radioButton_9, self.darcy, self.hazen_will,
        )
        estados_sinais = [(widget, widget.blockSignals(True)) for widget in controlos]
        try:
            unidade = str(dados.get("Unidade_vazao", self.icone_2.currentText()))
            indice = self.icone_2.findText(unidade)
            if indice >= 0:
                self.icone_2.setCurrentIndex(indice)

            vazao_si = float(dados.get("Vazao_total_m3s", dados.get("Vazao_total", 0.0)))
            vazao_display = self.conversor.converter_vazao(
                vazao_si, "m³/s", self.icone_2.currentText()
            )
            tempo = float(dados.get("Tempo", 0.0))
            self.Vazao_2.setText(f"{vazao_display:.8g}")
            self.Vazao.setText(f"{tempo:.8g}")

            formula = dados.get("Formula_Utilizada", "Darcy-Weisbach")
            material = dados.get("Material_Tubulacao", "")
            if formula == "Darcy-Weisbach":
                self.radioButton_10.setChecked(True)
                indice_material = self.darcy.findText(material)
                if indice_material >= 0:
                    self.darcy.setCurrentIndex(indice_material)
            else:
                self.radioButton_9.setChecked(True)
                indice_material = self.hazen_will.findText(material)
                if indice_material >= 0:
                    self.hazen_will.setCurrentIndex(indice_material)

            self.altura_geometrica_val = float(
                dados.get("Altura_Geometrica", self.altura_geometrica_val)
            )
            self.comprimento_tubulacao_val = float(
                dados.get("Comprimento_Tubulacao", self.comprimento_tubulacao_val)
            )
            self._historico_path = (
                getattr(self.historico_manager, "ultimo_caminho", None) or caminho
            )
        except (TypeError, ValueError, KeyError) as exc:
            logger.exception("Histórico inválido: %s", exc)
            QMessageBox.warning(
                self, "Histórico inválido",
                f"Não foi possível carregar o projecto: {exc}",
            )
            return False
        finally:
            for widget, estado_anterior in estados_sinais:
                widget.blockSignals(estado_anterior)

        if self._historico_path:
            self.config.adicionar_projeto_recente(self._historico_path)
            self.menu.atualizar_menu_recentes()

        self.atualizar_parametros_entrada()
        QMessageBox.information(self, "Sucesso", "Projecto carregado com sucesso!")
        return True

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
            self.bomba_encontrada.emit(bomba)

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

        # Variaveis para posterior uso
        self.modelo_bomba = bomba["modelo"]
        self.fabricante_bomba = bomba["fabricante"]

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
    
    # ================== MÉTODOS DE PESQUISA DE OBSERVAÇÕES ====
    def formatar_texto(self, text):
         text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
         return text
    
    def iniciar_consulta(self):
        self.thread = Observacoes(self.modelo_bomba, self.fabricante_bomba)
        self.thread.resultado.connect(self.mostrar_resultado)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()
        self.textEdit.setText("Consultando...")
    
    def on_finished(self):
        self.thread.deleteLater()
        self.thread = None

    def mostrar_resultado(self, conteudo):
        if not conteudo:
            self.textEdit.setText("**Consultando ...**")
            return
        
        self.textEdit.setHtml(self.formatar_texto(conteudo))

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
            self._historico_path = None
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
            self.acessorios_lista = []
            
            # ---------- Reset das seleções ----------
            self.icone_2.setCurrentIndex(0)  # Primeira unidade de vazão
            self.darcy.setCurrentIndex(0)    # Primeiro material Darcy
            self.hazen_will.setCurrentIndex(0)  # Primeiro material Hazen
            self.radioButton_10.setChecked(True)  # Darcy selecionado por padrão
            
            # ---------- Reset do mapa (via JavaScript) ----------
            self.view.page().runJavaScript("limpar_mapa();")
            if getattr(self, "gestor_bombas", None) is not None:
                self.gestor_bombas.limpar_bombas()
                self._acessorios_gestor_sincronizados = None

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
        self.config.salvar_indice_combobox(self.caudal_box, "caudal_unidade_indice")
        self.config.salvar_texto_combobox(self.darcy, "darcy_material_texto")
        self.config.salvar_texto_combobox(self.hazen_will, "hazen_material_texto")

    def restaurar_configuracoes(self):
        """Restaura estado salvo da janela e widgets."""
        self.config.restaurar_geometria_janela(self)
        self.config.restaurar_estado_splitter(self.splitter_2, "splitter_principal")
        self.config.restaurar_estado_splitter(self.splitter, "splitter_mapa_perfil")
        self.config.restaurar_indice_combobox(self.icone_2, "vazao_unidade_indice")
        self.config.restaurar_indice_combobox(self.caudal_box, "caudal_unidade_indice")
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
    app.setWindowIcon(QIcon(u":/img/logo_principal.png"))
    window = MainWindow()
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    sys.exit(app.exec())