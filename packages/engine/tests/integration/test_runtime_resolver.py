
from dcp_engine.language.directives.implementations.include_directive import (
    IncludeDirectiveHandler,
)
from dcp_engine.planning.graph.builder import RecipeGraphBuilder
from dcp_engine.planning.resolution.runtime_resolver import RuntimeResolver
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.solving.inspection.implementations.markdown_inspector import (
    MarkdownInspector,
)
from dcp_engine.solving.inspection.pipeline import InspectionPipeline
from dcp_engine.solving.resolution.resolution_state import ResolutionState


def test_capturing_variables_in_markdown(
    temp_workspace,
    recipe_manifest,
    markdown_file,
    planning_context,
    resource_resolver
):
    # Cria um arquivo markdown em uma pasta temporária
    markdown_file(
        'test_resolver.md',
        r'''
---
fields_definition:
project_title:
    data_type: "text"
    label: "Nome do Empreendimento"
discipline:
    data_type: "text"
    label: "Disciplina de projeto"
---
@include('cover.md')
@include('image_{{logo}}.png')

# MEMORIAL TÉCNICO DE ENGENHARIA

## 1. Escopo Estrutural do Projeto: {{ project_title }}

O cálculo de dimensionamento dos pilares de sustentação, no empreendimento {{localization}}, foi executado utilizando o critério de esbeltez e tensão admissível do material, conforme a formulação clássica:

$$ \sigma = \frac{P}{A} \pm \frac{M}{W} $$

Abaixo, apresentamos o diagrama lógico que descreve o fluxo de validação da infraestrutura da obra {{classe}}:
```mermaid
graph TD
    A[Sondagem do Terreno] --> B(Análise de Carga)
    B --> C{Carga Suportada?}
    C -- Sim --> D[Fundação Direta]
    C -- Não --> E[Estacas Profundas]
```
    '''
        )
    
    recipe_manifest.components[0].source = (
        temp_workspace / "test_resolver.md"
    ).as_posix()
    
    graph = RecipeGraphBuilder(resource_resolver).build(
        recipe_manifest
    )
    
    planning_context.inspector_registry.register(
        "md",
        MarkdownInspector()
    )
    planning_context.directive_registry.register(
        IncludeDirectiveHandler()
    )
    execution_context = ExecutionContext(
        inputs= {
            'logo':'generic',
            'project_title': 'Generic project',
            'localization': 'HERE'
        }
    )
    inspector_pipeline = InspectionPipeline()
    inspector_pipeline.execute(
        graph=graph,
        inspector_registry=planning_context.inspector_registry
        # planning_context=planning_context
    )

    resolver = RuntimeResolver()
    for node in graph.nodes.values():
        node.resolution = ResolutionState()

    resolver.resolve_node(
        next(iter(graph.nodes.values())),
        context=execution_context
    )
    # pprint(graph.model_dump())
    # print(list(graph.nodes.values())[0].inspection.body)
    # print(list(graph.nodes.values())[0].resolution.content)

    # assert False