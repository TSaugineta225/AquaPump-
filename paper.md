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
    orcid: 0009-0007-4292-7508
    corresponding: true
    affiliation: 1
affiliations:
  - name: Divisão de Agricultura, Instituto Superior Politécnico de Gaza, Moçambique
    index: 1
date: 27 November 2025
bibliography: paper.bib
---

# Summary

The sizing and selection of hydraulic pumps are critical processes in engineering that directly impact the energy efficiency and operational costs of pumping systems. However, the complexity of manual calculations and the dependence on manufacturer-specific software, which limits options to their own product lines, represent significant obstacles to optimized and independent selection.

`AquaPump` is an open-source Python software designed to optimize the sizing and selection of centrifugal pumps. It performs precise hydraulic sizing (calculating manometric head, pipe diameter, and power requirements) and assists in the efficient choice of equipment from multiple manufacturers by consulting a local, updatable database. The software automates the calculation of distributed and localized head losses, graphically simulates the system and pump characteristic curves, and suggests the most suitable equipment based on the operating point.

# Statement of need

Accurately sizing hydraulic pumps for irrigation and water supply systems is a complex, repetitive, and time-consuming task [@ferreira:2022; @vernillo:2024]. Existing commercial solutions, such as `KSB EasySelect` [@ksb:2025] and `Wilo-Select 5` [@wilo:2025], are robust but inherently limited, as they exclusively recommend equipment from their own catalogs. This restricts engineers from performing a truly independent, comparative, and cost-effective analysis.

Manual calculations using Excel or tools like Scilab [@torres:2022] are viable but require significant time and expertise, taking upwards of 30 minutes per scenario. `AquaPump` addresses this gap by providing a dedicated, interactive, and independent tool. It reduces the sizing process from approximately 30 minutes to under 2 minutes, with less than 1% variation compared to manual calculation methods. Its integrated map interface (via Leaflet.js) allows for the visual tracing of pipelines to automatically obtain topographic profiles and distances, bridging the gap between geospatial data and hydraulic design.

# State of the field

The primary tools in the industry for pump selection are the proprietary catalogs of manufacturers like KSB and Wilo. While highly accurate for their specific machines, they do not support cross-manufacturer comparisons. Generic academic tools exist (e.g., Scilab scripts, Excel spreadsheets), but they often lack a user-friendly interface and integrated databases.

`AquaPump` is not the only open-source tool for hydraulic calculations (e.g., `EPANET` for network analysis), but it fills a specific niche by focusing exclusively on the pump selection process with a direct link to a local market database. It was built from the ground up to provide a modern GUI (via PySide6), interactive geospatial mapping, and multi-manufacturer recommendation logic, features not commonly found in existing open-source alternatives for this specific application.

# Software design

`AquaPump` is built with a modular architecture to separate the calculation logic from the user interface:

1.  **Calculation Engine (`perdas_cargas.py`, `dimensionamento_tubulação.py`):** Implements the Darcy-Weisbach equation with the Churchill friction factor model and the Hazen-Williams formula for distributed head losses, alongside localized loss calculations. It leverages `CoolProp` for fluid properties and `NumPy`/`SciPy` for efficient numerical computation.
2.  **Geospatial Module (`index.html`, `web_channel.py`):** Integrates a Leaflet.js map through a `QWebEngineView`. Communication between Python and JavaScript is handled via `QWebChannel`, allowing the software to capture user-drawn polylines, calculate distances, and fetch elevation data via the Open-Elevation API to determine the geometric head.
3.  **Recommendation System (`gestor_database.py`):** Consults a local SQLite database containing specifications of 21 commercially available pump models in Mozambique. The selection algorithm uses a scoring function based on flow rate and head, with progressive tolerance bands to find the most efficient match.
4.  **User Interface and Reporting (`main.py`, `pdf_gen.py`, `csv_gen.py`):** The GUI is built with `PySide6` and styled with QSS. The software can export technical reports in both PDF (via `ReportLab`) and XLSX (via `pandas`/`openpyxl`), featuring embedded tables and dynamic graphs of the pump curves (H-Q, P-Q, η-Q) generated with `Matplotlib`.

# Research impact statement

The `AquaPump` prototype has demonstrated its effectiveness in a case study for an irrigation system. The time to perform a complete sizing was reduced from over 30 minutes to approximately 2 minutes, with a numerical accuracy within 1% of values calculated in Microsoft Excel. Its application is not only in research but also in professional practice, particularly in contexts like Mozambique, where access to a wide range of suppliers is critical. By integrating a local database of pumps, `AquaPump` transforms from a purely theoretical tool into a practical decision-making aid for engineers in the field.

# Mathematics

Single dollars ($) are required for inline mathematics, e.g., the manometric head $H_m$ is the sum of the geometric head $H_g$ and the total head loss $\Delta h$.

The core of the hydraulic calculation is the dimensionless friction factor $f$ from the Colebrook-White equation or the explicit Churchill equation:
\begin{equation}\label{eq:churchill}
f = 8 \left[ \left( \frac{8}{Re} \right)^{12} + \frac{1}{(A + B)^{1.5}} \right]^{1/12}
\end{equation}
where $Re$ is the Reynolds number and $A$ and $B$ are functions of $Re$ and the relative roughness $\varepsilon/D$ [@baptista:2014]. The total manometric head is then calculated as $H_m = H_g + \Delta h_{distributed} + \Delta h_{localized}$.

# Figures

![The AquaPump graphical user interface showing the integrated map, input fields, real-time calculation results, and dynamically generated pump curves.\label{fig:interface}](figure.png)

# AI usage disclosure

No generative AI tools were used in the development of this software, the writing of this manuscript, or the preparation of supporting materials.

# Acknowledgements

We acknowledge the contributions and supervision of Dr. Eng. Lateiro Salvador de Sousa and M. Eng. Nélia Dalúvia Rafael during the genesis of this project at the Instituto Superior Politécnico de Gaza.

# References