class Mapa:
    """Interface web do AquaPump: mapa geográfico, esquema SVG e perfil longitudinal.

    Mantém compatibilidade com MainWindow e com os objectos QWebChannel registados
    em main.py: ``altura``, ``comprimento`` e ``acessorios``.

    O esquema SVG é uma representação técnica 2D (não um modelo CAD de fabrico).
    Os coeficientes K apresentados nesta versão reproduzem os valores actualmente
    existentes em ``calculos/perdas_cargas.py``.
    """

    def __init__(self):
        self.html_code = r'''<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AquaPump — Sistema hidráulico</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<style>
:root {
  --bg:#f4f7fb; --panel:#ffffff; --line:#dce4ee; --text:#172638;
  --muted:#64748b; --blue:#1769aa; --blue2:#e8f2fb; --accent:#1592a6;
  --danger:#c43b43; --shadow:0 2px 12px rgba(20,45,75,.09);
  --radius:9px; --font:Inter,"Segoe UI",Arial,sans-serif;
}
*{box-sizing:border-box}
html,body{height:100%;width:100%;margin:0;overflow:hidden;font-family:var(--font);color:var(--text);background:var(--bg)}
button,input,select{font:inherit}
button{cursor:pointer}
#app{height:100%;display:flex;flex-direction:column}
#topbar{height:52px;flex:0 0 52px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:0 15px;z-index:1000;box-shadow:0 1px 4px rgba(20,45,75,.04)}
.brand{font-weight:750;letter-spacing:.2px;font-size:16px;color:#153b5b;white-space:nowrap}
.brand small{font-weight:500;color:#8291a2;font-size:10px;margin-left:5px}
.top-separator{height:24px;width:1px;background:var(--line)}
.mode-switch{display:flex;gap:4px;background:#f0f4f8;border-radius:8px;padding:3px}
.mode-switch button,.toolbar-btn{border:0;border-radius:6px;padding:7px 12px;background:transparent;color:#526477;font-size:12px;font-weight:650}
.mode-switch button.active{background:#fff;color:var(--blue);box-shadow:0 1px 4px rgba(20,45,75,.12)}
.top-spacer{flex:1}
.status-text{font-size:11px;color:#718096;white-space:nowrap}
.toolbar-btn{border:1px solid var(--line);background:#fff;color:#395168}
.toolbar-btn:hover{background:#f5f9fd;border-color:#a8c4dc}
.toolbar-btn.primary{background:var(--blue);border-color:var(--blue);color:#fff}
.toolbar-btn.danger{color:var(--danger)}
.view{display:none;flex:1;min-height:0}
.view.active{display:flex}
#mapPanel{position:relative}
#map{height:100%;width:100%;background:#e7edf3}
.map-hint{position:absolute;left:14px;bottom:14px;z-index:500;background:#fff;padding:8px 11px;border:1px solid var(--line);border-radius:7px;box-shadow:var(--shadow);font-size:11px;color:#526477;max-width:330px}
#diagramPanel{flex-direction:column;min-height:0}
#diagramToolbar{height:45px;flex:0 0 45px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;padding:0 12px;gap:7px}
.tool-separator{width:1px;height:23px;background:var(--line);margin:0 3px}
.tool-label{font-size:11px;color:var(--muted);font-weight:650;margin-right:3px}
#diagramWorkspace{display:grid;grid-template-columns:232px minmax(300px,1fr) 254px;flex:1;min-height:0;gap:0}
.side-panel{background:#fff;min-height:0;display:flex;flex-direction:column}
#libraryPanel{border-right:1px solid var(--line)}
#inspectorPanel{border-left:1px solid var(--line)}
.panel-heading{height:43px;flex:0 0 43px;padding:0 13px;border-bottom:1px solid #edf1f5;display:flex;align-items:center;justify-content:space-between;font-size:12px;font-weight:750;color:#30465b}
.panel-heading span.sub{font-weight:500;color:#8a98a8;font-size:10px}
#librarySearch{margin:10px 10px 7px;padding:8px 9px;border:1px solid var(--line);border-radius:6px;width:calc(100% - 20px);font-size:11px;outline:none}
#librarySearch:focus,.field input:focus,.field select:focus{border-color:#79a9d0;box-shadow:0 0 0 2px rgba(23,105,170,.08)}
#categoryList{display:flex;gap:4px;padding:0 10px 8px;overflow-x:auto;flex-shrink:0}
.category-btn{border:1px solid var(--line);background:#fff;border-radius:5px;padding:5px 7px;font-size:10px;color:#68798c;white-space:nowrap}
.category-btn.active{background:var(--blue2);color:var(--blue);border-color:#b7d2e8}
#componentList{overflow:auto;padding:2px 8px 12px;display:grid;grid-template-columns:1fr 1fr;gap:6px;align-content:start}
.component-card{border:1px solid #e1e8f0;border-radius:7px;background:#fff;min-height:75px;padding:6px 4px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;color:#3d5268}
.component-card:hover{border-color:#8eb7d7;background:#f7fbff}
.component-card svg{width:75px;height:38px;overflow:visible}
.component-card span{font-size:9px;line-height:1.2;text-align:center;max-width:100%;font-weight:600}
.library-note{padding:8px 10px;border-top:1px solid #edf1f5;color:#8a98a8;font-size:9px;line-height:1.45}
#canvasPanel{display:flex;flex-direction:column;min-width:0;min-height:0;background:#edf2f7;position:relative}
#canvasTabs{min-height:37px;flex:0 0 auto;display:flex;flex-wrap:wrap;align-items:center;padding:5px 12px;gap:5px;background:#f8fafc;border-bottom:1px solid #dfe7ef}
.canvas-tab{border:0;background:transparent;color:#718096;font-size:11px;padding:7px 10px;border-bottom:2px solid transparent}
.canvas-tab.active{color:var(--blue);font-weight:700;border-bottom-color:var(--blue)}
#schematicWrap,#profileWrap{flex:1;min-height:0;position:relative;overflow:hidden}
#schematic{display:block;width:100%;height:100%;background-color:#fbfdff;touch-action:none;cursor:default}
#schematic .grid-bg{fill:url(#gridPattern)}
.pipe-line{stroke:#2876a8;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}
.pipe-outline{stroke:#164f79;stroke-width:1.1;fill:none;opacity:.9}
.component-shape{stroke:#25465f;stroke-width:2.4;fill:#f8fbff;stroke-linecap:round;stroke-linejoin:round}
.component-detail{stroke:#25465f;stroke-width:1.8;fill:none;stroke-linecap:round;stroke-linejoin:round}
.component-fill{stroke:#25465f;stroke-width:2;fill:#dcebf5;stroke-linejoin:round}
.item-hitbox{fill:transparent;stroke:transparent;stroke-width:2;cursor:move}
.diagram-item.selected .item-hitbox{stroke:#2c91cf;stroke-dasharray:4 3;fill:rgba(44,145,207,.06)}
.item-label{font-family:var(--font);font-size:11px;font-weight:650;fill:#39536b;text-anchor:middle;pointer-events:none}
.pipe-label{font-family:var(--font);font-size:10px;fill:#557088;text-anchor:middle;pointer-events:none}
#profileWrap{display:flex;flex-direction:column;background:#fbfdff}
#profileSummary{min-height:42px;flex:0 0 auto;padding:6px 12px;display:flex;align-items:center;gap:9px 15px;flex-wrap:wrap;border-bottom:1px solid #e7edf3;background:#fff;color:#52677b;font-size:10px}
.profile-stat{white-space:nowrap}.profile-stat strong{color:#294c68;font-size:11px;margin-left:3px}
.profile-note{color:#8a6b3f;min-width:260px}
#profileSvg{flex:1;min-height:0;width:100%;height:auto;display:block;background:#fbfdff}
.profile-ground-area{fill:rgba(178,145,91,.16);stroke:none}
.profile-ground-line{fill:none;stroke:#98784c;stroke-width:2.6;stroke-linejoin:round}
.profile-pipe{fill:none;stroke:#2474a7;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.profile-grid{stroke:#e6edf4;stroke-width:1}
.profile-grid-major{stroke:#d7e1eb;stroke-width:1.2}
.profile-axis{stroke:#9aaaba;stroke-width:1.2}
.profile-label{font-size:11px;fill:#52677b}
.profile-small{font-size:9px;fill:#718398}
.profile-legend{font-size:11px;fill:#43596d;font-weight:650}
.canvas-empty{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;color:#8b9aaa;font-size:12px;pointer-events:none;line-height:1.7}
#profileEmpty{display:none;position:absolute;left:50%;top:58%;transform:translate(-50%,-50%);max-width:440px;line-height:1.6;background:rgba(255,255,255,.94);border:1px solid #dce4ee;border-radius:8px;box-shadow:var(--shadow)}
#inspectorContent{overflow:auto;padding:12px}
.empty-inspector{text-align:center;color:#8a98a8;font-size:11px;line-height:1.6;padding:34px 12px}
.field{display:flex;flex-direction:column;gap:5px;margin-bottom:11px}
.field label{font-size:10px;font-weight:700;color:#607286}
.field input,.field select{height:31px;border:1px solid #dce4ec;border-radius:5px;padding:5px 8px;color:#2b4055;background:#fff;font-size:11px;min-width:0;outline:none;width:100%}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.field-help{font-size:9px;color:#8b98a7;line-height:1.4;margin-top:-5px;margin-bottom:9px}
.inspector-actions{display:flex;gap:6px;margin-top:15px}
.inspector-actions button{flex:1;border:1px solid var(--line);background:#fff;border-radius:5px;padding:7px 4px;font-size:10px;color:#526477}
.inspector-actions button.delete{color:var(--danger);border-color:#efd3d5}
.k-chip{display:inline-block;padding:4px 7px;background:#eef5fa;border-radius:4px;color:#3b6687;font-size:10px;font-weight:700}
#profileControls{display:flex;align-items:center;gap:6px;margin-left:auto;font-size:10px;color:#6d7f91;white-space:nowrap}
#profileControls label{font-weight:650}
#profileControls input{width:54px;height:25px;border:1px solid var(--line);border-radius:4px;padding:3px 5px;font-size:10px}
#profileEmpty{padding:16px;text-align:center;color:#7f8fa0;font-size:11px}
@media(max-width:900px){#diagramWorkspace{grid-template-columns:190px minmax(250px,1fr) 220px}.brand small{display:none}}
@media(max-width:700px){#diagramWorkspace{grid-template-columns:150px minmax(200px,1fr)}#inspectorPanel{display:none}.status-text{display:none}.component-card svg{width:62px}}
</style>
</head>
<body>
<div id="app">
  <header id="topbar">
    <div class="brand">AquaPump <small>MODELADOR HIDRÁULICO</small></div>
    <div class="top-separator"></div>
    <div class="mode-switch">
      <button id="showMap" class="active" type="button">Mapa</button>
      <button id="showDiagram" type="button">Esquema hidráulico</button>
    </div>
    <div class="top-spacer"></div>
    <span id="statusText" class="status-text">Pronto</span>
  </header>

  <section id="mapPanel" class="view active">
    <div id="map"></div>
    <div class="map-hint">Desenhe a conduta no mapa para obter o comprimento e a diferença de cota. O esquema hidráulico é editado no separador correspondente.</div>
  </section>

  <section id="diagramPanel" class="view">
    <div id="diagramToolbar">
      <span class="tool-label">EDIÇÃO</span>
      <button id="drawPipeBtn" class="toolbar-btn" type="button">＋ Tubulação</button>
      <button id="rotateBtn" class="toolbar-btn" type="button">↻ Rodar</button>
      <button id="deleteBtn" class="toolbar-btn danger" type="button">Eliminar</button>
      <div class="tool-separator"></div>
      <button id="fitBtn" class="toolbar-btn" type="button">Enquadrar</button>
      <button id="clearBtn" class="toolbar-btn" type="button">Limpar esquema</button>
      <div class="top-spacer"></div>
      <span class="status-text">Arraste componentes da biblioteca para o esquema</span>
    </div>
    <div id="diagramWorkspace">
      <aside id="libraryPanel" class="side-panel">
        <div class="panel-heading">Biblioteca de componentes <span class="sub">25 acessórios</span></div>
        <input id="librarySearch" type="search" placeholder="Pesquisar acessório..." autocomplete="off">
        <div id="categoryList">
          <button class="category-btn active" data-category="todos">Todos</button>
          <button class="category-btn" data-category="curvas">Curvas</button>
          <button class="category-btn" data-category="valvulas">Válvulas</button>
          <button class="category-btn" data-category="transicoes">Transições</button>
          <button class="category-btn" data-category="outros">Outros</button>
        </div>
        <div id="componentList"></div>
        <div class="library-note">Símbolos técnicos esquemáticos. Seleccione um componente para editar DN, orientação, estado e coeficiente K.</div>
      </aside>

      <main id="canvasPanel">
        <div id="canvasTabs">
          <button class="canvas-tab active" id="tabSchematic" type="button">Esquema</button>
          <button class="canvas-tab" id="tabProfile" type="button">Perfil longitudinal</button>
          <div id="profileControls" style="display:none">
            <label for="coverDepth">Profundidade até ao eixo (m)</label>
            <input id="coverDepth" type="number" min="0" max="100" step="0.1" value="1.2" title="Distância vertical entre o terreno e o eixo da tubagem, em metros">
            <label for="profileStep">Amostragem</label>
            <input id="profileStep" type="number" min="10" max="500" step="10" value="50" title="Espaçamento aproximado entre pontos de cota, em metros">
            <label for="initialHgl">HGL inicial (m)</label>
            <input id="initialHgl" type="number" step="0.01" placeholder="Cota">
            <button id="refreshProfileBtn" class="toolbar-btn" type="button">Actualizar cotas</button>
          </div>
        </div>
        <div id="schematicWrap">
          <svg id="schematic" viewBox="0 0 1400 850" role="img" aria-label="Esquema do sistema hidráulico">
            <defs>
              <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e9eff5" stroke-width="1"/>
              </pattern>
            </defs>
            <rect class="grid-bg" x="-4000" y="-4000" width="8000" height="8000"/>
            <g id="pipeLayer"></g>
            <g id="componentLayer"></g>
          </svg>
          <div id="canvasEmpty" class="canvas-empty">O esquema está vazio.<br>Seleccione um acessório na biblioteca ou desenhe uma tubulação.</div>
        </div>
        <div id="profileWrap" style="display:none">
          <div id="profileSummary">O perfil será apresentado depois de desenhar uma conduta no mapa.</div>
          <svg id="profileSvg" viewBox="0 0 1200 610" preserveAspectRatio="none" aria-label="Perfil longitudinal do terreno, eixo da tubagem, HGL, EGL e acessórios"></svg>
          <div id="profileEmpty">Desenhe uma conduta no mapa. O AquaPump recolherá cotas ao longo de todo o percurso para construir o perfil longitudinal.</div>
        </div>
      </main>

      <aside id="inspectorPanel" class="side-panel">
        <div class="panel-heading">Propriedades <span class="sub" id="selectionType">Sem selecção</span></div>
        <div id="inspectorContent"><div class="empty-inspector">Seleccione uma tubulação ou acessório no esquema para consultar e editar as suas propriedades.</div></div>
      </aside>
    </div>
  </section>
</div>

<script>
(() => {
'use strict';

// Coeficientes reproduzidos da tabela Perdas._fator_localizadas() do projecto.
// São valores de referência internos da aplicação; não substituem dados do fabricante.
const ACCESSORIES = [
 {type:'ampliacao-gradual',name:'Ampliação gradual',category:'transicoes',k:0.30},
 {type:'comporta-aberta',name:'Comporta aberta',category:'valvulas',k:1.00},
 {type:'controlador-de-vazao',name:'Controlador de vazão',category:'valvulas',k:2.50},
 {type:'cotovelo-ou-joelho-45',name:'Cotovelo / joelho 45°',category:'curvas',k:0.40},
 {type:'cotovelo-ou-joelho-90',name:'Cotovelo / joelho 90°',category:'curvas',k:0.90},
 {type:'crivo',name:'Crivo',category:'outros',k:0.75},
 {type:'curva-22-5',name:'Curva 22,5°',category:'curvas',k:0.10},
 {type:'curva-45',name:'Curva 45°',category:'curvas',k:0.20},
 {type:'curva-90',name:'Curva 90°',category:'curvas',k:0.40},
 {type:'entrada-de-borda',name:'Entrada de borda',category:'outros',k:1.00},
 {type:'entrada-normal',name:'Entrada normal',category:'outros',k:0.50},
 {type:'juncao',name:'Junção',category:'outros',k:0.40},
 {type:'medidor-venturi',name:'Medidor Venturi',category:'outros',k:2.50},
 {type:'pequena-derivacao',name:'Pequena derivação',category:'outros',k:0.02},
 {type:'reducao-gradual',name:'Redução gradual',category:'transicoes',k:0.15},
 {type:'saida-livre',name:'Saída de canalização',category:'outros',k:1.00},
 {type:'te-passagem-directa',name:'Tê — passagem directa',category:'outros',k:0.60},
 {type:'te-saida-bilateral',name:'Tê — saída bilateral',category:'outros',k:1.80},
 {type:'te-saida-de-lado',name:'Tê — saída lateral',category:'outros',k:1.30},
 {type:'valvula-borboleta',name:'Válvula borboleta',category:'valvulas',k:0.30},
 {type:'valvula-angulo-aberta',name:'Válvula de ângulo aberta',category:'valvulas',k:5.00},
 {type:'valvula-gaveta-aberta',name:'Válvula de gaveta aberta',category:'valvulas',k:0.20},
 {type:'valvula-de-pe',name:'Válvula de pé',category:'valvulas',k:1.75},
 {type:'valvula-de-retencao',name:'Válvula de retenção',category:'valvulas',k:2.50},
 {type:'valvula-globo-aberta',name:'Válvula globo aberta',category:'valvulas',k:10.00}
];

const state = {
  map:null, bridge:{}, mapLayers:[], components:[], pipes:[], selected:null,
  activeCategory:'todos', activeCanvas:'schematic', pipeMode:false,
  drawingPipe:null, dragging:null, profile:[], profileReady:false,
  activeMapLayer:null, elevationCache:new Map(), profileLengthM:0,
  profileSampleSpacingM:50, profileError:null, profileRequestId:0,
  hydraulicProfile:null, hydraulicProfileError:null,
  viewBox:{x:0,y:0,w:1400,h:850}
};
const $ = id => document.getElementById(id);
const setStatus = msg => { $('statusText').textContent = msg; };
const uid = prefix => `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2,7)}`;
const accessoryByType = type => ACCESSORIES.find(a => a.type === type);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

// -------------------- QWebChannel / compatibilidade Python --------------------
function initWebChannel(){
  if (typeof QWebChannel === 'undefined' || !window.qt || !qt.webChannelTransport) return;
  new QWebChannel(qt.webChannelTransport, channel => {
    state.bridge = channel.objects || {};
    setStatus('Ligação ao AquaPump estabelecida');
    publishAccessories();
  });
}
function sendHeight(value){
  const n = Number(value);
  if (Number.isFinite(n) && state.bridge.altura && typeof state.bridge.altura.altura_ === 'function') {
    state.bridge.altura.altura_(n);
  }
}
function sendLength(value){
  const n = Number(value);
  if (Number.isFinite(n) && state.bridge.comprimento && typeof state.bridge.comprimento.comprimento_ === 'function') {
    state.bridge.comprimento.comprimento_(n);
  }
}
function projectComponentOnPipe(component){
  let best = null;
  for (const pipe of state.pipes) {
    const dx = pipe.x2 - pipe.x1, dy = pipe.y2 - pipe.y1;
    const length2 = dx*dx + dy*dy;
    if (length2 <= 1e-9) continue;
    const rawT = ((component.x-pipe.x1)*dx + (component.y-pipe.y1)*dy) / length2;
    const t = Math.max(0, Math.min(1, rawT));
    const px = pipe.x1 + t*dx, py = pipe.y1 + t*dy;
    const distance = Math.hypot(component.x-px, component.y-py);
    if (!best || distance < best.distance) best = {pipe, t, distance};
  }
  // O símbolo tem cerca de 116 unidades de largura. Um limite de 80
  // permite posicioná-lo sobre a linha sem associar peças distantes por engano.
  return best && best.distance <= 80 ? best : null;
}
function publishAccessories(){
  const pipes = state.pipes.map(p => ({
    id:p.id, x1:Number(p.x1), y1:Number(p.y1), x2:Number(p.x2), y2:Number(p.y2),
    comprimento_m:Number(p.lengthM), lengthM:Number(p.lengthM),
    diametro_dn:Number(p.dn), dn:Number(p.dn), material:p.material
  }));
  const components = state.components.map(c => {
    const link = projectComponentOnPipe(c);
    return {
      id:c.id, tipo:c.type, nome:c.name, cor:c.color,
      diametro_dn:Number(c.dn), dn:Number(c.dn),
      posicao_m:link ? link.t*Number(link.pipe.lengthM) : Number(c.positionM||0),
      orientacao:Number(c.rotation), estado:c.status,
      coeficiente_k:Number(c.k), x:Number(c.x), y:Number(c.y),
      troco_id:link ? link.pipe.id : null,
      distancia_tubulacao_svg:link ? Number(link.distance.toFixed(2)) : null
    };
  });
  const model = {
    versao_esquema:2,
    unidades:{comprimento:'m',diametro:'mm',caudal:'m3/s',cota:'m'},
    pipes, components,
    perfil_geografico:state.profileReady ? state.profile.map(p=>({progressiva_m:Number(p.distance),latitude:Number(p.lat),longitude:Number(p.lng),terreno_m:Number(p.elevation)})) : [],
    comprimento_perfil_geografico_m:Number(state.profileLengthM||0),
    profundidade_eixo_m:Math.max(0,Number($('coverDepth')?.value)||0),
    cota_piezometrica_inicial_m:$('initialHgl')?.value!=='' && Number.isFinite(Number($('initialHgl')?.value)) ? Number($('initialHgl').value) : null
  };
  const channel = state.bridge.acessorios;
  if (channel && typeof channel.modelo_hidraulico === 'function') {
    channel.modelo_hidraulico(model);
  } else if (channel && typeof channel.lista_acessorios === 'function') {
    // Compatibilidade com versões antigas de web_channel.py.
    channel.lista_acessorios(components);
  }
  const semLigacao = components.filter(c => !c.troco_id).length;
  if (semLigacao && pipes.length) {
    setStatus(`${semLigacao} acessório(s) fora da tubulação: coloque-os sobre um troço`);
  }
  return model;
}

// -------------------- Navegação principal --------------------
function showMode(mode){
  const isMap = mode === 'map';
  $('mapPanel').classList.toggle('active',isMap);
  $('diagramPanel').classList.toggle('active',!isMap);
  $('showMap').classList.toggle('active',isMap);
  $('showDiagram').classList.toggle('active',!isMap);
  if (isMap && state.map) setTimeout(()=>state.map.invalidateSize(),80);
  if (!isMap) renderDiagram();
}
$('showMap').addEventListener('click',()=>showMode('map'));
$('showDiagram').addEventListener('click',()=>showMode('diagram'));

// -------------------- Símbolos SVG dos acessórios --------------------
function glyph(type){
  const axis = '<path d="M-58 0 H58" class="pipe-line"/>';
  const body = (d,extra='') => `<path d="${d}" class="component-shape" ${extra}/>`;
  const detail = d => `<path d="${d}" class="component-detail"/>`;
  const circle = (x,y,r,extra='') => `<circle cx="${x}" cy="${y}" r="${r}" class="component-shape" ${extra}/>`;
  const rect = (x,y,w,h,rx=2) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" class="component-fill"/>`;
  let s = axis;
  switch(type){
    case 'ampliacao-gradual': s += body('M-28 -10 L8 -21 L28 -21 L28 21 L8 21 L-28 10 Z'); break;
    case 'reducao-gradual': s += body('M-28 -21 L8 -10 L28 -10 L28 10 L8 10 L-28 21 Z'); break;
    case 'comporta-aberta': s += body('M-18 -17 L0 0 L-18 17 Z M18 -17 L0 0 L18 17 Z') + detail('M0 -18 V-31 M-9 -31 H9'); break;
    case 'controlador-de-vazao': s += rect(-18,-18,36,36,4)+detail('M-10 0 H10 M0 -10 V10 M-5 -5 L5 5 M5 -5 L-5 5'); break;
    case 'cotovelo-ou-joelho-45': s = '<path d="M-58 0 H-15 Q-5 0 2 -8 L34 -40" class="pipe-line"/><path d="M-18 -7 Q-4 -7 4 -15" class="component-detail"/>'; break;
    case 'cotovelo-ou-joelho-90': s = '<path d="M-58 0 H5 Q18 0 18 13 V55" class="pipe-line"/><path d="M5 -8 Q26 -8 26 13" class="component-detail"/>'; break;
    case 'curva-22-5': s = '<path d="M-58 0 H8 Q19 0 25 -8 L48 -30" class="pipe-line"/><path d="M8 -7 Q24 -7 31 -17" class="component-detail"/>'; break;
    case 'curva-45': s = '<path d="M-58 0 H5 Q18 0 27 -9 L48 -30" class="pipe-line"/><path d="M5 -8 Q24 -8 32 -19" class="component-detail"/>'; break;
    case 'curva-90': s = '<path d="M-58 0 H0 Q18 0 18 18 V55" class="pipe-line"/><path d="M0 -8 Q26 -8 26 18" class="component-detail"/>'; break;
    case 'crivo': s += rect(-19,-15,38,30,3)+detail('M-12 -10 L12 10 M-12 0 L2 14 M-2 -14 L16 4 M-12 10 L12 -10 M-2 14 L16 -4'); break;
    case 'entrada-de-borda': s = '<path d="M-58 0 H35" class="pipe-line"/>'+body('M35 -17 V17 M35 -17 H48 M35 17 H48'); break;
    case 'entrada-normal': s = '<path d="M-58 0 H36" class="pipe-line"/>'+body('M36 -18 Q54 -18 54 0 Q54 18 36 18 Z'); break;
    case 'saida-livre': s = '<path d="M-58 0 H30" class="pipe-line"/>'+detail('M30 -18 V18 M30 -18 H45 M30 18 H45'); break;
    case 'juncao': s += body('M-18 -14 L0 0 L-18 14 Z M18 -14 L0 0 L18 14 Z')+detail('M0 0 V-31'); break;
    case 'medidor-venturi': s += body('M-34 -9 L-9 -9 L-2 -4 L2 -4 L9 -9 L34 -9 L34 9 L9 9 L2 4 L-2 4 L-9 9 L-34 9 Z')+detail('M0 -4 V-22 M-5 -22 H5'); break;
    case 'pequena-derivacao': s += detail('M0 0 V-30 M-8 -30 H8')+circle(0,0,5); break;
    case 'te-passagem-directa': s += detail('M0 0 V-31')+body('M-10 -4 L0 4 L10 -4'); break;
    case 'te-saida-bilateral': s += detail('M0 0 V-28 M0 0 V28 M-8 -28 H8 M-8 28 H8')+circle(0,0,6); break;
    case 'te-saida-de-lado': s += detail('M0 0 V-30 M-8 -30 H8')+circle(0,0,5); break;
    case 'valvula-borboleta': s += body('M-18 -18 L0 0 L-18 18 Z M18 -18 L0 0 L18 18 Z')+detail('M0 -18 V-29 M-9 -29 H9'); break;
    case 'valvula-angulo-aberta': s = '<path d="M-58 0 H-5 L24 -27 H58" class="pipe-line"/>'+body('M-18 -14 L0 0 L-18 14 Z M18 -14 L0 0 L18 14 Z')+detail('M0 -16 V-28'); break;
    case 'valvula-gaveta-aberta': s += body('M-18 -17 L0 0 L-18 17 Z M18 -17 L0 0 L18 17 Z')+detail('M0 -17 V-30 M-10 -30 H10 M-7 -34 L7 -26'); break;
    case 'valvula-de-pe': s += body('M-18 -14 L0 0 L-18 14 Z M18 -14 L0 0 L18 14 Z')+rect(-22,17,44,8,2)+detail('M-17 20 L-10 25 M-5 20 L2 25 M7 20 L14 25'); break;
    case 'valvula-de-retencao': s += body('M-18 -17 L18 0 L-18 17 Z')+detail('M20 -19 V19'); break;
    case 'valvula-globo-aberta': s += circle(0,0,18)+detail('M-11 11 L11 -11 M0 -18 V-31 M-9 -31 H9'); break;
    default: s += rect(-17,-14,34,28,4);
  }
  return `<svg viewBox="-65 -45 130 90" aria-hidden="true">${s}</svg>`;
}

// -------------------- Biblioteca de componentes --------------------
function renderLibrary(){
  const search = $('librarySearch').value.trim().toLocaleLowerCase('pt');
  const items = ACCESSORIES.filter(a => (state.activeCategory==='todos' || a.category===state.activeCategory) &&
    (!search || a.name.toLocaleLowerCase('pt').includes(search)));
  $('componentList').innerHTML = items.map(a =>
    `<button type="button" class="component-card" draggable="true" data-add-type="${a.type}" title="Adicionar ${esc(a.name)}">${glyph(a.type)}<span>${esc(a.name)}</span></button>`
  ).join('');
  $('componentList').querySelectorAll('[data-add-type]').forEach(btn=>{
    const type = btn.dataset.addType;
    btn.addEventListener('click',()=>addComponent(type,centerOfView()));
    btn.addEventListener('dragstart',event=>{
      event.dataTransfer.setData('application/x-aquapump-component',type);
      event.dataTransfer.effectAllowed='copy';
    });
  });
}
$('librarySearch').addEventListener('input',renderLibrary);
$('categoryList').querySelectorAll('[data-category]').forEach(btn=>btn.addEventListener('click',()=>{
  state.activeCategory=btn.dataset.category;
  $('categoryList').querySelectorAll('.category-btn').forEach(b=>b.classList.toggle('active',b===btn));
  renderLibrary();
}));

function centerOfView(){return {x:state.viewBox.x+state.viewBox.w/2,y:state.viewBox.y+state.viewBox.h/2};}
function addComponent(type, point){
  const meta = accessoryByType(type); if(!meta) return;
  const c = {id:uid('acc'),type:meta.type,name:meta.name,k:meta.k,dn:100,rotation:0,
    color:'#2876a8',status:'normalmente aberto',x:point.x,y:point.y,positionM:0};
  state.components.push(c); selectItem('component',c.id); renderDiagram(); publishAccessories();
  setStatus(`${meta.name} adicionado ao esquema`);
}
function snapPipeEndpoint(point){
  let nearest = null;
  for (const pipe of state.pipes) {
    for (const endpoint of [{x:pipe.x1,y:pipe.y1},{x:pipe.x2,y:pipe.y2}]) {
      const distance = Math.hypot(point.x-endpoint.x, point.y-endpoint.y);
      if (distance <= 22 && (!nearest || distance < nearest.distance)) {
        nearest = {x:endpoint.x,y:endpoint.y,distance};
      }
    }
  }
  return nearest ? {x:nearest.x,y:nearest.y} : point;
}
function addPipe(x1,y1,x2,y2){
  const start=snapPipeEndpoint({x:x1,y:y1});
  const end=snapPipeEndpoint({x:x2,y:y2});
  const p={id:uid('pipe'),x1:start.x,y1:start.y,x2:end.x,y2:end.y,lengthM:0,dn:0,material:'',roughness:null};
  state.pipes.push(p); selectItem('pipe',p.id); renderDiagram(); publishAccessories();
  setStatus('Troço criado. Defina o comprimento real, o DN e o material antes de calcular.');
}

// -------------------- Desenho SVG --------------------
function renderDiagram(){
  const pipeMarkup = state.pipes.map(p=>{
    const selected = state.selected?.kind==='pipe' && state.selected.id===p.id;
    const mx=(p.x1+p.x2)/2,my=(p.y1+p.y2)/2;
    return `<g class="pipe-item ${selected?'selected':''}" data-pipe-id="${p.id}">
      <line x1="${p.x1}" y1="${p.y1}" x2="${p.x2}" y2="${p.y2}" class="pipe-line"/>
      <line x1="${p.x1}" y1="${p.y1}" x2="${p.x2}" y2="${p.y2}" stroke="transparent" stroke-width="22" class="pipe-hit"/>
      <text x="${mx}" y="${my-10}" class="pipe-label">${Number(p.dn)>0?`DN ${p.dn}`:'DN por definir'} · ${Number(p.lengthM)>0?`${Number(p.lengthM).toFixed(1)} m`:'comprimento por definir'}</text>
      ${selected?`<circle cx="${p.x1}" cy="${p.y1}" r="6" fill="#fff" stroke="#2c91cf"/><circle cx="${p.x2}" cy="${p.y2}" r="6" fill="#fff" stroke="#2c91cf"/>`:''}
    </g>`;
  }).join('');
  const componentMarkup = state.components.map(c=>{
    const selected = state.selected?.kind==='component' && state.selected.id===c.id;
    return `<g class="diagram-item ${selected?'selected':''}" data-component-id="${c.id}" transform="translate(${c.x} ${c.y}) rotate(${c.rotation})">
      <rect class="item-hitbox" x="-62" y="-42" width="124" height="84" rx="7"/>
      ${glyph(c.type).replace('<svg viewBox="-65 -45 130 90" aria-hidden="true">','').replace('</svg>','')}
      <text class="item-label" x="0" y="55">${esc(c.name)}</text>
      <text class="pipe-label" x="0" y="68">DN ${Number(c.dn)} · K ${Number(c.k).toFixed(2)}</text>
    </g>`;
  }).join('');
  $('pipeLayer').innerHTML=pipeMarkup;
  $('componentLayer').innerHTML=componentMarkup;
  $('canvasEmpty').style.display=(state.pipes.length+state.components.length)?'none':'block';
  attachDiagramEvents();
  renderInspector();
}
function attachDiagramEvents(){
  $('componentLayer').querySelectorAll('[data-component-id]').forEach(node=>{
    node.addEventListener('pointerdown',event=>{
      event.stopPropagation();
      const id=node.dataset.componentId;
      selectItem('component',id);
      const c=state.components.find(x=>x.id===id); if(!c) return;
      state.dragging={kind:'component',id,start:svgPoint(event),originX:c.x,originY:c.y};
      $('schematic').setPointerCapture?.(event.pointerId);
      renderDiagram();
    });
  });
  $('pipeLayer').querySelectorAll('[data-pipe-id]').forEach(node=>{
    node.addEventListener('pointerdown',event=>{
      event.stopPropagation(); selectItem('pipe',node.dataset.pipeId);
    });
  });
}
function svgPoint(event){
  const svg=$('schematic'); const p=svg.createSVGPoint(); p.x=event.clientX; p.y=event.clientY;
  return p.matrixTransform(svg.getScreenCTM().inverse());
}
$('schematic').addEventListener('pointerdown',event=>{
  if(event.target.closest('[data-component-id]') || event.target.closest('[data-pipe-id]')) return;
  const p=svgPoint(event);
  if(state.pipeMode){const start=snapPipeEndpoint(p);state.drawingPipe={x1:start.x,y1:start.y,x2:start.x,y2:start.y};$('schematic').setPointerCapture?.(event.pointerId);return;}
  selectItem(null,null);
});
$('schematic').addEventListener('pointermove',event=>{
  if(state.dragging){
    const p=svgPoint(event); const c=state.components.find(x=>x.id===state.dragging.id);
    if(c){c.x=state.dragging.originX+(p.x-state.dragging.start.x);c.y=state.dragging.originY+(p.y-state.dragging.start.y);renderDiagram();}
  } else if(state.drawingPipe){
    const p=snapPipeEndpoint(svgPoint(event)); state.drawingPipe.x2=p.x;state.drawingPipe.y2=p.y;
    const old=$('temporaryPipe'); if(old) old.remove();
    const temp=document.createElementNS('http://www.w3.org/2000/svg','line');
    temp.setAttribute('id','temporaryPipe');temp.setAttribute('x1',state.drawingPipe.x1);temp.setAttribute('y1',state.drawingPipe.y1);
    temp.setAttribute('x2',p.x);temp.setAttribute('y2',p.y);temp.setAttribute('class','pipe-line');temp.setAttribute('stroke-dasharray','7 5');$('pipeLayer').appendChild(temp);
  }
});
$('schematic').addEventListener('pointerup',event=>{
  if(state.dragging){state.dragging=null;renderDiagram();publishAccessories();return;}
  if(state.drawingPipe){
    const p=snapPipeEndpoint(svgPoint(event));const d=state.drawingPipe;state.drawingPipe=null;
    const temp=$('temporaryPipe');if(temp)temp.remove();
    if(Math.hypot(p.x-d.x1,p.y-d.y1)>25)addPipe(d.x1,d.y1,p.x,p.y);
  }
});
$('schematic').addEventListener('pointercancel',()=>{state.dragging=null;state.drawingPipe=null;const temp=$('temporaryPipe');if(temp)temp.remove();});
$('schematic').addEventListener('dragover',event=>{event.preventDefault();event.dataTransfer.dropEffect='copy';});
$('schematic').addEventListener('drop',event=>{
  event.preventDefault();const type=event.dataTransfer.getData('application/x-aquapump-component');if(!type)return;
  const p=svgPoint(event);addComponent(type,p);
});

// -------------------- Inspector / propriedades --------------------
function selectItem(kind,id){state.selected=kind&&id?{kind,id}:null;renderDiagram();}
function renderInspector(){
  const panel=$('inspectorContent');
  if(!state.selected){$('selectionType').textContent='Sem selecção';panel.innerHTML='<div class="empty-inspector">Seleccione uma tubulação ou acessório no esquema para consultar e editar as suas propriedades.</div>';return;}
  if(state.selected.kind==='component'){
    const c=state.components.find(x=>x.id===state.selected.id);if(!c){state.selected=null;renderInspector();return;}
    $('selectionType').textContent='Acessório';
    panel.innerHTML=`
      <div class="field"><label>Componente</label><input value="${esc(c.name)}" disabled></div>
      <div class="field-row"><div class="field"><label>Diâmetro nominal (DN)</label><input id="propDn" type="number" min="1" step="1" value="${Number(c.dn)}"></div><div class="field"><label>Orientação (°)</label><input id="propRotation" type="number" step="15" value="${Number(c.rotation)}"></div></div>
      <div class="field"><label>Coeficiente de perda K</label><input id="propK" type="number" min="0" step="0.01" value="${Number(c.k)}"></div>
      <div class="field-help">Valor inicial copiado da tabela actual de perdas do AquaPump. Pode ser ajustado de acordo com o fabricante e a geometria real.</div>
      <div class="field"><label>Estado / configuração</label><select id="propStatus"><option ${c.status==='normalmente aberto'?'selected':''}>normalmente aberto</option><option ${c.status==='aberto'?'selected':''}>aberto</option><option ${c.status==='fechado'?'selected':''}>fechado</option><option ${c.status==='parcialmente aberto'?'selected':''}>parcialmente aberto</option><option ${c.status==='passagem livre'?'selected':''}>passagem livre</option></select></div>
      <div class="field-row"><div class="field"><label>Posição ao longo da conduta (m)</label><input id="propPosition" type="number" min="0" step="0.1" value="${Number(c.positionM)}"></div><div class="field"><label>Cor do símbolo</label><input id="propColor" type="color" value="${esc(c.color)}"></div></div>
      <div class="inspector-actions"><button id="rotateProp">Rodar 90°</button><button id="deleteProp" class="delete">Eliminar</button></div>`;
    $('propDn').addEventListener('change',e=>updateComponent(c,'dn',Math.max(1,Number(e.target.value)||c.dn)));
    $('propRotation').addEventListener('change',e=>updateComponent(c,'rotation',Number(e.target.value)||0));
    $('propK').addEventListener('change',e=>updateComponent(c,'k',Math.max(0,Number(e.target.value)||0)));
    $('propStatus').addEventListener('change',e=>updateComponent(c,'status',e.target.value));
    $('propPosition').addEventListener('change',e=>updateComponent(c,'positionM',Math.max(0,Number(e.target.value)||0)));
    $('propColor').addEventListener('change',e=>updateComponent(c,'color',e.target.value));
    $('rotateProp').addEventListener('click',()=>updateComponent(c,'rotation',(Number(c.rotation)+90)%360));
    $('deleteProp').addEventListener('click',deleteSelected);
  } else {
    const p=state.pipes.find(x=>x.id===state.selected.id);if(!p){state.selected=null;renderInspector();return;}
    $('selectionType').textContent='Tubulação';
    panel.innerHTML=`
      <div class="field"><label>Elemento</label><input value="Troço de tubulação" disabled></div>
      <div class="field-row"><div class="field"><label>Comprimento (m)</label><input id="pipeLength" type="number" min="0.01" step="0.1" value="${Number(p.lengthM)}"></div><div class="field"><label>Diâmetro nominal (DN)</label><input id="pipeDn" type="number" min="1" step="1" value="${Number(p.dn)}"></div></div>
      <div class="field"><label>Material</label><select id="pipeMaterial"><option value="" disabled ${!p.material?'selected':''}>Seleccionar material</option>${['PVC','PEAD','Aço carbono','Ferro fundido','PRFV','Betão','Cobre'].map(x=>`<option ${p.material===x?'selected':''}>${x}</option>`).join('')}</select></div>
      <div class="field-help">O comprimento real deve ser introduzido a partir do projecto ou obtido pelo traçado geográfico. O comprimento gráfico no esquema não está à escala.</div>
      <div class="inspector-actions"><button id="deleteProp" class="delete">Eliminar troço</button></div>`;
    $('pipeLength').addEventListener('change',e=>{p.lengthM=Math.max(.01,Number(e.target.value)||p.lengthM);renderDiagram();publishAccessories();});
    $('pipeDn').addEventListener('change',e=>{p.dn=Math.max(1,Number(e.target.value)||p.dn);renderDiagram();publishAccessories();});
    $('pipeMaterial').addEventListener('change',e=>{p.material=e.target.value;publishAccessories();});
    $('deleteProp').addEventListener('click',deleteSelected);
  }
}
function updateComponent(c,key,value){c[key]=value;renderDiagram();publishAccessories();}
function deleteSelected(){
  if(!state.selected)return;
  if(state.selected.kind==='component')state.components=state.components.filter(x=>x.id!==state.selected.id);
  else state.pipes=state.pipes.filter(x=>x.id!==state.selected.id);
  state.selected=null;renderDiagram();publishAccessories();
}

// -------------------- Ferramentas do esquema --------------------
$('drawPipeBtn').addEventListener('click',()=>{
  state.pipeMode=!state.pipeMode;
  $('drawPipeBtn').classList.toggle('primary',state.pipeMode);
  $('schematic').style.cursor=state.pipeMode?'crosshair':'default';
  setStatus(state.pipeMode?'Arraste no esquema para desenhar um troço de tubulação':'Modo de selecção activo');
});
$('rotateBtn').addEventListener('click',()=>{
  if(state.selected?.kind!=='component'){setStatus('Seleccione primeiro um acessório para o rodar');return;}
  const c=state.components.find(x=>x.id===state.selected.id);if(c){c.rotation=(c.rotation+90)%360;renderDiagram();publishAccessories();}
});
$('deleteBtn').addEventListener('click',deleteSelected);
$('clearBtn').addEventListener('click',()=>{
  if(!state.components.length&&!state.pipes.length)return;
  if(!window.confirm('Eliminar todos os componentes e troços deste esquema?'))return;
  state.components=[];state.pipes=[];state.selected=null;renderDiagram();publishAccessories();setStatus('Esquema limpo');
});
$('fitBtn').addEventListener('click',()=>{
  const all=[...state.components.map(c=>({x:c.x,y:c.y})),...state.pipes.flatMap(p=>[{x:p.x1,y:p.y1},{x:p.x2,y:p.y2}])];
  if(!all.length){$('schematic').setAttribute('viewBox','0 0 1400 850');return;}
  const xs=all.map(p=>p.x),ys=all.map(p=>p.y);const minX=Math.min(...xs)-130,maxX=Math.max(...xs)+130,minY=Math.min(...ys)-120,maxY=Math.max(...ys)+120;
  const w=Math.max(500,maxX-minX),h=Math.max(350,maxY-minY);$('schematic').setAttribute('viewBox',`${minX} ${minY} ${w} ${h}`);state.viewBox={x:minX,y:minY,w,h};
});
$('schematic').addEventListener('wheel',event=>{
  event.preventDefault();const p=svgPoint(event),factor=event.deltaY>0?1.1:.9;const vb=state.viewBox;
  const nw=Math.max(250,Math.min(4000,vb.w*factor)),nh=Math.max(160,Math.min(2600,vb.h*factor));
  const rx=(p.x-vb.x)/vb.w,ry=(p.y-vb.y)/vb.h;const nx=p.x-rx*nw,ny=p.y-ry*nh;
  state.viewBox={x:nx,y:ny,w:nw,h:nh};$('schematic').setAttribute('viewBox',`${nx} ${ny} ${nw} ${nh}`);
},{passive:false});

// -------------------- Perfil longitudinal --------------------
function showCanvasTab(tab){
  state.activeCanvas=tab;
  const schematic=tab==='schematic';
  $('schematicWrap').style.display=schematic?'block':'none';
  $('profileWrap').style.display=schematic?'none':'flex';
  $('tabSchematic').classList.toggle('active',schematic);
  $('tabProfile').classList.toggle('active',!schematic);
  $('profileControls').style.display=schematic?'none':'flex';
  if(!schematic){
    renderProfile();
    if(!state.profileReady && state.activeMapLayer) updateRoute(state.activeMapLayer);
  }
}
$('tabSchematic').addEventListener('click',()=>showCanvasTab('schematic'));
$('tabProfile').addEventListener('click',()=>showCanvasTab('profile'));
$('coverDepth').addEventListener('change',()=>{
  const input=$('coverDepth');
  const value=Number(input.value);
  if(!Number.isFinite(value)||value<0){input.value='1.2';}
  renderProfile();
  publishAccessories();
});
$('profileStep').addEventListener('change',()=>{
  const input=$('profileStep');
  const numeric=Number(input.value);
  const value=Number.isFinite(numeric)?Math.max(10,Math.min(500,numeric)):50;
  input.value=String(value);
  state.profileReady=false;
  if(state.activeMapLayer) updateRoute(state.activeMapLayer);
});
$('refreshProfileBtn').addEventListener('click',()=>{
  if(!state.activeMapLayer){setStatus('Desenhe primeiro uma conduta no mapa');return;}
  state.profileReady=false;
  updateRoute(state.activeMapLayer);
});
$('initialHgl').addEventListener('change',()=>{
  // A cota inicial é uma condição de fronteira, não uma estimativa do terreno.
  state.hydraulicProfile=null;
  state.hydraulicProfileError='Cota piezométrica alterada. Solicite novo cálculo hidráulico para actualizar HGL/EGL.';
  renderProfile();
  publishAccessories();
});

function renderProfile(){
  const svg=$('profileSvg');
  if(!state.profileReady || state.profile.length<2){
    svg.innerHTML='';
    $('profileEmpty').style.display='block';
    $('profileEmpty').textContent=state.profileError || 'Desenhe uma conduta no mapa. O AquaPump recolherá cotas ao longo de todo o percurso para construir o perfil longitudinal.';
    $('profileSummary').innerHTML=state.profileError
      ? `<span class="profile-note">${esc(state.profileError)}</span>`
      : 'A aguardar traçado geográfico e cotas de terreno.';
    return;
  }
  $('profileEmpty').style.display='none';

  const W=1200,H=610,pad={l:82,r:34,t:48,b:66};
  const data=state.profile;
  const distances=data.map(p=>p.distance);
  const terrain=data.map(p=>p.elevation);
  const depth=Math.max(0,Number($('coverDepth').value)||0);
  const pipeAxis=data.map(p=>p.elevation-depth);
  const hydraulic=state.hydraulicProfile && Array.isArray(state.hydraulicProfile.pontos)
    ? state.hydraulicProfile.pontos : [];
  const validHydraulic=hydraulic.filter(p=>Number.isFinite(Number(p.progressiva_m)) &&
    Number.isFinite(Number(p.hgl_m)) && Number.isFinite(Number(p.egl_m)));
  const allZ=terrain.concat(pipeAxis,validHydraulic.flatMap(p=>[Number(p.hgl_m),Number(p.egl_m)]));
  let minZ=Math.min(...allZ),maxZ=Math.max(...allZ);
  if(maxZ-minZ<2){const mid=(maxZ+minZ)/2;minZ=mid-1;maxZ=mid+1;}
  const zPad=(maxZ-minZ)*.12;minZ-=zPad;maxZ+=zPad;
  const minX=0,maxX=Math.max(1,state.profileLengthM||distances[distances.length-1]);
  const x=v=>pad.l+(v-minX)/(maxX-minX)*(W-pad.l-pad.r);
  const y=v=>H-pad.b-(v-minZ)/(maxZ-minZ)*(H-pad.t-pad.b);
  const makePath=values=>data.map((p,i)=>`${i?'L':'M'} ${x(p.distance).toFixed(2)} ${y(values[i]).toFixed(2)}`).join(' ');
  const groundPath=makePath(terrain);
  const pipePath=makePath(pipeAxis);
  const hydraulicPath=(key)=>validHydraulic.map((p,i)=>`${i?'L':'M'} ${x(Math.max(minX,Math.min(maxX,Number(p.progressiva_m)))).toFixed(2)} ${y(Number(p[key])).toFixed(2)}`).join(' ');
  const hglPath=validHydraulic.length>=2?hydraulicPath('hgl_m'):'';
  const eglPath=validHydraulic.length>=2?hydraulicPath('egl_m'):'';
  const area=`${groundPath} L ${x(maxX)} ${H-pad.b} L ${x(minX)} ${H-pad.b} Z`;

  const grid=[];
  const yTicks=6;
  for(let i=0;i<=yTicks;i++){
    const value=maxZ-(maxZ-minZ)*i/yTicks;
    const yy=y(value);
    grid.push(`<line x1="${pad.l}" y1="${yy}" x2="${W-pad.r}" y2="${yy}" class="${i===yTicks?'profile-grid-major':'profile-grid'}"/>`);
    grid.push(`<text x="${pad.l-12}" y="${yy+4}" text-anchor="end" class="profile-small">${value.toFixed(1)}</text>`);
  }
  const xTicks=5;
  for(let i=0;i<=xTicks;i++){
    const value=maxX*i/xTicks,xx=x(value);
    grid.push(`<line x1="${xx}" y1="${pad.t}" x2="${xx}" y2="${H-pad.b}" class="profile-grid"/>`);
    grid.push(`<text x="${xx}" y="${H-pad.b+20}" text-anchor="middle" class="profile-small">${value.toFixed(0)}</text>`);
  }

  const markerIndices=new Set([0,data.length-1]);
  const markerStride=Math.max(1,Math.floor(data.length/8));
  for(let i=markerStride;i<data.length-1;i+=markerStride)markerIndices.add(i);
  const markers=[...markerIndices].sort((a,b)=>a-b).map(i=>{
    const p=data[i];
    return `<circle cx="${x(p.distance)}" cy="${y(p.elevation)}" r="3.6" fill="#98784c"><title>Estaca ${p.distance.toFixed(1)} m · terreno ${p.elevation.toFixed(2)} m</title></circle>`;
  }).join('');
  const accessoryMarkers=(state.hydraulicProfile?.acessorios||[]).map(item=>{
    const chainage=Number(item.progressiva_m);
    if(!Number.isFinite(chainage))return '';
    const sample=data.reduce((best,p)=>Math.abs(p.distance-chainage)<Math.abs(best.distance-chainage)?p:best,data[0]);
    return `<path d="M ${x(chainage)-5} ${y(sample.elevation)-12} l 5 -7 l 5 7 z" fill="#6b4ca5"><title>${esc(item.nome)} · progressiva ${chainage.toFixed(1)} m · perda ${Number(item.perda_m||0).toFixed(3)} m</title></path>`;
  }).join('');
  const start=data[0],finish=data[data.length-1];
  const rise=finish.elevation-start.elevation;
  const ascent=data.slice(1).reduce((sum,p,i)=>sum+Math.max(0,p.elevation-data[i].elevation),0);
  const descent=data.slice(1).reduce((sum,p,i)=>sum+Math.max(0,data[i].elevation-p.elevation),0);
  const avgSlope=state.profileLengthM>0?100*rise/state.profileLengthM:0;
  const actualSpacing=state.profileLengthM/Math.max(1,data.length-1);
  const zeroElevationCount=terrain.filter(value=>value===0).length;
  const pressureValues=validHydraulic.map(p=>Number(p.pressao_estatica_m)).filter(Number.isFinite);
  const minPressure=pressureValues.length?Math.min(...pressureValues):null;
  const maxPressure=pressureValues.length?Math.max(...pressureValues):null;
  const legendY=25;

  svg.innerHTML=`
    ${grid.join('')}
    <path d="${area}" class="profile-ground-area"/>
    <path d="${groundPath}" class="profile-ground-line"/>
    <path d="${pipePath}" class="profile-pipe"/>
    ${hglPath?`<path d="${hglPath}" fill="none" stroke="#16845b" stroke-width="2.8" stroke-dasharray="8 4"><title>Linha piezométrica (HGL)</title></path>`:''}
    ${eglPath?`<path d="${eglPath}" fill="none" stroke="#bd6a22" stroke-width="2.8" stroke-dasharray="3 4"><title>Linha de energia (EGL)</title></path>`:''}
    <line x1="${pad.l}" y1="${H-pad.b}" x2="${W-pad.r}" y2="${H-pad.b}" class="profile-axis"/>
    <line x1="${pad.l}" y1="${pad.t}" x2="${pad.l}" y2="${H-pad.b}" class="profile-axis"/>
    ${markers}
    ${accessoryMarkers}
    <circle cx="${x(start.distance)}" cy="${y(start.elevation)}" r="5" fill="#98784c"><title>Início · cota ${start.elevation.toFixed(2)} m</title></circle>
    <circle cx="${x(finish.distance)}" cy="${y(finish.elevation)}" r="5" fill="#98784c"><title>Fim · cota ${finish.elevation.toFixed(2)} m</title></circle>
    <text x="${x(start.distance)+8}" y="${y(start.elevation)-12}" class="profile-small">Início ${start.elevation.toFixed(2)} m</text>
    <text x="${x(finish.distance)-8}" y="${y(finish.elevation)-12}" text-anchor="end" class="profile-small">Fim ${finish.elevation.toFixed(2)} m</text>
    <line x1="${W-330}" y1="${legendY}" x2="${W-300}" y2="${legendY}" class="profile-ground-line"/>
    <text x="${W-293}" y="${legendY+4}" class="profile-legend">Terreno (MDE)</text>
    <line x1="${W-175}" y1="${legendY}" x2="${W-145}" y2="${legendY}" class="profile-pipe"/>
    <text x="${W-138}" y="${legendY+4}" class="profile-legend">Eixo indicativo</text>
    ${hglPath?`<line x1="${W-330}" y1="${legendY+18}" x2="${W-300}" y2="${legendY+18}" stroke="#16845b" stroke-width="2.8" stroke-dasharray="8 4"/><text x="${W-293}" y="${legendY+22}" class="profile-legend">HGL</text>`:''}
    ${eglPath?`<line x1="${W-175}" y1="${legendY+18}" x2="${W-145}" y2="${legendY+18}" stroke="#bd6a22" stroke-width="2.8" stroke-dasharray="3 4"/><text x="${W-138}" y="${legendY+22}" class="profile-legend">EGL</text>`:''}
    <text x="${W/2}" y="${H-15}" text-anchor="middle" class="profile-label">Distância acumulada ao longo da conduta (m)</text>
    <text x="20" y="${H/2}" transform="rotate(-90 20 ${H/2})" text-anchor="middle" class="profile-label">Cota altimétrica (m)</text>
  `;

  $('profileSummary').innerHTML=`
    <span class="profile-stat">Comprimento<strong>${maxX.toFixed(1)} m</strong></span>
    <span class="profile-stat">Cota inicial<strong>${start.elevation.toFixed(2)} m</strong></span>
    <span class="profile-stat">Cota final<strong>${finish.elevation.toFixed(2)} m</strong></span>
    <span class="profile-stat">Desnível<strong>${rise>=0?'+':''}${rise.toFixed(2)} m</strong></span>
    <span class="profile-stat">Declive médio<strong>${avgSlope.toFixed(2)}%</strong></span>
    <span class="profile-stat">Subida acumulada<strong>${ascent.toFixed(1)} m</strong></span>
    <span class="profile-stat">Descida acumulada<strong>${descent.toFixed(1)} m</strong></span>
    <span class="profile-stat">Pontos / intervalo<strong>${data.length} / ${actualSpacing.toFixed(0)} m</strong></span>
    ${validHydraulic.length>=2?`<span class="profile-stat">HGL inicial<strong>${Number(validHydraulic[0].hgl_m).toFixed(2)} m</strong></span><span class="profile-stat">HGL final<strong>${Number(validHydraulic[validHydraulic.length-1].hgl_m).toFixed(2)} m</strong></span>`:''}
    ${pressureValues.length?`<span class="profile-stat">Pressão mínima<strong>${minPressure.toFixed(2)} m.c.a.</strong></span><span class="profile-stat">Pressão máxima<strong>${maxPressure.toFixed(2)} m.c.a.</strong></span>`:''}
    <span class="profile-note">Terreno: modelo digital, não levantamento. Eixo: profundidade definida até ao eixo da tubagem. ${validHydraulic.length>=2?'HGL/EGL recebidas do modelo hidráulico.':'HGL/EGL aguardam cálculo hidráulico e condição de fronteira.'}${state.hydraulicProfileError?` ${esc(state.hydraulicProfileError)}`:''}${zeroElevationCount?` ${zeroElevationCount} cota(s) chegaram como 0 m; confirme se são reais.`:''}</span>
  `;
}

function interpolateGeodesic(a,b,t){
  const rad=Math.PI/180;
  const lat1=a.lat*rad,lon1=a.lng*rad,lat2=b.lat*rad,lon2=b.lng*rad;
  const v1=[Math.cos(lat1)*Math.cos(lon1),Math.cos(lat1)*Math.sin(lon1),Math.sin(lat1)];
  const v2=[Math.cos(lat2)*Math.cos(lon2),Math.cos(lat2)*Math.sin(lon2),Math.sin(lat2)];
  const dot=Math.max(-1,Math.min(1,v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]));
  const omega=Math.acos(dot);
  if(omega<1e-10)return {lat:a.lat+(b.lat-a.lat)*t,lng:a.lng+(b.lng-a.lng)*t};
  const sinOmega=Math.sin(omega);
  const wa=Math.sin((1-t)*omega)/sinOmega,wb=Math.sin(t*omega)/sinOmega;
  const x=wa*v1[0]+wb*v2[0],y=wa*v1[1]+wb*v2[1],z=wa*v1[2]+wb*v2[2];
  return {lat:Math.atan2(z,Math.hypot(x,y))/rad,lng:Math.atan2(y,x)/rad};
}
function interpolateRoute(points, requestedSpacing=50, maxSamples=120){
  if(!Array.isArray(points)||points.length<2)throw new Error('A conduta precisa de pelo menos dois pontos.');
  const cumulative=[0];
  for(let i=1;i<points.length;i++){
    cumulative.push(cumulative[i-1]+points[i-1].distanceTo(points[i]));
  }
  const total=cumulative[cumulative.length-1];
  if(!Number.isFinite(total)||total<=0)throw new Error('O comprimento do traçado é nulo.');
  const count=Math.max(2,Math.min(maxSamples,Math.ceil(total/Math.max(10,requestedSpacing))+1));
  const samples=[],distances=[];
  let segment=0;
  for(let i=0;i<count;i++){
    const chainage=total*i/(count-1);
    while(segment<cumulative.length-2 && cumulative[segment+1]<chainage)segment++;
    const segmentLength=cumulative[segment+1]-cumulative[segment];
    const ratio=segmentLength>0?(chainage-cumulative[segment])/segmentLength:0;
    samples.push(interpolateGeodesic(points[segment],points[segment+1],ratio));
    distances.push(chainage);
  }
  return {points:samples,distances,totalLength:total,actualSpacing:total/(count-1)};
}

async function fetchElevations(coords){
  if(!Array.isArray(coords)||!coords.length)return [];
  const results=new Array(coords.length);
  const missing=[];
  coords.forEach((point,index)=>{
    const key=`${Number(point.lat).toFixed(5)},${Number(point.lng).toFixed(5)}`;
    if(state.elevationCache.has(key))results[index]=state.elevationCache.get(key);
    else missing.push({index,point,key});
  });
  // A API pública é consultada em lotes pequenos para evitar pedidos excessivos.
  const batchSize=25;
  for(let offset=0;offset<missing.length;offset+=batchSize){
    const batch=missing.slice(offset,offset+batchSize);
    const locations=batch.map(x=>`${Number(x.point.lat).toFixed(6)},${Number(x.point.lng).toFixed(6)}`).join('|');
    const url=`https://api.open-elevation.com/api/v1/lookup?locations=${encodeURIComponent(locations)}`;
    const response=await fetch(url);
    if(!response.ok)throw new Error(`Serviço de elevação indisponível (HTTP ${response.status}).`);
    const payload=await response.json();
    const elevations=payload.results||[];
    if(elevations.length!==batch.length)throw new Error('O serviço de elevação devolveu uma quantidade incompleta de cotas.');
    elevations.forEach((item,i)=>{
      const elevation=Number(item.elevation);
      if(!Number.isFinite(elevation))throw new Error('O serviço devolveu uma cota inválida.');
      const entry=batch[i];
      state.elevationCache.set(entry.key,elevation);
      results[entry.index]=elevation;
    });
  }
  return results;
}
function flattenLatLngs(value){
  if(!Array.isArray(value))return [];
  if(value.length&&value[0]&&typeof value[0].lat==='number')return value;
  return value.flatMap(flattenLatLngs);
}
async function updateRoute(layer){
  const points=flattenLatLngs(layer.getLatLngs());
  if(points.length<2)return;
  state.activeMapLayer=layer;
  const requestId=++state.profileRequestId;
  state.profileReady=false;
  state.profileError=null;
  const requestedSpacing=Math.max(10,Math.min(500,Number($('profileStep').value)||50));
  state.profileSampleSpacingM=requestedSpacing;
  try{
    const route=interpolateRoute(points,requestedSpacing,120);
    state.profileLengthM=route.totalLength;
    sendLength(route.totalLength);
    setStatus(`A obter cotas ao longo de ${route.totalLength.toFixed(0)} m…`);
    const elevations=await fetchElevations(route.points);
    if(requestId!==state.profileRequestId)return;
    if(elevations.length!==route.points.length)throw new Error('Não foi possível obter as cotas de todo o percurso.');
    state.profile=route.points.map((point,index)=>({
      distance:route.distances[index],
      elevation:elevations[index],
      lat:point.lat,
      lng:point.lng
    }));
    state.profileReady=true;
    const first=elevations[0],last=elevations[elevations.length-1];
    // Mantém o contrato legado: o cálculo existente recebe o módulo do desnível.
    sendHeight(Math.abs(last-first));
    renderProfile();
    publishAccessories();
    setStatus(`Perfil actualizado · ${(route.totalLength/1000).toFixed(2)} km · ${elevations.length} cotas`);
  }catch(err){
    if(requestId!==state.profileRequestId)return;
    state.profile=[];
    state.profileReady=false;
    state.profileError=`Não foi possível obter o perfil: ${err.message}`;
    renderProfile();
    setStatus('Comprimento actualizado; cotas indisponíveis');
    console.warn('Falha ao construir perfil longitudinal:',err);
  }
}

// -------------------- Mapa geográfico Leaflet --------------------
function initMap(){
  if(typeof L==='undefined'){setStatus('Biblioteca cartográfica indisponível');return;}
  const streets=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'});
  const satellite=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{attribution:'Tiles &copy; Esri'});
  state.map=L.map('map',{center:[-25.9667,32.5833],zoom:12,layers:[streets],doubleClickZoom:false});
  L.control.layers({'Padrão':streets,'Satélite':satellite}).addTo(state.map);
  L.control.scale({metric:true,imperial:false}).addTo(state.map);
  const drawn=new L.FeatureGroup().addTo(state.map);
  new L.Control.Draw({edit:{featureGroup:drawn},draw:{polyline:{shapeOptions:{color:'#1769aa',weight:4}},polygon:false,rectangle:false,circle:false,circlemarker:false,marker:false}}).addTo(state.map);
  state.map.on(L.Draw.Event.CREATED,async event=>{
    const layer=event.layer;drawn.addLayer(layer);state.mapLayers.push(layer);state.activeMapLayer=layer;
    await updateRoute(layer);
    layer.bindPopup(`<strong>Conduta desenhada</strong><br>Comprimento: ${state.profileLengthM.toFixed(1)} m`).openPopup();
  });
  state.map.on(L.Draw.Event.EDITED,event=>event.layers.eachLayer(layer=>{
    state.activeMapLayer=layer;
    updateRoute(layer);
  }));
  state.map.on(L.Draw.Event.DELETED,event=>{
    event.layers.eachLayer(layer=>{state.mapLayers=state.mapLayers.filter(x=>x!==layer);});
    if(state.activeMapLayer && !state.mapLayers.includes(state.activeMapLayer)){
      state.activeMapLayer=state.mapLayers[state.mapLayers.length-1]||null;
    }
    if(state.activeMapLayer){updateRoute(state.activeMapLayer);}
    else{
      state.profileRequestId++;
      state.profile=[];state.profileLengthM=0;state.profileReady=false;state.profileError=null;
      sendLength(0);sendHeight(0);renderProfile();publishAccessories();
    }
  });
  state.map.on('locationerror',()=>setStatus('Localização indisponível; pode navegar manualmente no mapa'));
  state.map.locate({setView:true,maxZoom:15,enableHighAccuracy:true});
}
window.pesquisar_lugar = async function(lugar){
  const query=String(lugar||'').trim();if(!query||!state.map)return;
  try{
    const response=await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
    if(!response.ok)throw new Error('Pesquisa indisponível');const data=await response.json();
    if(data.length)state.map.setView([Number(data[0].lat),Number(data[0].lon)],13);
    else setStatus('Local não encontrado');
  }catch(error){setStatus('Erro na pesquisa do local');console.warn(error);}
};

// -------------------- Funções chamadas pelo Python --------------------
window.receber_dados=function(v1,v2,v3,v4){
  const values=[v1,v2,v3,v4].map(Number);
  document.querySelectorAll('.leaflet-interactive').forEach((layer)=>{
    if(layer._path)layer._path.setAttribute('data-aquapump-values',values.join(','));
  });
};
window.receber_unidades=function(u1,u2,u3,u4){
  // Mantém a assinatura usada por Dados.enviar_unidades() no Python.
  window.aquapumpUnits={vazao:u1,diametro:u2,altura:u3,potencia:u4};
};
// Alias legado para versões anteriores de web_channel.py.
window.definir_unidades=window.receber_unidades;

// Recebe o resultado produzido por ModeloHidraulico.gerar_perfil_longitudinal().
// Contrato: {valido:true, pontos:[{progressiva_m,hgl_m,egl_m,...}], avisos:[]}
window.receber_perfil_hidraulico=function(resultado){
  if(!resultado || resultado.valido!==true || !Array.isArray(resultado.pontos)){
    state.hydraulicProfile=null;
    state.hydraulicProfileError='O motor hidráulico devolveu um perfil inválido.';
    renderProfile();
    return false;
  }
  const pontos=resultado.pontos.filter(p=>Number.isFinite(Number(p.progressiva_m)) &&
    Number.isFinite(Number(p.hgl_m)) && Number.isFinite(Number(p.egl_m)));
  if(pontos.length<2){
    state.hydraulicProfile=null;
    state.hydraulicProfileError='O perfil hidráulico precisa de pelo menos dois pontos válidos.';
    renderProfile();
    return false;
  }
  state.hydraulicProfile={...resultado,pontos};
  state.hydraulicProfileError=(resultado.avisos||[]).join(' ');
  renderProfile();
  setStatus('Perfil hidráulico actualizado · HGL/EGL recebidas do motor');
  return true;
};
window.limpar_perfil_hidraulico=function(){
  state.hydraulicProfile=null;state.hydraulicProfileError=null;renderProfile();
};

// -------------------- Inicialização --------------------
function boot(){
  renderLibrary();renderDiagram();initMap();initWebChannel();
  setStatus('Interface pronta');
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
</body>
</html>'''
