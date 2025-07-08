
import math
from CoolProp.CoolProp import PropsSI
from collections import ChainMap

class Perdas:
    def __init__(self, diametro_mm, comprimento_m, material_darcy, 
                 vazao_m3s=None, velocidade_ms=None,
                 gravidade_ms2=9.81):

        self.diametro_mm = diametro_mm
        self.diametro_m = diametro_mm / 1000.0
        self.comprimento_m = comprimento_m
        self.material_darcy = material_darcy
        self.gravidade_ms2 = gravidade_ms2

        T = 293.15  # 20°C   Temperatura em Kelvin's
        fluido = "Water"
        # Obtemos as propriedades
        viscosidade_dinamica = PropsSI("V", "T", T, "P", 101325, fluido)  # [Pa·s]
        densidade = PropsSI("D", "T", T, "P", 101325, fluido)             # [kg/m³]
        self.viscosidade_cinematica_m2s = viscosidade_dinamica / densidade         # [m²/s]

        self.fator_localizadas = {
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

        self.fator_c_hazen_wiliams = {
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

        self.rugosidade_darcy_mm = {
            "Aço": {
                "Aço comercial novo": 0.045, "Aço laminado novo": 0.075,
                "Aço soldado novo": 0.075, "Aço soldado limpo, usado": 0.175,
                "Aço soldado moderadamente oxidado": 0.4,
                "Aço soldado revestido de cimento centrifugado": 0.1,
                "Aço laminado revestido de asfalto": 0.05
            },
            "Ferro Fundido": {
                "Ferro fundido novo": 0.375, "Ferro fundido com leve oxidação": 0.3,
                "Ferro fundido velho": 1.25, "Ferro fundido centrifugado": 0.05,
                "Ferro fundido com revestimento asfáltico": 0.16
            },
            "Aço Galvanizado": {
                "Aço galvanizado, sem costura": 0.105, "Aço galvanizado, com costura": 0.175
            },
            "Concreto": {
                "Concreto armado liso (vários anos de uso)": 0.25,
                "Concreto com acabamento normal": 2.0, "Concreto protendido Freyssinet": 0.04
            },
            "Outros Materiais": {
                "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados": 0.005,
                "Cimento amianto novo": 0.0875, "Vidro": 0.0002
            }
        }

        self.area_secao_m2 = math.pi * (self.diametro_m / 2)**2

        if vazao_m3s is not None:
            self.vazao_m3s = vazao_m3s
            self.velocidade_ms = vazao_m3s / self.area_secao_m2
        elif velocidade_ms is not None:
            self.velocidade_ms = velocidade_ms
            self.vazao_m3s = velocidade_ms * self.area_secao_m2
        else:
            raise ValueError("Forneça a vazão ou a velocidade.")

        if self.velocidade_ms <= 0:
            raise ValueError("A velocidade deve ser positiva.")

        # Flatten rugosidade
        self.rugosidade_lookup_mm = dict(ChainMap(*self.rugosidade_darcy_mm.values()))
        self.rugosidade_abs_m = self.rugosidade_lookup_mm.get(material_darcy)
        if self.rugosidade_abs_m is None:
            raise ValueError(f"Material '{material_darcy}' não encontrado.")
        self.rugosidade_abs_m /= 1000.0

        if self.viscosidade_cinematica_m2s is None or self.viscosidade_cinematica_m2s <= 0:
            raise ValueError("A viscosidade cinemática deve ser positiva.")

    def calcular_numero_reynolds(self):
        return (self.velocidade_ms * self.diametro_m) / self.viscosidade_cinematica_m2s

    def calcular_fator_atrito_churchill(self):
        """
        Calcula o fator de atrito de Darcy-Weisbach usando a equação de Churchill.
        Válido para todos os regimes de escoamento (laminar, transição e turbulento).
        """
        Re = self.calcular_numero_reynolds()
        epsilon_D = self.rugosidade_abs_m / self.diametro_m

        try:
            A = (2.457 * math.log(1 / (((7 / Re)**0.9) + 0.27 * epsilon_D)))**16
            B = (37530 / Re)**16
            f = 8 * ((8 / Re)**12 + (A + B)**(-1.5))**(1/12)
            return f
        except Exception as e:
            return float('nan')

    def calcular_perda_carga_darcy(self):
        f = self.calcular_fator_atrito_churchill()
        return f * (self.comprimento_m / self.diametro_m) * (self.velocidade_ms**2 / (2 * self.gravidade_ms2))

    def calcular_perdas_localizadas(self, acessorios_k_values):
        total_k = 0
        for acessorio, qtd in acessorios_k_values.items():
            if acessorio not in self.fator_localizadas:
                raise ValueError(f"Acessório '{acessorio}' inválido.")
            total_k += self.fator_localizadas[acessorio] * qtd
        return total_k * (self.velocidade_ms**2 / (2 * self.gravidade_ms2))

    def calcular_perda_carga_hazen_williams(self, material_hazen, comprimento_1, comprimento_2, vazao_m3s):
        c = self.fator_c_hazen_wiliams.get(material_hazen)
        if c is None:
            raise ValueError(f"Material '{material_hazen}' não encontrado.")
        K = 10.675
        d = self.diametro_m
        hf1 = comprimento_1 * (K / d**4.87) * (vazao_m3s / c)**1.852
        hf2 = comprimento_2 * (K / d**4.87) * (vazao_m3s / c)**1.852
        return hf1 + hf2
