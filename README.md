Treliça Dinâmica — Ferramenta de Análise Dinâmica de Treliças 2D

Este projeto apresenta uma ferramenta desenvolvida em Python para realizar a análise dinâmica de treliças planas por meio do Método dos Elementos Finitos (MEF).
A aplicação permite estudar o comportamento de estruturas sob carregamentos dependentes do tempo utilizando diferentes métodos de integração temporal e uma interface gráfica intuitiva construída com Tkinter.

🧩 Funcionalidades principais
- Montagem automática das matrizes globais de rigidez (K), massa (M) e amortecimento (C).
- Cálculo das frequências naturais e modos de vibração.
- Execução da análise dinâmica utilizando três métodos:
  - Método de Newmark;
  - Método das Diferenças Centrais;
  - Método de explícito de Bathe.
- Escolha de diferentes funções temporais de carregamento: constante, rampa ou harmônica.
- Visualização gráfica e numérica dos resultados (deslocamento, velocidade e aceleração) em cada nó.
- Exibição das matrizes e das frequências naturais calculadas.

🖥️ Execução do programa
A ferramenta pode ser executada de duas maneiras:

1️⃣ Via arquivo executável (.exe)
Baixe o arquivo TreliçaDinâmica.exe disponível na página do repositório e execute-o diretamente.
Não é necessário ter o Python instalado.

2️⃣ Via código-fonte em Python
Certifique-se de ter o Python 3.9+ instalado.
1. Instale as dependências:
  - pip install numpy matplotlib
2. Execute o arquivo principal:
  - python interface.py

⚙️ Estrutura do repositório
📦 TrelicaDinamica
├── interface.py              # Interface gráfica principal (entrada de dados e controle)
├── janela_resultados.py      # Visualização e exportação dos resultados
├── gerar_matrizes.py         # Montagem das matrizes de rigidez, massa e amortecimento
├── newmark.py                # Implementação do método de Newmark
├── bathe.py                  # Implementação do método de Bathe
├── diferencascentrais.py     # Implementação do método das Diferenças Centrais
├── TrelicaDinamica.exe       # Versão executável da ferramenta
└── README.md                 # Este arquivo

🧠 Instruções gerais de uso
1. Defina as propriedades da estrutura:
2. Número de materiais, nós, elementos, apoios e nós com carga.
  - Insira coordenadas, incidência, materiais, cargas e apoios nas janelas correspondentes.
3. Escolha o método de integração temporal e a função temporal do carregamento.
4. Defina o intervalo de tempo (Δt) e o tempo total de simulação.
5. Execute a análise clicando em “Executar”.
  - Serão exibidas as janelas de resultados, gráficos e matrizes.

⚠️ Cuidados necessários
- O usuário tem liberdade para numerar os nós a partir de 0 ou de 1 (a ferramenta ajusta automaticamente os índices).
- O separador decimal deve ser o ponto (.) e não a vírgula.
- As propriedades de entrada devem estar em unidades coerentes do Sistema Internacional (SI):
  - Área (A): m²
  - Módulo de Elasticidade (E): N/m²
  - Densidade (ρ): kg/m³
  - Força (F): N
  - Tempo (t): s
  
🧾 Licença
Este projeto está sob a licença MIT.
Você é livre para utilizar, modificar e distribuir o código, desde que mantenha os créditos ao autor original.

👩‍💻 Autoria
Júlia Tschá Longo,
Trabalho de Conclusão de Curso — Bacharelado em Engenharia Civil,
Universidade Federal do Paraná
