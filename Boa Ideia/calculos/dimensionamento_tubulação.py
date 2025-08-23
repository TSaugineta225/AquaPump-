import math
import CoolProp.CoolProp as CP

class Tubulacao:
    def __init__(self):

        self.rho = CP.PropsSI("D", "T", 293.15, "P", 101325, "Water")
        self.peso_especifico = self.rho * 9.81  # kg/m³ * m/s² = N/m³

    def calcular_diametro(self, vazao, tempo):
        if tempo == 24:
            self.D = 1.2 * math.sqrt(vazao)
        else:
            self.D = 1.3 * math.sqrt(vazao) * (tempo / 24) ** (1 / 4)
        return self.D

    def area_seccao(self):
        if not hasattr(self, 'D'):
            raise ValueError("O diâmetro deve ser calculado primeiro.")
        return math.pi * (self.D / 2) ** 2

    def calcular_potencia(self, H_geometrico):
        return (H_geometrico * self.vazao * self.peso_especifico) / 75
