## AquaPump

### 1. Visão geral

AquaPump é um software de código aberto para o dimensionamento e selecção
de bombas hidráulicas centrífugas, desenvolvido em Python.
A ferramenta integra cálculos hidráulicos e visualização geoespacial
para apoiar decisões técnicas em sistemas de abastecimento de água e irrigação.


### 2. Funcionalidades

- Dimensionamento hidráulico de sistemas de bombeamento
- Cálculo da altura manométrica total
- Estimativa de perdas de carga na tubulação(distribuidas e localizadas)
- Visualização de traçados hidráulicos em mapa(Com Leaflet)
- Geração de curvas do sistema e da bomba
- Apoio à selecção de bombas centrífugas


    Entradas de dados -- (Vazão, tempo de funcionamento da bomba, tracado da tubulacao, acessorios de Tubulacao)
    Saidas/Output -- (Potência da bomba; rendimento; perdas de carga) 
    
<img width="765" height="480" alt="image" src="https://github.com/user-attachments/assets/c5b8f34c-5b19-46da-b49a-379c6b3c2772" />

    Figura_1: Esquema de funcionamento do AquaPump

### 3. Interfaces do Utilizador

 *Janela Principal*
 
 <img width="886" height="472" alt="image" src="https://github.com/user-attachments/assets/09b81201-23c5-4c8e-854d-8db7400bd88e" />
   
    Figura_2: Janela Principal do AquaPump
 
 **1.	Menus superiores (da esquerda à direita):**
   
    •	Menu “Arquivo” – Contém opções relacionadas à gestão de ficheiros, como criar novo projeto, abrir, salvar e fechar o programa;
    •	Menu “Editar” – Disponibiliza ferramentas para acessar as configurações do programa;
    •	Menu “Relatório” – Permite gerar relatórios técnicos com base nos dados inseridos ou resultados obtidos no projecto;
    •	Menu “Ajuda” – Fornece acesso à documentação do software, informações sobre a aplicação e instruções de utilização.

**2.	Campo de selecção de material** – Caixa de selecção onde o utilizador pode escolher o tipo de material, como “Aço Corrugado (chapa ondulada)”;

**3.	Campo de entrada de vazão** – Campo numérico para a inserção da vazão de projecto do sistema, com unidades especificadas (ex: L/s);

**4.	Campo de Selecção da unidade de vazão:** Uma caixa de seleção (dropdown) que permite ao utilizador escolher a unidade da vazão;

**5.	Campo de entrada de tempo** – Espaço para introduzir o tempo em horas, possivelmente;

**6.	Botão de visualização** – Alterna entre diferentes modos de visualização do mapa, como mapa base, satélite ou terreno;

**7.	Botões do Menu Lateral (descritos de forma ascendente)**

       •	Botão para expandir a janela lateral;
       •	Botão para pesquisar o local de dimensionamento;
       •	Botão para abrir o menu “Arquivos” presente na janela lateral;
       •	Botão para acessar área das exportações de relatórios (ex:pdf);
       •	Botão para acessar janela de Selecção de Bombas;
       •	Botão para acessar área de gráficos e de resumo de cálculos.

**8.	Botões de zoom (+ / -)** – Controlam o nível de ampliação do mapa, permitindo aproximar ou afastar a visualização.*

**9.	Ferramenta de desenho**

      •	Polilinha- para definir o traçado do sistema hidráulico directamente no mapa;
      •	Círculo – para definir os acessórios presentes no sistema;

**10.	Ferramentas de Manipulação**

      •	Ferramenta de edição – Utilizada para ajustar ou mover objetos previamente desenhados.
      •	Ferramenta de eliminação – Remove elementos desenhados de forma indesejada do mapa.

**11.	Botões de Controle**

      •	Botão de acesso às configurações gerais da aplicação;
      •	Botão para sair do programa.



*Janela de Configurações*
<img width="886" height="473" alt="image" src="https://github.com/user-attachments/assets/c689eb6e-785a-4878-94e9-e819cd37a156" />

    Figura_3: Janela das Configurações do AquaPump

**1.	Padrão de Unidades Preferencial** – Secção destinada à seleção do sistema de unidades a ser utilizado em todo o projeto. O utilizador pode escolher entre:

       •	Sistema Internacional (SI / Métrico) – usa unidades como metros (m), litros por segundo (L/s), etc.
       •	Sistema Imperial (EUA) – usa unidades como pés (ft), polegadas (in), galões por minuto (GPM), etc.
       •	Personalizado – permite configurar unidades específicas para cada parâmetro.
   
**2.	Ajuste individual de unidades por parâmetro** – Área que possibilita a configuração manual das unidades de medida para cada variável técnica.

**3.	Botão “Voltar”** – Retorna à página ou menu anterior sem guardar as alterações feitas nas definições.

**4.	Botão “Cancelar”** – Descarta todas as alterações realizadas, mantendo as configurações anteriores.

**5.	Botão “Aplicar”** – Guarda e implementa as alterações de unidades ou preferências definidas pelo utilizador.

### 4. Requisitos do Sistema

#### Sistema Operacional
- Windows 10 ou Windows 11 (64 bits)

#### Processador, Memória e Gráficos

**Mínimo:**
- Processador: Dual-core 64 bits  
  - Intel Core i3 (1ª–3ª geração)  
  - AMD Athlon / A6
- Memória: 4 GB RAM
- Gráficos: suporte a OpenGL 2.0

**Recomendado:**
- Processador: Quad-core  
  - Intel Core i5 / Ryzen 5 ou superior
- Arquitetura: 64 bits
- Memória: 8 GB RAM ou mais
- Gráficos:
  - Intel HD Graphics 4000 ou superior  
  - Qualquer GPU dedicada (NVIDIA / AMD)
 
### 5. Instalação

    git clone https://github.com/TSaugineta225/AquaPump-.git
    cd AquaPump
    pip install -r requirements.txt
    python main.py

### 6. Utilização básica
> Como usar em 5 passos.

1. Definir os parâmetros hidráulicos do sistema
2. Traçar a tubulação no mapa
3. Seleccionar materiais e acessórios
4. Executar os cálculos hidráulicos
5. Analisar os resultados e a recomendação da bomba

### 7. Tecnologias utilizadas

    Python 3.13
    PySide6
    Qt WebEngine
    Leaflet.js
    NumPy
    SciPy
    Matplotlib
    GeoPy
    ReportLab
    coolprop


### 8. Estrutura do Projecto
    
    AquaPump/
    │
    ├── src/             
    │    ├── __init__.py
    ├── gui/         
    ├── calculos/   
    ├── data/         
    ├── img/            
    ├── main.py
    ├── requirements.txt   
    ├── LICENSE            
    ├── README.md          



### 9. Limitações Actuais
1.    A base de dados, embora funcional, é um protótipo e necessita de um processo de atualização contínuo para se manter relevante;
  
3.    O software na sua versão 1.0 foca-se em bombas centrífugas únicas, não abordando cenários mais complexos como a associação de bombas ou a análise de redes de distribuição, que representam um caminho claro para trabalhos futuros;
  
5.    Adicionalmente, fenómenos transientes como o golpe de aríete não foram modelados e constituem uma área de expansão de alta complexidade e valor para futuras versões do software.

### 10. Estado do projecto e roadmap

- Versão actual: 1.0.0
- Estável para uso académico
- Futuras versões: associação de bombas, análise de redes, fenómenos transientes

### 11. Licença

Este projecto é distribuído sob a licença MIT.


