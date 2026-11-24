"""Gestão incremental de bombas, associações, cálculos e gráficos do AquaPump.

Compatibilidade:
- Mantém GestorBombas(ui, parent=None) como chamada principal.
- Mantém associacao_serie e associacao_paralelo para o comportamento antigo.
- Acrescenta associações nomeadas construídas a partir dos índices das bombas
  ou de outras associações já registadas.
- Mantém os cálculos internos no SI.

A classe continua a ser um orquestrador da interface existente; não substitui
os módulos Bomba, AssociacaoBombas, Perdas ou Grafico.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Optional

import numpy as np

# O gestor também pode ser importado em testes sem a interface Qt instalada.
try:  # pragma: no cover - depende do ambiente da aplicação
    from PySide6.QtCore import QObject
    from PySide6.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout, QWidget
    QT_AVAILABLE = True
except ImportError:  # fallback apenas para testes/headless
    QT_AVAILABLE = False

    class QObject:  # type: ignore[no-redef]
        def __init__(self, parent=None):
            self._qt_parent = parent

    class QWidget:  # type: ignore[no-redef]
        pass

    class QVBoxLayout:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise RuntimeError("PySide6 é necessário para construir gráficos na interface.")

    class QFileDialog:  # type: ignore[no-redef]
        @staticmethod
        def getSaveFileName(*args, **kwargs):
            raise RuntimeError("PySide6 é necessário para abrir diálogos de ficheiros.")

        @staticmethod
        def getOpenFileName(*args, **kwargs):
            raise RuntimeError("PySide6 é necessário para abrir diálogos de ficheiros.")

    class QMessageBox:  # type: ignore[no-redef]
        class StandardButton:
            Yes = 1
            No = 2

        @staticmethod
        def information(*args, **kwargs):
            return None

        @staticmethod
        def critical(*args, **kwargs):
            return None

        @staticmethod
        def question(*args, **kwargs):
            return QMessageBox.StandardButton.No

# Modelos do pacote src.
try:
    from .bomba import Bomba, BombaError
    from .associacao_bombas import AssociacaoBombas, curva_sistema_de_perdas
except ImportError:  # execução antiga com src/ no sys.path
    from bomba import Bomba, BombaError
    from associacao_bombas import AssociacaoBombas, curva_sistema_de_perdas

# Módulos que pertencem à pasta calculos/ no repositório original.
try:
    from calculos.curvas_bomba import Grafico
except ImportError:
    try:
        from curvas_bomba import Grafico
    except ImportError:
        Grafico = None  # type: ignore[assignment,misc]

try:
    from calculos.perdas_cargas import Perdas
except ImportError:
    try:
        from perdas_cargas import Perdas
    except ImportError:
        Perdas = None  # type: ignore[assignment,misc]

try:
    from calculos.unidades import ConversorUnidades
except ImportError:
    try:
        from unidades import ConversorUnidades
    except ImportError:
        ConversorUnidades = None  # type: ignore[assignment,misc]

try:
    from calculos.dimensionamento_tubulacao import Tubulacao
except ImportError:
    try:
        from calculos.dimensionamento_tubulação import Tubulacao
    except ImportError:
        try:
            from dimensionamento_tubulacao import Tubulacao
        except ImportError:
            try:
                from dimensionamento_tubulação import Tubulacao
            except ImportError:
                Tubulacao = None  # type: ignore[assignment,misc]


class GestorBombas(QObject):
    """Orquestra os modelos existentes do AquaPump e a interface PySide6."""

    PAGINAS = {
        "altura": 0,
        "potencia": 1,
        "rendimento": 2,
        "npsh": 3,
        "serie": 4,
        "paralelo": 5,
    }
    UNIDADES_VAZAO = ["m³/h", "m³/s", "L/s", "L/min", "L/h", "gal/min"]

    def __init__(
        self,
        ui,
        parent: Optional[QWidget] = None,
        *,
        carregar_demo: bool = True,
        construir_graficos: bool = True,
        conectar_sinais: bool = True,
        perdas_factory=None,
        tubulacao_factory=None,
        conversor_factory=None,
        grafico_factory=None,
    ):
        super().__init__(parent)
        self.ui = ui
        self.parent_widget = parent

        # Permite injecção de dependências em testes e mantém os imports antigos.
        perdas_factory = perdas_factory or Perdas
        tubulacao_factory = tubulacao_factory or Tubulacao
        conversor_factory = conversor_factory or ConversorUnidades
        self._grafico_factory = grafico_factory or Grafico
        if perdas_factory is None or conversor_factory is None:
            raise RuntimeError(
                "Não foi possível importar Perdas/ConversorUnidades. "
                "Verifique a estrutura da pasta calculos/ e as dependências."
            )

        self.bombas: list[Bomba] = []
        self.associacao_serie: Optional[AssociacaoBombas] = None
        self.associacao_paralelo: Optional[AssociacaoBombas] = None
        self.associacoes: dict[str, AssociacaoBombas] = {}
        # As definições guardam referências às bombas e nomes de associações,
        # permitindo reconstruir as curvas quando as bombas são actualizadas.
        self._definicoes_associacoes: dict[str, dict[str, Any]] = {}
        self.avisos_associacoes: list[str] = []

        self._perdas_factory = perdas_factory
        self._tubulacao_factory = tubulacao_factory
        self.perdas = perdas_factory(
            diametro_m=0.05,
            area=math.pi * 0.05**2 / 4.0,
        )
        self.tubulacao = tubulacao_factory() if tubulacao_factory else None
        self.conversor = conversor_factory()

        self.H_geometrico = 15.0
        self.comprimento_m = 100.0
        self.material_darcy = "Aço comercial novo"
        self.material_hazen = "Plástico"
        self.metodo_perdas = "darcy"
        self.tempo_funcionamento_h = 24.0
        self.diametro_automatico = True
        self.graficos: dict[str, Any] = {}
        self.ultimo_resultado: dict[str, Any] = {}
        self.ultimo_erro: Optional[str] = None

        self._configurar_perdas()
        if construir_graficos and ui is not None and self._grafico_factory is not None:
            self._criar_graficos()
        if ui is not None:
            self._popular_combos()
            if conectar_sinais:
                self._conectar_sinais()
        if carregar_demo:
            self._carregar_demo()
        self.atualizar_tudo()

    # ------------------------------------------------------------------
    # Inicialização e interface
    # ------------------------------------------------------------------
    def _configurar_perdas(self) -> None:
        """Sincroniza sempre material, diâmetro e área no objecto Perdas."""
        if hasattr(self.perdas, "definir_material_darcy"):
            self.perdas.definir_material_darcy(self.material_darcy)
        if hasattr(self.perdas, "definir_material_hazen"):
            self.perdas.definir_material_hazen(self.material_hazen)
        if hasattr(self.perdas, "atualizar_parametros"):
            d = float(getattr(self.perdas, "diametro_m", 0.05))
            if not np.isfinite(d) or d <= 0:
                d = 0.05
            self.perdas.atualizar_parametros(
                diametro_m=d,
                area=math.pi * d**2 / 4.0,
            )

    def _criar_graficos(self) -> None:
        containers = {
            "altura": getattr(self.ui, "altura", None),
            "potencia": getattr(self.ui, "potencia", None),
            "rendimento": getattr(self.ui, "rendimento", None),
            "npsh": getattr(self.ui, "npsh_2", None),
            "serie": getattr(self.ui, "serie", None),
            "paralelo": getattr(self.ui, "paralelo", None),
        }
        for nome, container in containers.items():
            if container is None:
                continue
            try:
                grafico = self._grafico_factory(figsize=(7.0, 4.4), dpi=100)
                if hasattr(grafico, "setMinimumSize"):
                    grafico.setMinimumSize(320, 220)
                layout = container.layout()
                if layout is None:
                    layout = QVBoxLayout(container)
                    layout.setContentsMargins(0, 0, 0, 0)
                    layout.setSpacing(0)
                layout.addWidget(grafico)
                self.graficos[nome] = grafico
            except Exception as exc:
                self._registar_erro(f"Não foi possível criar o gráfico '{nome}': {exc}")

    def _popular_combos(self) -> None:
        if hasattr(self.ui, "icone_2"):
            combo = self.ui.icone_2
            combo.clear()
            combo.addItems(self.UNIDADES_VAZAO)
            combo.setCurrentText("m³/h")
        if Perdas is not None and hasattr(self.ui, "darcy"):
            combo = self.ui.darcy
            combo.clear()
            combo.addItems(Perdas.get_lista_materiais_darcy())
            if self.material_darcy in Perdas.get_lista_materiais_darcy():
                combo.setCurrentText(self.material_darcy)
        perdas_cls = self._perdas_factory
        if perdas_cls is not None and hasattr(self.ui, "darcy"):
            combo = self.ui.darcy
            combo.clear()
            materiais = perdas_cls.get_lista_materiais_darcy()
            combo.addItems(materiais)
            if self.material_darcy in materiais:
                combo.setCurrentText(self.material_darcy)
        if perdas_cls is not None and hasattr(self.ui, "hazen_will"):
            combo = self.ui.hazen_will
            combo.clear()
            materiais = perdas_cls.get_lista_materiais_hazen()
            combo.addItems(materiais)
            if self.material_hazen in materiais:
                combo.setCurrentText(self.material_hazen)

    def _conectar_sinais(self) -> None:
        for nome, slot in (
            ("exportar_pdf", self.exportar_pdf),
            ("exportar_csv", self.exportar_csv),
            ("novo_arquivo", self.novo_projecto),
            ("salvar_projecto", self.salvar_projecto),
            ("abrir_arquivo", self.abrir_projecto),
        ):
            widget = getattr(self.ui, nome, None)
            if widget is not None and hasattr(widget, "clicked"):
                widget.clicked.connect(slot)

        # 'Vazao_2' é a vazão. 'Vazao' é o tempo de funcionamento (horas).
        # A versão anterior tentava ler 'Vazao' como vazão quando o primeiro
        # campo estava vazio, confundindo duas grandezas diferentes.
        q_widget = getattr(self.ui, "Vazao_2", None)
        if q_widget is not None and hasattr(q_widget, "textChanged"):
            q_widget.textChanged.connect(self.atualizar_resultados)
        t_widget = getattr(self.ui, "Vazao", None)
        if t_widget is not None and hasattr(t_widget, "textChanged"):
            t_widget.textChanged.connect(self._on_tempo_changed)
        combo_q = getattr(self.ui, "icone_2", None)
        if combo_q is not None and hasattr(combo_q, "currentTextChanged"):
            combo_q.currentTextChanged.connect(self.atualizar_resultados)
        combo_d = getattr(self.ui, "darcy", None)
        if combo_d is not None and hasattr(combo_d, "currentTextChanged"):
            combo_d.currentTextChanged.connect(self._on_material_changed)
        combo_h = getattr(self.ui, "hazen_will", None)
        if combo_h is not None and hasattr(combo_h, "currentTextChanged"):
            combo_h.currentTextChanged.connect(self._on_hazen_material_changed)
        if hasattr(self.ui, "grafico") and hasattr(self.ui.grafico, "clicked"):
            self.ui.grafico.clicked.connect(self._abrir_pagina_altura)

    def _abrir_pagina_altura(self) -> None:
        stack = getattr(self.ui, "stackedWidget_3", None)
        if stack is not None:
            stack.setCurrentIndex(self.PAGINAS["altura"])

    def _registar_erro(self, mensagem: str) -> None:
        self.ultimo_erro = str(mensagem)
        print(f"[GestorBombas] {mensagem}")

    def _limpar_erro(self) -> None:
        self.ultimo_erro = None

    def _on_tempo_changed(self, *_args) -> None:
        tempo = self._ler_tempo_h()
        if tempo is not None:
            self.tempo_funcionamento_h = tempo
        self.atualizar_resultados()

    def _on_material_changed(self, material: str) -> None:
        if material:
            self.material_darcy = str(material)
            self._configurar_perdas()
            self.atualizar_tudo()

    def _on_hazen_material_changed(self, material: str) -> None:
        if material:
            self.material_hazen = str(material)
            self._configurar_perdas()
            self.atualizar_tudo()

    # ------------------------------------------------------------------
    # Bombas
    # ------------------------------------------------------------------
    def _carregar_demo(self) -> None:
        q1 = np.array([0, 6, 12, 18, 24, 30], dtype=float) / 3600.0
        h1 = np.array([42, 40, 37, 32, 24, 12], dtype=float)
        eta1 = np.array([0, 35, 55, 68, 65, 45], dtype=float)
        npsh1 = np.array([1.8, 2.0, 2.4, 3.2, 4.5, 6.5], dtype=float)
        b1 = Bomba("Bomba A", rpm=3500, diametro_rotor_mm=170)
        b1.definir_dados(q1, h1, eta=eta1, npsh_r=npsh1)

        q2 = np.array([0, 5, 10, 15, 20, 25], dtype=float) / 3600.0
        h2 = np.array([40, 38, 35, 30, 22, 10], dtype=float)
        eta2 = np.array([0, 32, 52, 65, 60, 40], dtype=float)
        npsh2 = np.array([1.5, 1.8, 2.2, 3.0, 4.2, 6.0], dtype=float)
        b2 = Bomba("Bomba B", rpm=3500, diametro_rotor_mm=165)
        b2.definir_dados(q2, h2, eta=eta2, npsh_r=npsh2)
        self.bombas = [b1, b2]

    def adicionar_bomba(self, bomba: Bomba) -> None:
        if not isinstance(bomba, Bomba):
            raise TypeError("O elemento adicionado deve ser uma instância de Bomba.")
        self.bombas.append(bomba)
        self.atualizar_tudo()

    def remover_bomba(self, indice: int) -> None:
        if not isinstance(indice, int) or indice < 0 or indice >= len(self.bombas):
            raise IndexError("Índice de bomba inválido.")
        removida = self.bombas.pop(indice)
        # Eliminar definições que usam directamente a bomba removida. As
        # restantes associações serão reavaliadas e as referências inválidas
        # aparecerão em avisos, sem interromper a aplicação.
        removidas = {
            nome for nome, definicao in self._definicoes_associacoes.items()
            if any(item is removida for item in definicao["elementos"])
        }
        alterou = True
        while alterou:
            alterou = False
            for nome, definicao in list(self._definicoes_associacoes.items()):
                if nome not in removidas and any(
                    isinstance(item, str) and item in removidas
                    for item in definicao["elementos"]
                ):
                    removidas.add(nome)
                    alterou = True
        for nome in removidas:
            self._definicoes_associacoes.pop(nome, None)
        self.atualizar_tudo()

    def limpar_bombas(self) -> None:
        self.bombas.clear()
        self._definicoes_associacoes.clear()
        self.atualizar_tudo()

    def carregar_bombas(self, bombas: list[Bomba]) -> None:
        if any(not isinstance(b, Bomba) for b in bombas):
            raise TypeError("A lista deve conter apenas instâncias de Bomba.")
        self.bombas = list(bombas)
        # Definições antigas deixam de ser seguras quando a lista inteira é
        # substituída; não manter associações ligadas a objectos anteriores.
        self._definicoes_associacoes.clear()
        self.atualizar_tudo()

    # ------------------------------------------------------------------
    # Associações — compatibilidade mais construção manual
    # ------------------------------------------------------------------
    def criar_associacao(self, nome: str, tipo: str, elementos: list[Any]) -> AssociacaoBombas:
        """Cria associação a partir de índices de bombas e/ou nomes existentes.

        Exemplos:
            criar_associacao("Duas em paralelo", "paralelo", [0, 1])
            criar_associacao("Conjunto misto", "serie", ["Duas em paralelo", 2])

        Os índices referem-se à lista ``self.bombas``. Para combinações
        aninhadas, use o nome de uma associação já registada.
        """
        nome = str(nome).strip()
        tipo = str(tipo).strip().lower()
        if not nome:
            raise BombaError("A associação precisa de um nome.")
        if tipo not in AssociacaoBombas.TIPOS_VALIDOS:
            raise BombaError(f"Tipo de associação inválido: {tipo!r}.")
        if nome in self._definicoes_associacoes or nome in self.associacoes:
            raise BombaError(f"Já existe uma associação chamada '{nome}'.")
        if not isinstance(elementos, (list, tuple)) or len(elementos) < 2:
            raise BombaError("Seleccione pelo menos dois elementos para associar.")

        referencias: list[Any] = []
        for elemento in elementos:
            if isinstance(elemento, int):
                if elemento < 0 or elemento >= len(self.bombas):
                    raise BombaError(f"Índice de bomba inválido: {elemento}.")
                referencias.append(self.bombas[elemento])
            elif isinstance(elemento, Bomba):
                if elemento not in self.bombas:
                    raise BombaError("A bomba seleccionada não pertence à lista do projecto.")
                referencias.append(elemento)
            elif isinstance(elemento, str):
                if elemento not in self.associacoes:
                    raise BombaError(f"Não existe uma associação chamada '{elemento}'.")
                referencias.append(elemento)
            elif isinstance(elemento, AssociacaoBombas):
                encontrada = next(
                    (n for n, a in self.associacoes.items() if a is elemento), None
                )
                if encontrada is None:
                    raise BombaError("A associação aninhada deve estar registada no gestor.")
                referencias.append(encontrada)
            else:
                raise BombaError("Elemento não suportado na associação.")

        self._definicoes_associacoes[nome] = {"tipo": tipo, "elementos": referencias}
        try:
            self._reconstruir_associacoes()
            resultado = self.associacoes[nome]
        except Exception:
            self._definicoes_associacoes.pop(nome, None)
            self._reconstruir_associacoes()
            raise
        self.atualizar_graficos()
        return resultado

    def remover_associacao(self, nome: str) -> None:
        if nome not in self._definicoes_associacoes:
            raise KeyError(f"Associação personalizada não encontrada: {nome}")
        del self._definicoes_associacoes[nome]
        # Remover também as associações que dependiam dela, evitando referências
        # pendentes e mantendo a árvore de associações simples nesta versão.
        removidas = {nome}
        alterou = True
        while alterou:
            alterou = False
            for chave, definicao in list(self._definicoes_associacoes.items()):
                if any(isinstance(x, str) and x in removidas for x in definicao["elementos"]):
                    removidas.add(chave)
                    del self._definicoes_associacoes[chave]
                    alterou = True
        self._reconstruir_associacoes()
        self.atualizar_graficos()

    def obter_associacao(self, nome: str) -> AssociacaoBombas:
        try:
            return self.associacoes[nome]
        except KeyError as exc:
            raise KeyError(f"Associação não encontrada: {nome}") from exc

    def _construir_associacao_personalizada(self, nome: str, pilha=None):
        pilha = set() if pilha is None else set(pilha)
        if nome in pilha:
            raise BombaError(f"Foi detectada uma dependência circular na associação '{nome}'.")
        definicao = self._definicoes_associacoes[nome]
        elementos = []
        for referencia in definicao["elementos"]:
            if isinstance(referencia, Bomba):
                if referencia not in self.bombas:
                    raise BombaError(f"A associação '{nome}' contém uma bomba removida.")
                elementos.append(referencia)
            elif isinstance(referencia, str):
                if referencia in self._definicoes_associacoes:
                    elementos.append(self._construir_associacao_personalizada(referencia, pilha | {nome}))
                elif referencia in self.associacoes:
                    elementos.append(self.associacoes[referencia])
                else:
                    raise BombaError(f"A associação '{nome}' depende de '{referencia}', que não existe.")
        return AssociacaoBombas(elementos, definicao["tipo"], nome=nome)

    def _reconstruir_associacoes(self) -> None:
        """Actualiza associações automáticas e personalizadas."""
        self.associacao_serie = None
        self.associacao_paralelo = None
        self.associacoes = {}
        self.avisos_associacoes = []

        if len(self.bombas) >= 2:
            try:
                self.associacao_serie = AssociacaoBombas(self.bombas, "serie", nome="Série (todas)")
                self.associacoes["Série (todas)"] = self.associacao_serie
            except BombaError as exc:
                self.avisos_associacoes.append(f"Série automática indisponível: {exc}")
            try:
                self.associacao_paralelo = AssociacaoBombas(self.bombas, "paralelo", nome="Paralelo (todas)")
                self.associacoes["Paralelo (todas)"] = self.associacao_paralelo
            except BombaError as exc:
                self.avisos_associacoes.append(f"Paralelo automático indisponível: {exc}")

        # Construir as associações manuais. Falha numa configuração não impede
        # que as restantes associações continuem disponíveis.
        for nome in self._definicoes_associacoes:
            try:
                self.associacoes[nome] = self._construir_associacao_personalizada(nome)
            except BombaError as exc:
                self.avisos_associacoes.append(f"{nome}: {exc}")

    # ------------------------------------------------------------------
    # Configuração do sistema
    # ------------------------------------------------------------------
    def configurar_sistema(
        self,
        H_geometrico: Optional[float] = None,
        diametro_m: Optional[float] = None,
        comprimento_m: Optional[float] = None,
        material: Optional[str] = None,
        acessorios: Optional[list] = None,
        tempo_funcionamento_h: Optional[float] = None,
        metodo_perdas: Optional[str] = None,
        material_hazen: Optional[str] = None,
    ) -> None:
        if H_geometrico is not None:
            valor = float(H_geometrico)
            if not np.isfinite(valor) or valor < 0:
                raise ValueError("A altura geométrica deve ser finita e não negativa.")
            self.H_geometrico = valor
        if diametro_m is not None:
            valor = float(diametro_m)
            if not np.isfinite(valor) or valor <= 0:
                raise ValueError("O diâmetro deve ser positivo e finito.")
            self.diametro_automatico = False
            self._definir_diametro_estado(valor)
        if comprimento_m is not None:
            valor = float(comprimento_m)
            if not np.isfinite(valor) or valor < 0:
                raise ValueError("O comprimento deve ser finito e não negativo.")
            self.comprimento_m = valor
        if material is not None:
            self.material_darcy = str(material)
        if material_hazen is not None:
            self.material_hazen = str(material_hazen)
        if tempo_funcionamento_h is not None:
            tempo = float(tempo_funcionamento_h)
            if not np.isfinite(tempo) or not 0 < tempo <= 24:
                raise ValueError("O tempo de funcionamento deve estar entre 0 e 24 horas.")
            self.tempo_funcionamento_h = tempo
        if metodo_perdas is not None:
            metodo = str(metodo_perdas).strip().lower()
            if metodo not in ("darcy", "hazen"):
                raise ValueError("O método de perdas deve ser 'darcy' ou 'hazen'.")
            self.metodo_perdas = metodo
        if acessorios is not None:
            if hasattr(self.perdas, "definir_acessorios_lista"):
                self.perdas.definir_acessorios_lista(acessorios)
            else:
                raise RuntimeError("O módulo Perdas não suporta acessórios em lista.")
        self._configurar_perdas()
        self.atualizar_tudo()

    def _definir_diametro_estado(self, diametro_m: float) -> None:
        area = math.pi * diametro_m**2 / 4.0
        self.perdas.atualizar_parametros(diametro_m=diametro_m, area=area)
        if self.tubulacao is not None and hasattr(self.tubulacao, "D"):
            self.tubulacao.D = diametro_m

    def definir_diametro_manual(self, diametro_m: float) -> None:
        """Define um diâmetro fixo que não será substituído pelo cálculo automático."""
        d = float(diametro_m)
        if not np.isfinite(d) or d <= 0:
            raise ValueError("O diâmetro deve ser positivo e finito.")
        self.diametro_automatico = False
        self._definir_diametro_estado(d)
        self.atualizar_tudo()

    def usar_diametro_estimado(self) -> None:
        """Volta a calcular o diâmetro a partir da vazão e do tempo de serviço."""
        if self.tubulacao is None:
            raise RuntimeError("O módulo de dimensionamento de tubulação não está disponível.")
        self.diametro_automatico = True
        self.atualizar_tudo()

    def _H_sistema_fn(self):
        """Constrói a curva do sistema com o método de perdas escolhido."""
        material = self.material_hazen if self.metodo_perdas == "hazen" else self.material_darcy
        calculo = curva_sistema_de_perdas(
            H_geometrico=self.H_geometrico,
            perdas_obj=self.perdas,
            comprimento_m=self.comprimento_m,
            material=material,
            incluir_localizadas=True,
            incluir_hazen=(self.metodo_perdas == "hazen"),
        )

        # A função de curva é chamada muitas vezes pelo solver. Preservar o
        # estado do objecto Perdas evita que a última vazão de amostragem
        # substitua a vazão que o utilizador introduziu na interface.
        def curva_com_estado_preservado(q: float) -> float:
            atributos = ("vazao_m3s", "velocidade_ms", "diametro_m", "area",
                         "material_darcy", "material_hazen")
            anterior = {nome: getattr(self.perdas, nome, None) for nome in atributos}
            try:
                return float(calculo(q))
            finally:
                for nome, valor in anterior.items():
                    if hasattr(self.perdas, nome):
                        setattr(self.perdas, nome, valor)

        return curva_com_estado_preservado

    # ------------------------------------------------------------------
    # Actualização dos resultados
    # ------------------------------------------------------------------
    def _ler_vazao_m3s(self) -> Optional[float]:
        widget = getattr(self.ui, "Vazao_2", None) if self.ui is not None else None
        if widget is None or not hasattr(widget, "text"):
            return None
        texto = str(widget.text()).strip().replace(",", ".")
        if not texto:
            return None
        try:
            valor = float(texto)
            unidade_widget = getattr(self.ui, "icone_2", None)
            unidade = unidade_widget.currentText() if unidade_widget is not None else "m³/s"
            q = float(self.conversor.converter_vazao(valor, unidade or "m³/s", "m³/s"))
            return q if np.isfinite(q) and q > 0 else None
        except (TypeError, ValueError, AttributeError) as exc:
            self._registar_erro(f"Valor/unidade de vazão inválido: {exc}")
            return None

    def _ler_tempo_h(self) -> Optional[float]:
        widget = getattr(self.ui, "Vazao", None) if self.ui is not None else None
        if widget is None or not hasattr(widget, "text"):
            return self.tempo_funcionamento_h
        texto = str(widget.text()).strip().replace(",", ".")
        if not texto:
            return self.tempo_funcionamento_h
        try:
            valor = float(texto)
            if not np.isfinite(valor) or not 0 < valor <= 24:
                raise ValueError("o tempo deve estar entre 0 e 24 horas")
            return valor
        except (TypeError, ValueError) as exc:
            self._registar_erro(f"Tempo de funcionamento inválido: {exc}")
            return None

    @staticmethod
    def _set_text(ui, atributo: str, texto: str) -> None:
        widget = getattr(ui, atributo, None) if ui is not None else None
        if widget is not None and hasattr(widget, "setText"):
            widget.setText(texto)

    def atualizar_resultados(self) -> dict[str, Any]:
        """Actualiza labels e devolve os resultados calculados em SI."""
        q = self._ler_vazao_m3s()
        tempo = self._ler_tempo_h()
        if tempo is not None:
            self.tempo_funcionamento_h = tempo
        if q is None:
            for nome in ("vazao_resul", "diametro_resul", "seccao_resul", "velocidade_resul", "perdas_resul"):
                self._set_text(self.ui, nome, "—")
            self.ultimo_resultado = {}
            return {}

        if self.diametro_automatico and self.tubulacao is not None:
            try:
                d = float(self.tubulacao.calcular_diametro(q, tempo=self.tempo_funcionamento_h))
                if not np.isfinite(d) or d <= 0:
                    raise ValueError("o dimensionador devolveu um diâmetro inválido")
                self._definir_diametro_estado(d)
            except Exception as exc:
                self._registar_erro(f"Falha no dimensionamento automático: {exc}")

        d = float(getattr(self.perdas, "diametro_m", 0.0))
        area = math.pi * d**2 / 4.0 if d > 0 else 0.0
        velocidade = q / area if area > 0 else float("nan")
        h_distribuida = h_localizada = float("nan")
        try:
            self.perdas.atualizar_parametros(
                diametro_m=d, area=area, vazao_m3s=q,
            )
            if self.metodo_perdas == "hazen":
                self.perdas.definir_material_hazen(self.material_hazen)
                h_distribuida = float(self.perdas.calcular_perda_carga_hazen_williams(self.comprimento_m))
            else:
                self.perdas.definir_material_darcy(self.material_darcy)
                h_distribuida = float(self.perdas.calcular_perda_carga_darcy(self.comprimento_m))
            h_localizada = float(self.perdas.calcular_perdas_localizadas())
            if not all(np.isfinite(v) and v >= 0 for v in (h_distribuida, h_localizada)):
                raise ValueError("o cálculo de perdas devolveu valores inválidos")
        except Exception as exc:
            self._registar_erro(f"Falha no cálculo das perdas: {exc}")

        resultado = {
            "Q_m3s": q,
            "Q_m3h": q * 3600.0,
            "diametro_m": d,
            "area_m2": area,
            "velocidade_ms": velocidade,
            "perda_distribuida_m": h_distribuida,
            "perda_localizada_m": h_localizada,
            "perda_total_m": h_distribuida + h_localizada,
            "H_geometrico_m": self.H_geometrico,
        }
        self.ultimo_resultado = resultado
        self._set_text(self.ui, "vazao_resul", f"{q * 3600:.2f} m³/h")
        self._set_text(self.ui, "diametro_resul", f"{d * 1000:.1f} mm" if d > 0 else "—")
        self._set_text(self.ui, "seccao_resul", f"{area * 1e4:.2f} cm²" if area > 0 else "—")
        self._set_text(self.ui, "velocidade_resul", f"{velocidade:.2f} m/s" if np.isfinite(velocidade) else "—")
        if np.isfinite(resultado["perda_total_m"]):
            self._set_text(
                self.ui,
                "perdas_resul",
                f"{resultado['perda_total_m']:.2f} m  "
                f"(distribuída {h_distribuida:.2f} + localizada {h_localizada:.2f})",
            )
        else:
            self._set_text(self.ui, "perdas_resul", "Não calculado")
        return resultado

    # ------------------------------------------------------------------
    # Gráficos
    # ------------------------------------------------------------------
    def _elementos_para_grafico(self) -> list:
        elementos: list[Any] = list(self.bombas)
        for associacao in self.associacoes.values():
            if all(associacao is not item for item in elementos):
                elementos.append(associacao)
        return elementos

    def _plotar_seguro(self, nome_pagina: str, elementos, grandeza: str, H_sistema_fn=None, titulo=None) -> None:
        grafico = self.graficos.get(nome_pagina)
        if grafico is None:
            return
        if not elementos:
            grafico.limpar()
            return
        try:
            grafico.plotar_bombas(
                elementos,
                grandeza=grandeza,
                H_sistema_fn=H_sistema_fn,
                titulo=titulo or f"Curvas — {grandeza}",
            )
        except Exception as exc:
            self._registar_erro(f"Gráfico '{nome_pagina}' não actualizado: {exc}")

    def atualizar_graficos(self) -> None:
        if not self.bombas:
            for grafico in self.graficos.values():
                grafico.limpar()
            return
        h_sistema = self._H_sistema_fn()
        todos = self._elementos_para_grafico()
        self._plotar_seguro("altura", todos, "H", h_sistema, "Curvas H(Q) — bombas e associações")
        self._plotar_seguro("potencia", todos, "P", h_sistema, "Potência no eixo (W)")
        self._plotar_seguro("rendimento", todos, "eta", titulo="Rendimento (%)")
        self._plotar_seguro("npsh", todos, "npsh_r", titulo="NPSH requerido (m)")

        serie = list(self.bombas)
        paralelo = list(self.bombas)
        if self.associacao_serie is not None:
            serie.append(self.associacao_serie)
        if self.associacao_paralelo is not None:
            paralelo.append(self.associacao_paralelo)
        # Acrescentar também as associações personalizadas nas páginas gerais
        # de série/paralelo apenas quando o seu tipo corresponder.
        for a in self.associacoes.values():
            if a.tipo == "serie" and a is not self.associacao_serie:
                serie.append(a)
            elif a.tipo == "paralelo" and a is not self.associacao_paralelo:
                paralelo.append(a)
        self._plotar_seguro("serie", serie, "H", h_sistema, "Associações em série")
        self._plotar_seguro("paralelo", paralelo, "H", h_sistema, "Associações em paralelo")

    def atualizar_tudo(self) -> None:
        self._reconstruir_associacoes()
        try:
            self.atualizar_resultados()
        except Exception as exc:
            self._registar_erro(f"Falha ao actualizar resultados: {exc}")
        try:
            self.atualizar_graficos()
        except Exception as exc:
            self._registar_erro(f"Falha ao actualizar gráficos: {exc}")

    # ------------------------------------------------------------------
    # Exportação
    # ------------------------------------------------------------------
    def _grafico_visivel(self):
        stack = getattr(self.ui, "stackedWidget_3", None) if self.ui is not None else None
        if stack is None:
            return None
        indice = stack.currentIndex()
        for nome, pagina in self.PAGINAS.items():
            if pagina == indice:
                return self.graficos.get(nome)
        return None

    def exportar_pdf(self) -> None:
        grafico = self._grafico_visivel()
        if grafico is None:
            QMessageBox.information(self.parent_widget, "Exportar", "Nenhum gráfico visível.")
            return
        caminho, _ = QFileDialog.getSaveFileName(self.parent_widget, "Exportar PDF", "grafico.pdf", "PDF (*.pdf)")
        if not caminho:
            return
        try:
            grafico.salvar_pdf(caminho)
            QMessageBox.information(self.parent_widget, "Exportar", f"PDF guardado em:\n{caminho}")
        except Exception as exc:
            QMessageBox.critical(self.parent_widget, "Erro", str(exc))

    def exportar_csv(self) -> None:
        grafico = self._grafico_visivel()
        if grafico is None:
            QMessageBox.information(self.parent_widget, "Exportar", "Nenhum gráfico visível.")
            return
        caminho, _ = QFileDialog.getSaveFileName(self.parent_widget, "Exportar CSV", "grafico.csv", "CSV (*.csv)")
        if not caminho:
            return
        try:
            grafico.exportar_csv(caminho)
            QMessageBox.information(self.parent_widget, "Exportar", f"CSV guardado em:\n{caminho}")
        except Exception as exc:
            QMessageBox.critical(self.parent_widget, "Erro", str(exc))

    # ------------------------------------------------------------------
    # Persistência — mantém compatibilidade com projectos v1.0
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        associacoes = []
        for nome, definicao in self._definicoes_associacoes.items():
            refs = []
            for item in definicao["elementos"]:
                if isinstance(item, Bomba):
                    if item not in self.bombas:
                        continue
                    refs.append({"tipo": "bomba", "indice": self.bombas.index(item)})
                else:
                    refs.append({"tipo": "associacao", "nome": str(item)})
            associacoes.append({"nome": nome, "tipo": definicao["tipo"], "elementos": refs})

        acessorios = getattr(self.perdas, "acessorios_k", {})
        return {
            "versao": "1.1",
            "sistema": {
                "H_geometrico": self.H_geometrico,
                "comprimento_m": self.comprimento_m,
                "material_darcy": self.material_darcy,
                "material_hazen": self.material_hazen,
                "diametro_m": self.perdas.diametro_m,
                "area_m2": self.perdas.area,
                "tempo_funcionamento_h": self.tempo_funcionamento_h,
                "diametro_automatico": self.diametro_automatico,
                "metodo_perdas": self.metodo_perdas,
                "acessorios_k": dict(acessorios),
            },
            "bombas": [b.to_dict() for b in self.bombas],
            "associacoes": associacoes,
        }

    def from_dict(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("O projecto deve ser um objecto JSON.")
        sistema = data.get("sistema", {})
        h_geo = float(sistema.get("H_geometrico", 15.0))
        comprimento = float(sistema.get("comprimento_m", 100.0))
        diametro = float(sistema.get("diametro_m", 0.05))
        tempo = float(sistema.get("tempo_funcionamento_h", 24.0))
        if not np.isfinite(h_geo) or h_geo < 0:
            raise ValueError("Altura geométrica inválida no projecto.")
        if not np.isfinite(comprimento) or comprimento < 0:
            raise ValueError("Comprimento inválido no projecto.")
        if not np.isfinite(diametro) or diametro <= 0:
            raise ValueError("Diâmetro inválido no projecto.")
        if not np.isfinite(tempo) or not 0 < tempo <= 24:
            raise ValueError("Tempo de funcionamento inválido no projecto.")

        bombas = [Bomba.from_dict(item) for item in data.get("bombas", [])]
        definicoes: dict[str, dict[str, Any]] = {}
        for item in data.get("associacoes", []):
            nome = str(item.get("nome", "")).strip()
            tipo = str(item.get("tipo", "")).lower()
            if not nome or tipo not in AssociacaoBombas.TIPOS_VALIDOS:
                raise ValueError("Definição de associação inválida no projecto.")
            referencias = []
            for ref in item.get("elementos", []):
                if ref.get("tipo") == "bomba":
                    indice = int(ref["indice"])
                    if indice < 0 or indice >= len(bombas):
                        raise ValueError(f"Índice de bomba inválido na associação '{nome}'.")
                    referencias.append(bombas[indice])
                elif ref.get("tipo") == "associacao":
                    referencias.append(str(ref["nome"]))
                else:
                    raise ValueError(f"Referência inválida na associação '{nome}'.")
            definicoes[nome] = {"tipo": tipo, "elementos": referencias}

        self.H_geometrico = h_geo
        self.comprimento_m = comprimento
        self.material_darcy = str(sistema.get("material_darcy", "Aço comercial novo"))
        self.material_hazen = str(sistema.get("material_hazen", "Plástico"))
        self.tempo_funcionamento_h = tempo
        self.diametro_automatico = bool(sistema.get("diametro_automatico", False))
        self.metodo_perdas = str(sistema.get("metodo_perdas", "darcy")).lower()
        if self.metodo_perdas not in ("darcy", "hazen"):
            self.metodo_perdas = "darcy"
        self.bombas = bombas
        self._definicoes_associacoes = definicoes
        self._definir_diametro_estado(diametro)
        self._configurar_perdas()

        acessorios = sistema.get("acessorios_k", {})
        if acessorios and hasattr(self.perdas, "definir_acessorios"):
            self.perdas.definir_acessorios(acessorios)
        self._reconstruir_associacoes()

    def salvar_projecto(self) -> None:
        caminho, _ = QFileDialog.getSaveFileName(
            self.parent_widget, "Guardar projecto", "projecto_aquapump.json", "JSON (*.json)"
        )
        if not caminho:
            return
        try:
            Path(caminho).write_text(
                json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            QMessageBox.information(self.parent_widget, "Guardar", f"Projecto guardado em:\n{caminho}")
        except Exception as exc:
            QMessageBox.critical(self.parent_widget, "Erro", str(exc))

    def abrir_projecto(self) -> None:
        caminho, _ = QFileDialog.getOpenFileName(
            self.parent_widget, "Abrir projecto", "", "JSON (*.json)"
        )
        if not caminho:
            return
        try:
            data = json.loads(Path(caminho).read_text(encoding="utf-8"))
            self.from_dict(data)
            self.atualizar_tudo()
            QMessageBox.information(self.parent_widget, "Abrir", f"Projecto carregado ({len(self.bombas)} bombas).")
        except Exception as exc:
            QMessageBox.critical(self.parent_widget, "Erro", str(exc))

    def novo_projecto(self) -> None:
        resposta = QMessageBox.question(
            self.parent_widget,
            "Novo projecto",
            "Limpar o projecto e carregar novamente as bombas de demonstração?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return
        self.H_geometrico = 15.0
        self.comprimento_m = 100.0
        self.material_darcy = "Aço comercial novo"
        self.material_hazen = "Plástico"
        self.metodo_perdas = "darcy"
        self.tempo_funcionamento_h = 24.0
        self.diametro_automatico = True
        d = 0.05
        self.perdas = self._perdas_factory(diametro_m=d, area=math.pi * d**2 / 4.0)
        self._configurar_perdas()
        self._definicoes_associacoes.clear()
        self._carregar_demo()
        self.atualizar_tudo()

    # ------------------------------------------------------------------
    # Diagnóstico
    # ------------------------------------------------------------------
    def info(self) -> str:
        linhas = [
            f"Bombas: {len(self.bombas)}",
            *[f"  - {b}" for b in self.bombas],
            f"Sistema: H_geo={self.H_geometrico:.2f} m | L={self.comprimento_m:.2f} m "
            f"| D={self.perdas.diametro_m * 1000:.1f} mm | método={self.metodo_perdas}",
            f"Diâmetro: {'automático' if self.diametro_automatico else 'manual'}",
        ]
        for nome, associacao in self.associacoes.items():
            linhas.append(f"  - {nome}: {associacao}")
        if self.avisos_associacoes:
            linhas.append("Avisos:")
            linhas.extend(f"  - {aviso}" for aviso in self.avisos_associacoes)
        if self.ultimo_erro:
            linhas.append(f"Último erro: {self.ultimo_erro}")
        return "\n".join(linhas)
