---
title: 'AquaPump: A Python package for centrifugal pump sizing and selection'
tags:
  - Python
  - hydraulic-engineering
  - centrifugal-pumps
  - pump-sizing
  - water-supply
  - irrigation
authors:
  - name: Tenerife Saugineta
    corresponding: true
    orcid: 0009-0000-3033-8908
    affiliation: 1
affiliations:
  - name: Divisão de Agricultura, Instituto Superior Politécnico de Gaza, Moçambique
    index: 1
date: 27 November 2025
doi: 10.5281/zenodo.19712947
url: https://github.com/TSaugineta225/AquaPump-.git
bibliography: paper.bib
---

# Summary

The sizing and selection of hydraulic pumps are critical processes that directly impact the energy efficiency and operational costs of pumping systems. However, the complexity of manual calculations and the dependence on manufacturer-specific software, which restricts recommendations to a single product line, represent significant obstacles to optimized and independent selection.

`AquaPump` is an open-source Python software designed to optimize the sizing and selection of centrifugal pumps. It performs precise hydraulic sizing—calculating manometric head, pipe diameter, and power requirements—and assists in the efficient choice of equipment from multiple manufacturers through a local, updatable database. The software automates the computation of distributed and localized head losses, simulates system and pump characteristic curves, and suggests the most suitable pump based on the operating point. An integrated map interface allows users to trace pipelines, automatically extracting topographic profiles and distances.

# Statement of need

Accurately sizing hydraulic pumps for irrigation, water supply, and industrial systems is a repetitive and error-prone task when performed manually [@ferreira:2022; @vernillo:2024]. Existing commercial solutions, such as `KSB EasySelect` [@ksb:2025] and `Wilo-Select 5` [@wilo:2025], are robust but inherently limited to the manufacturer's own catalog. This forces engineers who need cross-brand comparisons to rely on generic tools like Excel spreadsheets or scripts, a process that can take over 30 minutes per scenario and demands specialized expertise [@torres:2022].

`AquaPump` addresses this gap by providing a dedicated, interactive tool that reduces the full sizing process to approximately two minutes, with less than 1% variation compared to manual calculations. Its integrated Leaflet‑based map, combined with elevation APIs, bridges the gap between geospatial data and hydraulic design—a feature not available in conventional pump selection software. By bundling a database of commercially available pumps in Mozambique, the software transforms into a practical, ready‑to‑use decision‑making aid for local engineers.

# State of the field

The primary tools for pump selection are the proprietary catalogs of manufacturers such as KSB and Wilo. While highly accurate for their specific equipment, they do not allow cross‑manufacturer comparisons. In academic and field practice, engineers often rely on spreadsheets or scientific calculators, which are flexible but lack integration, automation, and visual feedback. Open‑source hydraulic packages like `EPANET` focus on network analysis rather than the pump selection workflow, and scripting environments like `Scilab` [@scarabellot:2018] require significant user effort to match the level of interactivity and graphical output.

`AquaPump` fills a specific niche by targeting the pump selection process exclusively. It provides a modern graphical interface, a manufacturer‑independent recommendation system, and an integrated mapping module—all features absent from the current open‑source alternatives for this specific application.

# Software design

`AquaPump` follows a modular architecture that separates the hydraulic calculation engine from the user interface:

1. **Hydraulic engine** (`perdas_cargas.py`, `dimensionamento_tubulação.py`): Implements the Darcy‑Weisbach equation with the Churchill friction factor and the Hazen‑Williams formula for distributed losses, as well as localized head losses via K‑factors. Fluid properties are obtained from `CoolProp`, and numerical operations rely on `NumPy` and `SciPy`.

2. **Geospatial module** (`index.html`, `web_channel.py`): Embeds a Leaflet map inside a `QWebEngineView`. Bidirectional communication via `QWebChannel` enables the capture of user‑drawn polylines, distance calculations, and elevation queries using the Open‑Elevation API, which directly feed the geometric head into the hydraulic computation.

3. **Recommendation system** (`gestor_database.py`): A local SQLite database stores technical specifications of 21 commercially available pump models. The selection algorithm scores candidates using flow rate and head, applying progressive tolerance bands to identify the most efficient match.

4. **User interface and reporting** (`main.py`, `pdf_gen.py`, `csv_gen.py`): Built with `PySide6` and styled with QSS. The interface features real‑time updates of calculated values and dynamically generated pump curves (H–Q, P–Q, η–Q) using `Matplotlib`. Reports are exported as PDF (via `ReportLab`) or XLSX (via `pandas`/`openpyxl`), including tables, graphs, and metadata.

# Research impact statement

The effectiveness of `AquaPump` was validated through a case study simulating an irrigation system. The software achieved a deviation of less than 1% relative to the same calculations performed in Microsoft Excel, while reducing the total sizing time from over 30 minutes to roughly 2 minutes. Beyond speed and accuracy, the tool has practical relevance in Mozambique, where the integrated local pump database enables engineers to make informed choices without being limited to a single supplier. This combination of validated correctness, time efficiency, and local applicability makes `AquaPump` a valuable asset for both educational and professional use.

# Mathematics

The hydraulic calculations rely on the Darcy‑Weisbach equation for distributed head loss, using the Churchill explicit formulation for the friction factor $f$ [@baptista:2014]:

\begin{equation}
f = 8 \left[ \left( \frac{8}{Re} \right)^{12} + \frac{1}{(A + B)^{1.5}} \right]^{1/12}
\label{eq:churchill}
\end{equation}

where $A = \left[ 2.457 \ln \left( \left( \frac{7}{Re} \right)^{0.9} + 0.27 \frac{\varepsilon}{D} \right) \right]^{16}$,
$B = \left( \frac{37530}{Re} \right)^{16}$,
$Re$ is the Reynolds number, and $\varepsilon/D$ the relative roughness.

The total manometric head $H_m$ is then obtained by summing the geometric head $H_g$ and all head losses:

\begin{equation}
H_m = H_g + \Delta h_{\text{distributed}} + \Delta h_{\text{localized}}
\label{eq:manometric}
\end{equation}

The Hazen‑Williams formula is used as an alternative for certain pipe materials:

\begin{equation}
\Delta H = 10.675 \, L \, D^{-4.87} \left( \frac{Q}{C} \right)^{1.852}
\label{eq:hazen}
\end{equation}

where $C$ is the pipe coefficient and $Q$ the flow rate.

# AI usage disclosure

During the development of this software and the preparation of this manuscript, AI-based tools were used solely for the following purposes:
- Review of code for bug detection and correction.

All AI-generated suggestions were critically evaluated by the author to ensure correctness and alignment with the project's objectives. No content was generated autonomously; final decisions and implementations were always made by the human author.

# Acknowledgements

We acknowledge the contributions and supervision of Dr. Eng. Lateiro Salvador de Sousa and M. Eng. Nélia Dalúvia Rafael during the genesis of this project at the Instituto Superior Politécnico de Gaza.

