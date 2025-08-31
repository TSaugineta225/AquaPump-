from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMenu, QCompleter, QToolButton,
    QMessageBox, QFileDialog, QVBoxLayout, QSizePolicy
)
import json

class HistoricoManager:
    def __init__(self, parent=None):
        self.parent = parent
        
    def salvar_historico(self, dados_calculo):
        """
        Salva os dados de cálculo em um arquivo JSON
        dados_calculo: dicionário com os valores a serem salvos
        """
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.parent, "Salvar Arquivo", '', 'Json Files (*.json)'
            )
            if filename:
                if not filename.endswith('.json'):
                    filename += '.json'
                
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(dados_calculo, file, indent=4, ensure_ascii=False)
                return True
        except Exception as e:
            QMessageBox.critical(self.parent, 'ERRO', f'Erro ao salvar histórico: {e}')
            return False
    
    def carregar_historico(self):
        """
        Carrega dados de cálculo de um arquivo JSON
        Retorna: dicionário com os dados carregados ou None em caso de erro
        """
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self.parent, "Abrir Arquivo", '', 'Json Files (*.json)'
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    dados = json.load(file)
                return dados
        except Exception as e:
            QMessageBox.critical(self.parent, 'ERRO', f'Erro ao carregar histórico: {e}')
            return None