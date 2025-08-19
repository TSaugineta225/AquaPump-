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
    * { margin:0; padding:0; box-sizing:border-box; }
    #map { height:100vh; width:100vw; }

    .menu-popup {
        position: fixed;
        background:#fff;
        border:1px solid #ccc;
        border-radius:10px;
        padding:15px;
        box-shadow:0 4px 12px rgba(0,0,0,0.25);
        z-index:1000;
        min-width:240px;
        display:none;
    }
    .menu-popup h3 { margin-bottom:12px; font-size:16px; font-weight:bold; color:#222; }
    .menu-popup label { display:block; margin:10px 0 4px; font-size:13px; color:#444; }
    .menu-popup input, .menu-popup select {
        width:100%; padding:6px; border:1px solid #bbb; border-radius:6px; margin-bottom:6px;
    }
    .menu-actions { display:flex; gap:10px; margin-top:12px; }
    .menu-popup button { flex:1; padding:8px; border:none; border-radius:6px; cursor:pointer; color:white; }
    #apply-accessory { background:#bfbfbf; } #apply-accessory:hover { background:#0056b3; }
    #delete-accessory { background:#a29898; } #delete-accessory:hover { background:#a71d2a; }
    .close-btn { position:absolute; top:8px; right:8px; background:none; border:none; font-size:20px; color:#777; cursor:pointer; }
    .close-btn:hover { color:#333; }
</style>

<body>
    <div id="map"></div>

    <!-- Menu Popup -->
    <div id="popup-menu" class="menu-popup">
        <button class="close-btn">&times;</button>
        <h3>Editar Acessório</h3>

        <label for="acessorio-tipo">Nome do Acessorio</label>
        <select id="acessorio-tipo">
              <option value="ampliacao-gradual">Ampliação Gradual</option>
            <option value="comporta-aberta">Comporta Aberta</option>
            <option value="controlador-de-vazao">Controlador de Vazão</option>
            <option value="cotovelo-45">Cotovelo ou joelho de 45</option>
            <option value="cotovelo-90">Cotovelo ou joelho de 90</option>
            <option value="crivo">Crivo</option>
            <option value="curva-22-5">Curva de 22.5</option>
            <option value="curva-45">Curva 45</option>
            <option value="curva-90">Curva 90</option>
            <option value="entrada-de-borda">Entrada de Borda</option>
            <option value="entrada-normal">Entrada Normal</option>
            <option value="juncao">Junção</option>
            <option value="medidor-venturi">Medidor Venturi</option>
            <option value="pequena-derivacao">Pequena Derivação</option>
            <option value="reducao-gradual">Redução Gradual</option>
            <option value="saida-de-canalizacao">Saída de Canalização</option>
            <option value="te-passagem-directa">Tê de Passagem directa</option>
            <option value="te-saida-bilateral">Tê de saida Bilateral</option>
            <option value="te-saida-de-lado">Tê de saida de lado</option>
            <option value="valvula-borboleta">Válvula Borboleta</option>
            <option value="valvula-angulo-aberta">Válvula de ângulo aberta</option>
            <option value="valvula-gaveta-aberta">Válvula de gaveta aberta</option>
            <option value="valvula-de-pe">Válvula de pé</option>
            <option value="valvula-de-retencao">Válvula de retenção</option>
            <option value="valvula-globo-aberta">Válvula globo aberta</option>
        </select>

        <label for="acessorio-cor">Cor</label>
        <input type="color" id="acessorio-cor" value="#ff0000">

        <div class="menu-actions">
            <button id="apply-accessory">Aplicar</button>
            <button id="delete-accessory">Eliminar</button>
        </div>
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
            zoom: 12,
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
        let acessorios = []
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
                    window.acessorios = channel.objects.acessorios;
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
                const nome = layer.customProperties?.name || "Projecto";
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

    const menu = document.getElementById('popup-menu');

    function mostrarMenuPopup(e){
        menu.style.display='block';
        menu.style.left=`${Math.min(e.clientX, window.innerWidth - menu.offsetWidth -10)}px`;
        menu.style.top=`${Math.min(e.clientY, window.innerHeight - menu.offsetHeight -10)}px`;
    }
    function fecharMenu(){ menu.style.display='none'; }

    map.on(L.Draw.Event.CREATED, e=>{
        const layer = e.layer;
        layer.customProperties = { tipo:'Válvula de pé', cor:layer.options.color };
        drawnItems.addLayer(layer);

        if(layer instanceof L.Circle || layer instanceof L.CircleMarker){
            layer.on('click', event=>{
                layer_selecionada = layer;
                document.getElementById('acessorio-tipo').value = layer.customProperties.tipo;
                document.getElementById('acessorio-cor').value = layer.customProperties.cor;
                mostrarMenuPopup(event.originalEvent);
            });
        }
    });

    // Botões do popup
    document.querySelector('.close-btn').addEventListener('click', fecharMenu);

    document.getElementById('apply-accessory').addEventListener('click', ()=>{
        if(layer_selecionada){
            const tipo = document.getElementById('acessorio-tipo').value;
            const cor  = document.getElementById('acessorio-cor').value;

            layer_selecionada.setStyle({color:cor});
            layer_selecionada.customProperties = { tipo, cor };

            // ID único
            const id = L.Util.stamp(layer_selecionada);
            const obj = { id, tipo, cor};

            const idx = acessorios.findIndex(a => a.id === id);
            if(idx === -1){
                acessorios.push(obj);
            } else {
                acessorios[idx] = obj;
            }

            window.acessorios.lista_acessorios(acessorios);
            //console.log("Lista atual de acessórios:", acessorios);
        }
        fecharMenu();
    });

    document.getElementById('delete-accessory').addEventListener('click', ()=>{
        if(layer_selecionada){
            const id = L.Util.stamp(layer_selecionada);
            acessorios = acessorios.filter(a => a.id !== id);
            drawnItems.removeLayer(layer_selecionada);
            layer_selecionada=null;
            window.acessorios.lista_acessorios(acessorios);
            //console.log("Lista atual de acessórios:", acessorios);
        }
        fecharMenu();
    });


        function receber_dados(v1, v2) {
            valor_1_guardado = Number(v1);
            valor_2_guardado = Number(v2);
            drawnItems.eachLayer(actualizar_popup);
        }

        window.receber_dados = receber_dados;

        map.on('dblclick', () => document.getElementById('popup-menu').style.display = 'none');
    </script>
</body>
</html>
"""
        