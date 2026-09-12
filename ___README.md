# Document Composer

> **Engine modular para composição, resolução e compilação de documentos a partir de componentes reutilizáveis.**

O **Document Composer** é um motor de composição documental desenvolvido em Python para transformar um conjunto de componentes heterogêneos — como Markdown, templates, planilhas, imagens e diagramas — em documentos finais nos formatos **PDF, DOCX e HTML**.

O projeto foi concebido para separar claramente as responsabilidades de **inspeção, resolução de dependências, composição e compilação**, permitindo que novos tipos de componentes e formatos de saída sejam incorporados sem modificar o núcleo da aplicação.

---

## Sumário

* [Visão geral](#visão-geral)
* [Problema](#problema)
* [Conceito](#conceito)
* [Arquitetura](#arquitetura)
* [Pipeline de execução](#pipeline-de-execução)
* [Manifesto de composição](#manifesto-de-composição)
* [Componentes](#componentes)
* [Resolução de dependências](#resolução-de-dependências)
* [Análise estática](#análise-estática)
* [Adaptadores](#adaptadores)
* [Compiladores](#compiladores)
* [Extensibilidade](#extensibilidade)
* [Formatos suportados](#formatos-suportados)
* [Princípios arquiteturais](#princípios-arquiteturais)
* [Portabilidade](#portabilidade)
* [Estado atual](#estado-atual)
* [Próximos passos](#próximos-passos)

---

## Visão geral

A ideia central do Document Composer é tratar um documento não como um arquivo monolítico, mas como uma **composição de componentes independentes**.

Um documento pode, por exemplo, ser definido por:

```text
Documento
├── introducao.md
├── metodologia.md
├── resultados.md
├── tabela_resultados.xlsx
├── figura.png
└── diagrama.mermaid
```

Esses componentes podem possuir relações entre si.

Um template Markdown pode depender de uma planilha Excel:

```text
relatorio.md
    │
    └── tabela_resultados.xlsx
```

E essa planilha pode, por sua vez, participar de uma composição mais complexa.

O Composer resolve essas relações antes de produzir o documento final.

A saída do processo é um documento compilado:

```text
Recipe Manifest
       │
       ▼
Static Inspection
       │
       ▼
Dependency Resolution
       │
       ▼
Document Assembly
       │
       ▼
Unified Markdown
       │
       ├──────► HTML
       ├──────► PDF
       └──────► DOCX
```

---

# Problema

Sistemas tradicionais de geração documental normalmente começam com um template monolítico e acumulam lógica de composição ao longo do tempo.

Isso cria problemas como:

* dependências entre templates;
* processamento de arquivos externos;
* inclusão de tabelas e imagens;
* diagramas incorporados;
* condicionais;
* múltiplos formatos de saída;
* regras específicas para cada formato;
* acoplamento entre componentes;
* dificuldade para reutilizar partes de documentos.

O Document Composer busca resolver esse problema através de uma arquitetura na qual **componentes não precisam conhecer diretamente uns aos outros**.

A Engine funciona como o elemento coordenador responsável por resolver essas relações.

---

# Conceito

O projeto adota uma separação fundamental entre:

### 1. Componentes

São os recursos que participam da composição:

```text
Markdown
Excel
Imagem
Mermaid
PDF
DOCX
...
```

### 2. Inspeção

Determina previamente o que um componente necessita.

### 3. Resolução

Resolve variáveis e dependências entre componentes.

### 4. Montagem (Assembly)

Combina os componentes resolvidos em uma representação documental intermediária.

### 5. Compilação

Transforma a representação final no formato desejado.

Essa separação permite que a composição documental seja independente do formato de saída.

---

# Arquitetura

A arquitetura atual do Core está organizada em três grandes responsabilidades:

```text
                    ┌─────────────────────┐
                    │   Recipe Manifest   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Static Analysis   │
                    │     Inspectors      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Dependency /      │
                    │ Runtime Resolution  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Document Engine   │
                    │     Scheduler       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Document Assembly   │
                    │ Unified Markdown    │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
             ┌─────┐        ┌─────┐        ┌─────┐
             │ HTML│        │ PDF │        │DOCX │
             └─────┘        └─────┘        └─────┘
```

O núcleo deixou de ser um simples pipeline linear e passou a operar como uma **máquina de estados com pilha de execução**.

---

# Pipeline de execução

O ciclo de vida de uma composição pode ser resumido em:

```text
1. Carregar Manifest
        │
        ▼
2. Inspecionar componentes
        │
        ▼
3. Criar tarefas
        │
        ▼
4. Resolver dependências
        │
        ▼
5. Executar componentes
        │
        ▼
6. Montar documento
        │
        ▼
7. Gerar Markdown unificado
        │
        ▼
8. Compilar
        │
        ▼
9. Artefato final
```

O pipeline externo recebe a receita e os inputs, chama a Engine para realizar a composição e, posteriormente, seleciona o compilador correspondente ao formato solicitado.

---

# Máquina de estados

Um dos principais avanços arquiteturais do projeto foi substituir o processamento linear por um **TaskScheduler baseado em pilha LIFO**.

O scheduler mantém:

```text
stack
registry
```

A `stack` representa as tarefas pendentes de execução.

O `registry` mantém o estado das tarefas já processadas.

Isso permite lidar com dependências profundas:

```text
Markdown A
   │
   └── Excel B
          │
          └── Mermaid C
```

O processamento ocorre aproximadamente assim:

```text
A entra na stack
      │
      ▼
A é executado
      │
      ▼
A descobre B
      │
      ▼
B entra na stack
      │
      ▼
B é executado
      │
      ▼
B descobre C
      │
      ▼
C entra na stack
      │
      ▼
C é resolvido
      │
      ▼
B é concluído
      │
      ▼
A continua
```

Para dependências descobertas durante a execução, a Engine utiliza marcadores intermediários como:

```html
<!-- WAIT_FOR:id -->
```

O componente original pode então ser retomado depois que suas dependências forem concluídas.

---

# Manifesto de composição

A composição de um documento é orientada por uma **Recipe Manifest**.

O manifesto descreve a receita do documento e seus componentes.

Conceitualmente:

```json
{
  "recipe_name": "technical_report",
  "version": "1.0",
  "target_format": "pdf",
  "style": "default",
  "components": [
    {
      "id": "introduction",
      "type": "template",
      "source": "introduction.md",
      "file_format": "md",
      "is_required": true
    },
    {
      "id": "results",
      "type": "external",
      "source": "results.xlsx",
      "file_format": "xlsx",
      "is_required": true
    }
  ]
}
```

A receita funciona como uma declaração da composição, enquanto a Engine é responsável por determinar **como executar essa composição**.

---

# Componentes

Os componentes são tratados através de configurações que descrevem sua origem e características.

Entre os formatos trabalhados pelo projeto estão:

* Markdown;
* Excel;
* imagens;
* Mermaid;
* PDF;
* DOCX.

O objetivo da arquitetura é evitar que o núcleo precise conhecer detalhes específicos de cada formato.

Em vez disso, componentes são processados através de adaptadores especializados.

---

# Resolução de dependências

Uma característica importante do Composer é a possibilidade de um componente solicitar outro componente durante sua própria resolução.

Por exemplo:

```markdown
# Resultados

{{ incluir_tabela("resultados.xlsx") }}

Os resultados demonstram...
```

O Markdown não precisa conhecer diretamente o adaptador Excel.

A Engine fornece um mecanismo intermediário:

```text
MarkdownTemplateAdapter
          │
          │ external_resolver()
          ▼
      DocumentEngine
          │
          ▼
      Excel Adapter
```

Esse mecanismo utiliza **Inversão de Controle (IoC)** para impedir que adaptadores se tornem diretamente dependentes uns dos outros.

---

# Análise estática

Antes da execução completa, o Composer possui uma camada de **Static Analysis**.

O objetivo é descobrir dependências sem executar o documento.

O método:

```python
identify_dependencies()
```

permite analisar componentes previamente e identificar elementos como:

* variáveis Jinja;
* referências a arquivos;
* funções de inclusão;
* blocos Mermaid;
* possíveis dependências externas.

O `GenericMarkdownInspector` utiliza análise estrutural baseada em expressões regulares.

Uma propriedade importante dessa etapa é:

> **A inspeção não executa o componente e não produz efeitos colaterais.**

A análise é registrada através do `StaticInspectorRegistry`, permitindo que novos inspectores sejam adicionados sem alterar o núcleo.

---

# Adaptadores

Os adaptadores representam a camada responsável por transformar componentes individuais.

A arquitetura utiliza abstrações como:

```text
BaseAdapter
    │
    ├── MarkdownTemplateAdapter
    ├── Excel Adapter
    ├── Mermaid Adapter
    └── ...
```

Cada adaptador conhece seu próprio formato.

A Engine, por outro lado, não precisa implementar regras específicas de cada componente.

---

## MarkdownTemplateAdapter

Responsável por:

* processar templates Markdown;
* resolver Jinja;
* trabalhar com conteúdo inline;
* identificar/processar Mermaid incorporado;
* solicitar recursos externos através do `external_resolver`.

O adaptador não possui uma dependência direta com o adaptador Excel.

Essa decisão reduz significativamente o acoplamento da arquitetura.

---

# Compiladores

Após a composição, o sistema possui um Markdown unificado que pode ser direcionado para diferentes compiladores.

A arquitetura segue o princípio:

```text
                    Unified Markdown
                           │
                    Compiler Registry
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        HTML Compiler PDF Compiler DOCX Compiler
```

A seleção do compilador ocorre através de um registry.

Assim, adicionar um novo formato não exige alterar o fluxo principal da Engine.

---

## HTML

A saída HTML é produzida a partir do documento consolidado, utilizando a infraestrutura de conversão baseada em Pandoc.

---

## PDF

A estratégia de geração de PDF passou por uma mudança importante.

Inicialmente havia dependência de:

```text
LaTeX
WeasyPrint
GTK/GObject
```

Essas dependências introduziam problemas de portabilidade.

A implementação atual utiliza:

```text
Markdown
   │
   ▼
Pandoc
   │
   ▼
HTML controlado
   │
   ▼
xhtml2pdf / ReportLab
   │
   ▼
PDF
```

O `xhtml2pdf` foi escolhido para eliminar a necessidade de runtimes externos como GTK/GObject.

Também foi criado um template HTML controlado para evitar que o CSS gerado pelo Pandoc introduzisse seletores incompatíveis com o mecanismo de conversão PDF.

---

## DOCX

A geração de DOCX utiliza Pandoc, mas possui uma particularidade importante.

A lógica de merge estrutural de subdocumentos foi retirada do pipeline e incorporada ao:

```text
DocxCompilerAdapter
```

O compilador recebe suas dependências através de injeção de dependência, incluindo o `AdapterRegistry`.

Isso mantém as regras específicas do Word dentro do componente que realmente conhece o formato.

---

# Mermaid

O suporte a Mermaid foi integrado à arquitetura de componentes.

Um diagrama pode existir como componente independente:

```text
diagram.mermaid
```

ou aparecer embutido dentro de um documento:

````markdown
```mermaid
graph TD
    A --> B
```
````

O processamento deixou de depender de uma varredura global feita pela Engine e passou a ser tratado através da arquitetura de adaptadores.

---

# Excel

Planilhas podem participar da composição documental como recursos externos.

Um template pode solicitar uma tabela durante sua resolução:

```text
Markdown
   │
   └── include Excel
          │
          ▼
       Adapter
          │
          ▼
   conteúdo documental
```

A resolução é intermediada pela Engine, evitando que:

```text
MarkdownAdapter → ExcelAdapter
```

se torne uma dependência rígida.

---

# Arquitetura orientada a extensibilidade

Um dos objetivos centrais do projeto é permitir que novas capacidades sejam adicionadas através de registries e abstrações.

Exemplos:

```text
AdapterRegistry
CompilerRegistry
StaticInspectorRegistry
```

Isso permite uma arquitetura aberta para extensão:

```text
Novo formato
    │
    ├── Inspector
    ├── Adapter
    └── Compiler
```

sem necessidade de transformar a Engine em um conjunto crescente de condicionais.

---

# Princípios arquiteturais

O desenvolvimento do Core foi guiado principalmente pelos seguintes princípios:

### Single Responsibility

Cada componente possui uma responsabilidade específica.

A Engine coordena.

O Scheduler agenda.

Os Inspectors analisam.

Os Adapters transformam componentes.

Os Compilers produzem formatos finais.

---

### Open/Closed Principle

Novos formatos e comportamentos devem ser adicionados através de extensões, não através da modificação do fluxo central.

---

### Dependency Inversion

Dependências concretas são injetadas através de abstrações e registries.

---

### Inversion of Control

Um exemplo é o:

```python
external_resolver
```

injetado no `MarkdownTemplateAdapter`.

Isso permite que componentes permaneçam independentes entre si.

---

# Portabilidade

Um dos objetivos técnicos mais importantes do projeto foi reduzir dependências externas do sistema operacional.

A arquitetura atual evita depender diretamente de instalações globais como:

```text
pdflatex
GTK
GObject
```

O processamento foi direcionado para bibliotecas Python e ferramentas controladas pelo próprio pipeline.

Isso torna o Core significativamente mais portátil entre ambientes.

---

# Estrutura conceitual

O Core pode ser compreendido através das seguintes camadas:

```text
doc_engine/
│
├── core/
│   │
│   ├── engine
│   │     └── DocumentEngine
│   │
│   ├── scheduler
│   │     └── TaskScheduler
│   │
│   ├── inspectors
│   │     └── StaticInspectorRegistry
│   │
│   ├── adapters
│   │     ├── BaseAdapter
│   │     ├── MarkdownTemplateAdapter
│   │     └── ...
│   │
│   └── compilers
│         ├── BaseCompilerAdapter
│         ├── PdfCompilerAdapter
│         ├── DocxCompilerAdapter
│         └── ...
│
└── ...
```

A estrutura exata do repositório pode evoluir conforme as camadas de aplicação e entrega sejam adicionadas.

---

# Exemplo conceitual de execução

Uma aplicação cliente poderia fornecer:

```python
engine = DocumentEngine(...)

result = engine.assemble_document(
    manifest=manifest,
    variables={
        "project_name": "Project X",
        "author": "Everton"
    }
)
```

A Engine então:

```text
Manifest
   │
   ▼
Tasks
   │
   ▼
Static inspection
   │
   ▼
Scheduler
   │
   ├── Markdown
   │      │
   │      └── Excel
   │             │
   │             └── Mermaid
   │
   ▼
Resolved components
   │
   ▼
Assembled Markdown
   │
   ▼
Compiler
   │
   ▼
Final artifact
```

---

# Estado atual

O Core alcançou uma arquitetura funcionalmente madura, com os principais componentes estruturais implementados:

### Concluído

* `DocumentEngine`;
* `TaskScheduler`;
* sistema de execução baseado em pilha;
* `BaseAdapter`;
* `BaseCompilerAdapter`;
* `AdapterRegistry`;
* `StaticInspectorRegistry`;
* análise estática de dependências;
* resolução de dependências em múltiplos níveis;
* processamento de Markdown;
* integração de Excel;
* integração de Mermaid;
* compilação para PDF;
* compilação para HTML;
* compilação para DOCX;
* desacoplamento das regras específicas de DOCX;
* redução de dependências de sistema operacional.

Esses avanços representam a transformação do Core de um pipeline linear para um **motor de composição e compilação documental extensível**.

---

# Próximos passos

A próxima etapa prevista é construir as **portas de entrada externas** do sistema.

A arquitetura planejada contempla uma camada HTTP baseada em **FastAPI**, permitindo que o Core seja consumido por aplicações externas sem que a lógica de composição documental precise ser replicada na API.

Conceitualmente:

```text
                    ┌─────────────────┐
                    │     Frontend    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │      API        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Document Engine │
                    │      Core       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Compiler     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
             PDF            DOCX           HTML
```

A intenção é manter a API como uma **porta de entrada**, e não transformá-la em parte da lógica de negócio do Composer. O Core permanece responsável pela composição e compilação.

---

# Filosofia do projeto

O Document Composer parte de uma ideia simples:

> **Um documento complexo deve ser composto a partir de componentes independentes, e não implementado como um único template complexo.**

A arquitetura procura transformar:

```text
Template monolítico
       ↓
muitas regras
       ↓
muito acoplamento
       ↓
difícil manutenção
```

em:

```text
Componentes independentes
       ↓
Inspeção
       ↓
Resolução
       ↓
Composição
       ↓
Compilação
       ↓
Múltiplos formatos
```

O resultado é um núcleo que pode evoluir independentemente das interfaces de usuário, APIs e formatos específicos de distribuição.

---

## Status

**Core Engine:** 🟢 Implementado
**Dependency Scheduler:** 🟢 Implementado
**Static Analysis:** 🟢 Implementado
**Markdown Composition:** 🟢 Implementado
**PDF:** 🟢 Implementado
**DOCX:** 🟢 Implementado
**HTML:** 🟢 Implementado
**API / FastAPI:** 🔵 Próxima etapa
**Frontend:** 🔵 Planejado

---

## License

> A licença do projeto ainda não está definida.
