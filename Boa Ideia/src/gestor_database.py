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

        print("\n--- INICIANDO NOVA BUSCA DE BOMBA ---")
        print(f"--> PONTO DE OPERAÇÃO REQUERIDO: Vazão = {vazao_m3h:.2f} m³/h, Altura = {altura_m:.2f} m") 
        # Tolerâncias mais realistas (50% para vazão, 30% para altura)
        faixas_tolerancia = [
            (0.8, 1.2, 0.9, 1.1),    # Faixa 1: ±20% vazão, ±10% altura
            (0.7, 1.3, 0.85, 1.15),  # Faixa 2: ±30% vazão, ±15% altura  
            (0.6, 1.4, 0.8, 1.2),    # Faixa 3: ±40% vazão, ±20% altura
            (0.5, 1.5, 0.75, 1.25)   # Faixa 4: ±50% vazão, ±25% altura
        ]
        
        for i, tolerancia in enumerate(faixas_tolerancia):
            vaz_min_f, vaz_max_f, alt_min_f, alt_max_f = tolerancia

            limite_vazao_min = vazao_m3h * vaz_min_f
            limite_vazao_max = vazao_m3h * vaz_max_f
            limite_altura_min = altura_m * alt_min_f
            limite_altura_max = altura_m * alt_max_f

            print(f"\n[TENTATIVA {i+1}]")
            print(f"  - Procurando Vazão entre: {limite_vazao_min:.2f} e {limite_vazao_max:.2f} m³/h")
            print(f"  - Procurando Altura entre: {limite_altura_min:.2f} e {limite_altura_max:.2f} m")
            
            query = """
                SELECT *,
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
                    vazao_m3h, vazao_m3h,
                    altura_m, altura_m,
                    limite_vazao_min, limite_vazao_max,
                    limite_altura_min, limite_altura_max
                ))
                
                resultado = cursor.fetchone()
                if resultado:
                    print(f"  --> SUCESSO! Bomba encontrada nesta faixa.")
                    print("---------------------------------------\n")
                    bomba = dict(resultado)
                    bomba['faixa_tolerancia'] = f"Vazão: {vaz_min_f*100:.0f}%-{vaz_max_f*100:.0f}%, Altura: {alt_min_f*100:.0f}%-{alt_max_f*100:.0f}%"
                    return bomba
                else:
                    print(f"  --> Nenhuma bomba encontrada nesta faixa. A tentar a próxima.")
                    
            except Exception as e:
                logger.error(f"Erro ao buscar bomba na faixa {tolerancia}: {e}")
                continue
        
        print("\n--- FIM DA BUSCA: Nenhuma bomba encontrada em todas as faixas. ---\n")
        return None

    def fechar(self):
        if self.conexao:
            self.conexao.close()
            self.conexao = None
            logger.info("Conexão com o banco de dados fechada.")