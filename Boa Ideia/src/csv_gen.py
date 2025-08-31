import csv
import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog, QMessageBox

class CSV:
    """
    Classe para exportação de dados do sistema de bombeamento para formato CSV.
    Inspirada na estrutura da classe PDF para manter consistência nos dados.
    """
    
    def __init__(self):
        self.dados = []
        self.cabecalho = ['Parâmetro', 'Valor', 'Unidade', 'Data/Hora', 'Origem']
    
    def adicionar_dados(self, parametro, valor, unidade, origem="Sistema"):
        """
        Adiciona um conjunto de dados para exportação.
        
        Args:
            parametro (str): Nome do parâmetro (ex: "Vazão", "Pressão")
            valor (float/int/str): Valor do parâmetro
            unidade (str): Unidade de medida
            origem (str): Origem dos dados (ex: "Sensor", "Cálculo", "Manual")
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dados.append([parametro, str(valor), unidade, timestamp, origem])
    
    def adicionar_conjunto_dados(self, dados_dict, origem="Sistema"):
        """
        Adiciona um conjunto completo de dados no formato de dicionário.
        
        Args:
            dados_dict (dict): Dicionário no formato {parametro: (valor, unidade)}
            origem (str): Origem dos dados
        """
        for parametro, (valor, unidade) in dados_dict.items():
            self.adicionar_dados(parametro, valor, unidade, origem)
    
    def adicionar_secao(self, nome_secao):
        """
        Adiciona uma linha de seção para organizar o CSV.
        
        Args:
            nome_secao (str): Nome da seção
        """
        self.dados.append([f"--- {nome_secao} ---", "", "", "", ""])
    
    def adicionar_espaco(self):
        """Adiciona uma linha em branco para melhor organização."""
        self.dados.append(["", "", "", "", ""])
    
    def adicionar_metadados(self, titulo_relatorio, versao_sistema="1.0", info_adicional=""):
        """
        Adiciona metadados ao início do CSV.
        
        Args:
            titulo_relatorio (str): Título do relatório
            versao_sistema (str): Versão do sistema
            info_adicional (str): Informações adicionais
        """
        metadados = [
            ["Relatório do Sistema de Bombeamento", "", "", "", ""],
            [f"Título: {titulo_relatorio}", "", "", "", ""],
            [f"Data de geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "", "", "", ""],
            [f"Versão do sistema: {versao_sistema}", "", "", "", ""],
            [f"Informações: {info_adicional}", "", "", "", ""],
            ["", "", "", "", ""]  # Linha em branco
        ]
        
        self.dados = metadados + self.dados
    
    def exportar(self, caminho_arquivo=None, parent=None):
        """
        Exporta os dados para um arquivo CSV.
        
        Args:
            caminho_arquivo (str): Caminho onde o CSV será salvo. Se None, abre diálogo.
            parent: Widget pai para os diálogos (opcional)
        
        Returns:
            bool: True se a exportação foi bem-sucedida, False caso contrário
        """
        try:
            # Se nenhum caminho foi fornecido, abrir diálogo para salvar
            if caminho_arquivo is None:
                caminho_arquivo, _ = QFileDialog.getSaveFileName(
                    parent, "Salvar como CSV", "relatorio_bombeamento.csv", "Arquivos CSV (*.csv)"
                )
                if not caminho_arquivo:
                    return False  # Usuário cancelou
            
            # Garantir que a extensão .csv está presente
            if not caminho_arquivo.lower().endswith('.csv'):
                caminho_arquivo += '.csv'
            
            # Escrever dados no arquivo CSV
            with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.writer(arquivo)
                
                # Escrever cabeçalho
                escritor.writerow(self.cabecalho)
                
                # Escrever dados
                escritor.writerows(self.dados)
            
            QMessageBox.information(
                parent, 
                "Exportação Concluída", 
                f"Dados exportados com sucesso para:\n{os.path.basename(caminho_arquivo)}"
            )
            return True
            
        except Exception as e:
            QMessageBox.warning(
                parent, 
                "Erro na Exportação", 
                f"Falha ao exportar para CSV: {str(e)}"
            )
            return False
    
    def limpar_dados(self):
        """Limpa todos os dados armazenados para uma nova exportação."""
        self.dados = []
    
    def gerar_relatorio_completo(self, dados_bombeamento, dados_analise, dados_ambiente, caminho_arquivo=None, parent=None):
        """
        Gera um relatório CSV completo com todas as seções organizadas.
        
        Args:
            dados_bombeamento (dict): Dados do sistema de bombeamento
            dados_analise (dict): Dados de análise e cálculos
            dados_ambiente (dict): Dados ambientais
            caminho_arquivo (str): Caminho para salvar o arquivo
            parent: Widget pai para os diálogos
        """
        self.limpar_dados()
        
        # Adicionar metadados
        self.adicionar_metadados(
            "Relatório Completo do Sistema de Bombeamento",
            "1.0",
            "Relatório gerado automaticamente pelo sistema"
        )
        
        # Seção de dados do bombeamento
        self.adicionar_secao("DADOS DO SISTEMA DE BOMBEAMENTO")
        self.adicionar_conjunto_dados(dados_bombeamento, "Sistema de Bombeamento")
        self.adicionar_espaco()
        
        # Seção de análise
        self.adicionar_secao("ANÁLISE E CÁLCULOS")
        self.adicionar_conjunto_dados(dados_analise, "Análise do Sistema")
        self.adicionar_espaco()
        
        # Seção ambiental
        self.adicionar_secao("CONDIÇÕES AMBIENTAIS")
        self.adicionar_conjunto_dados(dados_ambiente, "Sensores Ambientais")
        
        # Exportar
        return self.exportar(caminho_arquivo, parent)