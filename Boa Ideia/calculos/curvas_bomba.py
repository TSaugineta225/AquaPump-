# Em curvas_bomba.py (Versão correta para SIMULAÇÃO)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationBar
from PySide6.QtWidgets import QWidget, QVBoxLayout

plt.style.use('seaborn-v0_8')

class Grafico(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationBar(self.canvas, self)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.toolbar)
        layout_principal.addWidget(self.canvas)
        self.setLayout(layout_principal)
        
        self.ax.clear()
        self.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
        self.canvas.draw()

    def plotar_dados(self, tipo_grafico, dados_curva1, dados_curva2=None, ponto_operacao=None,
                     unidade_vazao=None, unidade_y=None, titulo=None):
        """
        Método genérico para plotar diferentes tipos de gráficos.
        """
        self.ax.clear()

        # Plotar primeira curva
        self.ax.plot(dados_curva1['x'], dados_curva1['y'], 
                     label=dados_curva1.get('label', 'Curva 1'), 
                     color=dados_curva1.get('cor', '#1f77b4'), 
                     linewidth=2.2)

        # Plotar segunda curva se fornecida
        if dados_curva2 is not None:
            self.ax.plot(dados_curva2['x'], dados_curva2['y'], 
                         label=dados_curva2.get('label', 'Curva 2'), 
                         color=dados_curva2.get('cor', '#ff7f0e'), 
                         linewidth=2.2)

        # Plotar Ponto de Operação se fornecido
        if ponto_operacao is not None:
            px, py = ponto_operacao['x'], ponto_operacao['y']
            self.ax.plot(px, py, 'o', markersize=8, color='black', label="Ponto de Operação")
            
            # Determinar rótulo baseado no tipo de gráfico
            if tipo_grafico == 'Altura':
                label_text = f"Q = {px:.2f} [{unidade_vazao}]\nH = {py:.2f} [{unidade_y}]"
            elif tipo_grafico == 'Potência':
                label_text = f"Q = {px:.2f} [{unidade_vazao}]\nP = {py:.2f} [{unidade_y}]"
            elif tipo_grafico == 'Rendimento':
                label_text = f"Q = {px:.2f} [{unidade_vazao}]\nη = {py:.2f} [{unidade_y}]"
            else:
                label_text = f"Q = {px:.2f} [{unidade_vazao}]\nY = {py:.2f} [{unidade_y}]"
                          
            self.ax.annotate(label_text, (px, py), xytext=(15, -30),
                             textcoords="offset points",
                             bbox=dict(boxstyle="round,pad=0.4", fc='#f0f0f0', ec='gray', alpha=0.8),
                             fontsize=9, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

        # Configurações do Gráfico
        self.ax.set_title(titulo, fontsize=11, fontweight='bold')
        self.ax.set_xlabel(f"Vazão ({unidade_vazao})", fontsize=10)
        self.ax.set_ylabel(f"{tipo_grafico} ({unidade_y})", fontsize=10)
        self.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
        self.ax.legend(frameon=True, loc='best', fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.figure.tight_layout()
        self.canvas.draw()