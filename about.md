**AquaPump**


Software de Código aberto de dimensionamento e selecção de bombas hidraulicas centrífugas desenvolvido na linguagem Python usando o PySide6 como biblioteca para interface, assim como foi implementado mapas do LeafLet num arquivo HTML 

**Funcionalidades**

    Entradas de dados -- (Vazão, tempo de funcionamento da bomba, tracado da tubulacao, acessorios de Tubulacao)
    Saidas/Output -- (Potência da bomba; rendimento; perdas de carga, 
    
<img width="765" height="480" alt="image" src="https://github.com/user-attachments/assets/c5b8f34c-5b19-46da-b49a-379c6b3c2772" />

    Figura_1: Esquema de funcionamento do AquaPump

**Interfaces**

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




