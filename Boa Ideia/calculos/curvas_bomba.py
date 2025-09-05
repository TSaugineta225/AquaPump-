import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import QWidget, QVBoxLayout
from scipy.optimize import fsolve

# Aplicar estilo moderno global
plt.style.use('seaborn-v0_8')

class Grafico(QWidget):
    def __init__(self, tipo='altura', potencia='Kw', altura='m', v='vazao', perdas=0.003, 
                 vazao_nominal=4, altura_nominal=4, parent=None, modo_associacao='paralelo'):
        super().__init__(parent)

        self.tipo = tipo.lower()
        self.potencia = potencia
        self.altura = altura
        self.vazao = v
        self.Q_nominal = vazao_nominal
        self.H_nominal = altura_nominal
        self.H_geometrico = altura_nominal
        self.perda_carga = perdas
        self.modo_associacao = modo_associacao.lower()

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

        if self.tipo == "associacao":
            self.gerar_dados_associacao()
        else:
            self.gerar_dados_normais()

    def gerar_dados_normais(self):
        self.H_plot = self.H_0 - self.A * self.Q_plot ** 2
        self.H_plot[self.H_plot < 0] = 0

        self.C_plot = self.H_geometrico + self.perda_carga * self.Q_plot ** 2

        self.eta_plot = self.calcular_rendimento()
        self.P_plot = self.calcular_potencia()

        self.Q_op, self.H_op = self.encontrar_ponto_operacao(self.H_plot, self.C_plot)

    def gerar_dados_associacao(self):
        # Curva da bomba individual
        H_bomba = self.H_0 - self.A * self.Q_plot ** 2
        H_bomba[H_bomba < 0] = 0

        # Curva do sistema
        self.C_plot = self.H_geometrico + self.perda_carga * self.Q_plot ** 2

        if self.modo_associacao == 'paralelo':
            # Para bombas em paralelo: mesma altura, vazões somadas
            # Inverter a curva H(Q) para Q(H)
            H_range = np.linspace(0, self.H_0, 200)
            Q_bomba = np.sqrt((self.H_0 - H_range) / self.A) if self.A > 0 else np.zeros_like(H_range)
            
            # Para duas bombas iguais em paralelo
            Q_paralelo = 2 * Q_bomba
            
            # Recriar curva H(Q) para associação
            self.H_plot = np.interp(self.Q_plot, Q_paralelo, H_range, left=0, right=0)
            
        elif self.modo_associacao == 'serie':
            # Para bombas em série: mesma vazão, alturas somadas
            self.H_plot = 2 * H_bomba

        # Encontrar ponto de operação
        self.Q_op, self.H_op = self.encontrar_ponto_operacao(self.H_plot, self.C_plot)

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

    def encontrar_ponto_operacao(self, curva_bomba, curva_sistema):
        # Encontrar interseção entre as curvas
        def diferenca(Q):
            H_b = np.interp(Q, self.Q_plot, curva_bomba)
            H_s = np.interp(Q, self.Q_plot, curva_sistema)
            return H_b - H_s

        # Estimativa inicial como a vazão nominal
        Q_guess = self.Q_nominal
        try:
            Q_op = fsolve(diferenca, Q_guess)[0]
            H_op = np.interp(Q_op, self.Q_plot, curva_bomba)
        except:
            Q_op, H_op = 0, 0
            
        return Q_op, H_op

    def plotar_ponto_operacao(self, x_val, y_val, ylabel):
        self.ax.plot(x_val, y_val, 'o', markersize=8, color='black', label="Ponto de Operação")
        self.ax.annotate(f"Q = {x_val:.2f}\n{ylabel} = {y_val:.2f}",
                         (x_val, y_val),
                         xytext=(12, -25),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round,pad=0.4", fc='#f0f0f0', ec='gray'),
                         fontsize=9)

    def plotar(self):
        self.ax.clear()

        if self.tipo == "altura":
            self.ax.plot(self.Q_plot, self.H_plot, label="Curva da Bomba", color='#1f77b4', linewidth=2.2)
            self.ax.plot(self.Q_plot, self.C_plot, label="Curva do Sistema", color='#ff7f0e', linewidth=2.2)
            self.plotar_ponto_operacao(self.Q_op, self.H_op, f"Altura ({self.altura})")
            self.ax.set_title("Curva da Bomba - Altura vs Vazão", fontsize=11, fontweight='bold')
            self.ax.set_ylabel(f"Altura ({self.altura})", fontsize=10)

        elif self.tipo == "potencia":
            y_val = np.interp(self.Q_op, self.Q_plot, self.P_plot)
            self.ax.plot(self.Q_plot, self.P_plot, label="Potência", color='#2ca02c', linewidth=2.2)
            self.plotar_ponto_operacao(self.Q_op, y_val, f"Potência ({self.potencia})")
            self.ax.set_title("Potência vs Vazão", fontsize=11, fontweight='bold')
            self.ax.set_ylabel(f"Potência ({self.potencia})", fontsize=10)

        elif self.tipo == "rendimento":
            y_val = np.interp(self.Q_op, self.Q_plot, self.eta_plot * 100)
            self.ax.plot(self.Q_plot, self.eta_plot * 100, label="Rendimento", color='#d62728', linewidth=2.2)
            self.plotar_ponto_operacao(self.Q_op, y_val, "Rendimento (%)")
            self.ax.set_title("Rendimento vs Vazão", fontsize=11, fontweight='bold')
            self.ax.set_ylabel("Rendimento (%)", fontsize=10)

        elif self.tipo == "associacao":
            # Curva da bomba individual
            H_individual = self.H_0 - self.A * self.Q_plot ** 2
            H_individual[H_individual < 0] = 0
            
            self.ax.plot(self.Q_plot, H_individual, '--', label="Bomba Individual", color='#1f77b4', linewidth=1.5)
            self.ax.plot(self.Q_plot, self.H_plot, label=f"Associação ({self.modo_associacao})", color='#9467bd', linewidth=2.2)
            self.ax.plot(self.Q_plot, self.C_plot, label="Curva do Sistema", color='#ff7f0e', linewidth=2.2)
            
            self.plotar_ponto_operacao(self.Q_op, self.H_op, f"Altura ({self.altura})")
            
            title_mode = "Série" if self.modo_associacao == "serie" else "Paralelo"
            self.ax.set_title(f"Associação de Bombas em {title_mode}", fontsize=11, fontweight='bold')
            self.ax.set_ylabel(f"Altura ({self.altura})", fontsize=10)

        else:
            self.ax.text(0.5, 0.5, "Tipo de gráfico inválido", ha='center', va='center', fontsize=12)

        self.ax.set_xlabel(f"Vazão ({self.vazao})", fontsize=10)
        self.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
        self.ax.legend(frameon=True, loc='best', fontsize=9)
        self.canvas.draw()

    def actualizar_dados(self, altura, perda, modo_associacao=None):
        """ Atualiza os dados da bomba e recalcula os gráficos. """
        self.H_geometrico = altura
        self.perda_carga = perda
        
        if modo_associacao:
            self.modo_associacao = modo_associacao.lower()
            
        self.gerar_dados()
        self.plotar()