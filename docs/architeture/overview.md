# Software Architecture Overview
## Objective
- Create documents from independent components.

## Secondary objectives
- Facilitate the creation of highly standardized documents using components
- Enable document reproducibility through parameter adjustment
- Enable the management of information and data contained within a document

## Features
### Describe the overview of the main workflow of generating files
O fluxo é dividido em 4 etapas bem definidas:
**Descoberta (Discovery)**: O motor lê o arquivo "receita" (Manifesto JSON), acessa cada componente Markdown listado e extrai todos os metadados e variáveis de preenchimento ({{ campos }}).
**Injeção de Dados (Data Ingestion)**: O sistema consolida as variáveis sem duplicidade e gera um formulário (CLI agora, Flutter no futuro) para o usuário preencher os valores.
**Processamento (Render)**: O motor injeta os dados nos componentes de texto (via Jinja2) e gera arquivos Markdown temporários já preenchidos.
**Compilação (Compilation)**: O motor concatena os arquivos temporários seguindo a ordem da receita e aciona o Pandoc para converter o arquivo final no formato desejado (.docx, .pdf), aplicando a folha de estilo escolhida.

### How will elements as diagrams, equations and images be supported and added to the document?
Eles serão tratados nativamente pelo formato Markdown e convertidos na fase de compilação:
**Equações**: Escritas em sintaxe padrão LaTeX (ex: $$ E = mc^2 $$). O compilador final renderiza essas fórmulas perfeitamente no Word ou PDF.
**Diagramas**: Escritos em blocos de código Mermaid (sintaxe baseada em texto). Durante a compilação, uma extensão do Pandoc (ou uma biblioteca auxiliar) converte o código de texto do diagrama em uma imagem vetorial estática inserida diretamente no documento final.
**Imagens**: Inseridas via links de referência relativos padrões do Markdown (![Legenda](caminho/foto.jpg)).
**Tabelas**:

### How would the components be organized for compousing the final document?
A organização é hierárquica e desacoplada:
**Os Componentes (Blocos):** São arquivos independentes de Markdown (.md) salvos em uma estrutura de pastas categorizada (ex: /introducoes, /especificacoes, /tabelas). Cada bloco foca em apenas um assunto técnico.
**O Orquestrador (Manifesto):** Um arquivo JSON/YAML independente que funciona como a "lista de compras". Ele não contém texto, apenas os caminhos dos blocos na ordem exata em que devem aparecer no documento final e o arquivo de estilo que deve ser aplicado.

### How would other files format be accepted?
Arquivos em formatos externos (como uma capa em .docx ou um anexo em .pdf) são tratados como **Blocos Estáticos**. O motor Python não tentará ler ou substituir variáveis dentro deles. Em vez disso, ele reserva a posição desse arquivo na fila de montagem e usa bibliotecas utilitárias de manipulação de arquivos (como **python-docx para mesclar arquivos Word ou pypdf para PDFs**) para fundir fisicamente esses documentos ao restante do relatório gerado na fase de compilação.

### What file types are accepted?
**Entradas de Conteúdo:** 
- *.md (Markdown para os componentes dinâmicos), 
- *.docx (Word para capas ou seções externas do usuário)
- *.pdf (para relatórios ou plantas externas).
**Entradas de Configuração:** .json ou .yaml (para os manifestos e dados de preenchimento).

**Entradas de Design:**
- *.docx (como arquivo de referência de estilo para o Pandoc)
- *.css/.tex (para saídas HTML/PDF).

**Saídas do Sistema:** .docx, .pdf e .md.

### How will the technical report fields be defined?
Eles são definidos de duas formas combinadas:
**Implicitamente**: Pela mera presença de marcadores de texto (`{{ nome_campo }}`) espalhados pelo corpo do texto do componente Markdown.

**Explicitamente (Metadados)**: Através de um cabeçalho YAML Front Matter no topo de cada arquivo Markdown. Esse cabeçalho serve para tipar o dado (ex: definir se o campo é um texto, uma data, um número ou uma tabela completa de resultados) e criar etiquetas legíveis (Labels) para a interface do usuário.

### How will these independent components be created?
Eles serão arquivos de texto simples escritos em Markdown por qualquer editor do mercado (ou criados futuramente dentro de um editor de texto rico na própria interface Web/Flutter). O criador do componente só precisa respeitar duas regras simples:
- Iniciar o arquivo com o bloco de metadados entre três traços (---) para configurar as propriedades dos campos.
- Escrever o texto padrão utilizando marcadores `{{ ... }}` nos locais onde os dados técnicos e as variáveis devem ser injetados.