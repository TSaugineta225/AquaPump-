import pytest
from unidades import ConversorUnidades

@pytest.fixture
def conversor():
    return ConversorUnidades()

class TestConversor:
    def test_converter_vazao(self, conversor):
        # 1 L/s = 0.001 m³/s
        assert conversor.converter_vazao(1, "L/s", "m³/s") == pytest.approx(0.001)

    def test_converter_comprimento(self, conversor):
        assert conversor.converter_comprimento(10, "cm", "m") == pytest.approx(0.1)

    def test_converter_potencia(self, conversor):
        # 735.49875 W = 1 cv
        assert conversor.converter_potencia(735.49875, "watt", "cv") == pytest.approx(1.0)

    def test_converter_pressao(self, conversor):
        # 101325 Pa = 1 atm
        assert conversor.converter_pressao(101325, "Pa", "atm") == pytest.approx(1.0, rel=1e-3)

    def test_converter_temperatura(self, conversor):
        assert conversor.converter_temperatura(0, "C", "K") == pytest.approx(273.15)
        assert conversor.converter_temperatura(32, "F", "C") == pytest.approx(0.0, abs=0.01)

    def test_unidade_invalida(self, conversor):
        with pytest.raises(ValueError):
            conversor.converter_vazao(1, "m/s", "km/h")  # unidades não compatíveis

    def test_verificar_compatibilidade(self, conversor):
        assert conversor.verificar_compatibilidade("m", "ft")
        assert not conversor.verificar_compatibilidade("m", "kg")