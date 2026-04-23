import pytest
import sqlite3
from gestor_database import GestorDatabase

@pytest.fixture
def db_teste(tmp_path):
    """Cria um banco temporário com a tabela Bombas."""
    db_path = tmp_path / "aquapump.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE Bombas (
            id INTEGER PRIMARY KEY,
            marca TEXT,
            modelo TEXT,
            caudal_nominal_m3h REAL,
            altura_nominal_m REAL,
            potencia_nominal_kw REAL,
            rotacao_rpm INTEGER
        )
    """)
    # Inserir algumas bombas de exemplo
    bombas = [
        (1, "MarcaA", "ModeloA", 10, 50, 5.5, 1750),
        (2, "MarcaB", "ModeloB", 15, 60, 11, 1750),
        (3, "MarcaC", "ModeloC", 20, 70, 15, 1750),
        (4, "MarcaD", "ModeloD", 5, 30, 2.2, 3500),
    ]
    conn.executemany("INSERT INTO Bombas VALUES (?,?,?,?,?,?,?)", bombas)
    conn.commit()
    conn.close()
    return db_path

class TestGestorDatabase:
    def test_selecionar_melhor_bomba_exata(self, db_teste):
        gestor = GestorDatabase(str(db_teste))
        bomba = gestor.selecionar_melhor_bomba(vazao_m3h=10, altura_m=50)
        assert bomba is not None
        assert bomba["modelo"] == "ModeloA"

    def test_bomba_com_tolerancia(self, db_teste):
        gestor = GestorDatabase(str(db_teste))
        # Procurar uma vazão levemente diferente (9.5) dentro da tolerância
        bomba = gestor.selecionar_melhor_bomba(vazao_m3h=9.5, altura_m=50)
        assert bomba is not None
        # Deve retornar a mais próxima (ModeloA)
        assert bomba["modelo"] == "ModeloA"

    def test_nenhuma_bomba_encontrada(self, db_teste):
        gestor = GestorDatabase(str(db_teste))
        bomba = gestor.selecionar_melhor_bomba(vazao_m3h=100, altura_m=200)
        assert bomba is None

    def test_banco_inexistente(self):
        with pytest.raises(ConnectionError):
            GestorDatabase("caminho/inexistente.db")