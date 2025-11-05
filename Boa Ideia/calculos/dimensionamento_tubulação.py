import math
import CoolProp.CoolProp as CP
from scipy.constants import g

class Tubulacao:
    def __init__(self):
        self.rho = CP.PropsSI("D", "T", 293.15, "P", 101325, "Water")
        self.peso_especifico = self.rho * g  # kg/m³ * m/s² = N/m³
        self.D = 0.1  # Valor padrão inicial

    def calcular_diametro(self, vazao, tempo):
        """Calcula o diâmetro da tubulação com valores padrão seguros."""
        try:
            if vazao <= 0:
                self.D = 0.1  # Diâmetro padrão mínimo
            elif tempo == 24:
                self.D = 1.2 * math.sqrt(vazao)
            else:
                self.D = 1.3 * math.sqrt(vazao) * (tempo / 24) ** (1 / 4)
            
            self.D = max(self.D, 0.01)  # Mínimo 1cm
            self.D = min(self.D, 10.0)  # Máximo 10m (valor conservador)
            
            print(f"Diâmetro calculado: {self.D} m")
            return self.D
        except Exception as e:
            print(f"Erro no cálculo do diâmetro: {e}, usando valor padrão")
            self.D = 0.1
            return self.D

    def area_seccao(self):
        """Calcula a área da seção transversal com fallback."""
        try:
            if not hasattr(self, 'D') or self.D <= 0:
                self.D = 0.1  # Valor padrão
            area = math.pi * (self.D / 2) ** 2
            print(f"Área calculada: {area} m²")
            return area
        except Exception as e:
            print(f"Erro no cálculo da área: {e}, usando valor padrão")
            return 0.007854  # Área para diâmetro 0.1m

    def calcular_potencia(self, H_geometrico, vazao):
        """Calcula a potência requerida com tratamento de erros."""
        try:
            if H_geometrico <= 0 or vazao <= 0:
                return 0.0
            return (H_geometrico * vazao * self.peso_especifico) / 1000
        except Exception as e:
            print(f"Erro no cálculo da potência: {e}")
            return 0.0