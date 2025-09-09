import sqlite3
import logging
import time
from pathlib import Path
from typing import List, Dict, Optional
import os
import threading

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GestorDatabase:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path: str = 'data/aquapump.db'):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GestorDatabase, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, db_path: str = 'data/aquapump.db'):
        with self._lock:
            if self._initialized:
                return
                
            self.database_path = Path(db_path)
            self._ensure_database_dir()
            self.connexao = None
            self.cursor = None
            self._connect_with_retry()
            self._initialized = True

    def _ensure_database_dir(self) -> None:
        """Garante que o diretório do banco de dados existe"""
        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Erro ao criar diretório do banco: {e}")
            raise

    def _connect_with_retry(self, max_retries: int = 5, initial_delay: float = 0.1) -> None:
        """Tenta conectar com retry exponencial"""
        for attempt in range(max_retries):
            try:
                # Tentar conexão
                self.connexao = sqlite3.connect(
                    str(self.database_path),
                    timeout=30,
                    check_same_thread=False,
                    isolation_level=None
                )
                
                # Configurações para melhor resistência a locks
                self.connexao.execute("PRAGMA journal_mode=WAL")
                self.connexao.execute("PRAGMA busy_timeout=3000")
                self.connexao.execute("PRAGMA foreign_keys=ON")
                
                self.cursor = self.connexao.cursor()
                logger.info("Conexão com banco de dados estabelecida com sucesso")
                return
                
            except sqlite3.OperationalError as e:
                if "locked" in str(e):
                    logger.warning(f"Banco de dados bloqueado (tentativa {attempt + 1}/{max_retries})")
                    delay = initial_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    logger.error(f"Erro operacional: {e}")
                    break
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                break

        # Se todas as tentativas falharem, criar fallback em memória
        logger.warning("Criando banco de dados em memória como fallback")
        self._create_in_memory_fallback()

    def _create_in_memory_fallback(self) -> None:
        """Cria um banco em memória como fallback"""
        try:
            self.connexao = sqlite3.connect(":memory:", check_same_thread=False)
            self.connexao.execute("PRAGMA foreign_keys=ON")
            self.cursor = self.connexao.cursor()
            
            # Criar estrutura básica da tabela
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Bombas (
                    id_bomba INTEGER PRIMARY KEY AUTOINCREMENT,
                    modelo TEXT,
                    fabricante TEXT,
                    tipo_bomba TEXT,
                    caudal_nominal_m3h REAL,
                    altura_nominal_m REAL,
                    potencia_nominal_kW REAL,
                    velocidade_rpm INTEGER,
                    material_corpo TEXT,
                    pressao_max_bar REAL,
                    caminho_imagem TEXT,
                    status TEXT
                )
            ''')
            
            # Inserir alguns dados de exemplo
            self.cursor.executemany('''
                INSERT OR IGNORE INTO Bombas 
                (modelo, fabricante, tipo_bomba, caudal_nominal_m3h, altura_nominal_m, 
                 potencia_nominal_kW, velocidade_rpm, material_corpo, pressao_max_bar, caminho_imagem, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [
                ('Bomba Exemplo 1', 'Fabricante A', 'Centrífuga', 10.0, 20.0, 2.5, 2900, 
                 'Aço Inox', 10.0, 'imagens/bombas/exemplo1.png', 'ativa'),
                ('Bomba Exemplo 2', 'Fabricante B', 'Submersa', 15.0, 15.0, 3.0, 2900, 
                 'Ferro Fundido', 8.0, 'imagens/bombas/exemplo2.png', 'ativa')
            ])
            
            self.connexao.commit()
            logger.info("Banco em memória criado com sucesso como fallback")
            
        except Exception as e:
            logger.error(f"Falha ao criar banco em memória: {e}")
            raise ConnectionError("Não foi possível conectar a nenhum banco de dados")

    def pesquisar_bombas_candidatas(self, vazao_necessaria_m3h: float, 
                                  altura_necessaria_m: float) -> List[Dict]:
        """Pesquisa bombas candidatas com tratamento robusto de erros"""
        # Implementação mantida igual à versão anterior
        # ...

    def fechar_conexao(self) -> None:
        """Fecha a conexão de forma segura - apenas para uso no final da aplicação"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connexao:
                self.connexao.close()
            logger.info("Conexão com banco de dados fechada")
        except Exception as e:
            logger.error(f"Erro ao fechar conexão: {e}")

    def __del__(self):
        """Destrutor - não fecha a conexão automaticamente para permitir reuso"""
        pass

    def verificar_conexao(self) -> bool:
        """Verifica se a conexão está ativa"""
        try:
            if self.connexao and self.cursor:
                self.cursor.execute("SELECT 1")
                return True
        except:
            return False
        return False

    def is_fallback_db(self) -> bool:
        """Verifica se estamos usando o banco em memória (fallback)"""
        return self.connexao and str(self.database_path) == ":memory:"