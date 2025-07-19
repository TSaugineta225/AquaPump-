class Mapa:
    def __init__(self):
        self.html_code =  """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa</title>
    
    <!-- Leaflet e plugins -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
    <script src="https://unpkg.com/leaflet-plugins/layer/vector/KML.js"></script>
    <script src="https://unpkg.com/leaflet-omnivore@0.3.4/leaflet-omnivore.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>

    <!-- QWebChannel -->
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>

    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        #map { height: 100vh; width: 100vw; }
        .menu-popup {
            position: fixed;
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;

            min-width: 220px;
            display: none;
        }
        .menu-popup h3 { margin-bottom: 10px; color: #333; }
        .menu-popup label { display: block; margin: 8px 0 4px; color: #666; }
        .menu-popup input { width: 100%; }
        .menu-popup button {
            margin-top: 10px; padding: 8px;
            width: 100%; background: #007bff;
            color: white; border: none; border-radius: 4px;
            cursor: pointer;
        }
        .menu-popup button:hover { background: #0056b3; }
        .close-btn {
            position: absolute; top: 5px; right: 5px;
            background: none; border: none;
            cursor: pointer; font-size: 16px; color: #666;
        }
    </style>
</head>
<body>
    <div id="map"></div>

    <!-- Menu Popup -->
    <div id="popup-menu" class="menu-popup">
        <button class="close-btn">&times;</button>
        <h3>Editar Tubulação</h3>
        <label for="line-name">Nome da Tubulação:</label>
        <input type="text" id="line-name" placeholder="Digite um nome">
        <label for="line-color">Cor:</label>
        <input type="color" id="line-color" value="#0000ff">
        <label for="line-width">Espessura (1-10):</label>
        <input type="number" id="line-width" value="3" min="1" max="10">
        <button id="apply-style">Aplicar Estilo</button>
        <button id="delete-line" style="background: #dc3545;">Excluir Linha</button>
    </div>

    <script>
        // Inicialização do mapa
        const camadaPadrao = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        });

        const camadaSatelite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: '© Esri'
        });

        const map = L.map('map', {
            center: [-25.9667, 32.5833],
            zoom: 6,
            layers: [camadaPadrao]
        });

        L.control.layers({ 'Padrão': camadaPadrao, 'Satélite': camadaSatelite }).addTo(map);
        map.locate({ setView: true, maxZoom: 18, enableHighAccuracy: true });
        L.control.scale({ metric: true, imperial: false }).addTo(map);

        const drawnItems = new L.FeatureGroup().addTo(map);

        const drawControl = new L.Control.Draw({
            edit: { featureGroup: drawnItems },
            draw: {
                polyline: { shapeOptions: { color: '#0000ff', weight: 3 } },
                polygon: false, rectangle: false, circle: false, marker: false
            }
        }).addTo(map);

        let layer_selecionada = null;
        let valor_1_guardado = null;
        let valor_2_guardado = null;

        function carregarGeoJSON(conteudo) {
            const data = JSON.parse(conteudo);
            L.geoJSON(data, {
                onEachFeature: function (feature, layer) {
                    if (feature.properties) {
                        layer.bindPopup(Object.entries(feature.properties).map(([k, v]) => `${k}: ${v}`).join('<br>'));
                    }
                }
            }).addTo(map);
        }

        function carregarCSV(conteudo) {
            Papa.parse(conteudo, {
                header: true,
                dynamicTyping: true,
                complete: function(results) {
                    const features = results.data.map(row => {
                        if (!row.latitude || !row.longitude) return null;
                        return {
                            type: "Feature",
                            geometry: {
                                type: "Point",
                                coordinates: [parseFloat(row.longitude), parseFloat(row.latitude)]
                            },
                            properties: row
                        };
                    }).filter(f => f !== null);

                    const geojson = {
                        type: "FeatureCollection",
                        features: features
                    };

                    carregarGeoJSON(JSON.stringify(geojson));
                }
            });
        }

        function carregarKML(conteudo) {
            const blob = new Blob([conteudo], { type: 'application/vnd.google-earth.kml+xml' });
            const url = URL.createObjectURL(blob);
            omnivore.kml(url).on('ready', function() {
                this.eachLayer(function(layer) {
                    if (layer.feature && layer.feature.properties) {
                        layer.bindPopup(Object.entries(layer.feature.properties).map(([k, v]) => `${k}: ${v}`).join('<br>'));
                    }
                });
                this.addTo(map);
            });
        }

        document.addEventListener("DOMContentLoaded", function() {
            if (typeof QWebChannel !== "undefined") {
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.backend = channel.objects.backend;
                    window.mensagem = channel.objects.mensagem;
                    window.dados_bomba = channel.objects.dados_bomba;
                });
            }
        });

        function captar_mensagem() {
            const mensagem = "Erro ao obter dados de elevação. Tente ligar-se à internet!";
            if (window.mensagem && typeof window.mensagem.mensagem_recebida === "function") {
                window.mensagem.mensagem_recebida(mensagem);
            } else {
                alert(mensagem);
            }
        }

        async function getElevation(lat, lon) {
            const url = `https://api.open-elevation.com/api/v1/lookup?locations=${lat},${lon}`;
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error("Falha na resposta da API");
                const data = await response.json();
                return data.results?.[0]?.elevation ?? 0;
            } catch (error) {
                captar_mensagem();
                return 0;
            }
        }

        async function pesquisar_lugar(lugar) {
            try {
                const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(lugar)}`, {
                    headers: { "User-Agent": "MyLeafletApp/1.0" }
                });
                const data = await response.json();

                if (data.length > 0) {
                    let lat = parseFloat(data[0].lat);
                    let lon = parseFloat(data[0].lon);
                    map.setView([lat, lon], 9);

                } else {

                }
            } catch (error) {
                alert("Erro na pesquisa:", error);
            }
        }
        let altura = null
        async function calcularAltura(layer) {
            const latlngs = layer.getLatLngs();
            if (latlngs.length < 2) return 0;
            const elev1 = await getElevation(latlngs[0].lat, latlngs[0].lng);
            const elev2 = await getElevation(latlngs[latlngs.length - 1].lat, latlngs[latlngs.length - 1].lng);
            return altura = Math.abs(elev1 - elev2);
        }

        function calcular_distancia(layer) {
            const latlngs = layer.getLatLngs();
            return latlngs.reduce((total, _, i, arr) => {
                if (i === 0) return 0;
                return total + arr[i - 1].distanceTo(arr[i]);
            }, 0);
        }

        function calcular_diametro(flow, tempo) {
            if (tempo === 24) return 1.3 * Math.sqrt(flow);
            return 1.3 * Math.sqrt(flow) * Math.sqrt(tempo / 24);
        }

        function potencia(flow, altura) {
            return (flow * altura * 1000) / 75;
        }

        function actualizar_popup(layer) {
            calcularAltura(layer).then(altura => {
                const flow = valor_1_guardado;
                const tempo = valor_2_guardado;
                const nome = layer.customProperties?.name || "Sem nome";
                const distancia = calcular_distancia(layer);
                const diametro = calcular_diametro(flow, tempo);
                const pot = potencia(flow, altura);
                
                window.dados_bomba.valores_recebidos(altura, distancia, diametro)    // Enviar dados de altura e distancia ao python
                layer.bindPopup(`
                    <strong>${nome}</strong><br>
                    Distância: ${(distancia/1000).toFixed(2)} km<br>
                    Diâmetro: ${diametro?.toFixed(2)}<br>
                    Altura: ${altura?.toFixed(2)} m<br>
                    Potência: ${pot?.toFixed(2)} CV
                `).openPopup();
               

            });
        }

        function receber_dados(v1, v2) {
            valor_1_guardado = Number(v1);
            valor_2_guardado = Number(v2);
            drawnItems.eachLayer(actualizar_popup);
        }

        window.receber_dados = receber_dados;

        map.on(L.Draw.Event.CREATED, e => {
            const layer = e.layer;
            layer.customProperties = { name: "Sem nome" };


            drawnItems.addLayer(layer);

            layer.on('click', event => {
                layer_selecionada = layer;
                document.getElementById('line-name').value = layer.customProperties.name;
                document.getElementById('line-color').value = layer.options.color;
                document.getElementById('line-width').value = layer.options.weight;
                mostrar_menu_popup(event.originalEvent);
            });


            setTimeout(() => actualizar_popup(layer), 10);
        });


        document.querySelectorAll('.close-btn, #delete-line').forEach(btn => {
            btn.addEventListener('click', () => {
                if (btn.id === 'delete-line' && layer_selecionada) {
                    drawnItems.removeLayer(layer_selecionada);
                    layer_selecionada = null;
                }
                document.getElementById('popup-menu').style.display = 'none';
            });
        });

        document.getElementById('apply-style').addEventListener('click', () => {
            if (layer_selecionada) {
                const color = document.getElementById('line-color').value;
                const weight = parseInt(document.getElementById('line-width').value);
                const name = document.getElementById('line-name').value;
                layer_selecionada.setStyle({ color, weight });
                layer_selecionada.customProperties.name = name;
                actualizar_popup(layer_selecionada);
            }
        });

        function mostrar_menu_popup(event) {
            const menu = document.getElementById('popup-menu');
            menu.style.display = 'block';
            menu.style.left = `${Math.min(event.clientX, window.innerWidth - menu.offsetWidth - 10)}px`;
            menu.style.top = `${Math.min(event.clientY, window.innerHeight - menu.offsetHeight - 10)}px`;
        }

        map.on('dblclick', () => document.getElementById('popup-menu').style.display = 'none');
    </script>
</body>
</html>

"""
        