"""Cálculo de perdas de carga do AquaPump.

Mantém a API utilizada pelo main.py e acrescenta suporte aos dados detalhados
emitidos pelo editor JavaScript:
    {id, tipo, nome, cor, diametro_dn, posicao_m, orientacao,
     estado, coeficiente_k}

As perdas localizadas são calculadas por componente, usando o K configurado
para esse componente e o seu DN quando disponível. Quando não há DN definido,
usa-se o diâmetro geral do sistema.

Nota hidráulica: uma válvula marcada como fechada não é representada por um K
finito. O componente é excluído da soma de perdas e fica registado um aviso de
configuração inválida para o escoamento contínuo. A rede actual ainda não tem
um solver topológico para calcular caudal nulo/redistribuído em redes fechadas
ou ramificadas.
"""

from __future__ import annotations

import logging
import math
import unicodedata
from typing import Optional

try:
    from CoolProp.CoolProp import PropsSI
except ImportError:  # Permite executar testes e fallback sem CoolProp instalado.
    PropsSI = None

try:
    from scipy.constants import g
except ImportError:  # Valor convencional da aceleração gravítica (m/s²).
    g = 9.80665

logger = logging.getLogger(__name__)


class Perdas:
    """Calcula perdas distribuídas e localizadas numa conduta.

    Unidades internas:
      - caudal: m³/s
      - diâmetro: m
      - área: m²
      - comprimento: m
      - perdas: m de coluna de água
      - DN recebido do JavaScript: mm
    """

    def __init__(
        self,
        vazao_m3s: Optional[float] = None,
        diametro_m: Optional[float] = None,
        area: Optional[float] = None,
        material_darcy: Optional[str] = None,
        material_hazen: Optional[str] = None,
        gravidade_ms2: Optional[float] = g,
    ):
        self.diametro_m = self._numero_positivo(diametro_m, 0.1)
        area_padrao = math.pi * self.diametro_m**2 / 4.0
        self.area = self._numero_positivo(area, area_padrao)
        self.vazao_m3s = self._numero_nao_negativo(vazao_m3s, 0.0)
        self.gravidade_ms2 = self._numero_positivo(gravidade_ms2, 9.80665)

        self.material_darcy = material_darcy
        self.material_hazen = material_hazen

        # Compatibilidade: dicionário de quantidades por nome normalizado.
        self.acessorios_k: dict[str, int] = {}
        # Dados detalhados enviados pelo editor JavaScript.
        self.acessorios_detalhados: list[dict] = []
        self.avisos_acessorios: list[str] = []
        self.configuracao_acessorios_valida = True

        self.velocidade_ms = 0.0
        self.calcular_velocidade()

    # ------------------------------------------------------------------
    # Conversão e normalização
    # ------------------------------------------------------------------
    @staticmethod
    def _numero_finito(valor, padrao=None):
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            return padrao
        return numero if math.isfinite(numero) else padrao

    @classmethod
    def _numero_positivo(cls, valor, padrao):
        numero = cls._numero_finito(valor)
        return numero if numero is not None and numero > 0 else float(padrao)

    @classmethod
    def _numero_nao_negativo(cls, valor, padrao):
        numero = cls._numero_finito(valor)
        return numero if numero is not None and numero >= 0 else float(padrao)

    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        texto = str(valor or "").strip().lower()
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        texto = texto.replace("_", "-").replace(" ", "-")
        while "--" in texto:
            texto = texto.replace("--", "-")
        return texto

    # ------------------------------------------------------------------
    # Listagens públicas
    # ------------------------------------------------------------------
    @staticmethod
    def get_lista_materiais_darcy():
        return list(Perdas._rugosidade_darcy_mm().keys())

    @staticmethod
    def get_lista_materiais_hazen():
        return list(Perdas._fator_c_hazen_williams().keys())

    @staticmethod
    def get_lista_acessorios():
        return list(Perdas._fator_localizadas().keys())

    # ------------------------------------------------------------------
    # Configuração de materiais e acessórios
    # ------------------------------------------------------------------
    def definir_material_darcy(self, material):
        self.material_darcy = material

    def definir_material_hazen(self, material):
        self.material_hazen = material

    def definir_acessorios(self, acessorios_dict):
        """Define acessórios no formato legado ``{nome: quantidade}``.

        Também aceita uma lista detalhada, encaminhando-a para
        :meth:`definir_acessorios_lista`.
        """
        if isinstance(acessorios_dict, list):
            self.definir_acessorios_lista(acessorios_dict)
            return
        if not isinstance(acessorios_dict, dict):
            raise TypeError("Os acessórios devem ser uma lista ou um dicionário.")

        normalizados: dict[str, int] = {}
        self.avisos_acessorios = []
        self.configuracao_acessorios_valida = True
        for nome, quantidade in acessorios_dict.items():
            canonico = self._resolver_acessorio(nome)
            if canonico is None:
                aviso = f"Acessório não reconhecido: {nome!r}."
                self.avisos_acessorios.append(aviso)
                logger.warning(aviso)
                continue
            qtd_num = self._numero_finito(quantidade, 0)
            if qtd_num is None or qtd_num < 0:
                aviso = f"Quantidade inválida para {canonico}: {quantidade!r}."
                self.avisos_acessorios.append(aviso)
                logger.warning(aviso)
                continue
            qtd = int(qtd_num)
            if qtd:
                normalizados[canonico] = normalizados.get(canonico, 0) + qtd

        self.acessorios_k = normalizados
        self.acessorios_detalhados = []

    def definir_acessorios_lista(self, lista_acessorios):
        """Recebe a lista do QWebChannel e normaliza os 25 acessórios.

        Campos aceites (os restantes são ignorados):
          ``tipo`` ou ``type``; ``diametro_dn`` ou ``dn`` (mm);
          ``coeficiente_k`` ou ``k``; ``estado`` ou ``status``.

        Se K não vier indicado, é usado o valor de referência da tabela interna.
        Um K personalizado não altera a tabela global: aplica-se apenas à peça.
        """
        if lista_acessorios is None:
            lista_acessorios = []
        if not isinstance(lista_acessorios, (list, tuple)):
            raise TypeError("A lista de acessórios recebida deve ser uma lista.")

        agregados: dict[str, int] = {}
        detalhados: list[dict] = []
        avisos: list[str] = []
        configuracao_valida = True

        for indice, item in enumerate(lista_acessorios):
            if not isinstance(item, dict):
                aviso = f"Elemento de acessório na posição {indice} não é um objecto válido."
                avisos.append(aviso)
                logger.warning(aviso)
                continue

            tipo_original = item.get("tipo", item.get("type", ""))
            canonico = self._resolver_acessorio(tipo_original)
            if canonico is None:
                aviso = f"Acessório '{tipo_original}' não reconhecido; ignorado no cálculo."
                avisos.append(aviso)
                logger.warning(aviso)
                continue

            k_base = self._fator_localizadas()[canonico]
            k_recebido = item.get("coeficiente_k", item.get("k", None))
            k_personalizado = self._numero_finito(k_recebido)
            if k_personalizado is None:
                k = float(k_base)
                if k_recebido not in (None, ""):
                    aviso = f"K inválido em {canonico}; usado o valor de referência {k_base:g}."
                    avisos.append(aviso)
                    logger.warning(aviso)
            elif k_personalizado < 0:
                k = float(k_base)
                aviso = f"K negativo em {canonico}; usado o valor de referência {k_base:g}."
                avisos.append(aviso)
                logger.warning(aviso)
            else:
                k = float(k_personalizado)

            dn_recebido = item.get(
                "diametro_dn", item.get("dn", item.get("diametro_nominal", None))
            )
            dn_mm = self._numero_finito(dn_recebido)
            if dn_mm is not None and dn_mm <= 0:
                aviso = f"DN inválido em {canonico}; usado o diâmetro geral do sistema."
                avisos.append(aviso)
                logger.warning(aviso)
                dn_mm = None

            estado_raw = item.get("estado", item.get("status", "normalmente aberto"))
            estado = self._normalizar_texto(estado_raw)
            fechado = estado in {"fechado", "fechada", "closed"}
            if fechado:
                configuracao_valida = False
                aviso = (
                    f"{canonico} está fechado. O modelo actual não calcula o bloqueio "
                    "do escoamento; o componente não foi tratado como uma perda K finita."
                )
                avisos.append(aviso)
                logger.warning(aviso)
            elif estado in {"parcialmente-aberto", "parcialmente-aberta", "partially-open"}:
                aviso = (
                    f"{canonico} está parcialmente aberto; foi usado K={k:g}. "
                    "Confirme este K com os dados do fabricante ou uma tabela técnica."
                )
                avisos.append(aviso)
                logger.info(aviso)

            entrada = {
                "id": item.get("id", f"acessorio_{indice + 1}"),
                "tipo": canonico,
                "k": k,
                "dn_mm": dn_mm,
                "estado": estado,
                "fechado": fechado,
            }
            detalhados.append(entrada)
            agregados[canonico] = agregados.get(canonico, 0) + 1

        self.acessorios_k = agregados
        self.acessorios_detalhados = detalhados
        self.avisos_acessorios = avisos
        self.configuracao_acessorios_valida = configuracao_valida

    def obter_avisos_acessorios(self) -> list[str]:
        """Devolve uma cópia dos avisos da última configuração recebida."""
        return list(self.avisos_acessorios)

    @classmethod
    def _resolver_acessorio(cls, valor) -> Optional[str]:
        """Converte slugs do JavaScript e nomes antigos para nomes da tabela K."""
        chave = cls._normalizar_texto(valor)
        aliases = {
            # Transições
            "ampliacao-gradual": "Ampliação Gradual",
            "reducao-gradual": "Redução Gradual",
            # Válvulas / controlo
            "comporta-aberta": "Comporta Aberta",
            "controlador-de-vazao": "Controlador de Vazão",
            "valvula-borboleta": "Válvula Borboleta",
            "valvula-angulo-aberta": "Válvula de ângulo aberta",
            "valvula-de-angulo-aberta": "Válvula de ângulo aberta",
            "valvula-gaveta-aberta": "Válvula de gaveta aberta",
            "valvula-de-gaveta-aberta": "Válvula de gaveta aberta",
            "valvula-de-pe": "Válvula de pé",
            "valvula-pe": "Válvula de pé",
            "valvula-de-retencao": "Válvula de retenção",
            "valvula-retencao": "Válvula de retenção",
            "valvula-globo-aberta": "Válvula globo aberta",
            "valvula-de-globo-aberta": "Válvula globo aberta",
            # Curvas e cotovelos
            "cotovelo-45": "Cotovelo ou joelho de 45",
            "cotovelo-ou-joelho-45": "Cotovelo ou joelho de 45",
            "cotovelo-90": "Cotovelo ou joelho de 90",
            "cotovelo-ou-joelho-90": "Cotovelo ou joelho de 90",
            "curva-22-5": "Curva de 22.5",
            "curva-de-22-5": "Curva de 22.5",
            "curva-45": "Curva 45",
            "curva-90": "Curva 90",
            # Entradas, saídas e outros
            "crivo": "Crivo",
            "entrada-de-borda": "Entrada de Borda",
            "entrada-normal": "Entrada Normal",
            "juncao": "Junção",
            "medidor-venturi": "Medidor Venturi",
            "pequena-derivacao": "Pequena Derivação",
            "saida-livre": "Saída de Canalização",
            "saida-de-canalizacao": "Saída de Canalização",
            "saida-de-canalizacao-livre": "Saída de Canalização",
            "te-passagem-directa": "Tê de Passagem directa",
            "te-passagem-direta": "Tê de Passagem directa",
            "te-saida-bilateral": "Tê de saida Bilateral",
            "te-saida-de-lado": "Tê de saida de lado",
        }
        if chave in aliases:
            return aliases[chave]

        # Aceita também os nomes legados, com ou sem acentos.
        for nome in cls._fator_localizadas():
            if cls._normalizar_texto(nome) == chave:
                return nome
        return None

    # ------------------------------------------------------------------
    # Actualização dos parâmetros do escoamento
    # ------------------------------------------------------------------
    def atualizar_parametros(
        self,
        diametro_m: float = None,
        area: float = None,
        vazao_m3s: float = None,
    ):
        """Actualiza diâmetro, área e/ou caudal em unidades SI."""
        if diametro_m is not None:
            self.diametro_m = self._numero_positivo(diametro_m, self.diametro_m)
        if area is not None:
            self.area = self._numero_positivo(area, self.area)
        elif diametro_m is not None:
            self.area = math.pi * self.diametro_m**2 / 4.0
        if vazao_m3s is not None:
            self.vazao_m3s = self._numero_nao_negativo(vazao_m3s, self.vazao_m3s)
        self.calcular_velocidade()

    # ------------------------------------------------------------------
    # Propriedades do fluido e escoamento
    # ------------------------------------------------------------------
    def calcular_velocidade(self):
        """Calcula a velocidade média na secção geral da tubulação (m/s)."""
        if self.vazao_m3s is None or self.vazao_m3s <= 0 or self.area <= 0:
            self.velocidade_ms = 0.0
        else:
            self.velocidade_ms = self.vazao_m3s / self.area
        return self.velocidade_ms

    def calcular_viscosidade_cinematica(self):
        """Viscosidade cinemática da água a 20 °C e 1 atm (m²/s)."""
        if PropsSI is None:
            logger.warning(
                "CoolProp não está instalado; usada viscosidade aproximada da água a 20 °C."
            )
            return 1.004e-6
        temperatura = 293.15
        fluido = "Water"
        viscosidade_dinamica = PropsSI("V", "T", temperatura, "P", 101325, fluido)
        densidade = PropsSI("D", "T", temperatura, "P", 101325, fluido)
        if densidade <= 0:
            raise ValueError("Densidade do fluido inválida.")
        return viscosidade_dinamica / densidade

    def calcular_numero_reynolds(self):
        if self.velocidade_ms <= 0 or self.diametro_m <= 0:
            return 0.0
        try:
            nu = self.calcular_viscosidade_cinematica()
            return (self.velocidade_ms * self.diametro_m) / nu if nu > 0 else 0.0
        except Exception as exc:
            logger.warning("Não foi possível calcular o número de Reynolds: %s", exc)
            return 0.0

    def calcular_fator_atrito_churchill(self):
        if self.material_darcy not in self._rugosidade_darcy_mm():
            raise ValueError(f"Material '{self.material_darcy}' inválido.")
        reynolds = self.calcular_numero_reynolds()
        if reynolds <= 0:
            return 0.0
        rugosidade = self._rugosidade_darcy_mm()[self.material_darcy] / 1000.0
        epsilon_d = rugosidade / self.diametro_m
        termo_log = (7.0 / reynolds) ** 0.9 + 0.27 * epsilon_d
        if termo_log <= 0:
            raise ValueError("Parâmetros inválidos para o factor de atrito.")
        a = (2.457 * math.log(1.0 / termo_log)) ** 16
        b = (37530.0 / reynolds) ** 16
        return 8.0 * ((8.0 / reynolds) ** 12 + (a + b) ** -1.5) ** (1.0 / 12.0)

    # ------------------------------------------------------------------
    # Perdas distribuídas
    # ------------------------------------------------------------------
    def calcular_perda_carga_darcy(self, comprimento_m: Optional[float] = None):
        """Calcula a perda distribuída por Darcy-Weisbach (m)."""
        comprimento = self._numero_finito(comprimento_m)
        if comprimento is None or comprimento <= 0 or self.vazao_m3s <= 0:
            return 0.0
        if self.diametro_m <= 0 or self.gravidade_ms2 <= 0:
            return 0.0
        try:
            fator = self.calcular_fator_atrito_churchill()
            velocidade = self.calcular_velocidade()
            perda = fator * (comprimento / self.diametro_m) * (
                velocidade**2 / (2.0 * self.gravidade_ms2)
            )
            return perda if math.isfinite(perda) and perda >= 0 else 0.0
        except (ArithmeticError, ValueError, TypeError) as exc:
            logger.warning("Erro no cálculo Darcy-Weisbach: %s", exc)
            return 0.0

    def calcular_perdas_localizadas(self):
        """Calcula a soma das perdas localizadas (m de coluna de água).

        Para acessórios enviados pelo editor, aplica individualmente:
            h_local = K * V_DN² / (2g)
        usando o DN do componente (mm). Se o componente não tiver DN, utiliza
        o diâmetro global da conduta. A API legada continua a usar a velocidade
        global e as quantidades do dicionário ``acessorios_k``.
        """
        if self.vazao_m3s <= 0 or self.gravidade_ms2 <= 0:
            return 0.0

        total_perda = 0.0
        if self.acessorios_detalhados:
            for acessorio in self.acessorios_detalhados:
                if acessorio["fechado"]:
                    # Não atribuir artificialmente um K finito a uma válvula fechada.
                    continue
                k = acessorio["k"]
                dn_mm = acessorio["dn_mm"]
                diametro = (dn_mm / 1000.0) if dn_mm is not None else self.diametro_m
                if diametro <= 0:
                    aviso = f"Diâmetro inválido no acessório {acessorio['id']}; ignorado."
                    self.avisos_acessorios.append(aviso)
                    logger.warning(aviso)
                    continue
                area_local = math.pi * diametro**2 / 4.0
                velocidade_local = self.vazao_m3s / area_local
                perda = k * velocidade_local**2 / (2.0 * self.gravidade_ms2)
                if math.isfinite(perda) and perda >= 0:
                    total_perda += perda
                else:
                    aviso = f"Perda localizada inválida no acessório {acessorio['id']}; ignorada."
                    self.avisos_acessorios.append(aviso)
                    logger.warning(aviso)
        else:
            # Compatibilidade com chamadas antigas: {nome: quantidade}.
            velocidade = self.calcular_velocidade()
            soma_k = 0.0
            tabela = self._fator_localizadas()
            for nome, quantidade in self.acessorios_k.items():
                k = tabela.get(nome)
                if k is None:
                    logger.warning("Acessório '%s' não encontrado na base de factores.", nome)
                    continue
                qtd = self._numero_finito(quantidade, 0.0)
                if qtd is not None and qtd > 0:
                    soma_k += k * qtd
            total_perda = soma_k * velocidade**2 / (2.0 * self.gravidade_ms2)

        if not math.isfinite(total_perda) or total_perda < 0:
            logger.warning("Resultado inválido no cálculo de perdas localizadas.")
            return 0.0
        return total_perda

    # ------------------------------------------------------------------
    # Perdas distribuídas — Hazen-Williams
    # ------------------------------------------------------------------
    def calcular_perda_carga_hazen_williams(self, comprimento_m: Optional[float] = None):
        """Calcula a perda distribuída por Hazen-Williams (m)."""
        tabela_c = self._fator_c_hazen_williams()
        if self.material_hazen not in tabela_c:
            logger.warning("Material '%s' inválido para Hazen-Williams.", self.material_hazen)
            return 0.0

        comprimento = self._numero_finito(comprimento_m)
        if comprimento is None or comprimento <= 0:
            return 0.0
        if self.diametro_m <= 0 or self.vazao_m3s <= 0:
            return 0.0

        coeficiente_c = tabela_c[self.material_hazen]
        if coeficiente_c <= 0:
            logger.warning("Coeficiente C inválido: %s", coeficiente_c)
            return 0.0

        # Forma SI: Q em m³/s, D em m e L em m.
        constante = 10.675
        try:
            perda = comprimento * (constante / self.diametro_m**4.87) * (
                self.vazao_m3s / coeficiente_c
            ) ** 1.852
            return perda if math.isfinite(perda) and perda >= 0 else 0.0
        except (ArithmeticError, ValueError, OverflowError) as exc:
            logger.warning("Erro numérico no cálculo Hazen-Williams: %s", exc)
            return 0.0

    # ------------------------------------------------------------------
    # Bases de dados
    # ------------------------------------------------------------------
    @staticmethod
    def _rugosidade_darcy_mm():
        return {
            "Aço comercial novo": 0.045,
            "Aço laminado novo": 0.075,
            "Aço soldado novo": 0.075,
            "Aço soldado limpo, usado": 0.175,
            "Aço soldado moderadamente oxidado": 0.4,
            "Aço soldado revestido de cimento centrifugado": 0.1,
            "Aço laminado revestido de asfalto": 0.05,
            "Ferro fundido novo": 0.375,
            "Ferro fundido com leve oxidação": 0.3,
            "Ferro fundido velho": 1.25,
            "Ferro fundido centrifugado": 0.05,
            "Ferro fundido com revestimento asfáltico": 0.1,
            "Aço galvanizado, sem costura": 0.105,
            "Aço galvanizado, com costura": 0.175,
            "Concreto armado liso (vários anos de uso)": 0.25,
            "Concreto com acabamento normal": 2.0,
            "Concreto protendido Freyssinet": 0.04,
            "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados": 0.005,
            "Cimento amianto novo": 0.0875,
            "Vidro": 0.0002,
        }

    @staticmethod
    def _fator_c_hazen_williams():
        return {
            "Aço Corrugado(chapa ondulada)": 60,
            "Aço Galvanizado": 125,
            "Aço Rebitado em uso": 85,
            "Aço soldado novo": 130,
            "Aço Soldado com revestimento especial": 130,
            "Chumbo": 130,
            "Aço Soldado em uso": 90,
            "Ferro Fundido Usado": 90,
            "Concreto com acabamento comum": 120,
            "Ferro Fundido Revestido de Cimento": 130,
            "Latão": 130,
            "Ferro Fundido novo": 130,
            "Cobre": 130,
            "Manilha Cerâmica vidrada": 110,
            "Aço Rebitado novo": 110,
            "Tijolos em executados": 100,
            "Ferro Fundido de 15 a 20 anos de uso": 100,
            "Vidro": 140,
            "Plástico": 140,
            "Cimento Amianto": 140,
        }

    @staticmethod
    def _fator_localizadas():
        """Coeficientes K de referência já utilizados no AquaPump.

        São mantidos os valores originais do projecto. Para um projecto real,
        K deve ser confirmado de acordo com o tipo construtivo, geometria,
        abertura e dados do fabricante.
        """
        return {
            "Ampliação Gradual": 0.30,
            "Comporta Aberta": 1.00,
            "Controlador de Vazão": 2.50,
            "Cotovelo ou joelho de 45": 0.40,
            "Cotovelo ou joelho de 90": 0.90,
            "Crivo": 0.75,
            "Curva de 22.5": 0.10,
            "Curva 45": 0.20,
            "Curva 90": 0.40,
            "Entrada de Borda": 1.00,
            "Entrada Normal": 0.50,
            "Junção": 0.40,
            "Medidor Venturi": 2.50,
            "Pequena Derivação": 0.02,
            "Redução Gradual": 0.15,
            "Saída de Canalização": 1.00,
            "Tê de Passagem directa": 0.60,
            "Tê de saida Bilateral": 1.80,
            "Tê de saida de lado": 1.30,
            "Válvula Borboleta": 0.30,
            "Válvula de ângulo aberta": 5.00,
            "Válvula de gaveta aberta": 0.20,
            "Válvula de pé": 1.75,
            "Válvula de retenção": 2.50,
            "Válvula globo aberta": 10.00,
        }
