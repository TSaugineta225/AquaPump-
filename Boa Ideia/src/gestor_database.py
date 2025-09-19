import sqlite3
import logging
from pathlib import Path
from typing import List, Dict

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

    def pesquisar_bombas_por_faixa(self, vazao_min: float, vazao_max: float, altura_min: float, altura_max: float) -> List[Dict]:
        """
        Pesquisa bombas no banco de dados com base numa faixa de operação.
        """
        if not self.conexao:
            logger.error("A conexão com o banco de dados não está ativa.")
            return []
            
        query = """
            SELECT * FROM Bombas
            WHERE 
                caudal_nominal_m3h >= ? AND
                caudal_nominal_m3h <= ? AND
                altura_nominal_m >= ? AND
                altura_nominal_m <= ?
        """
        try:
            cursor = self.conexao.cursor()
            cursor.execute(query, (vazao_min, vazao_max, altura_min, altura_max))
            resultados = [dict(row) for row in cursor.fetchall()]
            return resultados
        except Exception as e:
            logger.error(f"Erro ao pesquisar bombas: {e}")
            return []

    def fechar(self):
        if self.conexao:
            self.conexao.close()
            self.conexao = None
            logger.info("Conexão com o banco de dados fechada.")