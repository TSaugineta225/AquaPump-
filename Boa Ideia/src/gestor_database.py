import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class GestorDatabase:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GestorDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: str = 'data/aquapump.db'):
        if hasattr(self, 'conexao') and self.conexao:
            return
            
        self.db_path = Path(db_path)
        self.conexao = None
        self.conectar()

    def conectar(self):
        try:
            self.conexao = sqlite3.connect(f"file:{self.db_path}?mode=rw", uri=True)
            self.conexao.row_factory = sqlite3.Row
            logger.info(f"Conexão com DB '{self.db_path}' estabelecida.")
        except sqlite3.OperationalError:
            logger.error(f"Erro: Banco de dados não encontrado em '{self.db_path}'. Certifique-se que o arquivo existe.")
            raise ConnectionError(f"DB não encontrado em {self.db_path}")

    def selecionar_melhor_bomba(self, vazao_m3h: float, altura_m: float) -> Optional[Dict]:
        """
        Seleciona a melhor bomba com tolerâncias mais realistas e critério melhorado.
        """
        logger.info(f"Buscando bomba para: Vazão={vazao_m3h} m³/h, Altura={altura_m} m")
        if not self.conexao:
            logger.error("A conexão com o banco de dados não está ativa.")
            return None
            
        # Tolerâncias mais realistas (50% para vazão, 30% para altura)
        # Busca em múltiplas faixas progressivamente mais amplas
        faixas_tolerancia = [
            (0.8, 1.2, 0.9, 1.1),    # Faixa 1: ±20% vazão, ±10% altura
            (0.7, 1.3, 0.85, 1.15),  # Faixa 2: ±30% vazão, ±15% altura  
            (0.6, 1.4, 0.8, 1.2),    # Faixa 3: ±40% vazão, ±20% altura
            (0.5, 1.5, 0.75, 1.25)   # Faixa 4: ±50% vazão, ±25% altura
        ]
        
        for tolerancia in faixas_tolerancia:
            vaz_min, vaz_max, alt_min, alt_max = tolerancia
            
            query = """
                SELECT *,
                       -- Critério de pontuação melhorado (pesos relativos)
                       (ABS(caudal_nominal_m3h - ?) / ? * 0.6 + 
                        ABS(altura_nominal_m - ?) / ? * 0.4) as score
                FROM Bombas
                WHERE 
                    caudal_nominal_m3h >= ? AND
                    caudal_nominal_m3h <= ? AND
                    altura_nominal_m >= ? AND
                    altura_nominal_m <= ?
                ORDER BY score ASC
                LIMIT 1
            """
            
            try:
                cursor = self.conexao.cursor()
                cursor.execute(query, (
                    vazao_m3h, vazao_m3h,  # Para cálculo do score
                    altura_m, altura_m,     # Para cálculo do score  
                    vazao_m3h * vaz_min, vazao_m3h * vaz_max,
                    altura_m * alt_min, altura_m * alt_max
                ))
                
                resultado = cursor.fetchone()
                if resultado:
                    bomba = dict(resultado)
                    bomba['score'] = resultado['score']
                    bomba['faixa_tolerancia'] = f"Vazão: {vaz_min*100:.0f}%-{vaz_max*100:.0f}%, Altura: {alt_min*100:.0f}%-{alt_max*100:.0f}%"
                    return bomba
                    
            except Exception as e:
                logger.error(f"Erro ao buscar bomba na faixa {tolerancia}: {e}")
                continue
        
        return None

    def fechar(self):
        if self.conexao:
            self.conexao.close()
            self.conexao = None
            logger.info("Conexão com o banco de dados fechada.")