# Adicione este arquivo ao seu projeto como unidades.py
from pint import UnitRegistry

class ConversorUnidades:
    def __init__(self):
        self.ureg = UnitRegistry()
        self.Q_ = self.ureg.Quantity
        
        # Definir unidades personalizadas se necessário
        self.ureg.define('litro_por_segundo = liter / second = L/s')
        self.ureg.define('metro_cubico_por_hora = meter**3 / hour = m³/h')
        self.ureg.define('litro_por_hora = liter / hour = L/h')
        
    def converter_vazao(self, valor, de_unidade, para_unidade):
        """
        Converte valores de vazão entre diferentes unidades
        """
        try:
            quantidade = self.Q_(valor, de_unidade)
            return quantidade.to(para_unidade).magnitude
        except Exception as e:
            print(f"Erro na conversão de vazão: {e}")
            return valor
    
    def converter_comprimento(self, valor, de_unidade, para_unidade):
        """
        Converte valores de comprimento entre diferentes unidades
        """
        try:
            quantidade = self.Q_(valor, de_unidade)
            return quantidade.to(para_unidade).magnitude
        except Exception as e:
            print(f"Erro na conversão de comprimento: {e}")
            return valor
    
    def converter_potencia(self, valor, de_unidade, para_unidade):
        """
        Converte valores de potência entre diferentes unidades
        """
        try:
            quantidade = self.Q_(valor, de_unidade)
            return quantidade.to(para_unidade).magnitude
        except Exception as e:
            print(f"Erro na conversão de potência: {e}")
            return valor
    
    def converter_pressao(self, valor, de_unidade, para_unidade):
        """
        Converte valores de pressão entre diferentes unidades
        """
        try:
            quantidade = self.Q_(valor, de_unidade)
            return quantidade.to(para_unidade).magnitude
        except Exception as e:
            print(f"Erro na conversão de pressão: {e}")
            return valor
    
    def get_unidades_vazao(self):
        """Retorna lista de unidades de vazão suportadas"""
        return [
            'm³/s', 'm³/h', 'L/s', 'L/h', 'L/min',
            'gal/s', 'gal/min', 'gal/h',
            'ft³/s', 'ft³/min', 'ft³/h'
        ]
    
    def get_unidades_comprimento(self):
        """Retorna lista de unidades de comprimento suportadas"""
        return ['m', 'cm', 'mm', 'km', 'in', 'ft', 'yd', 'mi']
    
    def get_unidades_potencia(self):
        """Retorna lista de unidades de potência suportadas"""
        return ['W', 'kW', 'MW', 'hp', 'cv']
    
    def get_unidades_pressao(self):
        """Retorna lista de unidades de pressão suportadas"""
        return ['Pa', 'kPa', 'MPa', 'bar', 'psi', 'atm']
    
    def converter_temperatura(self, valor, de_unidade, para_unidade):
        """
        Converte valores de temperatura entre diferentes unidades
        """
        try:
            # Pint lida especialmente com temperatura
            if de_unidade.upper() == 'K':
                quantidade = self.Q_(valor, 'kelvin')
            elif de_unidade.upper() == 'C':
                quantidade = self.Q_(valor, 'celsius')
            elif de_unidade.upper() == 'F':
                quantidade = self.Q_(valor, 'fahrenheit')
            else:
                quantidade = self.Q_(valor, de_unidade)
            
            if para_unidade.upper() == 'K':
                return quantidade.to('kelvin').magnitude
            elif para_unidade.upper() == 'C':
                return quantidade.to('celsius').magnitude
            elif para_unidade.upper() == 'F':
                return quantidade.to('fahrenheit').magnitude
            else:
                return quantidade.to(para_unidade).magnitude
                
        except Exception as e:
            print(f"Erro na conversão de temperatura: {e}")
            return valor
