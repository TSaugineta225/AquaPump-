import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt


class Grafico(QWidget):
    def __init__(self, vazao_nominal=2, altura_nominal=2, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        #self.navegador_grafico = NavigationBar(self.canvas, self)
        self.ax = self.figure.add_subplot(111)
        

        self.Q_nominal = vazao_nominal
        self.H_nominal = altura_nominal
        self.H_0 = self.H_nominal * 1.2

        if self.Q_nominal > 0:
            self.A = (self.H_0 - self.H_nominal) / (self.Q_nominal ** 2)
        else:
            self.A = 0

        self.Q_plot = None
        self.H_plot = None

        # Configurar layout e canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.gerar_pontos_curva()
        self.plotar_grafico()

    def gerar_pontos_curva(self):
        """Gera os pontos (Q, H) para a curva característica."""
        q_max_plot = self.Q_nominal * 1.5
        self.Q_plot = np.linspace(0, q_max_plot, 200)
        self.H_plot = self.H_0 - self.A * (self.Q_plot ** 2)
        self.H_plot[self.H_plot < 0] = 0

    def plotar_grafico(self, nome="Curva Característica (H x Q)", preencher=True):
        """Plota o gráfico dentro do canvas matplotlib embutido."""

        self.ax.clear()
        self.ax.plot(self.Q_plot, self.H_plot, label=nome, color='blue', linewidth=2.5)
        if preencher:
            self.ax.fill_between(self.Q_plot, self.H_plot, color='blue', alpha=0.1)

        # Configuração do gráfico
        self.ax.set_title("Curva Característica da Bomba (Simulação)", fontsize=10, fontfamily='arial', fontweight='bold')
        self.ax.set_xlabel("Vazão (m³/h)")
        self.ax.set_ylabel("Altura Manométrica (m)")
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.3, alpha=0.7)
        self.ax.legend()

        self.canvas.draw()