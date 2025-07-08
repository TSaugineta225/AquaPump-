import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import QWidget, QVBoxLayout

class Grafico(QWidget):
    def __init__(self, vazao_nominal=2, altura_nominal=2, parent=None):
        super().__init__(parent)

        # Vazão nominal (Qn) e altura manométrica nominal (Hn)
        self.Q_nominal = vazao_nominal              # [m³/h] ou [L/s] — ajustar unidade conforme necessário
        self.H_nominal = altura_nominal 
        self.H_geometrico = altura_nominal            # [m]

        # Considera que a altura máxima (em vazão zero) é 20% maior que a altura nominal
        self.H_0 = self.H_nominal * 1.2             # [m] — H(0), altura máxima da curva

        # Coeficiente A da parábola: H(Q) = H₀ - A·Q²
        # A fórmula é deduzida isolando A na equação da curva característica
        # A = (H₀ - Hn) / Qn²
        self.A = (self.H_0 - self.H_nominal) / (self.Q_nominal ** 2) if self.Q_nominal > 0 else 0

        # ===========   Curva Caracteristica da Curva   ==================== #
        #self.curva_sistema = self.H_geometrico + self.perda_carga*pow(self.Q_nominal,2)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.navegador_grafico = NavigationBar(self.canvas, self)

        # Layout vertical: barra + gráfico
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.navegador_grafico)
        layout_principal.addWidget(self.canvas)
        self.setLayout(layout_principal)

        self.gerar_pontos_curva()
        self.plotar_grafico()

    def gerar_pontos_curva(self):
        # Define o intervalo de vazões a serem simuladas: de 0 até 1,5 × Q_nominal
        q_max_plot = self.Q_nominal * 1.5
        self.Q_plot = np.linspace(0, q_max_plot, 200)   # 200 pontos uniformes entre 0 e Qmax

        # Aplica a equação da curva característica da bomba: H(Q) = H₀ - A·Q²
        self.H_plot = self.H_0 - self.A * (self.Q_plot ** 2)

        # Evita que apareçam valores negativos no gráfico (por questões visuais)
        self.H_plot[self.H_plot < 0] = 0

    def plotar_grafico(self, nome="Curva Característica (H x Q)", preencher=True):
        # Limpa qualquer gráfico anterior
        self.ax.clear()
        self.ax.plot(self.Q_plot, self.H_plot, label=nome, color='blue', linewidth=2.5)

        # Preenche a área abaixo da curva (opcional, apenas visual)
        if preencher:
            self.ax.fill_between(self.Q_plot, self.H_plot, color='blue', alpha=0.1)

        self.ax.set_title("Curva Característica da Bomba (Simulação)",
                          fontsize=10, fontfamily='arial', fontweight='bold')
        self.ax.set_xlabel("Vazão (m³/h)") 
        self.ax.set_ylabel("Altura Manométrica (m)")

        self.ax.grid(True, which='both', linestyle='--', linewidth=0.3, alpha=0.7)

        self.ax.legend()
        self.canvas.draw()
