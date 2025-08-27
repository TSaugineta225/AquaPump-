import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolBar, 
                               QPushButton, QLabel, QSizePolicy)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QAction

class NavigationToolbar(QToolBar):
    def __init__(self, chart_view, parent=None):
        super().__init__(parent)
        self.chart_view = chart_view
        self.setMovable(False)
        self.setFloatable(False)
        
        # Botões de navegação
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.addAction(self.zoom_in_action)
        
        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.addAction(self.zoom_out_action)
        
        self.pan_left_action = QAction("Pan Left", self)
        self.pan_left_action.triggered.connect(self.pan_left)
        self.addAction(self.pan_left_action)
        
        self.pan_right_action = QAction("Pan Right", self)
        self.pan_right_action.triggered.connect(self.pan_right)
        self.addAction(self.pan_right_action)
        
        self.reset_action = QAction("Reset View", self)
        self.reset_action.triggered.connect(self.reset_view)
        self.addAction(self.reset_action)
        
        # Adicionar um espaçador
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)
        
        # Label para mostrar informações do ponto de operação
        self.ponto_op_label = QLabel("Ponto de operação: ")
        self.addWidget(self.ponto_op_label)
    
    def zoom_in(self):
        self.chart_view.chart().zoomIn()
    
    def zoom_out(self):
        self.chart_view.chart().zoomOut()
    
    def pan_left(self):
        chart = self.chart_view.chart()
        axis_x = chart.axisX()[0]
        current_min = axis_x.min()
        current_max = axis_x.max()
        range_val = current_max - current_min
        axis_x.setRange(current_min - range_val * 0.1, current_max - range_val * 0.1)
    
    def pan_right(self):
        chart = self.chart_view.chart()
        axis_x = chart.axisX()[0]
        current_min = axis_x.min()
        current_max = axis_x.max()
        range_val = current_max - current_min
        axis_x.setRange(current_min + range_val * 0.1, current_max + range_val * 0.1)
    
    def reset_view(self):
        self.chart_view.chart().zoomReset()
    
    def atualizar_ponto_operacao(self, x, y, tipo_grafico, unidade_x, unidade_y):
        """Atualiza o label com as informações do ponto de operação"""
        if tipo_grafico == "altura":
            texto = f"Ponto de operação: Q = {x:.2f} {unidade_x}, H = {y:.2f} {unidade_y}"
        elif tipo_grafico == "potencia":
            texto = f"Ponto de operação: Q = {x:.2f} {unidade_x}, P = {y:.2f} {unidade_y}"
        else:  # rendimento
            texto = f"Ponto de operação: Q = {x:.2f} {unidade_x}, η = {y:.2f}%"
        
        self.ponto_op_label.setText(texto)


class Grafico(QWidget):
    def __init__(self, tipo='altura', potencia='Kw', altura='m', v='vazao', 
                 perdas=0.003, vazao_nominal=4, altura_nominal=4, parent=None):
        super().__init__(parent)

        self.tipo = tipo.lower()
        self.potencia = potencia
        self.altura = altura
        self.vazao = v
        self.Q_nominal = vazao_nominal
        self.H_nominal = altura_nominal
        self.H_geometrico = altura_nominal
        self.perda_carga = perdas

        self.H_0 = self.H_nominal * 1.2
        self.A = (self.H_0 - self.H_nominal) / (self.Q_nominal ** 2) if self.Q_nominal > 0 else 0

        # Configurar o layout e gráfico
        layout_principal = QVBoxLayout()
        
        # Criar chart e chart view
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeLight)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Criar eixos (serão configurados no plotar)
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        
        # Barra de navegação personalizada
        self.toolbar = NavigationToolbar(self.chart_view)
        
        layout_principal.addWidget(self.toolbar)
        layout_principal.addWidget(self.chart_view)
        self.setLayout(layout_principal)

        self.gerar_dados()
        self.plotar()

    def gerar_dados(self):
        q_max = self.Q_nominal * 1.5
        self.Q_plot = np.linspace(0.1, q_max, 200)

        self.H_plot = self.H_0 - self.A * self.Q_plot ** 2
        self.H_plot[self.H_plot < 0] = 0

        self.C_plot = self.H_geometrico + self.perda_carga * self.Q_plot ** 2

        self.eta_plot = self.calcular_rendimento()
        self.P_plot = self.calcular_potencia()

        self.Q_op, self.H_op = self.encontrar_ponto_operacao()

    def calcular_rendimento(self):
        eta_max = 0.75
        k = 0.01
        return eta_max - k * (self.Q_plot - self.Q_nominal) ** 2

    def calcular_potencia(self, g=9.81):
        rho = 1000
        Q_m3s = self.Q_plot 
        eta_seguro = np.where(self.eta_plot > 0, self.eta_plot, np.nan)
        P = (rho * g * Q_m3s * self.H_plot) / eta_seguro
        return P / 1000

    def encontrar_ponto_operacao(self):
        diferenca = np.abs(self.H_plot - self.C_plot)
        indice_otimo = np.argmin(diferenca)
        return self.Q_plot[indice_otimo], self.H_plot[indice_otimo]

    def criar_serie(self, x_data, y_data, nome, cor, espessura=2.2):
        """Cria uma série de linha com os dados fornecidos"""
        serie = QLineSeries()
        serie.setName(nome)
        
        # Adicionar pontos à série
        for x, y in zip(x_data, y_data):
            if not np.isnan(y):  # Ignorar valores NaN
                serie.append(float(x), float(y))
        
        # Configurar estilo da linha
        pen = QPen(QColor(cor))
        pen.setWidthF(espessura)
        serie.setPen(pen)
        
        return serie

    def criar_ponto_operacao(self, x, y):
        """Cria um ponto de operação (scatter)"""
        serie = QScatterSeries()
        serie.setName("Ponto de Operação")
        serie.append(float(x), float(y))
        serie.setMarkerSize(12.0)
        serie.setColor(QColor('#FF0000'))  # Vermelho
        serie.setBorderColor(QColor('#000000'))
        #serie.setBorderWidth(2)
        
        return serie

    def configurar_eixos(self):
        """Configura os eixos com base no tipo de gráfico"""
        # Configurar eixo X
        self.axis_x.setTitleText(f"Vazão [{self.vazao}]")
        self.axis_x.setLabelFormat("%.1f")
        
        # Configurar eixo Y com base no tipo de gráfico
        if self.tipo == "altura":
            self.axis_y.setTitleText(f"Altura [{self.altura}]")
            # Ajustar faixa dos eixos
            min_y = min(np.min(self.H_plot), np.min(self.C_plot)) * 0.9
            max_y = max(np.max(self.H_plot), np.max(self.C_plot)) * 1.1
        elif self.tipo == "potencia":
            self.axis_y.setTitleText(f"Potência [{self.potencia}]")
            min_y = np.min(self.P_plot) * 0.9
            max_y = np.max(self.P_plot) * 1.1
        elif self.tipo == "rendimento":
            self.axis_y.setTitleText("Rendimento [%]")
            min_y = 0  # Rendimento não pode ser negativo
            max_y = np.max(self.eta_plot * 100) * 1.1
        
        # Ajustar faixa do eixo X
        min_x = 0
        max_x = np.max(self.Q_plot) * 1.05
        
        self.axis_x.setRange(min_x, max_x)
        self.axis_y.setRange(min_y, max_y)

    def plotar(self):
        # Limpar gráfico existente, mas manter os eixos
        self.chart.removeAllSeries()
        
        # Configurar eixos
        self.configurar_eixos()
        
        # Adicionar eixos se não estiverem já adicionados
        if not self.chart.axisX():
            self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        if not self.chart.axisY():
            self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        
        if self.tipo == "altura":
            # Adicionar séries
            serie_bomba = self.criar_serie(self.Q_plot, self.H_plot, "Curva da Bomba", '#1f77b4')
            serie_sistema = self.criar_serie(self.Q_plot, self.C_plot, "Curva do Sistema", '#ff7f0e')
            ponto_op = self.criar_ponto_operacao(self.Q_op, self.H_op)
            
            self.chart.addSeries(serie_bomba)
            self.chart.addSeries(serie_sistema)
            self.chart.addSeries(ponto_op)
            
            self.chart.setTitle("Curva da Bomba - Altura vs Vazão")
            
            # Atualizar informações do ponto de operação
            self.toolbar.atualizar_ponto_operacao(
                self.Q_op, self.H_op, self.tipo, self.vazao, self.altura
            )
            
        elif self.tipo == "potencia":
            y_val = np.interp(self.Q_op, self.Q_plot, self.P_plot)
            
            serie_potencia = self.criar_serie(self.Q_plot, self.P_plot, "Potência", '#2ca02c')
            ponto_op = self.criar_ponto_operacao(self.Q_op, y_val)
            
            self.chart.addSeries(serie_potencia)
            self.chart.addSeries(ponto_op)
            
            self.chart.setTitle("Potência vs Vazão")
            
            # Atualizar informações do ponto de operação
            self.toolbar.atualizar_ponto_operacao(
                self.Q_op, y_val, self.tipo, self.vazao, self.potencia
            )
            
        elif self.tipo == "rendimento":
            y_val = np.interp(self.Q_op, self.Q_plot, self.eta_plot * 100)
            
            serie_rendimento = self.criar_serie(self.Q_plot, self.eta_plot * 100, "Rendimento", '#d62728')
            ponto_op = self.criar_ponto_operacao(self.Q_op, y_val)
            
            self.chart.addSeries(serie_rendimento)
            self.chart.addSeries(ponto_op)
            
            self.chart.setTitle("Rendimento vs Vazão")
            
            # Atualizar informações do ponto de operação
            self.toolbar.atualizar_ponto_operacao(
                self.Q_op, y_val, self.tipo, self.vazao, "%"
            )
            
        else:
            # Tipo inválido
            return

        # Conectar séries aos eixos
        for series in self.chart.series():
            series.attachAxis(self.axis_x)
            series.attachAxis(self.axis_y)
        
        # Configurar legendas
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        
        # Ajustar visualização
        self.chart_view.update()

    def actualizar_dados(self, altura, perda):
        """Atualiza os dados da bomba e recalcula os gráficos."""
        self.H_geometrico = altura
        self.perda_carga = perda
        self.gerar_dados()
        self.plotar()