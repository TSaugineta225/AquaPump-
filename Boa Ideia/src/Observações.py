from openai import OpenAI
from PySide6.QtCore import QThread, Signal


class Observacoes(QThread):
    resultado = Signal(str)

    def __init__(self, vazao, altura, marca ,modelo,  parent=None):
        super().__init__(parent)
        self.vazao = vazao
        self.altura = altura
        self.marca = marca
        self.modelo = modelo
        
    def run(self):
        client = OpenAI(api_key="k-proj-8kP8PdXO0w0AZnfEjdylTrjY3sglhZQ805LeAHoGQH2NbA7NoCrVWbPdazaNU04bUKjn54u0YiT3BlbkFJJUIhPSqatZ7SsNcG48pYHc5dQFlYiwwb4LgHdhsXYn01c8-bCwMbnkMGEMttz6LCoYhFfXAZAA")

        prompt = f"""

            Forneça observações técnicas e práticas sobre a bomba hidráulica da marca {self.marca}, 
            modelo {self.modelo}, considerando os seguintes parâmetros de operação: 
            - Vazão: {self.vazao} 
            - Altura manométrica: {self.altura} 

            Inclua nas observações:  
            1. Possíveis aplicações da bomba (setores, usos específicos).  
            2. Limitações ou cuidados de operação.  
            4. Recomendações de manutenção preventiva.  
            5. Sugestões de otimização do desempenho em campo.  
            
            """

        try:
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em Bombas Hidraulicas Centrifugas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )

            conteudo = resposta.choices[0].message.content
            self.resultado.emit(conteudo)

        except Exception as e:
            self.resultado.emit(f"Ocorreu um erro: {str(e)}")
