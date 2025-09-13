from openai import OpenAI
from PySide6.QtCore import QThread, Signal

class ConsultaBomba(QThread):
    resultado = Signal(str)

    def __init__(self, vazao, altura, potencia, parent=None):
        super().__init__(parent)
        self.vazao = vazao
        self.altura = altura
        self.potencia = potencia

    def run(self):
        client = OpenAI(api_key="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")

        prompt = f"""
        Preciso de no mínimo 10 bombas hidráulicas de pelo menos 3 fabricantes para uma aplicação de abastecimento, quais são os modelos existentes e suas especificações próximas aos detalhes abaixo.
        A vazão necessária é de {self.vazao} m³/s, altura manométrica de {self.altura} m e potência de {self.potencia} CV. Por favor, forneça:
        - Somente Bombas centrífugas;
        - Preços em dólar e Meticais de cada bomba;
        - Formula da CCurva da Bomba
        - Links para obter mais informações de cada bomba; 
        """

        try:
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em engenharia hidráulica."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            conteudo = resposta.choices[0].message.content
            self.resultado.emit(conteudo)
        except Exception as e:
            self.resultado.emit(f"Ocorreu um erro: {str(e)}")


class ConsultaBOM(QThread):
    resposta = Signal(str)

    def __init__(self, vazao, altura, potencia, latitude, longitude, parent=None):
        super().__init__(parent)
        self.vazao = vazao
        self.altura = altura
        self.potencia = potencia
        self.latitude = latitude
        self.longitude = longitude

    def run(self):
        client = OpenAI(api_key="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")

        prompt = f"""
        Desenvolva uma lista contendo **pelo menos 10 modelos** de bombas hidráulicas centrífugas, provenientes de **no mínimo 3 fabricantes diferentes**, para uma aplicação de abastecimento. Cada modelo deve atender aos seguintes requisitos técnicos:
        - **Vazão necessária:** {self.vazao} m³/s
        - **Altura manométrica:** {self.altura} m
        - **Potência:** {self.potencia} CV
        - **Localização da instalação:** Latitude {self.latitude} e Longitude {self.longitude}

        A resposta deve incluir, para cada modelo:
        1. **Identificação:** Nome do modelo e fabricante.
        2. **Especificações Técnicas Detalhadas:** Características operacionais, materiais, eficiência, entre outros.
        3. Estudo do Locl de instalação das bombas atraves ds coordenadas: verificar se a fonte de captacao e adequada e ou suficiente para atender a demanda
        5. **Referências:** Links confiáveis para mais informações e fontes de dados sobre cada modelo.

        Apresente os dados de forma organizada e clara, garantindo que as informações sejam atualizadas e provenientes de fontes confiáveis. Nunca faça em forma de tabela
        """

        try:
            detalhes = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em engenharia hidráulica, com ênfase na seleção de bombas hidráulicas." },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            conteudo = detalhes.choices[0].message.content
            self.resposta.emit(conteudo)
        except Exception as e:
            self.resposta.emit(f"Ocorreu um erro: {str(e)}")
