import math
import logging
from typing import Optional
from CoolProp.CoolProp import PropsSI
from scipy.constants import g

# Configurar logging
logger = logging.getLogger(__name__)

class Perdas:
    def __init__(self, vazao_m3s: Optional[float] = None, 
                diametro_m: Optional[float] = None,
                area: Optional[float] = None,
                material_darcy: Optional[str] = None,
                material_hazen: Optional[str] = None,
                gravidade_ms2: Optional[float] = g):
        
        # Valores padrão seguros para evitar erros de inicialização
        self.diametro_m = diametro_m if diametro_m is not None and diametro_m > 0 else 0.1
        self.area = area if area is not None and area > 0 else 0.007854  # Área padrão para diâmetro 0.1m
        self.vazao_m3s = vazao_m3s
        self.gravidade_ms2 = gravidade_ms2

        self.material_darcy = material_darcy
        self.material_hazen = material_hazen
        self.acessorios_k = {}

        self.velocidade_ms = 0.0  # Inicializar com um valor padrão
        if self.vazao_m3s is not None and self.area is not None and self.area > 0:
            self.calcular_velocidade()

    # ---------- Métodos de listagem ----------
    @staticmethod
    def get_lista_materiais_darcy():
        return list(Perdas._rugosidade_darcy_mm().keys())

    @staticmethod
    def get_lista_materiais_hazen():
        return list(Perdas._fator_c_hazen_williams().keys())

    @staticmethod
    def get_lista_acessorios():
        return list(Perdas._fator_localizadas().keys())

    # ---------- Definições ----------
    def definir_material_darcy(self, material):
        self.material_darcy = material

    def definir_material_hazen(self, material):
        self.material_hazen = material

    def definir_acessorios(self, acessorios_dict):
        """Define manualmente acessórios no formato {tipo: quantidade}"""
        self.acessorios_k = acessorios_dict

    def definir_acessorios_lista(self, lista_acessorios):
        """
        Recebe uma lista de acessórios no formato:
        [{'id':..., 'tipo':..., 'cor':...}, ...]
        e converte para {tipo: quantidade} para uso no cálculo.
        """
        acessorios_dict = {}

        mapa_equivalencia = {
            "curva-22-5": "Curva de 22.5",
            "curva-45": "Curva 45",
            "curva-90": "Curva 90",
            "cotovelo-ou-joelho-45": "Cotovelo ou joelho de 45",
            "cotovelo-ou-joelho-90": "Cotovelo ou joelho de 90",
            "ampliacao-gradual": "Ampliação Gradual",
            "entrada-normal": "Entrada Normal",
            "entrada-de-borda": "Entrada de Borda",
            "saida-livre": "Saída de Canalização",
            "crivo": "Crivo",
            "controlador-de-vazao": "Controlador de Vazão",
            "medidor-venturi": "Medidor Venturi",
            "comporta-aberta": "Comporta Aberta",
            "juncao": "Junção",
            "pequena-derivacao": "Pequena Derivação"
        }

        for acessorio in lista_acessorios:
            tipo = acessorio["tipo"].lower()
            if tipo in mapa_equivalencia:
                nome_normalizado = mapa_equivalencia[tipo]
                acessorios_dict[nome_normalizado] = acessorios_dict.get(nome_normalizado, 0) + 1
            else:
                print(f"Acessório '{tipo}' não encontrado na base de fatores.")

        self.acessorios_k = acessorios_dict

    # ---------- Método para atualizar parâmetros ----------
    def atualizar_parametros(self, diametro_m: float = None, area: float = None, vazao_m3s: float = None):
        """Atualiza os parâmetros principais para recálculo."""
        if diametro_m is not None and diametro_m > 0:
            self.diametro_m = diametro_m
        if area is not None and area > 0:
            self.area = area
        if vazao_m3s is not None:
            self.vazao_m3s = vazao_m3s
            if self.area and self.area > 0:
                self.calcular_velocidade()

    # ---------- Cálculos hidráulicos ----------

    def calcular_velocidade(self):
        """Calcula velocidade com proteção contra divisão por zero."""
        if self.vazao_m3s is None or self.area <= 1e-9:
            self.velocidade_ms = 1e-6  # Velocidade mínima para evitar problemas
            return self.velocidade_ms
            
        try:
            self.velocidade_ms = self.vazao_m3s / self.area
            # Limitar velocidade a um valor mínimo seguro
            self.velocidade_ms = max(self.velocidade_ms, 1e-6)
            return self.velocidade_ms
        except ZeroDivisionError:
            self.velocidade_ms = 1e-6
            return self.velocidade_ms

    def calcular_viscosidade_cinematica(self):
        T = 293.15
        fluido = "Water"
        viscosidade_dinamica = PropsSI("V", "T", T, "P", 101325, fluido)
        densidade = PropsSI("D", "T", T, "P", 101325, fluido)
        return viscosidade_dinamica / densidade

    def calcular_numero_reynolds(self):
        try:
            return (self.velocidade_ms * self.diametro_m) / self.calcular_viscosidade_cinematica()
        except (ValueError, ZeroDivisionError):
            return 1e6  # Valor padrão seguro

    def calcular_fator_atrito_churchill(self):
        if self.material_darcy not in self._rugosidade_darcy_mm():
            raise ValueError(f"Material '{self.material_darcy}' inválido.")
        rugosidade = self._rugosidade_darcy_mm()[self.material_darcy] / 1000
        Re = self.calcular_numero_reynolds()
        epsilon_D = rugosidade / self.diametro_m
        A = (2.457 * math.log(1 / (((7 / Re)**0.9) + 0.27 * epsilon_D)))**16
        B = (37530 / Re)**16
        return 8 * ((8 / Re)**12 + (A + B)**(-1.5))**(1/12)

    def calcular_perda_carga_darcy(self, comprimento_m: Optional[float] = None):
        """Calcula perda de carga usando Darcy-Weisbach com proteção contra erros."""
        try:
            # Validações de segurança
            if comprimento_m is None or comprimento_m <= 1e-6:
                return 0.0
                
            if self.diametro_m <= 1e-6 or self.vazao_m3s <= 1e-9:
                return 0.0
                
            f = self.calcular_fator_atrito_churchill()
            velocidade = self.calcular_velocidade()
            
            # Cálculo seguro
            perda = f * (comprimento_m / self.diametro_m) * (velocidade**2 / (2 * self.gravidade_ms2))
            
            # Garantir resultado válido
            if math.isnan(perda) or math.isinf(perda) or perda < 0:
                return 0.0
                
            return perda
            
        except Exception as e:
            logger.warning(f"Erro no cálculo Darcy-Weisbach: {e}")
            return 0.0

    def calcular_perdas_localizadas(self):
        total_k = 0
        for acessorio, qtd in self.acessorios_k.items():
            if acessorio not in self._fator_localizadas():
                logger.warning(f"Acessório '{acessorio}' não encontrado na base de fatores.")
                continue
            total_k += self._fator_localizadas()[acessorio] * qtd
        try:
            return total_k * (self.velocidade_ms**2 / (2 * self.gravidade_ms2))
        except (ValueError, ZeroDivisionError):
            return 0.0

    def calcular_perda_carga_hazen_williams(self, comprimento_m: Optional[float] = None):
        """
        Calcula perda de carga usando Hazen-Williams com proteção completa contra erros numéricos.
        """
        # VALIDAÇÃO ROBUSTA - Verifica todos os parâmetros críticos
        if self.material_hazen not in self._fator_c_hazen_williams():
            logger.warning(f"Material '{self.material_hazen}' inválido para Hazen-Williams.")
            return 0.0
        
        # Proteção contra valores zero ou negativos
        if comprimento_m is None or comprimento_m <= 1e-6:
            return 0.0  # Sem comprimento, sem perda
        
        if self.diametro_m is None or self.diametro_m <= 1e-6:
            logger.warning(f"Diâmetro inválido para cálculo: {self.diametro_m}")
            return 0.0
        
        if self.vazao_m3s is None or self.vazao_m3s < 1e-9:
            return 0.0  # Vazão insignificante, perda zero

        c = self._fator_c_hazen_williams()[self.material_hazen]
        
        # Proteção adicional contra coeficiente C zero ou negativo
        if c <= 1e-6:
            logger.warning(f"Coeficiente C inválido: {c}")
            return 0.0
        
        K = 10.675
        d = self.diametro_m
        
        # CÁLCULO SEGURO com tratamento de exceções
        try:
            # Garante que o diâmetro seja um valor mínimo seguro
            d_seguro = max(d, 1e-4)  # Diâmetro mínimo de 0.1mm para evitar underflow
            
            termo_diametro = d_seguro ** 4.87
            # Evita underflow em vazões muito pequenas
            vazao_segura = max(self.vazao_m3s, 1e-9)
            termo_vazao_coeficiente = (vazao_segura / c) ** 1.852
            
            perda_carga = comprimento_m * (K / termo_diametro) * termo_vazao_coeficiente
            
            # Verifica se o resultado é numérico válido e não negativo
            if math.isnan(perda_carga) or math.isinf(perda_carga) or perda_carga < 0:
                logger.warning(f"Resultado numérico inválido: {perda_carga}")
                return 0.0
                
            return perda_carga
            
        except (ZeroDivisionError, OverflowError, ValueError) as e:
            logger.warning(f"Erro numérico no cálculo Hazen-Williams: {e}")
            return 0.0
        except Exception as e:
            logger.error(f"Erro inesperado no cálculo Hazen-Williams: {e}")
            return 0.0
     
    # ---------- Bases de dados ----------
    @staticmethod
    def _rugosidade_darcy_mm():
        return {
            "Aço comercial novo": 0.045, "Aço laminado novo": 0.075,
            "Aço soldado novo": 0.075, "Aço soldado limpo, usado": 0.175,
            "Aço soldado moderadamente oxidado": 0.4,
            "Aço soldado revestido de cimento centrifugado": 0.1,
            "Aço laminado revestido de asfalto": 0.05,
            "Ferro fundido novo": 0.375, "Ferro fundido com leve oxidação": 0.3,
            "Ferro fundido velho": 1.25, "Ferro fundido centrifugado": 0.05,
            "Ferro fundido com revestimento asfáltico": 0.1,
            "Aço galvanizado, sem costura": 0.105, "Aço galvanizado, com costura": 0.175,
            "Concreto armado liso (vários anos de uso)": 0.25,
            "Concreto com acabamento normal": 2.0, "Concreto protendido Freyssinet": 0.04,
            "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados": 0.005,
            "Cimento amianto novo": 0.0875, "Vidro": 0.0002
        }

    @staticmethod
    def _fator_c_hazen_williams():
        return {
            'Aço Corrugado(chapa ondulada)': 60, 'Aço Galvanizado': 125,
            'Aço Rebitado em uso': 85, 'Aço soldado novo': 130,
            'Aço Soldado com revestimento especial': 130, 'Chumbo': 130,
            'Aço Soldado em uso': 90, 'Ferro Fundido Usado': 90,
            'Concreto com acabamento comum': 120, 'Ferro Fundido Revestido de Cimento': 130,
            'Latão': 130, 'Ferro Fundido novo': 130, 'Cobre': 130,
            'Manilha Cerâmica vidrada': 110, 'Aço Rebitado novo': 110,
            'Tijolos em executados': 100, 'Ferro Fundido de 15 a 20 anos de uso': 100,
            'Vidro': 140, 'Plástico': 140, 'Cimento Amianto': 140
        }

    @staticmethod
    def _fator_localizadas():
        return {
            "Ampliação Gradual": 0.30, "Comporta Aberta": 1, "Controlador de Vazão": 2.5,
            "Cotovelo ou joelho de 45": 0.4, "Cotovelo ou joelho de 90": 0.9,
            "Crivo": 0.75, "Curva de 22.5": 0.1, "Curva 45": 0.2, "Curva 90": 0.4,
            "Entrada de Borda": 1, "Entrada Normal": 0.5, "Junção": 0.4,
            "Medidor Venturi": 2.5, "Pequena Derivação": 0.02, "Redução Gradual": 0.15,
            "Saída de Canalização": 1, "Tê de Passagem directa": 0.6,
            "Tê de saida Bilateral": 1.80, "Tê de saida de lado": 1.3,
            "Válvula Borboleta": 0.3, "Válvula de ângulo aberta": 5,
            "Válvula de gaveta aberta": 0.2, "Válvula de pé": 1.75,
            "Válvula de retenção": 2.5, "Válvula globo aberta": 10,
        }