import logging
from typing import List, Dict
from src.gestor_database import GestorDatabase

logger = logging.getLogger(__name__)

class MotorSelecao:
    def __init__(self, gestor_db: GestorDatabase):
        self.gestor_db = gestor_db

    def selecionar_melhores_bombas(self, vazao_requerida_m3h: float, altura_requerida_m: float, 
                                   tolerancia: float = 0.5) -> List[Dict]:
        """
        Orquestra a busca e a classificação de bombas.
        
        Args:
            vazao_requerida_m3h: A vazão que o sistema necessita.
            altura_requerida_m: A altura que o sistema necessita.
            tolerancia: Percentagem para definir a faixa de busca (ex: 0.5 para 50%).
            
        Returns:
            Uma lista de dicionários de bombas, ordenadas pela melhor pontuação.
        """
        if vazao_requerida_m3h <= 0 or altura_requerida_m <= 0:
            return []

        # 1. Definir a faixa de busca com base na tolerância
        vazao_min = vazao_requerida_m3h * (1 - tolerancia)
        vazao_max = vazao_requerida_m3h * (1 + tolerancia)
        altura_min = altura_requerida_m * (1 - tolerancia)
        altura_max = altura_requerida_m * (1 + tolerancia)
        
        # 2. Buscar as bombas candidatas na base de dados
        bombas_candidatas = self.gestor_db.pesquisar_bombas_por_faixa(
            vazao_min, vazao_max, altura_min, altura_max
        )
        
        if not bombas_candidatas:
            return []
            
        # 3. Calcular a pontuação de cada bomba
        resultados_pontuados = []
        for bomba in bombas_candidatas:
            score = self._calcular_score(
                vazao_requerida_m3h, altura_requerida_m,
                bomba['caudal_nominal_m3h'], bomba['altura_nominal_m']
            )
            bomba['score'] = score
            resultados_pontuados.append(bomba)
            
        # 4. Ordenar pelo maior score
        return sorted(resultados_pontuados, key=lambda x: x['score'], reverse=True)

    def _calcular_score(self, q_req, h_req, q_bomba, h_bomba) -> float:
        """
        Calcula uma pontuação de adequação. A pontuação é maior quanto mais perto
        o ponto requerido está do ponto nominal da bomba (seu ponto de melhor eficiência).
        """
        try:
            # Normalizar as distâncias para que vazão e altura tenham pesos iguais
            distancia_vazao = abs(q_req - q_bomba) / q_req
            distancia_altura = abs(h_req - h_bomba) / h_req
            
            distancia_total = (distancia_vazao**2 + distancia_altura**2)**0.5

            score = max(0, 1 - distancia_total)
            
            return score
        except ZeroDivisionError:
            return 0.0