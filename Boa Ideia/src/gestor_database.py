"""Acesso à base SQLite local de modelos de bombas."""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class GestorDatabase:
    """Uma ligação por instância; não reutiliza silenciosamente outra base de dados."""

    def __init__(self, db_path: str | Path = "data/aquapump.db"):
        self.db_path = Path(db_path).expanduser().resolve()
        self.conexao: sqlite3.Connection | None = None
        self.conectar()

    def conectar(self):
        if not self.db_path.is_file():
            raise ConnectionError(f"Base de dados não encontrada: {self.db_path}")
        try:
            # O caminho é passado como string, sem URI manual; funciona também
            # em Windows quando o caminho contém espaços ou caracteres acentuados.
            self.conexao = sqlite3.connect(str(self.db_path), timeout=10)
            self.conexao.row_factory = sqlite3.Row
            self.conexao.execute("PRAGMA foreign_keys = ON")
            logger.info("Conexão com DB '%s' estabelecida.", self.db_path)
            return self.conexao
        except sqlite3.Error as exc:
            self.conexao = None
            logger.exception("Não foi possível abrir a base de dados %s", self.db_path)
            raise ConnectionError(f"Não foi possível abrir a base de dados: {exc}") from exc

    def selecionar_melhor_bomba(
        self, vazao_m3h: float, altura_m: float
    ) -> Optional[dict]:
        """Escolhe a bomba mais próxima dentro de bandas progressivas de tolerância."""
        try:
            vazao = float(vazao_m3h)
            altura = float(altura_m)
        except (TypeError, ValueError) as exc:
            raise ValueError("Vazão e altura devem ser valores numéricos.") from exc
        if vazao <= 0 or altura <= 0:
            raise ValueError("A vazão e a altura devem ser superiores a zero.")
        if self.conexao is None:
            raise ConnectionError("A ligação à base de dados não está activa.")

        bandas = (
            (0.8, 1.2, 0.9, 1.1),
            (0.7, 1.3, 0.85, 1.15),
            (0.6, 1.4, 0.8, 1.2),
            (0.5, 1.5, 0.75, 1.25),
        )
        query = """
            SELECT *,
                   (ABS(caudal_nominal_m3h - ?) / ? * 0.6 +
                    ABS(altura_nominal_m - ?) / ? * 0.4) AS score
            FROM Bombas
            WHERE caudal_nominal_m3h BETWEEN ? AND ?
              AND altura_nominal_m BETWEEN ? AND ?
            ORDER BY score ASC
            LIMIT 1
        """
        for q_min, q_max, h_min, h_max in bandas:
            params = (
                vazao, vazao, altura, altura,
                vazao * q_min, vazao * q_max,
                altura * h_min, altura * h_max,
            )
            try:
                row = self.conexao.execute(query, params).fetchone()
            except sqlite3.Error:
                logger.exception("Falha ao consultar a tabela de bombas.")
                raise
            if row:
                resultado = dict(row)
                resultado["faixa_tolerancia"] = (
                    f"Vazão: {q_min:.0%}-{q_max:.0%}, "
                    f"altura: {h_min:.0%}-{h_max:.0%}"
                )
                return resultado
        return None

    def fechar(self):
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None
            logger.info("Conexão com a base de dados fechada.")
