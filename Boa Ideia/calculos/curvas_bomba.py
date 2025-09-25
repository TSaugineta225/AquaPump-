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
        layout_principal.setContentsMargins(0,0,0,0)
        layout_principal.addWidget(self.toolbar)
        layout_principal.addWidget(self.canvas)
        self.setLayout(layout_principal)
        self.ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)
        self.canvas.draw()

    def plotar_curvas_associacao(self, titulo, unidade_vazao, unidade_altura, curva_sistema, *curvas_bombas):
        """
        Método flexível para plotar múltiplas curvas de bombas e a curva do sistema.
        - curva_sistema: Dicionário com dados da curva do sistema.
        - *curvas_bombas: Uma sequência de dicionários, cada um representando uma curva de bomba.
        """
        self.ax.clear()

        # Plotar as curvas das bombas
        cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] 
        for i, curva in enumerate(curvas_bombas):
            if curva and curva.get('x') is not None and curva.get('y') is not None:
                self.ax.plot(curva['x'], curva['y'], 
                             label=curva.get('label', f'Bomba {i+1}'), 
                             color=cores[i % len(cores)], 
                             linewidth=2.0, linestyle=curva.get('linestyle', '-'))

        # Plotar a curva do sistema
        if curva_sistema and curva_sistema.get('x') is not None and curva_sistema.get('y') is not None:
            self.ax.plot(curva_sistema['x'], curva_sistema['y'], 
                         label=curva_sistema.get('label', 'Curva do Sistema'), 
                         color='black', 
                         linewidth=2.2, linestyle='--')

        # Configurações do Gráfico
        self.ax.set_title(titulo, fontsize=12, fontweight='bold', pad=10)
        self.ax.set_xlabel(f"Vazão ({unidade_vazao})", fontsize=10)
        self.ax.set_ylabel(f"Altura ({unidade_altura})", fontsize=10)
        self.ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.legend(frameon=True, loc='best', fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=9)
        self.ax.set_xlim(left=0)
        self.ax.set_ylim(bottom=0)
        
        self.figure.tight_layout()
        self.canvas.draw()