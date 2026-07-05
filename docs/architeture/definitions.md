**Adapter**: Tranform custom object as word, pdf, excel in markdown. Also is responsable for evaluate fields, images and mermaid graph for filling final distribution_markdown.md
**Compiler**: Transform distribution_markdown.md to a specified format. In this moment all references are join together in a single file.

**Variável**: marcada com {{...}} nos arquivos markdown. Revelam campos dinâmicos que necessitarão da resolução pelo usuário. Resolvidos pela *Engine.*

**Diretiva**: Funcionam como funções no markdown. Identificadas por @nome_funcao(\*\*params) onde \*\*params marca o conjunto de parâmetros nomeados. Argumentos de uma diretiva pode ainda receber valores de variáveis, tornando-as diretivas dinâmicas. São resolvidas em tempo de execução com a resolução do usuário. São resolvidas pelo *Parser* quando estáticas. Se dinâmicas, são resolvidas pela *Engine*. Ver classe `IncludeDirective`

Os argumentos são: string, número, booleano e expressão Jinja

Mais nada.

Exemplos válidos:
`@include("imagem.png")`
`@include("imagem.png", width=300)`
`@include("imagem.png", optional=True)`
`@include("imagem_{{ indice }}.png")`
`@include(condition="{{ tem_imagem }}")`



# Qual a responsabilidade do Scheduler?

Responder à pergunta:

> **"Em que ordem e sob quais condições cada componente deve ser processado?"**

Isso envolve:

* respeitar dependências;
* aplicar condições (`condition`);
* determinar a ordem de execução;
* eventualmente permitir paralelismo futuro.
