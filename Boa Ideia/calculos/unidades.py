# unidades.py - Versão corrigida
from pint import UnitRegistry
from pint.errors import DimensionalityError, UndefinedUnitError

class ConversorUnidades:
    def __init__(self):
        self.ureg = UnitRegistry()
        self.Q_ = self.ureg.Quantity
        
        # Definir unidades personalizadas corretamente
        self.ureg.define('litro_por_segundo = liter / second = L/s')
        self.ureg.define('metro_cubico_por_hora = meter**3 / hour = m³/h')
        self.ureg.define('litro_por_hora = liter / hour = L/h')
        self.ureg.define('cv = 735.49875 * watt = cavalo_vapor')
        
    def _validar_unidades(self, de_unidade, para_unidade, tipo):
        """Valida se as unidades fornecidas são suportadas"""
        unidades_suportadas = {
            'vazao': self.get_unidades_vazao(),
            'comprimento': self.get_unidades_comprimento(),
            'potencia': self.get_unidades_potencia(),
            'pressao': self.get_unidades_pressao(),
            'temperatura': ['K', 'C', 'F', 'kelvin', 'celsius', 'fahrenheit']
        }
        
        if tipo not in unidades_suportadas:
            raise ValueError(f"Tipo '{tipo}' não suportado")
        
        if (de_unidade not in unidades_suportadas[tipo] or 
            para_unidade not in unidades_suportadas[tipo]):
            raise ValueError(f"Unidade não suportada para tipo '{tipo}'. "
                           f"Suportadas: {unidades_suportadas[tipo]}")
    
    def converter_vazao(self, valor, de_unidade, para_unidade):
        """
        Converte valores de vazão entre diferentes unidades
        """
        try:
            self._validar_unidades(de_unidade, para_unidade, 'vazao')
            quantidade = self.Q_(valor, de_unidade)
            resultado = quantidade.to(para_unidade).magnitude
            return resultado
        except (DimensionalityError, UndefinedUnitError, ValueError) as e:
            raise ValueError(f"Erro na conversão de vazão: {e}") from e
    
    def converter_comprimento(self, valor, de_unidade, para_unidade):
        """
        Converte valores de comprimento entre diferentes unidades
        """
        try:
            self._validar_unidades(de_unidade, para_unidade, 'comprimento')
            quantidade = self.Q_(valor, de_unidade)
            resultado = quantidade.to(para_unidade).magnitude
            return resultado
        except (DimensionalityError, UndefinedUnitError, ValueError) as e:
            raise ValueError(f"Erro na conversão de comprimento: {e}") from e
    
    def converter_potencia(self, valor, de_unidade, para_unidade):
        """
        Converte valores de potência entre diferentes unidades
        """
        try:
            self._validar_unidades(de_unidade, para_unidade, 'potencia')
            quantidade = self.Q_(valor, de_unidade)
            resultado = quantidade.to(para_unidade).magnitude
            return resultado
        except Exception as e:
            print("Erro na conversão de potência devido a", e)
    
    def converter_pressao(self, valor, de_unidade, para_unidade):
        """
        Converte valores de pressão entre diferentes unidades
        """
        try:
            self._validar_unidades(de_unidade, para_unidade, 'pressao')
            quantidade = self.Q_(valor, de_unidade)
            resultado = quantidade.to(para_unidade).magnitude
            return resultado
        except (DimensionalityError, UndefinedUnitError, ValueError) as e:
            raise ValueError(f"Erro na conversão de pressão: {e}") from e
    
    def converter_temperatura(self, valor, de_unidade, para_unidade):
        """
        Converte valores de temperatura entre diferentes unidades
        """
        try:
            # Mapear abreviações para nomes completos
            mapa_unidades = {
                'K': 'kelvin', 'C': 'celsius', 'F': 'fahrenheit',
                'kelvin': 'kelvin', 'celsius': 'celsius', 'fahrenheit': 'fahrenheit'
            }
            
            if de_unidade not in mapa_unidades or para_unidade not in mapa_unidades:
                raise ValueError("Unidades de temperatura devem ser K, C, F, kelvin, celsius ou fahrenheit")
            
            de_unidade_completo = mapa_unidades[de_unidade]
            para_unidade_completo = mapa_unidades[para_unidade]
            
            quantidade = self.Q_(valor, de_unidade_completo)
            resultado = quantidade.to(para_unidade_completo).magnitude
            return resultado
            
        except (DimensionalityError, UndefinedUnitError, ValueError) as e:
            raise ValueError(f"Erro na conversão de temperatura: {e}") from e
    
    def get_unidades_vazao(self):
        """Retorna lista de unidades de vazão suportadas"""
        return [
            'm³/s', 'm³/h', 'L/s', 'L/h', 'L/min',
            'gal/s', 'gal/min', 'gal/h',
            'ft³/s', 'ft³/min', 'ft³/h',
            'litro_por_segundo', 'metro_cubico_por_hora', 'litro_por_hora'
        ]
    
    def get_unidades_comprimento(self):
        """Retorna lista de unidades de comprimento suportadas"""
        return ['m', 'cm', 'mm', 'km', 'in', 'ft', 'yd', 'mi']
    
    def get_unidades_potencia(self):
        """Retorna lista de unidades de potência suportadas"""
        return ['watt', 'kilowatt', 'megawatt', 'horsepower', 'cv']
    
    def get_unidades_pressao(self):
        """Retorna lista de unidades de pressão suportadas"""
        return ['Pa', 'kPa', 'MPa', 'bar', 'psi', 'atm']
    
    def converter_generico(self, valor, de_unidade, para_unidade):
        """
        Método genérico para conversão entre quaisquer unidades compatíveis
        """
        try:
            quantidade = self.Q_(valor, de_unidade)
            resultado = quantidade.to(para_unidade).magnitude
            return resultado
        except (DimensionalityError, UndefinedUnitError, ValueError) as e:
            raise ValueError(f"Erro na conversão de {de_unidade} para {para_unidade}: {e}") from e
    
    def obter_dimensao(self, unidade):
        """
        Retorna a dimensão física da unidade (ex: length, time, etc.)
        """
        try:
            quantidade = self.Q_(1, unidade)
            return str(quantidade.dimensionality)
        except UndefinedUnitError as e:
            raise ValueError(f"Unidade '{unidade}' não reconhecida: {e}") from e
    
    def verificar_compatibilidade(self, de_unidade, para_unidade):
        """
        Verifica se duas unidades são dimensionalmente compatíveis
        """
        try:
            quantidade1 = self.Q_(1, de_unidade)
            quantidade2 = self.Q_(1, para_unidade)
            return quantidade1.dimensionality == quantidade2.dimensionality
        except UndefinedUnitError as e:
            raise ValueError(f"Unidade não reconhecida: {e}") from e

    def converter_diametro(self, valor, de_unidade, para_unidade):
        """
        Converte valores de diâmetro entre diferentes unidades
        """
        return self.converter_comprimento(valor, de_unidade, para_unidade)

    def converter_comprimento(self, valor, de_unidade, para_unidade):
        """
        Converte valores de comprimento entre diferentes unidades
        """
        try:
            self._validar_unidades(de_unidade, para_unidade, 'comprimento')
            quantidade = self.Q_(valor, de_unidade)
            resultado = quantidade.to(para_unidade).magnitude
            return resultado
        except (DimensionalityError, UndefinedUnitError, ValueError) as e:
            raise ValueError(f"Erro na conversão de comprimento: {e}") from e

    # Atualizar a lista de unidades suportadas
    def get_unidades_comprimento(self):
        """Retorna lista de unidades de comprimento suportadas"""
        return ['m', 'cm', 'mm', 'km', 'in', 'ft', 'yd', 'mi']