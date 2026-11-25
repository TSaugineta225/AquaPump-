"""Modelo hidráulico incremental para o editor de esquemas do AquaPump.

Nesta etapa suporta uma única linha principal em série, composta por um ou
mais troços ligados ponta-a-ponta. Cada troço tem DN, material e comprimento
próprios. Os acessórios são associados ao troço mais próximo pelo editor SVG.

Redes ramificadas, malhadas ou com válvulas fechadas são rejeitadas de forma
explícita: ainda não existe um solver de distribuição de caudais.
"""
from __future__ import annotations

import math
from typing import Any

from calculos.perdas_cargas import Perdas


class ErroModeloHidraulico(ValueError):
    """Erro de validação/topologia do esquema hidráulico."""


class ModeloHidraulico:
    TOLERANCIA_LIGACAO_SVG = 12.0

    # Mapeamentos iniciais entre os materiais simplificados do editor e as
    # categorias disponíveis nas tabelas actuais de Perdas.
    MATERIAIS = {
        "pvc": (
            "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados",
            "Plástico",
        ),
        "pead": (
            "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados",
            "Plástico",
        ),
        "prfv": (
            "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados",
            "Plástico",
        ),
        "aço carbono": ("Aço comercial novo", "Aço soldado novo"),
        "ferro fundido": ("Ferro fundido novo", "Ferro Fundido novo"),
        "betão": ("Concreto com acabamento normal", "Concreto com acabamento comum"),
        "concreto": ("Concreto com acabamento normal", "Concreto com acabamento comum"),
        "cobre": (
            "Cobre, latão, aço revestido de epóxi, PVC, plásticos em geral, tubos extrudados",
            "Cobre",
        ),
    }

    @staticmethod
    def _num(valor: Any, nome: str, minimo: float | None = None) -> float:
        try:
            n = float(valor)
        except (TypeError, ValueError):
            raise ErroModeloHidraulico(f"Valor inválido para {nome}: {valor!r}.")
        if not math.isfinite(n) or (minimo is not None and n < minimo):
            raise ErroModeloHidraulico(f"{nome} deve ser um número finito maior ou igual a {minimo}.")
        return n

    @staticmethod
    def _obter(item: dict, *chaves, default=None):
        for chave in chaves:
            if chave in item and item[chave] is not None:
                return item[chave]
        return default

    @classmethod
    def _node_id(cls, point: tuple[float, float], nodes: list[tuple[float, float]]) -> int:
        x, y = point
        for idx, (nx, ny) in enumerate(nodes):
            if math.hypot(x - nx, y - ny) <= cls.TOLERANCIA_LIGACAO_SVG:
                return idx
        nodes.append((x, y))
        return len(nodes) - 1

    @classmethod
    def ordenar_trocos(cls, pipes: list[dict]) -> list[dict]:
        """Valida e ordena uma única cadeia hidráulica sem ramificações."""
        if not pipes:
            raise ErroModeloHidraulico("O esquema ainda não contém troços de tubulação.")

        nodes: list[tuple[float, float]] = []
        adjacency: dict[int, list[tuple[int, dict]]] = {}
        edge_nodes: dict[str, tuple[int, int]] = {}
        seen_ids: set[str] = set()

        for index, pipe in enumerate(pipes):
            if not isinstance(pipe, dict):
                raise ErroModeloHidraulico(f"Troço na posição {index} não é válido.")
            pipe_id = str(cls._obter(pipe, "id", default=f"troco_{index + 1}"))
            if pipe_id in seen_ids:
                raise ErroModeloHidraulico(f"Identificador de troço duplicado: {pipe_id}.")
            seen_ids.add(pipe_id)

            x1 = cls._num(cls._obter(pipe, "x1"), f"x1 do troço {pipe_id}")
            y1 = cls._num(cls._obter(pipe, "y1"), f"y1 do troço {pipe_id}")
            x2 = cls._num(cls._obter(pipe, "x2"), f"x2 do troço {pipe_id}")
            y2 = cls._num(cls._obter(pipe, "y2"), f"y2 do troço {pipe_id}")
            if math.hypot(x2 - x1, y2 - y1) <= 1e-6:
                raise ErroModeloHidraulico(f"O troço {pipe_id} tem comprimento gráfico nulo.")

            n1 = cls._node_id((x1, y1), nodes)
            n2 = cls._node_id((x2, y2), nodes)
            if n1 == n2:
                raise ErroModeloHidraulico(f"As duas extremidades do troço {pipe_id} coincidem.")
            edge_nodes[pipe_id] = (n1, n2)
            adjacency.setdefault(n1, []).append((n2, pipe))
            adjacency.setdefault(n2, []).append((n1, pipe))

        # Primeiro verificar conectividade, para distinguir troços soltos de
        # uma ramificação dentro da mesma rede.
        first_node = next(iter(adjacency))
        visited_nodes = set()
        stack = [first_node]
        while stack:
            node = stack.pop()
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            stack.extend(neighbour for neighbour, _ in adjacency[node])
        if len(visited_nodes) != len(adjacency):
            raise ErroModeloHidraulico(
                "Existem troços desconectados. Ligue as extremidades para formar uma única conduta."
            )

        if any(len(edges) > 2 for edges in adjacency.values()):
            raise ErroModeloHidraulico(
                "O esquema contém uma ramificação (nó com mais de duas ligações). "
                "Nesta versão só é calculada uma linha principal em série."
            )

        start_nodes = [node for node, edges in adjacency.items() if len(edges) == 1]
        if len(start_nodes) != 2:
            raise ErroModeloHidraulico(
                "A tubulação deve formar uma única linha aberta com duas extremidades. "
                "Circuitos fechados ainda não são suportados."
            )

        ordered: list[dict] = []
        used_ids: set[str] = set()
        current = start_nodes[0]
        previous_id = None
        while True:
            candidates = []
            for neighbour, pipe in adjacency[current]:
                pipe_id = str(cls._obter(pipe, "id", default=""))
                if pipe_id not in used_ids:
                    candidates.append((neighbour, pipe))
            if not candidates:
                break
            if len(candidates) != 1:
                raise ErroModeloHidraulico("Não foi possível ordenar a cadeia de tubulações sem ambiguidade.")
            neighbour, pipe = candidates[0]
            pipe_id = str(cls._obter(pipe, "id", default=""))
            used_ids.add(pipe_id)
            ordered.append(pipe)
            previous_id, current = pipe_id, neighbour

        if len(ordered) != len(pipes):
            raise ErroModeloHidraulico("Nem todos os troços pertencem à mesma linha principal.")
        return ordered


    @classmethod
    def _orientar_cadeia(cls, pipes: list[dict]) -> list[tuple[dict, bool]]:
        """Devolve os troços ordenados com indicação de x1→x2 ou x2→x1."""
        if not pipes:
            return []

        tol = cls.TOLERANCIA_LIGACAO_SVG
        first = pipes[0]
        if len(pipes) == 1:
            return [(first, True)]

        # A extremidade inicial da cadeia é a extremidade do primeiro troço
        # que não coincide com nenhuma extremidade do segundo.
        a1 = (cls._num(first.get("x1"), "x1"), cls._num(first.get("y1"), "y1"))
        a2 = (cls._num(first.get("x2"), "x2"), cls._num(first.get("y2"), "y2"))
        second_ends = [
            (cls._num(pipes[1].get("x1"), "x1"), cls._num(pipes[1].get("y1"), "y1")),
            (cls._num(pipes[1].get("x2"), "x2"), cls._num(pipes[1].get("y2"), "y2")),
        ]
        first_forward = min(math.hypot(a1[0]-p[0], a1[1]-p[1]) for p in second_ends) > tol
        oriented = [(first, first_forward)]
        previous_end = a2 if first_forward else a1

        for pipe in pipes[1:]:
            p1 = (cls._num(pipe.get("x1"), "x1"), cls._num(pipe.get("y1"), "y1"))
            p2 = (cls._num(pipe.get("x2"), "x2"), cls._num(pipe.get("y2"), "y2"))
            d1 = math.hypot(previous_end[0]-p1[0], previous_end[1]-p1[1])
            d2 = math.hypot(previous_end[0]-p2[0], previous_end[1]-p2[1])
            if min(d1, d2) > tol:
                raise ErroModeloHidraulico("Não foi possível orientar os troços para gerar o perfil longitudinal.")
            forward = d1 <= d2
            oriented.append((pipe, forward))
            previous_end = p2 if forward else p1
        return oriented

    @classmethod
    def gerar_perfil_longitudinal(
        cls,
        modelo: dict,
        resultado: dict,
        cota_piezometrica_inicial_m: float,
    ) -> dict:
        """Gera perfil longitudinal integrado com terreno, eixo, HGL/EGL e acessórios.

        O perfil geográfico é recebido do editor após consulta ao modelo digital
        de elevação. A profundidade recebida representa a distância vertical
        entre a superfície do terreno e o eixo da tubagem (não o recobrimento).
        A progressiva geográfica é ajustada proporcionalmente ao comprimento
        hidráulico total quando os dois comprimentos diferem.
        """
        if not isinstance(modelo, dict) or not isinstance(resultado, dict) or not resultado.get("valido"):
            raise ErroModeloHidraulico("Modelo ou resultado hidráulico inválido para gerar o perfil.")

        hgl0 = cls._num(cota_piezometrica_inicial_m, "cota piezométrica inicial")
        pipes = modelo.get("pipes") or modelo.get("tubulacoes") or []
        ordered = cls.ordenar_trocos(pipes)
        oriented = cls._orientar_cadeia(ordered)
        result_by_id = {str(t["id"]): t for t in resultado.get("trocos", [])}
        if len(result_by_id) != len(oriented):
            raise ErroModeloHidraulico("O resultado não contém dados para todos os troços do perfil.")

        components = modelo.get("components") or modelo.get("acessorios") or []
        depth = cls._num(modelo.get("profundidade_eixo_m", 1.2), "profundidade até ao eixo", minimo=0.0)
        geo = modelo.get("perfil_geografico") or []
        if len(geo) < 2:
            raise ErroModeloHidraulico("Obtenha primeiro pelo menos duas cotas do terreno no mapa.")
        geo_points = []
        for i, point in enumerate(geo):
            geo_points.append((
                cls._num(point.get("progressiva_m"), f"progressiva geográfica {i}"),
                cls._num(point.get("terreno_m"), f"cota do terreno {i}"),
            ))
        geo_points.sort(key=lambda item: item[0])
        geo_length = cls._num(modelo.get("comprimento_perfil_geografico_m", geo_points[-1][0]), "comprimento geográfico", minimo=0.001)

        # Construir cadeia hidráulica e eventos de perda localizada por posição.
        segments = []
        total_length = 0.0
        accessory_events = []
        warnings = []
        for pipe, forward in oriented:
            pid = str(cls._obter(pipe, "id"))
            result_pipe = result_by_id[pid]
            length = cls._num(result_pipe.get("comprimento_m"), f"comprimento do troço {pid}", minimo=0.001)
            velocity = cls._num(result_pipe.get("velocidade_ms"), f"velocidade do troço {pid}", minimo=0.0)
            hdist = cls._num(result_pipe.get("perda_distribuida_m"), f"perda distribuída do troço {pid}", minimo=0.0)
            hlocal = cls._num(result_pipe.get("perda_localizada_m"), f"perda localizada do troço {pid}", minimo=0.0)
            segments.append({"id": pid, "start": total_length, "end": total_length + length,
                             "length": length, "velocity": velocity, "hdist": hdist, "hlocal": hlocal})
            fittings = [c for c in components if str(cls._obter(c, "troco_id", "pipe_id", default="")) == pid]
            k_values = [max(0.0, float(cls._obter(c, "coeficiente_k", "k", default=0.0) or 0.0)) for c in fittings]
            k_total = sum(k_values)
            for fitting, kval in zip(fittings, k_values):
                raw_pos = cls._num(cls._obter(fitting, "posicao_m", "position_m", default=0.0), "posição do acessório", minimo=0.0)
                local_pos = min(length, max(0.0, raw_pos))
                if not forward:
                    local_pos = length - local_pos
                share = (kval / k_total) if k_total > 0 else (1.0 / len(fittings) if fittings else 0.0)
                accessory_events.append({"progressiva_m": total_length + local_pos,
                                         "perda_m": hlocal * share,
                                         "nome": cls._obter(fitting, "nome", "tipo", default="Acessório"),
                                         "troco_id": pid})
            if hlocal > 0 and not fittings:
                accessory_events.append({"progressiva_m": total_length + length, "perda_m": hlocal,
                                         "nome": "Perda localizada agregada", "troco_id": pid})
            total_length += length

        scale = total_length / geo_length
        if abs(scale - 1.0) > 0.02:
            warnings.append("O comprimento do traçado geográfico difere mais de 2% do comprimento hidráulico; as cotas foram distribuídas proporcionalmente ao longo da cadeia.")

        def terrain_at(chainage: float) -> float:
            g = chainage / scale
            if g <= geo_points[0][0]: return geo_points[0][1]
            if g >= geo_points[-1][0]: return geo_points[-1][1]
            for (d0, z0), (d1, z1) in zip(geo_points, geo_points[1:]):
                if d0 <= g <= d1:
                    ratio = (g - d0) / max(1e-12, d1 - d0)
                    return z0 + ratio * (z1 - z0)
            return geo_points[-1][1]

        # Fricção distribuída é linear por troço; perdas singulares são aplicadas
        # como saltos na posição de cada acessório.
        event_map: dict[float, list[dict]] = {}
        for event in accessory_events:
            event_map.setdefault(round(event["progressiva_m"], 6), []).append(event)
        chainages = {0.0, total_length}
        for _, (d, _) in enumerate(geo_points): chainages.add(max(0.0, min(total_length, d * scale)))
        for seg in segments: chainages.update((seg["start"], seg["end"]))
        chainages.update(event_map.keys())
        ordered_chainages = sorted(chainages)

        def segment_at(s: float):
            for seg in segments:
                if seg["start"] - 1e-8 <= s <= seg["end"] + 1e-8:
                    return seg
            return segments[-1]

        def distributed_loss_at(s: float) -> float:
            loss = 0.0
            for seg in segments:
                if s >= seg["end"]:
                    loss += seg["hdist"]
                elif s > seg["start"]:
                    loss += seg["hdist"] * ((s - seg["start"]) / seg["length"])
                    break
                else:
                    break
            return loss

        event_loss_before = 0.0
        points = []
        for chainage in ordered_chainages:
            seg = segment_at(chainage)
            terrain = terrain_at(chainage)
            pipe_axis = terrain - depth
            velocity_head = seg["velocity"] ** 2 / (2.0 * 9.80665)
            egl_before = hgl0 + (segments[0]["velocity"] ** 2 / (2.0 * 9.80665)) - distributed_loss_at(chainage) - event_loss_before
            hgl_before = egl_before - velocity_head
            points.append({"progressiva_m": chainage, "troco_id": seg["id"],
                           "cota_terreno_m": terrain, "cota_conduta_m": pipe_axis,
                           "hgl_m": hgl_before, "egl_m": egl_before,
                           "pressao_estatica_m": hgl_before - pipe_axis,
                           "velocidade_ms": seg["velocity"], "evento": "antes_acessorio" if round(chainage, 6) in event_map else None})
            events_here = event_map.get(round(chainage, 6), [])
            for event in events_here:
                event_loss_before += event["perda_m"]
                egl_after = egl_before - event_loss_before
                hgl_after = egl_after - velocity_head
                points.append({"progressiva_m": chainage, "troco_id": seg["id"],
                               "cota_terreno_m": terrain, "cota_conduta_m": pipe_axis,
                               "hgl_m": hgl_after, "egl_m": egl_after,
                               "pressao_estatica_m": hgl_after - pipe_axis,
                               "velocidade_ms": seg["velocity"], "evento": "perda_localizada",
                               "acessorio": event["nome"], "perda_localizada_m": event["perda_m"]})

        return {
            "valido": True,
            "unidades": {"distancia": "m", "cota": "m", "carga": "m", "pressao": "m.c.a."},
            "cota_piezometrica_inicial_m": hgl0,
            "comprimento_total_m": total_length,
            "profundidade_eixo_m": depth,
            "pontos": points,
            "acessorios": accessory_events,
            "avisos": list(dict.fromkeys(warnings + [
                "As cotas do terreno provêm de um modelo digital de elevação e não substituem levantamento topográfico.",
                "A profundidade introduzida é medida até ao eixo da tubagem; não é o recobrimento até à geratriz superior.",
                "A cota piezométrica inicial é uma condição de fronteira fornecida pelo utilizador; confirme o nível de água, bomba e sentido do escoamento.",
            ])),
        }

    @classmethod
    def calcular(
        cls,
        modelo: dict,
        vazao_m3s: float,
        metodo: str = "darcy",
        material_darcy_padrao: str | None = None,
        material_hazen_padrao: str | None = None,
    ) -> dict:
        """Calcula perdas por troço e totaliza a linha principal em série."""
        if not isinstance(modelo, dict):
            raise ErroModeloHidraulico("O modelo recebido do editor não é um objecto válido.")
        q = cls._num(vazao_m3s, "caudal", minimo=0.0)
        if q <= 0:
            raise ErroModeloHidraulico("Introduza um caudal positivo antes de calcular o esquema.")

        pipes = modelo.get("pipes") or modelo.get("tubulacoes") or []
        components = modelo.get("components") or modelo.get("acessorios") or []
        if not isinstance(pipes, list) or not isinstance(components, list):
            raise ErroModeloHidraulico("A lista de tubulações ou acessórios tem formato inválido.")
        ordered_pipes = cls.ordenar_trocos(pipes)

        pipes_by_id = {str(cls._obter(p, "id")): p for p in ordered_pipes}
        grouped: dict[str, list[dict]] = {pipe_id: [] for pipe_id in pipes_by_id}
        for index, component in enumerate(components):
            if not isinstance(component, dict):
                raise ErroModeloHidraulico(f"Acessório na posição {index} não é válido.")
            pipe_id = cls._obter(component, "troco_id", "pipe_id")
            if not pipe_id or str(pipe_id) not in pipes_by_id:
                label = cls._obter(component, "nome", "tipo", default=f"acessório {index + 1}")
                raise ErroModeloHidraulico(
                    f"{label}: coloque o acessório sobre uma tubulação para o associar a um troço."
                )
            grouped[str(pipe_id)].append(component)

        metodo_norm = str(metodo or "darcy").strip().lower()
        if metodo_norm not in {"darcy", "hazen", "hazen-williams", "hazen_williams"}:
            raise ErroModeloHidraulico(f"Método de perda não suportado: {metodo!r}.")
        usar_darcy = metodo_norm == "darcy"

        resultados_trocos = []
        total_distribuida = 0.0
        total_localizada = 0.0
        total_comprimento = 0.0
        avisos: list[str] = []

        for pipe in ordered_pipes:
            pipe_id = str(cls._obter(pipe, "id"))
            dn_mm = cls._num(
                cls._obter(pipe, "diametro_interno_mm", "diametro_dn", "dn"),
                f"DN do troço {pipe_id}", minimo=0.001,
            )
            diameter_m = dn_mm / 1000.0
            length_m = cls._num(
                cls._obter(pipe, "comprimento_m", "lengthM", "length_m"),
                f"comprimento do troço {pipe_id}", minimo=0.001,
            )
            material = str(cls._obter(pipe, "material", default="PVC")).strip()
            material_key = material.casefold()
            if material_key not in cls.MATERIAIS:
                raise ErroModeloHidraulico(
                    f"Material '{material}' do troço {pipe_id} ainda não tem correspondência na base de cálculo."
                )
            darcy_material, hazen_material = cls.MATERIAIS[material_key]
            if material_key in {"aço carbono", "ferro fundido", "betão", "concreto", "prfv"}:
                avisos.append(
                    f"Troço {pipe_id}: '{material}' foi associado a uma categoria de referência. "
                    "Confirme a rugosidade/coeficiente C e o estado real da tubulação."
                )

            area = math.pi * diameter_m**2 / 4.0
            engine = Perdas(
                vazao_m3s=q,
                diametro_m=diameter_m,
                area=area,
                material_darcy=darcy_material if usar_darcy else material_darcy_padrao,
                material_hazen=hazen_material if not usar_darcy else material_hazen_padrao,
            )
            fittings = []
            for fitting in grouped[pipe_id]:
                fitting_data = dict(fitting)
                canonical = Perdas._resolver_acessorio(
                    cls._obter(fitting_data, "tipo", "type", default="")
                ) or ""
                # O estado aberto/fechado só altera a disponibilidade de
                # válvulas e órgãos de controlo; um cotovelo não é uma válvula.
                is_valve = (
                    canonical.startswith("Válvula")
                    or canonical in {"Comporta Aberta", "Controlador de Vazão"}
                )
                if not is_valve:
                    fitting_data["estado"] = "normalmente aberto"
                fittings.append(fitting_data)
            engine.definir_acessorios_lista(fittings)
            if not engine.configuracao_acessorios_valida:
                detalhes = "; ".join(engine.obter_avisos_acessorios())
                raise ErroModeloHidraulico(
                    f"O troço {pipe_id} contém uma válvula fechada ou configuração inválida. {detalhes}"
                )

            if usar_darcy:
                h_distribuida = engine.calcular_perda_carga_darcy(length_m)
            else:
                h_distribuida = engine.calcular_perda_carga_hazen_williams(length_m)
            h_localizada = engine.calcular_perdas_localizadas()
            avisos.extend(engine.obter_avisos_acessorios())

            resultados_trocos.append({
                "id": pipe_id,
                "comprimento_m": length_m,
                "diametro_nominal_mm": dn_mm,
                "diametro_interno_assumido_mm": dn_mm,
                "material": material,
                "caudal_m3s": q,
                "velocidade_ms": engine.calcular_velocidade(),
                "perda_distribuida_m": h_distribuida,
                "perda_localizada_m": h_localizada,
                "perda_total_m": h_distribuida + h_localizada,
                "numero_acessorios": len(fittings),
            })
            total_distribuida += h_distribuida
            total_localizada += h_localizada
            total_comprimento += length_m

        return {
            "valido": True,
            "tipo_rede": "linha_principal_em_serie",
            "metodo": "darcy" if usar_darcy else "hazen-williams",
            "caudal_m3s": q,
            "comprimento_total_m": total_comprimento,
            "perdas_distribuidas_m": total_distribuida,
            "perdas_localizadas_m": total_localizada,
            "perdas_totais_m": total_distribuida + total_localizada,
            "trocos": resultados_trocos,
            "avisos": list(dict.fromkeys(avisos)),
            "nota": (
                "O DN foi usado como aproximação do diâmetro interno. Para maior precisão, "
                "introduza o diâmetro interno real. O modelo desta etapa só resolve uma linha em série."
            ),
        }
