import math
import pytest
from dimensionamento_tubulação import Tubulacao

class TestTubulacao:
    @pytest.fixture
    def tub(self):
        return Tubulacao()

    def test_calculo_diametro_24h(self, tub):
        d = tub.calcular_diametro(0.01, 24)
        # Para vazão 0.01 m³/s, tempo 24h: D = 1.2 * sqrt(0.01) = 0.12 m
        assert abs(d - 0.12) < 1e-9

    def test_calculo_diametro_12h(self, tub):
        d = tub.calcular_diametro(0.02, 12)
        # D = 1.3 * sqrt(0.02) * (12/24)^(1/4) = 1.3 * 0.1414 * 0.8409 ≈ 0.1547
        assert abs(d - 0.1547) < 0.001

    def test_diametro_minimo(self, tub):
        d = tub.calcular_diametro(1e-8, 1)  # vazão muito pequena
        assert d >= 0.01

    def test_diametro_maximo(self, tub):
        d = tub.calcular_diametro(1000, 1)  # vazão enorme
        assert d <= 10.0

    def test_area_seccao(self, tub):
        tub.D = 0.2
        area = tub.area_seccao()
        assert abs(area - math.pi * 0.01) < 1e-9  # pi*(0.1)^2

    def test_calcular_potencia(self, tub):
        # H=10m, vazao=0.01 m³/s, peso específico = rho*g ≈ 1000*9.81 ≈ 9810 N/m³
        # P = (10*0.01*9810)/1000 = 0.981 kW
        pot = tub.calcular_potencia(10, 0.01)
        assert abs(pot - 0.981) < 0.01

    def test_potencia_negativa(self, tub):
        assert tub.calcular_potencia(-5, 0.01) == 0.0
        assert tub.calcular_potencia(10, -0.01) == 0.0