import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import QWidget, QVBoxLayout
from calculos.unidades import ConversorUnidades  

plt.style.use('seaborn-v0_8')

class Grafico(QWidget):
    def __init__(self, tipo='altura', potencia='kW', altura='m', v='m³/h', perdas=0.003, vazao_nominal=4, altura_nominal=4, parent=None):
        super().__init__(parent)
        
        self.conversor = ConversorUnidades()

        self.unidade_potencia = potencia
        self.unidade_altura = altura
        self.unidade_vazao = v
        
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

    def converter_vazao_para_m3h(self, valor, unidade):
        """Convert flow rate to m³/h for internal calculations"""
        if unidade == 'm³/h':
            return valor
        elif unidade == 'm³/s':
            return valor * 3600
        elif unidade == 'L/s':
            return valor * 3.6
        elif unidade == 'L/h':
            return valor / 1000
        elif unidade == 'gal/s':
            return valor * 0.00378541 * 3600
        elif unidade == 'gal/min':
            return valor * 0.00378541 * 60
        elif unidade == 'gal/h':
            return valor * 0.00378541
        elif unidade == 'ft³/s':
            return valor * 101.941
        elif unidade == 'ft³/min':
            return valor * 1.69901
        elif unidade == 'ft³/h':
            return valor * 0.0283168
        else:
            return valor  # Default to no conversion

    def converter_vazao_de_m3h(self, valor, unidade):
        """Convert flow rate from m³/h to target unit"""
        if unidade == 'm³/h':
            return valor
        elif unidade == 'm³/s':
            return valor / 3600
        elif unidade == 'L/s':
            return valor / 3.6
        elif unidade == 'L/h':
            return valor * 1000
        elif unidade == 'gal/s':
            return valor / (0.00378541 * 3600)
        elif unidade == 'gal/min':
            return valor / (0.00378541 * 60)
        elif unidade == 'gal/h':
            return valor / 0.00378541
        elif unidade == 'ft³/s':
            return valor / 101.941
        elif unidade == 'ft³/min':
            return valor / 1.69901
        elif unidade == 'ft³/h':
            return valor / 0.0283168
        else:
            return valor  # Default to no conversion

    def converter_altura_para_m(self, valor, unidade):
        """Convert height to meters for internal calculations"""
        if unidade == 'm':
            return valor
        elif unidade == 'ft':
            return valor * 0.3048
        elif unidade == 'cm':
            return valor / 100
        elif unidade == 'mm':
            return valor / 1000
        else:
            return valor  # Default to no conversion

    def converter_altura_de_m(self, valor, unidade):
        """Convert height from meters to target unit"""
        if unidade == 'm':
            return valor
        elif unidade == 'ft':
            return valor / 0.3048
        elif unidade == 'cm':
            return valor * 100
        elif unidade == 'mm':
            return valor * 1000
        else:
            return valor  # Default to no conversion

    def converter_potencia_para_kw(self, valor, unidade):
        """Convert power to kW for internal calculations"""
        if unidade == 'kW':
            return valor
        elif unidade == 'W':
            return valor / 1000
        elif unidade == 'CV':
            return valor * 0.7355
        elif unidade == 'hp':
            return valor * 0.7457
        else:
            return valor  

    def converter_potencia_de_kw(self, valor, unidade):
        """Convert power from kW to target unit"""
        if unidade == 'kW':
            return valor
        elif unidade == 'W':
            return valor * 1000
        elif unidade == 'CV':
            return valor / 0.7355
        elif unidade == 'hp':
            return valor / 0.7457
        else:
            return valor  
    def gerar_dados(self):
        Q_nominal_m3h = self.converter_vazao_para_m3h(self.Q_nominal, self.unidade_vazao)
        H_nominal_m = self.converter_altura_para_m(self.H_nominal, self.unidade_altura)
        H_geometrico_m = self.converter_altura_para_m(self.H_geometrico, self.unidade_altura)
        
        q_max = Q_nominal_m3h * 1.5
        self.Q_plot_m3h = np.linspace(0.1, q_max, 200)

        # Calculate curves in base units
        self.H_0_m = H_nominal_m * 1.2
        self.A_m = (self.H_0_m - H_nominal_m) / (Q_nominal_m3h ** 2) if Q_nominal_m3h > 0 else 0

        self.H_plot_m = self.H_0_m - self.A_m * self.Q_plot_m3h ** 2
        self.H_plot_m[self.H_plot_m < 0] = 0

        self.C_plot_m = H_geometrico_m + self.perda_carga * self.Q_plot_m3h ** 2

        self.eta_plot = self.calcular_rendimento()
        self.P_plot_kW = self.calcular_potencia()

        self.Q_op_m3h, self.H_op_m = self.encontrar_ponto_operacao()

    def calcular_rendimento(self):
        eta_max = 0.75
        k = 0.01
        return eta_max - k * (self.Q_plot_m3h - self.converter_vazao_para_m3h(self.Q_nominal, self.unidade_vazao)) ** 2

    def calcular_potencia(self, g=9.81):
        rho = 1000
        Q_m3s = self.Q_plot_m3h / 3600
        eta_seguro = np.where(self.eta_plot > 0, self.eta_plot, np.nan)
        P = (rho * g * Q_m3s * self.H_plot_m) / eta_seguro
        return P / 1000  # Convert to kW

    def encontrar_ponto_operacao(self):
        diferenca = np.abs(self.H_plot_m - self.C_plot_m)
        indice_otimo = np.argmin(diferenca)
        return self.Q_plot_m3h[indice_otimo], self.H_plot_m[indice_otimo]

    def plotar_ponto_operacao(self, y_valor_m, ylabel):
        # Convert values to display units
        Q_op_display = self.converter_vazao_de_m3h(self.Q_op_m3h, self.unidade_vazao)
        y_valor_display = self.converter_altura_de_m(y_valor_m, self.unidade_altura) if 'Altura' in ylabel else y_valor_m
        
        if 'Potência' in ylabel:
            y_valor_display = self.converter_potencia_de_kw(y_valor_m, self.unidade_potencia)
        
        self.ax.plot(Q_op_display, y_valor_display, 'o', markersize=8, color='black', label="Ponto de Operação")
        self.ax.annotate(f"Q = {Q_op_display:.2f} {self.unidade_vazao}\nY = {y_valor_display:.2f} {ylabel.split('(')[-1].rstrip(')') if '(' in ylabel else ''}",
                         (Q_op_display, y_valor_display),
                         xytext=(12, -25),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round,pad=0.4", fc='#f0f0f0', ec='gray'),
                         fontsize=9)

        self.ax.set_ylabel(ylabel, fontsize=10)
    
    def plotar(self):
        self.ax.clear()

        Q_plot_display = self.converter_vazao_de_m3h(self.Q_plot_m3h, self.unidade_vazao)
        
        if self.tipo == "altura":
            H_plot_display = self.converter_altura_de_m(self.H_plot_m, self.unidade_altura)
            C_plot_display = self.converter_altura_de_m(self.C_plot_m, self.unidade_altura)
            
            self.ax.plot(Q_plot_display, H_plot_display, label="Curva da Bomba", color='#1f77b4', linewidth=2.2)
            self.ax.plot(Q_plot_display, C_plot_display, label="Curva do Sistema", color='#ff7f0e', linewidth=2.2)
            self.plotar_ponto_operacao(self.H_op_m, f"Altura ({self.unidade_altura})")
            self.ax.set_title("Curva da Bomba - Altura vs Vazão", fontsize=11, fontweight='bold')

        elif self.tipo == "potencia":
            # Convert power values to display units
            P_plot_display = self.converter_potencia_de_kw(self.P_plot_kW, self.unidade_potencia)
            y_val = np.interp(self.Q_op_m3h, self.Q_plot_m3h, self.P_plot_kW)
            
            self.ax.plot(Q_plot_display, P_plot_display, label="Potência", color='#2ca02c', linewidth=2.2)
            self.plotar_ponto_operacao(y_val, f"Potência ({self.unidade_potencia})")
            self.ax.set_title("Potência vs Vazão", fontsize=11, fontweight='bold')

        elif self.tipo == "rendimento":
            y_val = np.interp(self.Q_op_m3h, self.Q_plot_m3h, self.eta_plot * 100)
            self.ax.plot(Q_plot_display, self.eta_plot * 100, label="Rendimento", color='#d62728', linewidth=2.2)
            self.plotar_ponto_operacao(y_val, "Rendimento (%)")
            self.ax.set_title("Rendimento vs Vazão", fontsize=11, fontweight='bold')

        else:
            self.ax.text(0.5, 0.5, "Tipo de gráfico inválido", ha='center', va='center', fontsize=12)

        self.ax.set_xlabel(f"Vazão ({self.unidade_vazao})", fontsize=10)
        self.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
        self.ax.legend(frameon=True, loc='best', fontsize=9)
        self.canvas.draw()

    def actualizar_dados(self, altura, perda):
        """ Atualiza os dados da bomba e recalcula os gráficos. """
        self.H_geometrico = self.converter_altura_para_m(altura, self.unidade_altura)
        self.perda_carga = perda
        
        self.Q_nominal = self.converter_vazao_para_m3h(self.Q_nominal, self.unidade_vazao)
        self.H_nominal = self.converter_altura_para_m(self.H_nominal, self.unidade_altura)
        
        self.gerar_dados()
        self.plotar()