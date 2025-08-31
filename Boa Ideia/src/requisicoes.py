from PySide6.QtCore import QStringListModel, QThread, Signal, Slot
from PySide6.QtWidgets import QMessageBox
from geopy.distance import geodesic
import requests, time


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

class Perfil_elevacao():
    def processamento_pontos(self, pontos, grafico):
        if len(pontos) < 2:
            grafico.removeAllSeries()
            return
        
    def interpolar_pontos(self, pontos, espaco=0.1):
        interpolados = []
        for i in range(len(pontos)-1):
            inicio = pontos[i]
            fim = pontos[i + 1]
            dist = geodesic(inicio, fim).km

            passos = max(2, int(dist/espaco))
            for j in range(passos):
                lat = inicio[0] + (fim[0] - inicio[0]) * (j / passos)
                lon = inicio[1] + (fim[1] - inicio[1]) * (j / passos)
                interpolados.append([lat, lon])
        interpolados.append(pontos[-1])
        return interpolados

    def buscar_elevaction(self, pontos):
        elevacoes = []
        total_pontos = 100  
        for i in range(0, len(pontos), total_pontos):
            batch = pontos[i:i+total_pontos]
            localizacao = "|".join([f"{lat},{lon}" for lat, lon in batch])
            try:
                url = f"https://api.open-elevation.com/api/v1/lookup?locations={localizacao}"
                response = requests.get(url, timeout=15)
                response.raise_for_status() 
                data = response.json()
                batch_elev = [entry["elevation"] for entry in data["results"]]
                elevacoes.extend(batch_elev)
                print(f"Lote de {len(batch)} elevações obtido com sucesso.")
                time.sleep(0.5)  
            except Exception as e:
                QMessageBox.critical(self, "Erro de API", f"Falha ao obter elevação: {e}")
                return []
        return elevacoes
    
    def calcular_distancia(self, ponto):
        distancia = [0]
        total = 0
        for i in range(1, len(ponto)):
            d = geodesic(ponto[i-1], ponto[i]).km
            total += d
            distancia.append(total)
        return distancia