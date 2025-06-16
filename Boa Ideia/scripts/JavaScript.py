class Mapa:
    def __init__(self):
        self.html_code =  """<!DOCTYPE html>
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
    
    <!-- Menu de edição -->
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
        // Camadas base
        const camadaPadrao = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });

        const camadaSatelite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: '© Esri'
        });

        // Inicialização do mapa
        const map = L.map('map', {
            center: [-25.9667, 32.5833], 
            zoom: 6,
            layers: [camadaPadrao] 
        });

        // Camadas base disponíveis
        const camadasBase = {
            'Padrão': camadaPadrao,
            'Satélite': camadaSatelite
        };

        // Adiciona controle de camadas
        L.control.layers(camadasBase).addTo(map);

        map.locate({setView: true, maxZoom: 18, enableHighAccuracy: true});

        L.control.scale({
            metric: true,
            imperial: false,
            maxWidth: 200,
            position: 'bottomleft'
        }).addTo(map);

        // FeatureGroup para linhas desenhadas
        const drawnItems = new L.FeatureGroup().addTo(map);

        const drawControl = new L.Control.Draw({
            edit: { featureGroup: drawnItems },
            draw: { polyline: { shapeOptions: { color: '#0000ff', weight: 3 } }, polygon: false, rectangle: false, circle: false, marker: false }
        });
        map.addControl(drawControl);

        // Variáveis globais
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

            // CSV
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

        // KML
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

        // Comunicação com backend Qt
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
            let mensagem = `Erro ao obter dados de elevação. Tente ligar-se à internet!`;
            if (window.mensagem && typeof window.mensagem.mensagem_recebida === "function") {
                window.mensagem.mensagem_recebida(mensagem);
            } else {
                alert(mensagem);
            }
        }

        // Função para obter a elevação
        async function getElevation(lat, lon) {
            const url = `https://api.open-elevation.com/api/v1/lookup?locations=${lat},${lon}`;
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error("Falha na resposta da API");
                const data = await response.json();
                if (data.results && data.results[0] && typeof data.results[0].elevation === "number") {
                    return data.results[0].elevation;
                } else {
                    throw new Error("Resposta inesperada da API");
                }
            } catch (error) {
                captar_mensagem();
                return 0;
            }
        }

        // Calcula diferença de altura entre início e fim da linha
        async function calcularAltura(layer) {
            const latlngs = layer.getLatLngs();
            if (latlngs.length < 2) return 0;
            const start = latlngs[0];
            const end = latlngs[latlngs.length - 1];
            const startElev = await getElevation(start.lat, start.lng);
            const endElev = await getElevation(end.lat, end.lng);
            return Math.abs(endElev - startElev);
        }

        function formatar_distancia(metros) {
            return metros >= 1000 ? `${(metros/1000).toFixed(2)} km` : `${metros.toFixed(2)} metros`;
        }

        function calcular_distancia(layer) {
            let latlngs = layer.getLatLngs();
            let distancia_total = 0;
            for (let i = 1; i < latlngs.length; i++) {
                distancia_total += latlngs[i - 1].distanceTo(latlngs[i]);
            }
            return distancia_total;
        }

        function calcular_diametro(flow, tempo) {
            if (typeof flow !== "number" || typeof tempo !== "number" || isNaN(flow) || isNaN(tempo) || tempo <= 0) return null;
            if (tempo === 24) {
                return 1.3 * Math.sqrt(flow);
            } else if (tempo < 24) {
                return 1.3 * Math.sqrt(flow) * Math.sqrt(tempo/24);
            }
            return null;
        }

        function potencia(flow, altura) {
            if (!altura || isNaN(altura) || !flow || isNaN(flow)) return null;
            return (flow * altura * 1000) / 75;
        }

        function calcular_eficiencia(flow, altura, potencia_valor) {
            try {
                if (!potencia_valor || isNaN(potencia_valor)) return null;
                return (flow * altura * 1000) / potencia_valor;
            } catch (error) {
                console.error(error);
                return null;
            }
        }

        function receber_dados(valor_1, valor_2) {
            valor_1_guardado = Number(valor_1);
            valor_2_guardado = Number(valor_2);
            drawnItems.eachLayer(async layer => {
                await actualizar_popup(layer);
            });
        }

        async function actualizar_popup(layer) {
            const altura = await calcularAltura(layer);
            const flow = Number(valor_1_guardado);
            const tempo = Number(valor_2_guardado);
            const nome = layer.customProperties?.name || "Sem nome";
            const distancia = formatar_distancia(calcular_distancia(layer));
            const diametro = calcular_diametro(flow, tempo);
            const potencia_total = potencia(flow, altura);

            layer.bindPopup(`
                <strong>${nome}</strong><br>
                Distância: ${distancia}<br>
                Diâmetro: ${diametro !== null ? diametro.toFixed(2) : 'N/A'}<br>
                Altura: ${altura?.toFixed(2)} m<br>
                Potência: ${potencia_total !== null ? potencia_total.toFixed(2) : 'N/A'} CV
            `).openPopup();
        }

        async function obter_dados_bomba(layer) {
            const flow = Number(valor_1_guardado);
            const tempo = Number(valor_2_guardado);
            const diametro = calcular_diametro(flow, tempo);

            if (isNaN(flow) || isNaN(tempo) || diametro === null) {
                console.warn("Dados inválidos para envio ao Python:", { flow, tempo, diametro });
                return;
            }

            if (window.dados_bomba && typeof window.dados_bomba.valores_recebidos === "function") {
                window.dados_bomba.valores_recebidos(flow, tempo, diametro);
            } else {
                console.error("Objeto dados_bomba ou método valores_recebidos não encontrado");
            }
        }


        // Evento de criação de linha
        map.on(L.Draw.Event.CREATED, async e => {
            const layer = e.layer;
            layer.customProperties = { name: "Sem nome" };
            drawnItems.addLayer(layer);

            await actualizar_popup(layer);
            await obter_dados_bomba(layer);

            layer.on('click', event => {
                layer_selecionada = layer;
                document.getElementById('line-name').value = layer.customProperties.name;
                document.getElementById('line-color').value = layer.options.color;
                document.getElementById('line-width').value = layer.options.weight;
                mostrar_menu_popup(event.originalEvent);
            });
        });

        // Evento de edição de linha
        map.on(L.Draw.Event.EDITED, async e => {
            e.layers.eachLayer(async layer => {
                await actualizar_popup(layer);
                await obter_dados_bomba(layer);
            });
        });

        // Função para mostrar menu popup
        function mostrar_menu_popup(event) {
            const menu = document.getElementById('popup-menu');
            menu.style.display = 'block';
            // Garante que o menu não ultrapasse a janela
            menu.style.left = `${Math.min(event.clientX, window.innerWidth - menu.offsetWidth - 10)}px`;
            menu.style.top = `${Math.min(event.clientY, window.innerHeight - menu.offsetHeight - 10)}px`;
        }

        // Fechar menu ou excluir linha
        document.querySelectorAll('.close-btn, #delete-line').forEach(btn => {
            btn.addEventListener('click', () => {
                if (btn.id === 'delete-line' && layer_selecionada) {
                    if (confirm('Deseja excluir esta linha?')) {
                        drawnItems.removeLayer(layer_selecionada);
                        layer_selecionada = null;
                    }
                }
                document.getElementById('popup-menu').style.display = 'none';
            });
        });

        // Aplicar estilo à linha selecionada
        document.getElementById('apply-style').addEventListener('click', () => {
            if (layer_selecionada) {
                const color = document.getElementById('line-color').value;
                const weight = Math.min(10, Math.max(1, parseInt(document.getElementById('line-width').value)));
                const name = document.getElementById('line-name').value;
                layer_selecionada.setStyle({ color, weight });
                layer_selecionada.customProperties.name = name;
                actualizar_popup(layer_selecionada);
            }
        });

        // Fechar menu ao duplo clique fora dele
        map.on('dblclick', () => document.getElementById('popup-menu').style.display = 'none');

        // Exemplo de integração: window.receber_dados(valor1, valor2);
        window.receber_dados = receber_dados;

    </script>
</body>
</html>

"""
        