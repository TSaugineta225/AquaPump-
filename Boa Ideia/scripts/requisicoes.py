from PySide6.QtCore import QStringListModel, QThread, Signal, Slot
from PySide6.QtWidgets import QMessageBox
import requests

class Pesquisa(QThread):
    resultado = Signal(list)

    def __init__(self, texto_busca):
        super().__init__()
        self.texto_busca = texto_busca
    

    def run(self):
        try:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={self.texto_busca}&limit=5&addressdetails=1"
            headers = {"User-Agent": "PySide6-Autocomplete-App"}
            resposta = requests.get(url, headers=headers, timeout=5)

            sugestoes = []
            if resposta.status_code == 200:
                dados = resposta.json()
                for item in dados:
                    mostrar = item.get('dispaly_name', '')
                    sugestoes.append(mostrar)
            
            self.resultado.emit(sugestoes)

        except Exception as e:
            QMessageBox.critical(self, "Erro", "Falha ao requisitar dados", e)
            self.resultado.emit([])