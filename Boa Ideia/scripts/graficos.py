import numpy as np
from PySide6.QtCharts import QLineSeries, QChart, QValueAxis
from PySide6.QtGui import QBrush, QFont, QColor, QPen
from PySide6.QtCore import Qt

class Graficos:
    def __init__(self, vazao_nominal, altura_nominal):
        self.Q_nominal = vazao_nominal
        self.H_nominal = altura_nominal
        self.H_0 = self.H_nominal * 1.2

        if self.Q_nominal > 0:
            self.A = (self.H_0 - self.H_nominal) / (self.Q_nominal**2)
        else:
            self.A = 0 

        self.chart = QChart()
        self.Q_plot = None 
        self.H_plot = None 
        self.series = None

    def gerar_pontos_curva(self):
        """Gera os pontos (Q, H) para a curva característica."""
        q_max_plot = self.Q_nominal * 1.5
        self.Q_plot = np.linspace(0, q_max_plot, 200)
        self.H_plot = self.H_0 - self.A * (self.Q_plot**2)
        self.H_plot[self.H_plot < 0] = 0


    def configurar_grafico(self):
        """Método único para configurar e desenhar o gráfico."""
        
        self.chart.legend().setAlignment(Qt.AlignLeft)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.setBackgroundBrush(QBrush(Qt.white))
        self.chart.setPlotAreaBackgroundBrush(QBrush(Qt.white))
        self.chart.setTitle("Curva Característica da Bomba (Simulação)")
        self.chart.setTitleFont(QFont("Roboto", 12, QFont.Bold))

    def plotar_grafico(self, nome="Curva Característica (H x Q)"):
        self.series = QLineSeries()
        self.series.setName(nome)
        self.series.setPointsVisible(False) 
        self.series.setPen(QPen(QColor("blue"), 2.5))
        for q, h in zip(self.Q_plot, self.H_plot):
            self.series.append(q, h)

        self.chart.addSeries(self.series)

    def configurar_eixo_x(self, tick_count = 10, titulo_x="Vazão", formato ="%.1f"):
        axis_x = QValueAxis()
        axis_x.setTitleText(titulo_x)
        axis_x.setLabelFormat(formato)
        axis_x.setGridLineVisible(True)
        axis_x.setMinorGridLineVisible(True)
        axis_x.setTickCount(tick_count)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)
        

    def configurar_eixo_y(self, tick_count=10, titulo_y ="Altura Manométrica (m)", formato= "%.1f"):
        axis_y = QValueAxis()
        axis_y.setTitleText(titulo_y)
        axis_y.setLabelFormat(formato)
        axis_y.setGridLineVisible(True)
        axis_y.setMinorGridLineVisible(True)
        axis_y.setTickCount(tick_count)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)
    
 