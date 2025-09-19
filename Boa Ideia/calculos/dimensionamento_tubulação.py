import math
import CoolProp.CoolProp as CP
from scipy.constants import g

class Tubulacao:
    def __init__(self):

        self.rho = CP.PropsSI("D", "T", 293.15, "P", 101325, "Water")
        self.peso_especifico = self.rho * g  # kg/m³ * m/s² = N/m³

    def calcular_diametro(self, vazao, tempo):
        if tempo == 24:
            self.D = 1.2 * math.sqrt(vazao)
        else:
            self.D = 1.3 * math.sqrt(vazao) * (tempo / 24) ** (1 / 4)
        print(f"Diâmetro calculado: {self.D} m")
        return self.D

    def area_seccao(self):
        if not hasattr(self, 'D'):
            raise ValueError("O diâmetro deve ser calculado primeiro.")
        return math.pi * (self.D / 2) ** 2

    def calcular_potencia(self, H_geometrico, vazao):
        return (H_geometrico * vazao * self.peso_especifico) / 1000
