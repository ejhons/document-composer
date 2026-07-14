**Adapter**: Tranforms ComponentNode what rpresents a custom object as word, pdf, excel content to a markdown language.  Also is responsable creating respective assets neccessary for that representation.
**Compiler**: Transform FragmentedMarkdown/DocumentIR to a specified format. In this moment all references are join together in a single file.

**Input**: marked with {{...}} in the Markdown files. They reveal dynamic fields that require resolution by the user. Resolved by the *Engine*.]

**InputDefinition:** define property of inputs as type, description and any other metadata relevant for backend and frontend.

**Diretiva**: They operate like functions within Markdown. They are identified by `@function_name(**params)`, where `**params` denotes the set of named parameters. Directive arguments can also accept inpur values, making them dynamic directives. They are resolved at runtime based on user Execution Context. Static directives are resolved by the *DependencyResolver*, while dynamic ones are first treated for *RuntimeResolver.* If succesfull, *DependencyResolver* acts as expected in firective. See the `IncludeDirective` class.

Os inputs são: string, número, booleano e expressão Jinja

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
