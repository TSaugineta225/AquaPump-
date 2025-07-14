import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import QWidget, QVBoxLayout

# Aplicar estilo moderno global (estilo 'seaborn-v0_8' ou outro moderno como 'bmh', 'ggplot', 'fivethirtyeight')
plt.style.use('seaborn-v0_8')

class Grafico(QWidget):
    def __init__(self, tipo='altura', perdas=0.003, vazao_nominal=4, altura_nominal=4, parent=None):
        super().__init__(parent)

        self.tipo = tipo.lower()
        self.Q_nominal = vazao_nominal
        self.H_nominal = altura_nominal
        self.H_geometrico = altura_nominal
        self.perda_carga = perdas

        self.H_0 = self.H_nominal * 1.2
        self.A = (self.H_0 - self.H_nominal) / (self.Q_nominal ** 2) if self.Q_nominal > 0 else 0

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationBar(self.canvas, self)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.toolbar)
        layout_principal.addWidget(self.canvas)
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
        Q_m3s = self.Q_plot / 3600
        eta_seguro = np.where(self.eta_plot > 0, self.eta_plot, np.nan)
        P = (rho * g * Q_m3s * self.H_plot) / eta_seguro
        return P / 1000

    def encontrar_ponto_operacao(self):
        diferenca = np.abs(self.H_plot - self.C_plot)
        indice_otimo = np.argmin(diferenca)
        return self.Q_plot[indice_otimo], self.H_plot[indice_otimo]

    def plotar_ponto_operacao(self, y_valor, ylabel):
        self.ax.plot(self.Q_op, y_valor, 'o', markersize=8, color='black', label="Ponto de Operação")
        self.ax.annotate(f"Q = {self.Q_op:.2f}\nY = {y_valor:.2f}",
                         (self.Q_op, y_valor),
                         xytext=(12, -25),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round,pad=0.4", fc='#f0f0f0', ec='gray'),
                         fontsize=9)

        self.ax.set_ylabel(ylabel, fontsize=10)

    def plotar(self):
        self.ax.clear()

        if self.tipo == "altura":
            self.ax.plot(self.Q_plot, self.H_plot, label="Curva da Bomba", color='#1f77b4', linewidth=2.2)
            self.ax.plot(self.Q_plot, self.C_plot, label="Curva do Sistema", color='#ff7f0e', linewidth=2.2)
            self.plotar_ponto_operacao(self.H_op, "Altura (m)")
            self.ax.set_title("Curva da Bomba - Altura vs Vazão", fontsize=11, fontweight='bold')

        elif self.tipo == "potencia":
            y_val = np.interp(self.Q_op, self.Q_plot, self.P_plot)
            self.ax.plot(self.Q_plot, self.P_plot, label="Potência", color='#2ca02c', linewidth=2.2)
            self.plotar_ponto_operacao(y_val, "Potência (kW)")
            self.ax.set_title("Potência vs Vazão", fontsize=11, fontweight='bold')

        elif self.tipo == "rendimento":
            y_val = np.interp(self.Q_op, self.Q_plot, self.eta_plot * 100)
            self.ax.plot(self.Q_plot, self.eta_plot * 100, label="Rendimento", color='#d62728', linewidth=2.2)
            self.plotar_ponto_operacao(y_val, "Rendimento (%)")
            self.ax.set_title("Rendimento vs Vazão", fontsize=11, fontweight='bold')

        else:
            self.ax.text(0.5, 0.5, "Tipo de gráfico inválido", ha='center', va='center', fontsize=12)

        self.ax.set_xlabel("Vazão (m³/h)", fontsize=10)
        self.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
        self.ax.legend(frameon=True, loc='best', fontsize=9)
        self.canvas.draw()
