import json
import geopandas as gpd
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox

class Arquivos:
    def __init__(self, web):
        self.page = web
    
    def carregar_geojson(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Selecionar arquivo GeoJSON", "", "GeoJSON (*.geojson *.json);;Todos os arquivos (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    geojson_obj = json.load(f)
                    geojson_str = json.dumps(geojson_obj)
                    self.page.page().runJavaScript(f"carregarGeoJSON({geojson_str});")
            except Exception as e:
                self._mostrar_erro("Erro ao carregar GeoJSON", str(e))

    def carregar_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Selecionar arquivo CSV", "", "CSV (*.csv);;Todos os arquivos (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    csv_text = f.read()
                    csv_text_escaped = json.dumps(csv_text)
                    self.page.page().runJavaScript(f"carregarCSV({csv_text_escaped});")
            except Exception as e:
                self._mostrar_erro("Erro ao carregar CSV", str(e))

    def carregar_kml(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Selecionar arquivo KML", "", "KML (*.kml);;Todos os arquivos (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    kml_text = f.read()
                    kml_text_escaped = json.dumps(kml_text)
                    self.page.page().runJavaScript(f"carregarKML({kml_text_escaped});")
            except Exception as e:
                self._mostrar_erro("Erro ao carregar KML", str(e))

    def carregar_shapefile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Selecionar arquivo Shapefile", "", "Shapefile (*.shp);;Todos os arquivos (*)"
        )
        if file_path:
            try:
                gdf = gpd.read_file(file_path)
                geojson_str = gdf.to_json()
                geojson_str_escaped = json.dumps(json.loads(geojson_str)) 
                self.page.page().runJavaScript(f"carregarGeoJSON({geojson_str_escaped});")
            except Exception as e:
                self._mostrar_erro("Erro ao carregar Shapefile", str(e))

    def _mostrar_erro(self, titulo, mensagem):
        QMessageBox.critical(self, titulo, mensagem)
