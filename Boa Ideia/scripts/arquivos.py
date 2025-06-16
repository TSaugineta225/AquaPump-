import json
from PySide6.QtWidgets import QFileDialog
import geopandas as gpd

class Arquivos:
    def _carregar_e_enviar_conteudo(self, titulo_dialogo, filtro_arquivos, funcao_js):
        """Método auxiliar para ler um arquivo como texto e enviá-lo para o JavaScript."""
        file_path, _ = QFileDialog.getOpenFileName(self, titulo_dialogo, "", filtro_arquivos)
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                conteudo_js = json.dumps(conteudo)
                self.web.page().runJavaScript(f"{funcao_js}({conteudo_js});")
        except Exception as e:
            print(f"Erro ao carregar o arquivo {file_path}: {e}")

    def carregar_geojson(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo GeoJSON", "", "GeoJSON (*.geojson);;Todos os arquivos (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson_obj = json.load(f) 
                geojson_str_para_js = json.dumps(geojson_obj) 
                self.web.page().runJavaScript(f"carregarGeoJSON({geojson_str_para_js});")

    def carregar_csv(self):
        self._carregar_e_enviar_conteudo(
            "Selecionar arquivo CSV",
            "CSV (*.csv);;Todos os arquivos (*)",
            "carregarCSV"
        )

    def carregar_kml(self):
        self._carregar_e_enviar_conteudo(
            "Selecionar arquivo KML",
            "KML (*.kml);;Todos os arquivos (*)",
            "carregarKML"
        )

    def carregar_shapefile(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo Shapefile", "", "Shapefile (*.shp);;Todos os arquivos (*)")
            if file_path:
                gdf = gpd.read_file(file_path, encoding='utf-8') 
                geojson_str = gdf.to_json()
                self.web.page().runJavaScript(f"carregarGeoJSON({geojson_str});")
        except Exception as e:
            print("Erro ao carregar Shapefile:", e)