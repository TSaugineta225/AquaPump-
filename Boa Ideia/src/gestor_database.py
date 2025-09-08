import sqlite3

class GestorDatabase:
    def __init__(self, db_path=r'data/aquapump.db'):
        self.database_path = db_path
        try:
            self.connexao = sqlite3.connect(self.database_path)
            self.cursor = self.connexao.cursor()
        except:
            print(f"Tenerife, Ocoreu um erro ao conectar ao banco de dados em {self.database_path}")

    def pesquisar_bombas_candidatas(self, vazao_necessaria_m3h, altura_necessaria_m):
        """
        Pesquisa bombas candidatas adequadas para o ponto de operação desejado,
        considerando margens de segurança e características técnicas.
        """
        try:
            # Definir margens de segurança (ajustáveis conforme necessidades)
            margem_altura = 1.05  # 5% acima da altura necessária
            margem_vazao = 1.1    # 10% acima da vazão necessária

            # Query otimizada com múltiplas camadas de verificação
            self.cursor.execute('''
                WITH CurvasFiltradas AS (
                    SELECT 
                        id_bomba,
                        -- Verifica se atinge altura suficiente na vazão necessária
                        MAX(CASE WHEN vazao_m3h >= ? THEN valor END) AS altura_na_vazao_desejada,
                        -- Verifica ponto mais próximo para análise posterior
                        MIN(ABS(vazao_m3h - ?)) AS diff_vazao_proxima
                    FROM PontosCurva
                    WHERE tipo_curva = 'caracteristica'
                    GROUP BY id_bomba
                    HAVING altura_na_vazao_desejada >= ?
                )
                SELECT 
                    B.id_bomba,
                    B.modelo,
                    B.fabricante,
                    B.rotor,
                    B.motor_volts,
                    CF.altura_na_vazao_desejada,
                    CF.diff_vazao_proxima
                FROM Bombas B
                INNER JOIN CurvasFiltradas CF ON B.id_bomba = CF.id_bomba
                -- Verificação adicional de capacidade máxima
                WHERE B.altura_maxima >= ?
                    AND B.vazao_maxima >= ?
                    AND B.status = 'ativa'
                -- Ordenar por proximidade à vazão desejada e eficiência
                ORDER BY CF.diff_vazao_proxima ASC,
                        B.eficiencia_energetica DESC
            ''', (
                vazao_necessaria_m3h * 0.9,  # Margem inferior de vazão
                vazao_necessaria_m3h,
                altura_necessaria_m * margem_altura,
                altura_necessaria_m * margem_altura,
                vazao_necessaria_m3h * margem_vazao
            ))

            # Coletar resultados com informações detalhadas
            resultados = self.cursor.fetchall()
            
            # Log para debugging
            print(f"Bombas candidatas encontradas: {len(resultados)}")
            
            return resultados

        except sqlite3.Error as e:
            print(f"Erro ao pesquisar bombas candidatas: {e}")
            import traceback
            traceback.print_exc()
            return []
        
    def fechar_conexao(self):
        if self.connexao:
            self.connexao.close()