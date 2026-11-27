"""Editor geográfico do AquaPump.

O mapa é o ambiente principal de desenho e edição. As tubulações, acessórios,
propriedades e o perfil longitudinal usam o mesmo modelo de dados e a mesma
geometria geográfica.

Compatibilidade: MainWindow instancia Mapa() e carrega Mapa.html_code no
QWebEngineView. O modelo é enviado pelo objecto QWebChannel "acessorios".
"""


class Mapa:
    def __init__(self):
        self.html_code = r'''<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Editor hidráulico geográfico</title>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<style>
:root{--bg:#f1f5f9;--panel:#fff;--line:#dce4ed;--text:#192b3d;--muted:#64768a;--blue:#1769aa;--blue-light:#eaf3fb;--teal:#12877d;--red:#b63b45;--amber:#a96c16;--shadow:0 4px 18px rgba(21,46,72,.11);--radius:9px;font-family:"Segoe UI",Arial,sans-serif}
*{box-sizing:border-box}html,body,#app{height:100%;width:100%;margin:0;overflow:hidden}body{background:var(--bg);color:var(--text);font-size:13px}button,input,select{font:inherit}button{cursor:pointer}
#app{display:flex;flex-direction:column}
#topbar{height:54px;flex:0 0 54px;display:flex;align-items:center;gap:9px;padding:0 13px;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 1px 4px rgba(0,0,0,.04);z-index:1000}
.brand{font-size:16px;font-weight:800;color:#143b5b;white-space:nowrap}.brand small{font-size:9px;color:#8090a1;font-weight:600;letter-spacing:.7px;margin-left:5px}.sep{height:25px;width:1px;background:var(--line);margin:0 3px}
.btn{height:32px;border:1px solid var(--line);border-radius:6px;background:#fff;color:#40576c;padding:0 10px;font-size:11px;font-weight:650;white-space:nowrap}.btn:hover{background:#f5f9fc;border-color:#a9c6dd}.btn.primary{background:var(--blue);border-color:var(--blue);color:#fff}.btn.primary:hover{background:#0f5792}.btn.active{background:var(--blue-light);border-color:#a8cbe5;color:var(--blue)}.btn.danger{color:var(--red)}.btn:disabled{opacity:.42;cursor:not-allowed}
#topSpacer{flex:1}#status{font-size:10px;color:#6e8092;white-space:nowrap;max-width:270px;overflow:hidden;text-overflow:ellipsis}
#workspace{flex:1;min-height:0;display:grid;grid-template-columns:222px minmax(300px,1fr) 270px;gap:0}
.panel{min-height:0;display:flex;flex-direction:column;background:#fff}.panel.left{border-right:1px solid var(--line)}.panel.right{border-left:1px solid var(--line)}.panelHead{height:45px;flex:0 0 45px;border-bottom:1px solid #e9eef3;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:11px;font-weight:800;color:#314a60}.panelHead small{font-size:9px;color:#8392a2;font-weight:500}
#librarySearch{margin:10px 9px 7px;width:calc(100% - 18px);height:31px;border:1px solid var(--line);border-radius:6px;padding:0 9px;font-size:11px;outline:none}#categoryList{display:flex;gap:4px;padding:0 9px 8px;overflow-x:auto} .cat{border:1px solid var(--line);background:#fff;border-radius:5px;padding:5px 7px;font-size:9px;color:#6d7f91;white-space:nowrap}.cat.active{background:var(--blue-light);border-color:#b8d4e9;color:var(--blue)}
#componentList{overflow:auto;padding:2px 8px 10px;display:grid;grid-template-columns:1fr 1fr;gap:6px;align-content:start}.componentCard{min-height:70px;border:1px solid #e0e7ef;border-radius:7px;background:#fff;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;color:#365168;padding:6px 3px}.componentCard:hover{border-color:#85b1d3;background:#f6fbff}.componentCard.selected{border-color:#1769aa;background:#eaf3fb;box-shadow:0 0 0 2px rgba(23,105,170,.12)}.componentIcon{width:27px;height:27px;border-radius:50%;background:#eaf3fb;color:#1769aa;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800}.componentCard b{font-size:9px;text-align:center;line-height:1.2}.componentCard small{font-size:8px;color:#8795a4}.libraryNote{margin-top:auto;padding:9px 10px;border-top:1px solid #edf1f5;color:#8997a6;font-size:9px;line-height:1.45}
#mapArea{position:relative;min-width:0;min-height:0;background:#e7edf2}#map{height:100%;width:100%;position:relative;z-index:1;touch-action:pan-x pan-y;background-color:#e7edf2;background-image:linear-gradient(45deg,#dce4eb 25%,transparent 25%),linear-gradient(-45deg,#dce4eb 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#dce4eb 75%),linear-gradient(-45deg,transparent 75%,#dce4eb 75%);background-size:22px 22px;background-position:0 0,0 11px,11px -11px,-11px 0}
.mapOverlay{position:absolute;z-index:450;left:12px;top:12px;display:flex;gap:6px;align-items:center;flex-wrap:wrap;max-width:calc(100% - 24px)}.mapSearch{height:32px;width:200px;border:1px solid #d8e1ea;border-radius:6px;background:#fff;padding:0 9px;font-size:11px;box-shadow:var(--shadow);outline:none}.mapHint{position:absolute;z-index:450;left:12px;bottom:13px;max-width:390px;padding:8px 10px;background:rgba(255,255,255,.95);border:1px solid var(--line);border-radius:7px;box-shadow:var(--shadow);font-size:10px;line-height:1.45;color:#52677b;pointer-events:none}.mapHint strong{color:#2b4e6b}
#mapFallback{display:none;position:absolute;inset:0;z-index:600;background:#f7fafc;align-items:center;justify-content:center;text-align:center;padding:30px;color:#596e82}.fallbackCard{max-width:470px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px;box-shadow:var(--shadow)}.fallbackCard h3{margin:0 0 8px;color:#203d58}.fallbackCard p{font-size:12px;line-height:1.55}.fallbackCard button{margin-top:8px}
#inspector{overflow:auto;padding:12px}.empty{color:#8a98a7;font-size:11px;line-height:1.6;padding:30px 8px;text-align:center}.field{display:flex;flex-direction:column;gap:5px;margin-bottom:10px}.field label{font-size:10px;color:#60758a;font-weight:750}.field input,.field select,.field textarea{height:31px;border:1px solid #dce4ec;border-radius:5px;padding:5px 8px;background:#fff;color:#294158;font-size:11px;outline:none;min-width:0;width:100%}.field textarea{height:62px;resize:vertical}.field input:focus,.field select:focus,.field textarea:focus{border-color:#79a9d0;box-shadow:0 0 0 2px rgba(23,105,170,.08)}.fieldRow{display:grid;grid-template-columns:1fr 1fr;gap:8px}.help{font-size:9px;color:#8b98a6;line-height:1.4;margin:-4px 0 10px}.actions{display:flex;gap:6px;margin-top:13px}.actions .btn{flex:1}.pill{display:inline-flex;align-items:center;padding:4px 7px;border-radius:4px;background:#edf5fa;color:#31658a;font-weight:800;font-size:9px}.warning{background:#fff7e8;border:1px solid #f0d8a9;color:#8b621f;padding:8px;border-radius:6px;font-size:10px;line-height:1.4;margin:0 0 10px}
.leaflet-container{font-family:"Segoe UI",Arial,sans-serif}.leaflet-control-attribution{font-size:9px!important}.leaflet-popup-content{font-size:11px}.leaflet-div-icon{background:transparent;border:0}.accMarker{width:25px;height:25px;border:2px solid #fff;border-radius:50%;background:#216e9f;box-shadow:0 1px 5px rgba(0,0,0,.35);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800}.accMarker.unattached{background:#c17b21}.vertexHandle{width:13px;height:13px;border-radius:50%;background:#fff;border:2px solid #1478ba;box-shadow:0 1px 4px rgba(0,0,0,.22)}.snapHalo{width:24px;height:24px;border-radius:50%;border:2px solid #16a085;background:rgba(22,160,133,.15);box-shadow:0 0 0 4px rgba(22,160,133,.12)}
#profileModal{display:none;position:fixed;inset:0;z-index:2000;background:rgba(16,34,52,.48);padding:24px;align-items:center;justify-content:center}#profileCard{width:min(1120px,96vw);height:min(760px,92vh);background:#fff;border-radius:11px;box-shadow:0 12px 50px rgba(0,0,0,.28);display:flex;flex-direction:column;overflow:hidden}#profileHeader{height:49px;flex:0 0 49px;padding:0 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line)}#profileTitle{font-size:13px;font-weight:800;color:#23445f}#profileHeader .spacer{flex:1}#profileControls{display:flex;align-items:center;gap:7px;font-size:10px;color:#63778a}#profileControls input{height:27px;width:62px;border:1px solid var(--line);border-radius:5px;padding:3px 5px;font-size:10px}#profileSummary{padding:10px 14px;min-height:48px;display:flex;gap:8px 18px;flex-wrap:wrap;align-items:center;border-bottom:1px solid #edf1f5;color:#5d7185;font-size:10px}#profileSummary span{white-space:nowrap}#profileSummary strong{color:#234d6d;margin-left:4px;font-size:11px}#profileChart{flex:1;min-height:0;width:100%;display:block;background:#fbfdff}#profileFoot{padding:8px 14px;border-top:1px solid #edf1f5;font-size:9px;color:#8997a6;line-height:1.4}
@media(max-width:1050px){#workspace{grid-template-columns:185px minmax(250px,1fr) 230px}.mapSearch{width:150px}.brand small{display:none}}
@media(max-width:760px){#workspace{grid-template-columns:155px minmax(220px,1fr)}.panel.right{display:none}#status{display:none}.mapSearch{width:130px}}
</style>
</head>
<body>
<div id="app">
<header id="topbar">
  <div class="brand">Projecto hidráulico</div><div class="sep"></div>
  <button id="drawPipeBtn" class="btn primary" type="button" disabled>＋ Traçar tubulação</button>
  <button id="finishPipeBtn" class="btn" type="button" disabled>Concluir troço</button>
  <button id="cancelDrawBtn" class="btn" type="button" disabled>Cancelar</button>
  <button id="areaSelectBtn" class="btn" type="button" disabled>▧ Seleccionar área</button>
  <button id="profileBtn" class="btn" type="button" disabled>Perfil longitudinal</button>
  <button id="schematicBtn" class="btn" type="button" disabled>Esquema hidráulico</button>
  <button id="deleteBtn" class="btn danger" type="button" disabled>Eliminar</button>
  <div id="topSpacer"></div><span id="status">A iniciar o mapa…</span>
</header>
<div id="workspace">
  <aside class="panel left">
    <div class="panelHead">Biblioteca de acessórios <small id="accessoryCount">25 elementos</small></div>
    <input id="librarySearch" type="search" placeholder="Pesquisar válvula, curva, filtro…" autocomplete="off">
    <div id="categoryList">
      <button class="cat active" data-category="todos">Todos</button><button class="cat" data-category="curvas">Curvas</button><button class="cat" data-category="valvulas">Válvulas</button><button class="cat" data-category="transicoes">Transições</button><button class="cat" data-category="outros">Outros</button>
    </div>
    <div id="componentList"></div>
    <div class="libraryNote"><strong>Como inserir:</strong> escolha um acessório e clique junto à tubulação. O editor procura o ponto mais próximo e só o aceita dentro da tolerância de encaixe.</div>
  </aside>
  <main id="mapArea">
    <div id="map"></div>
    <div class="mapOverlay">
      <input id="mapSearch" class="mapSearch" type="search" placeholder="Pesquisar local…">
      <button id="searchBtn" class="btn" type="button">Pesquisar</button>
      <span style="background:#fff;border:1px solid #dce4ed;border-radius:6px;height:32px;display:flex;align-items:center;gap:6px;padding:0 8px;box-shadow:var(--shadow);font-size:9px;color:#586e83">Snap máximo <input id="snapTolerance" type="number" min="0.2" max="20" step="0.2" value="5" style="width:43px;height:23px;border:1px solid #dce4ed;border-radius:4px;padding:2px;font-size:10px"> m</span>
    </div>
    <div class="mapHint"><strong>Mapa = área de projecto.</strong> Trace a conduta por pontos e clique em “Concluir troço”. Seleccione-a para editar propriedades e vértices. Use o botão de perfil apenas quando quiser analisar o troço seleccionado.</div>
    <div id="mapFallback"><div class="fallbackCard"><h3>Não foi possível carregar o mapa</h3><p id="fallbackDetail">A biblioteca cartográfica não respondeu. Verifique a ligação à Internet ou tente carregar novamente.</p><button id="retryMapBtn" class="btn primary" type="button">Tentar novamente</button></div></div>
  </main>
  <aside class="panel right">
    <div class="panelHead">Detalhes do elemento <small id="selectionType">Sem selecção</small></div>
    <div id="inspector"><div class="empty">Seleccione uma tubulação no mapa para editar comprimento, função, DN e material. Os acessórios ficam associados ao troço em que são encaixados.</div></div>
  </aside>
</div>
</div>
<div id="profileModal" role="dialog" aria-modal="true" aria-labelledby="profileTitle">
  <section id="profileCard">
    <header id="profileHeader"><span id="profileTitle">Perfil longitudinal do troço</span><div class="spacer"></div><div id="profileControls"><label for="profileDepth">Profundidade até ao eixo (m)</label><input id="profileDepth" type="number" min="0" max="100" step="0.1" value="1.2"><label for="profileSpacing">Amostragem (m)</label><input id="profileSpacing" type="number" min="10" max="500" step="10" value="40"><label for="initialHgl">Cota HGL inicial (m)</label><input id="initialHgl" type="number" step="0.01" placeholder="Opcional"><button id="refreshProfileBtn" class="btn" type="button">Actualizar</button></div><button id="closeProfileBtn" class="btn" type="button">Fechar</button></header>
    <div id="profileSummary">O perfil só é calculado quando o utilizador solicita esta vista.</div>
    <svg id="profileChart" viewBox="0 0 1200 610" preserveAspectRatio="none" aria-label="Perfil longitudinal do troço seleccionado"></svg>
    <div id="profileFoot">As cotas do terreno são provenientes de um serviço de modelo digital de elevação e não substituem levantamento topográfico. A linha do eixo é indicativa e depende da profundidade definida.</div>
  </section>
</div>
<div id="schematicModal" role="dialog" aria-modal="true" aria-labelledby="schematicTitle" style="display:none;position:fixed;inset:0;z-index:1900;background:rgba(16,34,52,.48);padding:24px;align-items:center;justify-content:center">
  <section style="width:min(1120px,96vw);height:min(680px,90vh);background:#fff;border-radius:11px;box-shadow:0 12px 50px rgba(0,0,0,.28);display:flex;flex-direction:column;overflow:hidden">
    <header style="height:49px;flex:0 0 49px;padding:0 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line)">
      <strong id="schematicTitle" style="font-size:13px;color:#23445f">Esquema hidráulico gerado a partir do mapa</strong><div style="flex:1"></div><button id="closeSchematicBtn" class="btn" type="button">Fechar</button>
    </header>
    <div id="schematicSummary" style="padding:9px 14px;border-bottom:1px solid #edf1f5;font-size:10px;color:#62788b">Representação derivada dos troços e acessórios definidos no mapa.</div>
    <svg id="schematicSvg" viewBox="0 0 1200 580" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%;min-height:0;background:#fbfdff" aria-label="Esquema hidráulico gerado do modelo geográfico"></svg>
    <div style="padding:8px 14px;border-top:1px solid #edf1f5;font-size:9px;color:#8997a6">Vista de consulta. Para alterar o traçado, seleccione e edite os elementos directamente no mapa.</div>
  </section>
</div>
<script>
(() => {
'use strict';

const ACCESSORIES = [
 {type:'ampliacao-gradual',name:'Ampliação gradual',category:'transicoes',k:0.30,icon:'⇧'},
 {type:'comporta-aberta',name:'Comporta aberta',category:'valvulas',k:1.00,icon:'⊣'},
 {type:'controlador-de-vazao',name:'Controlador de vazão',category:'valvulas',k:2.50,icon:'◉'},
 {type:'cotovelo-ou-joelho-45',name:'Cotovelo / joelho 45°',category:'curvas',k:0.40,icon:'↗'},
 {type:'cotovelo-ou-joelho-90',name:'Cotovelo / joelho 90°',category:'curvas',k:0.90,icon:'↱'},
 {type:'crivo',name:'Crivo',category:'outros',k:0.75,icon:'▦'},
 {type:'curva-22-5',name:'Curva 22,5°',category:'curvas',k:0.10,icon:'⌁'},
 {type:'curva-45',name:'Curva 45°',category:'curvas',k:0.20,icon:'↗'},
 {type:'curva-90',name:'Curva 90°',category:'curvas',k:0.40,icon:'↱'},
 {type:'entrada-de-borda',name:'Entrada de borda',category:'outros',k:1.00,icon:'⇥'},
 {type:'entrada-normal',name:'Entrada normal',category:'outros',k:0.50,icon:'⇢'},
 {type:'juncao',name:'Junção',category:'outros',k:0.40,icon:'Y'},
 {type:'medidor-venturi',name:'Medidor Venturi',category:'outros',k:2.50,icon:'◈'},
 {type:'pequena-derivacao',name:'Pequena derivação',category:'outros',k:0.02,icon:'┬'},
 {type:'reducao-gradual',name:'Redução gradual',category:'transicoes',k:0.15,icon:'⇩'},
 {type:'saida-livre',name:'Saída de canalização',category:'outros',k:1.00,icon:'⇥'},
 {type:'te-passagem-directa',name:'Tê — passagem directa',category:'outros',k:0.60,icon:'┬'},
 {type:'te-saida-bilateral',name:'Tê — saída bilateral',category:'outros',k:1.80,icon:'┼'},
 {type:'te-saida-de-lado',name:'Tê — saída lateral',category:'outros',k:1.30,icon:'┤'},
 {type:'valvula-borboleta',name:'Válvula borboleta',category:'valvulas',k:0.30,icon:'◁'},
 {type:'valvula-angulo-aberta',name:'Válvula de ângulo aberta',category:'valvulas',k:5.00,icon:'⌞'},
 {type:'valvula-gaveta-aberta',name:'Válvula de gaveta aberta',category:'valvulas',k:0.20,icon:'⊗'},
 {type:'valvula-de-pe',name:'Válvula de pé',category:'valvulas',k:1.75,icon:'⊣'},
 {type:'valvula-de-retencao',name:'Válvula de retenção',category:'valvulas',k:2.50,icon:'▷'},
 {type:'valvula-globo-aberta',name:'Válvula globo aberta',category:'valvulas',k:10.00,icon:'◉'}
];

const state = {
  map:null, bridge:{}, pipes:[], components:[], selectedPipeIds:[], selectedComponentId:null,
  mode:'select', drawingPoints:[], drawingLayer:null, selectionStart:null, selectionLayer:null, layerClickTargets:new WeakMap(),
  pendingAccessory:null, vertexLayers:[], snapHalo:null, activeCategory:'todos',
  profileOpen:false, profileData:null, hydraulicProfile:null, elevationCache:new Map(),
  profileRequest:0, modelSendQueued:false
};
const $ = id => document.getElementById(id);
const status = message => { $('status').textContent=String(message||''); };
const uid = prefix => `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2,7)}`;
const esc = value => String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number = (v, fallback=0) => Number.isFinite(Number(v)) ? Number(v) : fallback;
const findPipe = id => state.pipes.find(p=>p.id===id);
const findComponent = id => state.components.find(c=>c.id===id);

// Carrega Leaflet por duas CDNs. Se ambas falharem, a interface explica o problema
// em vez de deixar uma janela cinzenta sem diagnóstico.
function loadCss(url){return new Promise(resolve=>{const l=document.createElement('link');l.rel='stylesheet';l.href=url;l.onload=()=>resolve(true);l.onerror=()=>resolve(false);document.head.appendChild(l);});}
function loadScript(url){return new Promise(resolve=>{const s=document.createElement('script');s.src=url;s.onload=()=>resolve(true);s.onerror=()=>{s.remove();resolve(false);};document.head.appendChild(s);});}
async function loadLeaflet(){
  const cssUrls=['https://unpkg.com/leaflet@1.9.4/dist/leaflet.css','https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css'];
  const jsUrls=['https://unpkg.com/leaflet@1.9.4/dist/leaflet.js','https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js'];
  for(const url of cssUrls){if(await loadCss(url))break;}
  if(window.L)return true;
  for(const url of jsUrls){if(await loadScript(url)&&window.L)return true;}
  return false;
}

function initWebChannel(){
  if(typeof QWebChannel==='undefined'||!window.qt||!qt.webChannelTransport){
    status('Mapa activo; ligação ao motor hidráulico ainda não disponível');return;
  }
  new QWebChannel(qt.webChannelTransport,channel=>{
    state.bridge=channel.objects||{};
    status('Mapa e motor hidráulico ligados');
    if(state.modelSendQueued)publishModel();
  });
}
function mercatorXY(latlng){
  const r=6378137,lat=Math.max(-85.05112878,Math.min(85.05112878,latlng.lat))*Math.PI/180;
  return {x:r*latlng.lng*Math.PI/180,y:r*Math.log(Math.tan(Math.PI/4+lat/2))};
}
function hydraulicNodeXY(latlng){
  // O ModeloHidraulico existente usa tolerância topológica de 12 unidades,
  // herdada do SVG. Factor 60 faz essas 12 unidades equivalerem a 0,20 m.
  const p=mercatorXY(latlng);return {x:p.x*60,y:p.y*60};
}
function routeLength(latlngs){let total=0;for(let i=1;i<latlngs.length;i++)total+=latlngs[i-1].distanceTo(latlngs[i]);return total;}
function routeName(index){return `Troço ${index+1}`;}

// ---------------- Biblioteca de acessórios ----------------
function renderLibrary(){
  const query=$('librarySearch').value.trim().toLocaleLowerCase('pt');
  const visible=ACCESSORIES.filter(a=>(state.activeCategory==='todos'||a.category===state.activeCategory)&&(!query||a.name.toLocaleLowerCase('pt').includes(query)));
  $('componentList').innerHTML=visible.map(a=>`<button class="componentCard ${state.pendingAccessory?.type===a.type?'selected':''}" type="button" data-add="${a.type}" title="Seleccionar ${esc(a.name)}"><span class="componentIcon">${esc(a.icon)}</span><b>${esc(a.name)}</b><small>K inicial ${a.k.toFixed(2)}</small></button>`).join('');
  $('componentList').querySelectorAll('[data-add]').forEach(btn=>btn.addEventListener('click',()=>{
    const item=ACCESSORIES.find(a=>a.type===btn.dataset.add);if(!item)return;
    state.pendingAccessory=item;state.mode='placeAccessory';updateToolbar();clearSnapHalo();renderLibrary();
    const pipe=selectedPipe();
    status(`ACESSÓRIO: ${item.name} seleccionado${pipe?` · alvo: ${pipe.name}`:''}. Clique directamente sobre a tubulação para encaixar. ESC cancela.`);
  }));
}
$('librarySearch').addEventListener('input',renderLibrary);
$('categoryList').querySelectorAll('[data-category]').forEach(btn=>btn.addEventListener('click',()=>{
  state.activeCategory=btn.dataset.category;
  $('categoryList').querySelectorAll('.cat').forEach(b=>b.classList.toggle('active',b===btn));renderLibrary();
}));

// ---------------- Selecção e desenho no próprio mapa ----------------
function updateToolbar(){
  const drawing=state.mode==='drawPipe';
  $('drawPipeBtn').disabled=!state.map;
  $('areaSelectBtn').disabled=!state.map;
  $('drawPipeBtn').classList.toggle('active',drawing);
  $('finishPipeBtn').disabled=!drawing||state.drawingPoints.length<2;
  $('cancelDrawBtn').disabled=!state.map||(state.mode==='select'&&!state.drawingPoints.length);
  $('areaSelectBtn').classList.toggle('active',state.mode==='selectArea');
  $('profileBtn').disabled=!state.map||state.selectedPipeIds.length!==1||!!state.selectedComponentId;
  $('schematicBtn').disabled=!state.map||state.pipes.length===0;
  $('deleteBtn').disabled=!state.map||(!state.selectedPipeIds.length&&!state.selectedComponentId);
}
function selectedPipe(){return state.selectedPipeIds.length===1?findPipe(state.selectedPipeIds[0]):null;}
function clearVertexHandles(){state.vertexLayers.forEach(layer=>{if(state.map)state.map.removeLayer(layer);});state.vertexLayers=[];}
function showVertexHandles(pipe){
  clearVertexHandles();if(!pipe||!state.map)return;
  pipe.latlngs.forEach((latlng,index)=>{
    const marker=L.marker(latlng,{draggable:true,keyboard:false,icon:L.divIcon({className:'',html:'<div class="vertexHandle"></div>',iconSize:[13,13],iconAnchor:[6.5,6.5]})});
    marker.addTo(state.map);marker.on('click',e=>{if(e.originalEvent)L.DomEvent.stop(e.originalEvent);});marker.on('drag',e=>{
      pipe.latlngs[index]=e.target.getLatLng();pipe.layer.setLatLngs(pipe.latlngs);pipe.lengthM=routeLength(pipe.latlngs);updatePipeLabel(pipe);refreshAccessoryAnchors(pipe,false);
    });
    marker.on('dragend',()=>{pipe.lengthM=routeLength(pipe.latlngs);refreshAccessoryAnchors(pipe,true);renderInspector();publishModel();});
    state.vertexLayers.push(marker);
  });
}
function stylePipe(pipe){
  if(!pipe.layer)return;const selected=state.selectedPipeIds.includes(pipe.id);
  pipe.layer.setStyle({color:selected?'#d36b18':'#1769aa',weight:selected?7:5,opacity:1});
  if(selected)pipe.layer.bringToFront();
}
function selectPipe(pipeId, additive=false){
  state.selectedComponentId=null;
  if(additive){
    state.selectedPipeIds=state.selectedPipeIds.includes(pipeId)?state.selectedPipeIds.filter(id=>id!==pipeId):[...state.selectedPipeIds,pipeId];
  }else state.selectedPipeIds=[pipeId];
  state.pipes.forEach(stylePipe);const pipe=selectedPipe();showVertexHandles(pipe);renderInspector();updateToolbar();
  if(pipe){status(`${pipe.name} seleccionado · ${pipe.lengthM.toFixed(1)} m`);}
  else if(state.selectedPipeIds.length>1){status(`${state.selectedPipeIds.length} troços seleccionados`);}
  publishModel();
}
function selectComponent(componentId){
  state.selectedComponentId=componentId;state.selectedPipeIds=[];state.pipes.forEach(stylePipe);clearVertexHandles();renderInspector();updateToolbar();
}
function clearSelection(){state.selectedPipeIds=[];state.selectedComponentId=null;state.pipes.forEach(stylePipe);clearVertexHandles();renderInspector();updateToolbar();}
function createPipe(latlngs){
  if(latlngs.length<2){status('Um troço precisa de pelo menos dois pontos');return;}
  const id=uid('pipe');const p={id,name:routeName(state.pipes.length),role:'sucção',material:'PVC',dn:100,lengthM:routeLength(latlngs),latlngs:latlngs.map(x=>L.latLng(x.lat,x.lng)),notes:'',layer:null,chainStartM:0};
  p.layer=L.polyline(p.latlngs,{color:'#1769aa',weight:7,opacity:.98,lineCap:'round',lineJoin:'round',bubblingMouseEvents:true}).addTo(state.map);
  // Clique tratado na própria camada: evita perder a referência do troço quando
  // o evento chega ao mapa e impede inserções duplicadas no mesmo clique.
  p.layer.on('click',e=>{
    if(state.mode==='drawPipe'){
      if(e.originalEvent)L.DomEvent.stop(e.originalEvent);
      addDrawingVertex(e.latlng);return;
    }
    if(state.mode==='placeAccessory'){
      if(e.originalEvent)L.DomEvent.stop(e.originalEvent);
      placeAccessory(e.latlng,{clickedPipeId:p.id});return;
    }
    if(state.mode==='selectArea')return;
    if(e.originalEvent)L.DomEvent.stop(e.originalEvent);
    selectPipe(p.id,!!(e.originalEvent&&(e.originalEvent.ctrlKey||e.originalEvent.shiftKey)));
  });
  p.layer.bindTooltip(()=>`${esc(p.name)} · ${p.role} · ${p.lengthM.toFixed(1)} m`,{sticky:true});
  state.pipes.push(p);selectPipe(id);status(`${p.name} criado. Confirme as propriedades no painel direito.`);publishModel();
}
function snapToExistingPipeEndpoint(latlng){
  let best=null;
  for(const pipe of state.pipes){
    for(const endpoint of [pipe.latlngs[0],pipe.latlngs[pipe.latlngs.length-1]]){
      const distance=latlng.distanceTo(endpoint);
      if(distance<=snapToleranceM()&&(!best||distance<best.distance))best={latlng:endpoint,distance,pipe};
    }
  }
  return best;
}
function addDrawingVertex(latlng){
  const snap=snapToExistingPipeEndpoint(latlng);
  const point=snap?L.latLng(snap.latlng.lat,snap.latlng.lng):L.latLng(latlng.lat,latlng.lng);
  const last=state.drawingPoints[state.drawingPoints.length-1];
  if(last&&last.distanceTo(point)<0.5){status('Ponto demasiado próximo do vértice anterior; escolha outra posição.');return;}
  state.drawingPoints.push(point);
  if(state.drawingLayer)state.map.removeLayer(state.drawingLayer);
  state.drawingLayer=L.polyline(state.drawingPoints,{color:'#16a085',weight:4,dashArray:'7 6'}).addTo(state.map);
  updateToolbar();status(snap?`Vértice ligado à extremidade de ${snap.pipe.name} · ${snap.distance.toFixed(2)} m`:`${state.drawingPoints.length} ponto(s) definidos · clique em “Concluir troço”`);
}
function finishPipeDrawing(){
  if(state.drawingPoints.length<2){status('Indique pelo menos dois pontos no mapa');return;}
  const coords=[...state.drawingPoints];
  if(state.drawingLayer)state.map.removeLayer(state.drawingLayer);
  state.drawingLayer=null;state.drawingPoints=[];state.mode='select';
  if(state.map)state.map.dragging.enable();
  createPipe(coords);updateToolbar();
}
function cancelCurrentMode(){
  state.mode='select';state.pendingAccessory=null;state.drawingPoints=[];
  if(state.drawingLayer){state.map.removeLayer(state.drawingLayer);state.drawingLayer=null;}
  if(state.selectionLayer){state.map.removeLayer(state.selectionLayer);state.selectionLayer=null;}
  if(state.map)state.map.dragging.enable();clearSnapHalo();renderLibrary();updateToolbar();status('Modo de edição cancelado');
}
$('drawPipeBtn').addEventListener('click',()=>{
  if(state.mode==='drawPipe'){cancelCurrentMode();return;}
  cancelCurrentMode();state.mode='drawPipe';
  if(state.map)state.map.dragging.disable();
  clearSelection();updateToolbar();
  status('DESENHO ACTIVO — clique no mapa para marcar cada vértice; depois prima “Concluir troço”.');
});
$('finishPipeBtn').addEventListener('click',finishPipeDrawing);
$('cancelDrawBtn').addEventListener('click',cancelCurrentMode);
window.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&(state.mode==='drawPipe'||state.mode==='placeAccessory'||state.mode==='selectArea')){cancelCurrentMode();return;}
  if((event.key==='Backspace'||event.key==='Delete')&&state.mode==='drawPipe'&&state.drawingPoints.length){
    event.preventDefault();state.drawingPoints.pop();
    if(state.drawingLayer){if(state.drawingPoints.length>1)state.drawingLayer.setLatLngs(state.drawingPoints);else{state.map.removeLayer(state.drawingLayer);state.drawingLayer=null;}}
    updateToolbar();status(`${state.drawingPoints.length} ponto(s) no traçado; continue ou conclua o troço.`);
  }
});
$('areaSelectBtn').addEventListener('click',()=>{
  cancelCurrentMode();state.mode='selectArea';state.map.dragging.disable();updateToolbar();status('Arraste um rectângulo no mapa para seleccionar os troços dentro da área');
});

// Selecção rectangular com teste geométrico em coordenadas do ecrã.
function insideRect(p,rect){return p.x>=rect.min.x&&p.x<=rect.max.x&&p.y>=rect.min.y&&p.y<=rect.max.y;}
function segmentIntersectsRect(a,b,r){
  if(insideRect(a,r)||insideRect(b,r))return true;
  const edges=[[{x:r.min.x,y:r.min.y},{x:r.max.x,y:r.min.y}],[{x:r.max.x,y:r.min.y},{x:r.max.x,y:r.max.y}],[{x:r.max.x,y:r.max.y},{x:r.min.x,y:r.max.y}],[{x:r.min.x,y:r.max.y},{x:r.min.x,y:r.min.y}]];
  const cross=(p1,p2,p3)=>((p2.x-p1.x)*(p3.y-p1.y)-(p2.y-p1.y)*(p3.x-p1.x));
  for(const [c,d] of edges){const d1=cross(a,b,c),d2=cross(a,b,d),d3=cross(c,d,a),d4=cross(c,d,b);if(d1*d2<=0&&d3*d4<=0)return true;}return false;
}
function pipeIntersectsRect(pipe,bounds){
  const r={min:state.map.latLngToContainerPoint(bounds.getSouthWest()),max:state.map.latLngToContainerPoint(bounds.getNorthEast())};
  if(r.min.x>r.max.x){const t=r.min.x;r.min.x=r.max.x;r.max.x=t;}if(r.min.y>r.max.y){const t=r.min.y;r.min.y=r.max.y;r.max.y=t;}
  const pts=pipe.latlngs.map(ll=>state.map.latLngToContainerPoint(ll));
  for(let i=1;i<pts.length;i++)if(segmentIntersectsRect(pts[i-1],pts[i],r))return true;return pts.some(p=>insideRect(p,r));
}
function finishAreaSelection(bounds){
  const ids=state.pipes.filter(p=>pipeIntersectsRect(p,bounds)).map(p=>p.id);
  state.mode='select';state.selectedComponentId=null;state.selectedPipeIds=ids;state.pipes.forEach(stylePipe);
  if(state.selectionLayer){state.map.removeLayer(state.selectionLayer);state.selectionLayer=null;}
  showVertexHandles(selectedPipe());renderInspector();updateToolbar();
  status(ids.length?`${ids.length} troço(s) abrangidos pelo rectângulo`:'Nenhum troço encontrado dentro da área');
}

// ---------------- Snap dos acessórios sobre a geometria da tubulação ----------------
function snapToleranceM(){return Math.max(0.2,Math.min(20,number($('snapTolerance').value,2)));}
function nearestPointOnPipe(latlng,pipe){
  const p=state.map.latLngToLayerPoint(latlng);let best=null;let chainage=0;
  for(let i=1;i<pipe.latlngs.length;i++){
    const aLL=pipe.latlngs[i-1],bLL=pipe.latlngs[i];const a=state.map.latLngToLayerPoint(aLL),b=state.map.latLngToLayerPoint(bLL);
    const dx=b.x-a.x,dy=b.y-a.y,len2=dx*dx+dy*dy;if(len2<1e-8)continue;
    const t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/len2));
    const q={x:a.x+t*dx,y:a.y+t*dy};const distance=Math.hypot(p.x-q.x,p.y-q.y);const segmentLength=aLL.distanceTo(bLL);
    const snapped=state.map.layerPointToLatLng(L.point(q.x,q.y));
    const geometryLength=routeLength(pipe.latlngs);
    const scale=geometryLength>0?number(pipe.lengthM,geometryLength)/geometryLength:1;
    const result={latlng:snapped,distance,distanceM:latlng.distanceTo(snapped),positionM:(chainage+t*segmentLength)*scale,pipeId:pipe.id};
    if(!best||distance<best.distance)best=result;chainage+=segmentLength;
  }
  return best;
}
function nearestPipeSnap(latlng,excludedId=null){
  let best=null;for(const pipe of state.pipes){if(excludedId&&pipe.id!==excludedId)continue;const hit=nearestPointOnPipe(latlng,pipe);if(hit&&(!best||hit.distance<best.distance))best={...hit,pipe};}return best;
}
function showSnapHalo(latlng){
  if(state.snapHalo){state.map.removeLayer(state.snapHalo);state.snapHalo=null;}
  state.snapHalo=L.marker(latlng,{interactive:false,keyboard:false,icon:L.divIcon({className:'',html:'<div class="snapHalo"></div>',iconSize:[24,24],iconAnchor:[12,12]})}).addTo(state.map);
}
function clearSnapHalo(){if(state.snapHalo){state.map.removeLayer(state.snapHalo);state.snapHalo=null;}}
function componentIcon(component){
  const meta=ACCESSORIES.find(a=>a.type===component.type);const text=meta?.icon||'•';
  return L.divIcon({className:'',html:`<div class="accMarker ${component.attached?'':'unattached'}">${esc(text)}</div>`,iconSize:[25,25],iconAnchor:[12.5,12.5]});
}
function placeAccessory(latlng,options={}){
  const hit=nearestPipeSnap(latlng,options.clickedPipeId||null);
  if(!hit){status('Desenhe primeiro uma tubulação para poder associar acessórios.');return;}
  // Num clique directamente sobre o traço, o próprio evento da camada confirma
  // que o utilizador apontou visualmente para a tubulação; encaixamos no ponto
  // matematicamente mais próximo. Em cliques no fundo do mapa continua a valer
  // a tolerância métrica introduzida pelo utilizador.
  const clickedOnPipe=!!options.clickedPipeId;
  if(!clickedOnPipe&&hit.distanceM>snapToleranceM()){
    status(`Sem encaixe: aproxime o clique de uma tubulação (máximo ${snapToleranceM()} m). O acessório não foi colocado.`);return;
  }
  const meta=state.pendingAccessory;if(!meta)return;
  const c={id:uid('acc'),type:meta.type,name:meta.name,k:meta.k,dn:100,rotation:0,status:'normalmente aberto',pipeId:hit.pipeId,positionM:hit.positionM,latlng:hit.latlng,attached:true,marker:null};
  c.marker=L.marker(hit.latlng,{draggable:true,icon:componentIcon(c),zIndexOffset:800}).addTo(state.map);
  c.marker.bindTooltip(`${esc(c.name)} · ${esc(hit.pipe.name)} · ${hit.positionM.toFixed(1)} m`);
  c.marker.on('click',e=>{if(e.originalEvent)L.DomEvent.stop(e.originalEvent);selectComponent(c.id);});
  c.marker.on('dragstart',()=>{c._previous={latlng:c.marker.getLatLng(),pipeId:c.pipeId,positionM:c.positionM};});
  c.marker.on('dragend',()=>moveAccessoryToNearestPipe(c));
  state.components.push(c);state.pendingAccessory=null;state.mode='select';clearSnapHalo();renderLibrary();selectComponent(c.id);updateToolbar();publishModel();
  status(`${c.name} encaixado em ${hit.pipe.name}, a ${hit.positionM.toFixed(1)} m do início`);
}
function moveAccessoryToNearestPipe(component){
  const hit=nearestPipeSnap(component.marker.getLatLng());
  if(!hit||hit.distanceM>snapToleranceM()){
    const old=component._previous;if(old){component.marker.setLatLng(old.latlng);component.pipeId=old.pipeId;component.positionM=old.positionM;}
    status(`Movimento rejeitado: o acessório tem de ficar a no máximo ${snapToleranceM()} m de uma tubulação.`);return;
  }
  component.pipeId=hit.pipeId;component.positionM=hit.positionM;component.latlng=hit.latlng;component.attached=true;
  component.marker.setLatLng(hit.latlng);component.marker.setIcon(componentIcon(component));component.marker.setTooltipContent(`${esc(component.name)} · ${esc(hit.pipe.name)} · ${hit.positionM.toFixed(1)} m`);
  renderInspector();publishModel();status(`${component.name} encaixado em ${hit.pipe.name}`);
}
function refreshAccessoryAnchors(pipe,strict){
  for(const c of state.components.filter(x=>x.pipeId===pipe.id)){
    const target=pointAtChainage(pipe,c.positionM);
    if(target){c.latlng=target;c.marker.setLatLng(target);c.attached=true;c.marker.setIcon(componentIcon(c));}
    else if(strict){c.attached=false;c.marker.setIcon(componentIcon(c));}
  }
}
function pointAtChainage(pipe,chainage){
  const geometryLength=routeLength(pipe.latlngs);
  const scale=number(pipe.lengthM,geometryLength)>0?geometryLength/number(pipe.lengthM,geometryLength):1;
  let remaining=Math.max(0,Math.min(pipe.lengthM,number(chainage)))*scale;
  for(let i=1;i<pipe.latlngs.length;i++){
    const a=pipe.latlngs[i-1],b=pipe.latlngs[i],length=a.distanceTo(b);
    if(remaining<=length||i===pipe.latlngs.length-1){const t=length>0?Math.min(1,remaining/length):0;return L.latLng(a.lat+(b.lat-a.lat)*t,a.lng+(b.lng-a.lng)*t);}remaining-=length;
  }return pipe.latlngs[pipe.latlngs.length-1]||null;
}
function updatePipeLabel(pipe){
  if(pipe.layer&&pipe.layer.getTooltip()){pipe.layer.setTooltipContent(`${esc(pipe.name)} · ${esc(pipe.role)} · ${pipe.lengthM.toFixed(1)} m`);}
}

// ---------------- Eventos do mapa ----------------
function attachMapHandlers(){
  state.map.on('click',e=>{
    const clickedPipeId=e.originalEvent?state.layerClickTargets.get(e.originalEvent)||null:null;
    if(e.originalEvent)state.layerClickTargets.delete(e.originalEvent);
    if(state.mode==='drawPipe'){addDrawingVertex(e.latlng);return;}
    if(state.mode==='placeAccessory'){placeAccessory(e.latlng,{clickedPipeId});return;}
    if(state.mode==='selectArea')return;
    if(!e.originalEvent?.target?.closest?.('.leaflet-interactive'))clearSelection();
  });
  state.map.on('mousedown',e=>{
    if(state.mode==='drawPipe')return;
    if(state.mode!=='selectArea')return;
    state.selectionStart=e.latlng;state.map.dragging.disable();
    if(state.selectionLayer)state.map.removeLayer(state.selectionLayer);
    state.selectionLayer=L.rectangle([e.latlng,e.latlng],{color:'#159b83',weight:2,dashArray:'6 5',fillOpacity:.08,interactive:false}).addTo(state.map);
  });
  state.map.on('mousemove',e=>{
    if(state.mode==='selectArea'&&state.selectionStart&&state.selectionLayer){state.selectionLayer.setBounds(L.latLngBounds(state.selectionStart,e.latlng));}
    if(state.mode==='drawPipe'&&state.drawingPoints.length){
      const points=[...state.drawingPoints,e.latlng];
      if(state.drawingLayer)state.drawingLayer.setLatLngs(points);
    }
    if(state.mode==='placeAccessory'){
      const hit=nearestPipeSnap(e.latlng);if(hit&&hit.distanceM<=snapToleranceM())showSnapHalo(hit.latlng);else clearSnapHalo();
    }else if(state.mode==='drawPipe'){
      const hit=snapToExistingPipeEndpoint(e.latlng);if(hit)showSnapHalo(hit.latlng);else clearSnapHalo();
    }
  });
  state.map.on('mouseup',e=>{
    if(state.mode!=='selectArea'||!state.selectionStart)return;
    const bounds=L.latLngBounds(state.selectionStart,e.latlng);state.selectionStart=null;state.map.dragging.enable();finishAreaSelection(bounds);
  });
  window.addEventListener('mouseup',event=>{
    if(state.mode!=='selectArea'||!state.selectionStart||!state.map)return;
    const ll=state.map.mouseEventToLatLng(event);const bounds=L.latLngBounds(state.selectionStart,ll);state.selectionStart=null;state.map.dragging.enable();finishAreaSelection(bounds);
  });
  state.map.on('mouseout',()=>clearSnapHalo());
}

// ---------------- Propriedades ----------------
function field(label,id,value,type='text',attrs=''){return `<div class="field"><label for="${id}">${label}</label><input id="${id}" type="${type}" value="${esc(value)}" ${attrs}></div>`;}
function renderInspector(){
  const panel=$('inspector');
  if(state.selectedComponentId){
    const c=findComponent(state.selectedComponentId);if(!c){state.selectedComponentId=null;return renderInspector();}
    const pipe=findPipe(c.pipeId);$('selectionType').textContent='Acessório';
    panel.innerHTML=`<span class="pill">${esc(c.name)}</span><div style="height:10px"></div>${field('Diâmetro nominal (DN)','accDn',c.dn,'number','min="1" step="1"')}${field('Coeficiente de perda K','accK',c.k,'number','min="0" step="0.01"')}${field('Orientação (°)','accRotation',c.rotation,'number','step="15"')}<div class="field"><label for="accStatus">Estado</label><select id="accStatus"><option ${c.status==='normalmente aberto'?'selected':''}>normalmente aberto</option><option ${c.status==='aberto'?'selected':''}>aberto</option><option ${c.status==='fechado'?'selected':''}>fechado</option><option ${c.status==='parcialmente aberto'?'selected':''}>parcialmente aberto</option></select></div>${field('Progressiva no troço (m)','accPosition',c.positionM,'number','min="0" step="0.1"')}<div class="help">${pipe?`Associado a ${esc(pipe.name)}.`:'Este acessório ainda não está associado a uma tubulação.'} O marcador é encaixado na linha; se for afastado para fora da tolerância, o movimento é rejeitado.</div><div class="actions"><button id="deleteSelectedComponent" class="btn danger">Eliminar acessório</button><button id="focusPipe" class="btn" ${pipe?'':'disabled'}>Ver troço</button></div>`;
    $('accDn').addEventListener('change',e=>{c.dn=Math.max(1,number(e.target.value,c.dn));publishModel();});
    $('accK').addEventListener('change',e=>{c.k=Math.max(0,number(e.target.value,c.k));publishModel();});
    $('accRotation').addEventListener('change',e=>{c.rotation=number(e.target.value,c.rotation);publishModel();});
    $('accStatus').addEventListener('change',e=>{c.status=e.target.value;publishModel();});
    $('accPosition').addEventListener('change',e=>{const value=Math.max(0,number(e.target.value,c.positionM));const target=pipe?pointAtChainage(pipe,value):null;if(target&&pipe){c.positionM=Math.min(pipe.lengthM,value);c.latlng=target;c.marker.setLatLng(target);$('accPosition').value=c.positionM.toFixed(1);publishModel();}else e.target.value=c.positionM;});
    $('deleteSelectedComponent').addEventListener('click',deleteSelected);
    $('focusPipe').addEventListener('click',()=>{if(pipe)state.map.fitBounds(pipe.layer.getBounds().pad(.2));});
    return;
  }
  if(state.selectedPipeIds.length>1){
    $('selectionType').textContent=`${state.selectedPipeIds.length} troços`;
    panel.innerHTML=`<span class="pill">Selecção por área</span><p style="font-size:11px;color:#607489;line-height:1.5">${state.selectedPipeIds.length} troços seleccionados. As propriedades seguintes serão aplicadas a todos os elementos abrangidos pelo rectângulo.</p><div class="field"><label for="bulkRole">Função</label><select id="bulkRole"><option value="sucção">Sucção</option><option value="recalque">Recalque</option><option value="adutora">Adutora</option><option value="derivação">Derivação</option></select></div>${field('Diâmetro nominal (DN)','bulkDn','100','number','min="1" step="1"')}<div class="field"><label for="bulkMaterial">Material</label><select id="bulkMaterial">${materialOptions('PVC')}</select></div><div class="actions"><button id="applyBulk" class="btn primary">Aplicar aos seleccionados</button><button id="clearBulk" class="btn">Limpar selecção</button></div>`;
    $('applyBulk').addEventListener('click',()=>{const role=$('bulkRole').value,dn=Math.max(1,number($('bulkDn').value,100)),material=$('bulkMaterial').value;state.pipes.filter(p=>state.selectedPipeIds.includes(p.id)).forEach(p=>{p.role=role;p.dn=dn;p.material=material;updatePipeLabel(p);});renderInspector();publishModel();status('Propriedades aplicadas aos troços seleccionados');});
    $('clearBulk').addEventListener('click',clearSelection);return;
  }
  const p=selectedPipe();
  if(!p){$('selectionType').textContent='Sem selecção';panel.innerHTML='<div class="empty">Seleccione uma tubulação no mapa para editar comprimento, função, DN e material. Os acessórios ficam associados ao troço em que são encaixados.</div>';return;}
  $('selectionType').textContent='Tubulação';
  panel.innerHTML=`<span class="pill">${esc(p.name)}</span><div style="height:10px"></div>${field('Identificação','pipeName',p.name)}<div class="field"><label for="pipeRole">Função hidráulica</label><select id="pipeRole"><option value="sucção" ${p.role==='sucção'?'selected':''}>Sucção</option><option value="recalque" ${p.role==='recalque'?'selected':''}>Recalque</option><option value="adutora" ${p.role==='adutora'?'selected':''}>Adutora</option><option value="derivação" ${p.role==='derivação'?'selected':''}>Derivação</option></select></div>${field('Comprimento real (m)','pipeLength',p.lengthM.toFixed(2),'number','min="0.01" step="0.01"')}${field('Diâmetro interno / DN (mm)','pipeDn',p.dn,'number','min="1" step="1"')}<div class="field"><label for="pipeMaterial">Material</label><select id="pipeMaterial">${materialOptions(p.material)}</select></div><div class="field"><label for="pipeNotes">Observações</label><textarea id="pipeNotes">${esc(p.notes)}</textarea></div><div class="help">Comprimento geométrico calculado pelo percurso no mapa: ${routeLength(p.latlngs).toFixed(2)} m. Ao seleccionar o troço, aparecem pegas nos vértices para ajustar cuidadosamente o traçado.</div><div class="actions"><button id="zoomPipe" class="btn">Enquadrar</button><button id="deleteSelectedPipe" class="btn danger">Eliminar troço</button></div>`;
  $('pipeName').addEventListener('change',e=>{p.name=e.target.value.trim()||p.name;updatePipeLabel(p);publishModel();});
  $('pipeRole').addEventListener('change',e=>{p.role=e.target.value;updatePipeLabel(p);publishModel();});
  $('pipeLength').addEventListener('change',e=>{p.lengthM=Math.max(.01,number(e.target.value,p.lengthM));refreshAccessoryAnchors(p,true);renderInspector();publishModel();});
  $('pipeDn').addEventListener('change',e=>{p.dn=Math.max(1,number(e.target.value,p.dn));publishModel();});
  $('pipeMaterial').addEventListener('change',e=>{p.material=e.target.value;publishModel();});
  $('pipeNotes').addEventListener('change',e=>{p.notes=e.target.value;publishModel();});
  $('zoomPipe').addEventListener('click',()=>state.map.fitBounds(p.layer.getBounds().pad(.2)));
  $('deleteSelectedPipe').addEventListener('click',deleteSelected);
}
function materialOptions(selected){return ['PVC','PEAD','Aço carbono','Ferro fundido','PRFV','Betão','Cobre'].map(v=>`<option ${v===selected?'selected':''}>${v}</option>`).join('');}
function deleteSelected(){
  if(state.selectedComponentId){const c=findComponent(state.selectedComponentId);if(c?.marker)state.map.removeLayer(c.marker);state.components=state.components.filter(x=>x.id!==state.selectedComponentId);state.selectedComponentId=null;}
  else if(state.selectedPipeIds.length){const ids=[...state.selectedPipeIds];for(const id of ids){const p=findPipe(id);if(p?.layer)state.map.removeLayer(p.layer);state.components.filter(c=>c.pipeId===id).forEach(c=>{if(c.marker)state.map.removeLayer(c.marker);});}state.pipes=state.pipes.filter(p=>!ids.includes(p.id));state.components=state.components.filter(c=>!ids.includes(c.pipeId));state.selectedPipeIds=[];}
  clearVertexHandles();state.pipes.forEach(stylePipe);renderInspector();updateToolbar();publishModel();status('Elemento(s) eliminado(s)');
}
$('deleteBtn').addEventListener('click',deleteSelected);

// ---------------- Modelo hidráulico partilhado com Python ----------------
function orderedPipesForProfile(){
  if(!state.pipes.length)return [];
  const nodes=[];const edges=state.pipes.map(pipe=>{
    const a=mercatorXY(pipe.latlngs[0]),b=mercatorXY(pipe.latlngs[pipe.latlngs.length-1]);
    const node=(pt)=>{let i=nodes.findIndex(n=>Math.hypot(n.x-pt.x,n.y-pt.y)<=0.2);if(i<0){nodes.push(pt);i=nodes.length-1;}return i;};
    return {pipe,a:node(a),b:node(b)};
  });
  const adj=new Map();edges.forEach((edge,i)=>{for(const [u,v] of [[edge.a,edge.b],[edge.b,edge.a]]){if(!adj.has(u))adj.set(u,[]);adj.get(u).push({edge:i,other:v});}});
  if([...adj.values()].some(v=>v.length>2))return [];
  const ends=[...adj.entries()].filter(([,v])=>v.length===1).map(([id])=>id);if(ends.length!==2)return edges.length===1?edges.map(e=>({pipe:e.pipe,reverse:false})):[];
  const ordered=[];const used=new Set();let current=ends[0];
  while(true){const next=(adj.get(current)||[]).find(v=>!used.has(v.edge));if(!next)break;used.add(next.edge);const e=edges[next.edge];ordered.push({pipe:e.pipe,reverse:e.a!==current});current=next.other;}
  return used.size===edges.length?ordered:[];
}
function interpolateProfileElevation(samples,chainage){
  if(!Array.isArray(samples)||samples.length<2)return null;
  if(chainage<=samples[0].distance)return samples[0].elevation;
  if(chainage>=samples[samples.length-1].distance)return samples[samples.length-1].elevation;
  for(let i=1;i<samples.length;i++){const a=samples[i-1],b=samples[i];if(a.distance<=chainage&&chainage<=b.distance){const t=(chainage-a.distance)/Math.max(1e-9,b.distance-a.distance);return a.elevation+(b.elevation-a.elevation)*t;}}
  return null;
}
function buildGeoProfile(){
  const ordered=orderedPipesForProfile();
  if(!ordered.length||ordered.some(item=>!Array.isArray(item.pipe.profileSamples)||item.pipe.profileSamples.length<2))return [];
  const geo=[];let cumulative=0;
  ordered.forEach(({pipe,reverse})=>{
    pipe.chainStartM=cumulative;pipe.profileReverse=reverse;
    const samples=reverse?[...pipe.profileSamples].reverse():pipe.profileSamples;
    samples.forEach((sample,index)=>{
      if(geo.length&&index===0){
        const previous=geo[geo.length-1];
        if(Math.hypot(previous.latitude-sample.lat,previous.longitude-sample.lng)<1e-7)return;
      }
      const local=reverse?pipe.lengthM-sample.distance:sample.distance;
      geo.push({progressiva_m:cumulative+local,latitude:sample.lat,longitude:sample.lng,terreno_m:sample.elevation});
    });
    cumulative+=pipe.lengthM;
  });
  return geo.length>=2?geo:[];
}
function publishModel(){
  const pipes=state.pipes.map(p=>{
    const first=hydraulicNodeXY(p.latlngs[0]),last=hydraulicNodeXY(p.latlngs[p.latlngs.length-1]);
    return {id:p.id,nome:p.name,funcao:p.role,x1:first.x,y1:first.y,x2:last.x,y2:last.y,comprimento_m:number(p.lengthM),lengthM:number(p.lengthM),diametro_dn:number(p.dn),diametro_interno_mm:number(p.dn),dn:number(p.dn),material:p.material,geometry:p.latlngs.map(ll=>({lat:ll.lat,lng:ll.lng}))};
  });
  const components=state.components.map(c=>({id:c.id,tipo:c.type,type:c.type,nome:c.name,nome_componente:c.name,diametro_dn:number(c.dn),dn:number(c.dn),posicao_m:number(c.positionM),position_m:number(c.positionM),orientacao:number(c.rotation),estado:c.status,coeficiente_k:number(c.k),k:number(c.k),troco_id:c.attached?c.pipeId:null,pipe_id:c.attached?c.pipeId:null,latitude:c.latlng?.lat,longitude:c.latlng?.lng}));
  const initialText=$('initialHgl').value.trim();
  const initialHgl=initialText!==''&&Number.isFinite(Number(initialText))?Number(initialText):null;
  const model={versao_esquema:3,unidades:{comprimento:'m',diametro:'mm',caudal:'m3/s',cota:'m'},pipes,components,perfil_geografico:buildGeoProfile(),comprimento_perfil_geografico_m:0,profundidade_eixo_m:number($('profileDepth').value,1.2),cota_piezometrica_inicial_m:initialHgl};
  if(model.perfil_geografico.length){model.comprimento_perfil_geografico_m=model.perfil_geografico[model.perfil_geografico.length-1].progressiva_m;}
  const bridge=state.bridge.acessorios;
  if(bridge&&typeof bridge.modelo_hidraulico==='function'){
    try{bridge.modelo_hidraulico(model);state.modelSendQueued=false;}catch(error){state.modelSendQueued=true;console.warn('Falha ao enviar modelo:',error);}
  }else state.modelSendQueued=true;
  return model;
}

// ---------------- Perfil longitudinal: apenas por pedido ----------------
function interpolateGeodesic(a,b,t){
  const rad=Math.PI/180,deg=180/Math.PI;
  const lat1=a.lat*rad,lon1=a.lng*rad,lat2=b.lat*rad,lon2=b.lng*rad;
  const v1=[Math.cos(lat1)*Math.cos(lon1),Math.cos(lat1)*Math.sin(lon1),Math.sin(lat1)];
  const v2=[Math.cos(lat2)*Math.cos(lon2),Math.cos(lat2)*Math.sin(lon2),Math.sin(lat2)];
  const dot=Math.max(-1,Math.min(1,v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]));
  const omega=Math.acos(dot);
  if(omega<1e-10)return {lat:a.lat+(b.lat-a.lat)*t,lng:a.lng+(b.lng-a.lng)*t};
  const sinOmega=Math.sin(omega);
  const wa=Math.sin((1-t)*omega)/sinOmega,wb=Math.sin(t*omega)/sinOmega;
  const x=wa*v1[0]+wb*v2[0],y=wa*v1[1]+wb*v2[1],z=wa*v1[2]+wb*v2[2];
  return {lat:Math.atan2(z,Math.hypot(x,y))*deg,lng:Math.atan2(y,x)*deg};
}
function sampleRoute(latlngs,spacing,maxSamples=180){
  if(!Array.isArray(latlngs)||latlngs.length<2)throw new Error('O troço precisa de pelo menos dois vértices.');
  const cumulative=[0];
  for(let i=1;i<latlngs.length;i++)cumulative.push(cumulative[i-1]+latlngs[i-1].distanceTo(latlngs[i]));
  const total=cumulative[cumulative.length-1];if(!Number.isFinite(total)||total<=0)throw new Error('O comprimento do troço é nulo.');
  const desired=Math.max(10,number(spacing,40));
  const count=Math.max(2,Math.min(maxSamples,Math.ceil(total/desired)+1));
  const samples=[];let segment=0;
  for(let i=0;i<count;i++){
    const chain=total*i/(count-1);
    while(segment<cumulative.length-2&&cumulative[segment+1]<chain)segment++;
    const segmentLength=cumulative[segment+1]-cumulative[segment];
    const t=segmentLength>0?(chain-cumulative[segment])/segmentLength:0;
    const ll=interpolateGeodesic(latlngs[segment],latlngs[segment+1],t);
    samples.push({...ll,distance:chain});
  }
  return {samples,total,actualSpacing:total/(count-1)};
}
async function fetchElevations(points){
  const output=new Array(points.length),missing=[];
  points.forEach((p,i)=>{const key=`${p.lat.toFixed(5)},${p.lng.toFixed(5)}`;if(state.elevationCache.has(key))output[i]=state.elevationCache.get(key);else missing.push({i,p,key});});
  for(let start=0;start<missing.length;start+=20){
    const batch=missing.slice(start,start+20);const locations=batch.map(x=>`${x.p.lat.toFixed(6)},${x.p.lng.toFixed(6)}`).join('|');
    const controller=typeof AbortController!=='undefined'?new AbortController():null;
    const timeout=controller?setTimeout(()=>controller.abort(),18000):null;
    let response;
    try{
      response=await fetch(`https://api.open-elevation.com/api/v1/lookup?locations=${encodeURIComponent(locations)}`,controller?{signal:controller.signal}:{});
    }catch(error){
      if(error?.name==='AbortError')throw new Error('o serviço de cotas demorou mais de 18 segundos; tente novamente');
      throw error;
    }finally{if(timeout)clearTimeout(timeout);}
    if(!response.ok)throw new Error(`serviço de cotas respondeu HTTP ${response.status}`);
    const result=await response.json();if(!Array.isArray(result.results)||result.results.length!==batch.length)throw new Error('o serviço devolveu cotas incompletas');
    result.results.forEach((item,i)=>{const z=Number(item.elevation);if(!Number.isFinite(z))throw new Error('o serviço devolveu uma cota inválida');const ref=batch[i];state.elevationCache.set(ref.key,z);output[ref.i]=z;});
  }
  return output;
}
async function openLongitudinalProfile(){
  const pipe=selectedPipe();if(!pipe){status('Seleccione exactamente um troço antes de abrir o perfil longitudinal');return;}
  $('profileModal').style.display='flex';state.profileOpen=true;$('profileTitle').textContent=`Perfil longitudinal · ${pipe.name}`;
  $('profileSummary').textContent='A recolher cotas do terreno para o troço seleccionado…';$('profileChart').innerHTML='';
  const request=++state.profileRequest;const spacing=Math.max(10,Math.min(500,number($('profileSpacing').value,40)));
  try{
    const ordered=orderedPipesForProfile();
    const profilePipes=ordered.length===state.pipes.length?ordered:[{pipe,reverse:false}];
    // O troço seleccionado é sempre processado primeiro. Se um troço vizinho
    // falhar no serviço MDE, o perfil pedido continua disponível; nesse caso
    // apenas não será possível obter HGL/EGL para a cadeia completa.
    const prioritised=[{pipe,reverse:profilePipes.find(x=>x.pipe.id===pipe.id)?.reverse||false},
      ...profilePipes.filter(x=>x.pipe.id!==pipe.id)];
    let neighbourWarning='';
    for(const item of prioritised){
      const target=item.pipe;
      try{
        const route=sampleRoute(target.latlngs,spacing);const elevations=await fetchElevations(route.samples);
        if(request!==state.profileRequest)return;
        const scale=route.total>0?target.lengthM/route.total:1;
        target.profileSamples=route.samples.map((sample,index)=>({...sample,distance:sample.distance*scale,elevation:elevations[index]}));
      }catch(error){
        if(target.id===pipe.id)throw error;
        target.profileSamples=null;
        neighbourWarning=` Perfil do troço seleccionado disponível, mas ${target.name} não tem cotas; HGL/EGL podem não ser apresentadas.`;
      }
    }
    const selectedSamples=pipe.profileSamples||[];
    if(selectedSamples.length<2)throw new Error('Não foram obtidas cotas suficientes para o troço seleccionado.');
    state.profileData={pipeId:pipe.id,total:pipe.lengthM,samples:selectedSamples.map(p=>({...p})),neighbourWarning};
    publishModel();
    const first=selectedSamples[0].elevation,last=selectedSamples[selectedSamples.length-1].elevation;
    if(state.bridge.altura&&typeof state.bridge.altura.altura_==='function')state.bridge.altura.altura_(Math.abs(last-first));
    if(state.bridge.comprimento&&typeof state.bridge.comprimento.comprimento_==='function')state.bridge.comprimento.comprimento_(pipe.lengthM);
    renderProfile();status(`Perfil de ${pipe.name} actualizado · ${pipe.lengthM.toFixed(1)} m${neighbourWarning?' · perfil parcial':''}`);
  }catch(error){
    if(request!==state.profileRequest)return;
    state.profileData=null;$('profileSummary').innerHTML=`<span style="color:#a13f37">Não foi possível obter as cotas: ${esc(error.message)}. Verifique a ligação ao serviço de elevação e tente novamente.</span>`;$('profileChart').innerHTML='';status('Falha ao obter cotas para o perfil');
  }
}
function renderProfile(){
  const d=state.profileData;if(!d)return;
  const pipe=findPipe(d.pipeId);if(!pipe)return;
  const data=(d.samples||[]).filter(p=>Number.isFinite(Number(p.distance))&&Number.isFinite(Number(p.elevation)));
  if(data.length<2){$('profileChart').innerHTML='';$('profileSummary').textContent='Não existem pontos de cota suficientes para desenhar o perfil.';return;}
  const W=1200,H=610,pad={l:88,r:42,t:76,b:74},depth=Math.max(0,number($('profileDepth').value,1.2));
  const terrain=data.map(p=>Number(p.elevation)),axis=terrain.map(z=>z-depth);
  const hPoints=(state.hydraulicProfile?.pontos||[]).filter(p=>String(p.troco_id)===String(pipe.id)&&Number.isFinite(Number(p.progressiva_m))&&Number.isFinite(Number(p.hgl_m))&&Number.isFinite(Number(p.egl_m)));
  const hydraulicLevels=hPoints.flatMap(p=>[Number(p.hgl_m),Number(p.egl_m)]);
  let minZ=Math.min(...terrain,...axis,...hydraulicLevels),maxZ=Math.max(...terrain,...axis,...hydraulicLevels);
  if(!Number.isFinite(minZ)||!Number.isFinite(maxZ)){minZ=0;maxZ=1;}
  if(maxZ-minZ<1){const mid=(maxZ+minZ)/2;minZ=mid-.5;maxZ=mid+.5;}
  const extra=(maxZ-minZ)*.13;minZ-=extra;maxZ+=extra;
  const total=Math.max(.01,Number(d.total)||Number(pipe.lengthM)||.01);
  const x=v=>pad.l+Math.max(0,Math.min(total,v))/total*(W-pad.l-pad.r);
  const y=v=>H-pad.b-(v-minZ)/(maxZ-minZ)*(H-pad.t-pad.b);
  const path=values=>data.map((p,i)=>`${i?'L':'M'}${x(p.distance).toFixed(2)},${y(values[i]).toFixed(2)}`).join(' ');
  const terrainPath=path(terrain),axisPath=path(axis);
  const areaPath=`${terrainPath} L ${x(total)} ${H-pad.b} L ${x(0)} ${H-pad.b} Z`;
  const grid=[];
  for(let i=0;i<=6;i++){
    const z=maxZ-(maxZ-minZ)*i/6,yy=y(z);
    grid.push(`<line x1="${pad.l}" y1="${yy}" x2="${W-pad.r}" y2="${yy}" stroke="${i===6?'#cbd7e2':'#e7edf3'}" stroke-width="${i===6?1.3:1}"/>`);
    grid.push(`<text x="${pad.l-12}" y="${yy+4}" text-anchor="end" fill="#63778b" font-size="10">${z.toFixed(2)}</text>`);
  }
  for(let i=0;i<=6;i++){
    const s=total*i/6,xx=x(s);
    grid.push(`<line x1="${xx}" y1="${pad.t}" x2="${xx}" y2="${H-pad.b}" stroke="#edf1f5"/>`);
    grid.push(`<text x="${xx}" y="${H-pad.b+20}" text-anchor="middle" fill="#63778b" font-size="10">${s.toFixed(0)}</text>`);
  }
  // O motor hidráulico fornece progressivas globais. Recentrar no início do troço
  // e inverter a abscissa quando o sentido da cadeia difere do desenho original.
  const hydraulicOffset=hPoints.length?Math.min(...hPoints.map(p=>Number(p.progressiva_m))):0;
  const localHydraulicDistance=p=>{
    const local=Number(p.progressiva_m)-hydraulicOffset;
    return pipe.profileReverse?total-local:local;
  };
  const hydraulicPath=key=>hPoints.map((p,i)=>`${i?'L':'M'}${x(localHydraulicDistance(p))},${y(Number(p[key]))}`).join(' ');
  const hgl=hPoints.length>=2?hydraulicPath('hgl_m'):'';
  const egl=hPoints.length>=2?hydraulicPath('egl_m'):'';
  const markers=data.map((p,i)=>{
    if(i!==0&&i!==data.length-1&&i%Math.max(1,Math.floor(data.length/9))!==0)return '';
    return `<circle cx="${x(p.distance)}" cy="${y(p.elevation)}" r="3.5" fill="#98784c"><title>Estaca ${Number(p.distance).toFixed(1)} m · cota ${Number(p.elevation).toFixed(2)} m</title></circle>`;
  }).join('');
  const accessories=state.components.filter(c=>c.pipeId===pipe.id).sort((a,b)=>a.positionM-b.positionM).map(c=>{
    const s=Math.max(0,Math.min(total,Number(c.positionM)||0));
    const sample=data.reduce((best,p)=>Math.abs(p.distance-s)<Math.abs(best.distance-s)?p:best,data[0]);
    const xx=x(s),yy=y(sample.elevation)-16;
    const label=esc(c.name);
    return `<line x1="${xx}" y1="${yy+5}" x2="${xx}" y2="${y(sample.elevation)-3}" stroke="#7654a4" stroke-width="1.2" stroke-dasharray="3 2"/><path d="M ${xx} ${yy-5} l 5 5 l -5 5 l -5 -5 z" fill="#7654a4"><title>${label} · progressiva ${s.toFixed(1)} m</title></path><text x="${xx+7}" y="${yy-7}" fill="#68488f" font-size="9" font-weight="700">${label.length>22?label.slice(0,19)+'…':label}</text>`;
  }).join('');
  const first=data[0],last=data[data.length-1],rise=last.elevation-first.elevation;
  const gain=data.slice(1).reduce((sum,p,i)=>sum+Math.max(0,p.elevation-data[i].elevation),0);
  const loss=data.slice(1).reduce((sum,p,i)=>sum+Math.max(0,data[i].elevation-p.elevation),0);
  const grade=100*rise/total,actualSpacing=total/(data.length-1);
  const hglPath=hgl?`<path d="${hgl}" fill="none" stroke="#16845b" stroke-width="2.8" stroke-dasharray="9 4"><title>Linha piezométrica (HGL)</title></path>`:'';
  const eglPath=egl?`<path d="${egl}" fill="none" stroke="#bd6a22" stroke-width="2.8" stroke-dasharray="3 4"><title>Linha de energia (EGL)</title></path>`:'';
  const legend=[
    `<line x1="${pad.l}" y1="27" x2="${pad.l+28}" y2="27" stroke="#98784c" stroke-width="3"/><text x="${pad.l+35}" y="31" fill="#455b70" font-size="11">Terreno (MDE)</text>`,
    `<line x1="${pad.l+155}" y1="27" x2="${pad.l+183}" y2="27" stroke="#2474a7" stroke-width="3.5"/><text x="${pad.l+190}" y="31" fill="#455b70" font-size="11">Eixo da tubagem</text>`,
    hgl?`<line x1="${pad.l+340}" y1="27" x2="${pad.l+368}" y2="27" stroke="#16845b" stroke-width="2.8" stroke-dasharray="8 4"/><text x="${pad.l+375}" y="31" fill="#455b70" font-size="11">HGL</text>`:'',
    egl?`<line x1="${pad.l+440}" y1="27" x2="${pad.l+468}" y2="27" stroke="#bd6a22" stroke-width="2.8" stroke-dasharray="3 4"/><text x="${pad.l+475}" y="31" fill="#455b70" font-size="11">EGL</text>`:'',
    `<path d="M ${pad.l+560} 27 l 5 -5 l 5 5 l -5 5 z" fill="#7654a4"/><text x="${pad.l+578}" y="31" fill="#455b70" font-size="11">Acessório</text>`
  ].join('');
  $('profileChart').innerHTML=`
    <rect x="0" y="0" width="${W}" height="${H}" fill="#fbfdff"/>
    ${legend}${grid.join('')}
    <path d="${areaPath}" fill="rgba(178,145,91,.16)"/>
    <path d="${terrainPath}" fill="none" stroke="#98784c" stroke-width="2.8" stroke-linejoin="round"/>
    <path d="${axisPath}" fill="none" stroke="#2474a7" stroke-width="3.5" stroke-linejoin="round"/>
    ${hglPath}${eglPath}${markers}${accessories}
    <circle cx="${x(0)}" cy="${y(first.elevation)}" r="5" fill="#98784c" stroke="#fff" stroke-width="1.5"/>
    <circle cx="${x(total)}" cy="${y(last.elevation)}" r="5" fill="#98784c" stroke="#fff" stroke-width="1.5"/>
    <text x="${x(0)+8}" y="${y(first.elevation)-10}" fill="#795d36" font-size="10" font-weight="700">Início ${first.elevation.toFixed(2)} m</text>
    <text x="${x(total)-8}" y="${y(last.elevation)-10}" text-anchor="end" fill="#795d36" font-size="10" font-weight="700">Fim ${last.elevation.toFixed(2)} m</text>
    <line x1="${pad.l}" y1="${H-pad.b}" x2="${W-pad.r}" y2="${H-pad.b}" stroke="#91a2b2" stroke-width="1.3"/>
    <line x1="${pad.l}" y1="${pad.t}" x2="${pad.l}" y2="${H-pad.b}" stroke="#91a2b2" stroke-width="1.3"/>
    <text x="${W/2}" y="${H-17}" text-anchor="middle" fill="#52677b" font-size="11">Progressiva ao longo do troço (m)</text>
    <text x="20" y="${H/2}" text-anchor="middle" transform="rotate(-90 20 ${H/2})" fill="#52677b" font-size="11">Cota altimétrica (m)</text>
  `;
  const hydraulicLabel=hPoints.length>=2?'HGL/EGL do cálculo hidráulico disponíveis':'HGL/EGL não apresentados: falta condição de fronteira ou cadeia hidráulica completa';
  $('profileSummary').innerHTML=`
    <span>Comprimento<strong>${total.toFixed(1)} m</strong></span>
    <span>Cota inicial<strong>${first.elevation.toFixed(2)} m</strong></span>
    <span>Cota final<strong>${last.elevation.toFixed(2)} m</strong></span>
    <span>Desnível<strong>${rise>=0?'+':''}${rise.toFixed(2)} m</strong></span>
    <span>Declive médio<strong>${grade.toFixed(2)}%</strong></span>
    <span>Subida acumulada<strong>${gain.toFixed(1)} m</strong></span>
    <span>Descida acumulada<strong>${loss.toFixed(1)} m</strong></span>
    <span>Amostras<strong>${data.length} / ${actualSpacing.toFixed(1)} m</strong></span>
    <span>Profundidade ao eixo<strong>${depth.toFixed(2)} m</strong></span>
    <span>Acessórios<strong>${state.components.filter(c=>c.pipeId===pipe.id).length}</strong></span>
    <span style="color:${hPoints.length>=2?'#16734f':'#9a6b26'}">${esc(hydraulicLabel)}</span>
  `;
  $('profileFoot').textContent='As cotas provêm de um modelo digital de elevação (MDE), não de levantamento topográfico. O eixo da tubagem é estimado por profundidade constante abaixo do terreno. Confirme cotas, recobrimento, nível de água e condições de fronteira antes de utilizar o perfil em projecto executivo.'+(d.neighbourWarning||'');
}
$('profileBtn').addEventListener('click',openLongitudinalProfile);
$('closeProfileBtn').addEventListener('click',()=>{$('profileModal').style.display='none';state.profileOpen=false;state.profileRequest++;});
$('refreshProfileBtn').addEventListener('click',openLongitudinalProfile);
$('profileDepth').addEventListener('change',()=>{publishModel();if(state.profileData)renderProfile();});
$('initialHgl').addEventListener('change',()=>{publishModel();status('Condição de fronteira actualizada; o motor hidráulico irá recalcular o perfil quando disponível.');});

// ---------------- Esquema de consulta gerado do mesmo modelo do mapa ----------------
function openSchematic(){
  if(!state.pipes.length){status('Desenhe primeiro pelo menos um troço no mapa');return;}
  const svg=$('schematicSvg'),W=1200,H=580,ordered=orderedPipesForProfile();
  const isSingleChain=ordered.length===state.pipes.length;
  const rows=isSingleChain?[ordered.map(x=>x.pipe)]:state.pipes.map(p=>[p]);
  const rowTop=90,rowGap=Math.min(150,(H-150)/Math.max(1,rows.length));
  const pieces=[];let totalAccessories=0;
  rows.forEach((row,rowIndex)=>{
    const y=rowTop+rowIndex*rowGap+38;const left=90,right=1110;
    const lengths=row.map(p=>Math.max(1,number(p.lengthM,1)));const sum=lengths.reduce((a,b)=>a+b,0);
    const gaps= Math.max(0,row.length-1)*20;const usable=right-left-gaps;let cursor=left;
    row.forEach((pipe,i)=>{
      const width=Math.max(1,usable*lengths[i]/sum);const x1=cursor,x2=Math.min(right,cursor+width);cursor=x2+20;
      pieces.push(`<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="#2876a8" stroke-width="7" stroke-linecap="round"/><line x1="${x1}" y1="${y-9}" x2="${x2}" y2="${y-9}" stroke="#164f79" stroke-width="1.2"/><circle cx="${x1}" cy="${y}" r="5" fill="#fff" stroke="#164f79" stroke-width="2"/><circle cx="${x2}" cy="${y}" r="5" fill="#fff" stroke="#164f79" stroke-width="2"/>`);
      pieces.push(`<text x="${(x1+x2)/2}" y="${y-24}" text-anchor="middle" fill="#25465f" font-size="13" font-weight="700">${esc(pipe.name)} · ${esc(pipe.role)}</text><text x="${(x1+x2)/2}" y="${y+29}" text-anchor="middle" fill="#63788b" font-size="10">DN ${number(pipe.dn)} mm · ${number(pipe.lengthM).toFixed(1)} m · ${esc(pipe.material)}</text>`);
      const fittings=state.components.filter(c=>c.pipeId===pipe.id).sort((a,b)=>a.positionM-b.positionM);
      fittings.forEach(c=>{totalAccessories++;const t=Math.max(0,Math.min(1,number(c.positionM)/Math.max(.001,number(pipe.lengthM))));const cx=x1+(x2-x1)*t;pieces.push(`<circle cx="${cx}" cy="${y}" r="11" fill="#fff" stroke="#6b4ca5" stroke-width="2.5"/><text x="${cx}" y="${y+4}" text-anchor="middle" fill="#6b4ca5" font-size="12" font-weight="800">${esc((ACCESSORIES.find(a=>a.type===c.type)?.icon)||'•')}</text><text x="${cx}" y="${y-17}" text-anchor="middle" fill="#5d4b7d" font-size="9">${esc(c.name)}</text>`);});
    });
    pieces.push(`<text x="55" y="${y+4}" text-anchor="middle" fill="#1769aa" font-size="10" font-weight="800">${rowIndex+1}</text>`);
  });
  svg.innerHTML=`<defs><pattern id="schematicGrid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#edf1f5" stroke-width="1"/></pattern></defs><rect width="1200" height="580" fill="url(#schematicGrid)"/>${pieces.join('')}<text x="600" y="545" text-anchor="middle" fill="#8493a2" font-size="10">Representação esquemática; os comprimentos são indicativos e não estão à escala.</text>`;
  $('schematicSummary').textContent=`${state.pipes.length} troço(s) · ${totalAccessories} acessório(s) · ${isSingleChain?'linha ligada em série':'troços não formam uma única linha contínua; cada troço é apresentado separadamente'}. As alterações continuam a ser feitas no mapa.`;
  $('schematicModal').style.display='flex';
}
$('schematicBtn').addEventListener('click',openSchematic);
$('closeSchematicBtn').addEventListener('click',()=>{$('schematicModal').style.display='none';});
$('schematicModal').addEventListener('click',e=>{if(e.target.id==='schematicModal')$('schematicModal').style.display='none';});

// O MainWindow chama estas funções através de runJavaScript.
window.receber_perfil_hidraulico=function(result){state.hydraulicProfile=result&&result.valido&&Array.isArray(result.pontos)?result:null;if(state.profileOpen&&state.profileData)renderProfile();return !!state.hydraulicProfile;};
window.limpar_perfil_hidraulico=function(){state.hydraulicProfile=null;if(state.profileOpen&&state.profileData)renderProfile();};
window.limpar_mapa=function(){
  state.pipes.forEach(p=>{if(p.layer)state.map.removeLayer(p.layer);});state.components.forEach(c=>{if(c.marker)state.map.removeLayer(c.marker);});
  state.pipes=[];state.components=[];state.selectedPipeIds=[];state.selectedComponentId=null;state.profileData=null;state.hydraulicProfile=null;state.pendingAccessory=null;state.mode='select';$('profileModal').style.display='none';$('schematicModal').style.display='none';state.profileOpen=false;clearVertexHandles();clearSelection();renderInspector();updateToolbar();publishModel();status('Projecto geográfico limpo');
};
window.pesquisar_lugar=async function(query){
  const value=String(query||'').trim();if(!value||!state.map)return;
  try{const response=await fetch(`https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(value)}`);if(!response.ok)throw new Error(`HTTP ${response.status}`);const rows=await response.json();if(!rows.length){status('Local não encontrado');return;}const ll=L.latLng(Number(rows[0].lat),Number(rows[0].lon));state.map.setView(ll,15);status(`Mapa centrado em ${rows[0].display_name||value}`);}catch(error){status(`Falha na pesquisa: ${error.message}`);}
};
$('searchBtn').addEventListener('click',()=>window.pesquisar_lugar($('mapSearch').value));$('mapSearch').addEventListener('keydown',e=>{if(e.key==='Enter')window.pesquisar_lugar(e.target.value);});

// ---------------- Arranque do mapa ----------------
function initMap(){
  state.map=L.map('map',{center:[-25.9667,32.5833],zoom:15,doubleClickZoom:false,preferCanvas:false});
  const streets=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors',crossOrigin:true});
  const satellite=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Tiles &copy; Esri'});
  streets.addTo(state.map);L.control.layers({'Mapa':streets,'Satélite':satellite},null,{collapsed:true}).addTo(state.map);L.control.scale({metric:true,imperial:false}).addTo(state.map);
  let tileErrors=0;streets.on('tileerror',()=>{tileErrors++;if(tileErrors>=3)status('Mapa carregado, mas os mapas-base não respondem. Verifique a Internet.');});
  attachMapHandlers();renderInspector();updateToolbar();state.map.whenReady(()=>{setTimeout(()=>state.map.invalidateSize(),100);window.aquapumpReady=true;status('Mapa pronto · clique em “Traçar tubulação” para começar');});
}
async function boot(){
  renderLibrary();initWebChannel();
  const loaded=await loadLeaflet();
  if(!loaded){$('mapFallback').style.display='flex';$('fallbackDetail').textContent='As bibliotecas Leaflet não puderam ser descarregadas de unpkg.com nem de jsDelivr. O mapa requer acesso à Internet para carregar a biblioteca e os mapas-base. Verifique firewall/proxy e tente novamente.';status('Falha no carregamento da biblioteca cartográfica');return;}
  try{initMap();}catch(error){$('mapFallback').style.display='flex';$('fallbackDetail').textContent=`A biblioteca foi carregada, mas o mapa não pôde ser inicializado: ${error.message}`;status('Erro ao inicializar o mapa');console.error(error);}
}
$('retryMapBtn').addEventListener('click',()=>{$('mapFallback').style.display='none';boot();});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
</body>
</html>'''
