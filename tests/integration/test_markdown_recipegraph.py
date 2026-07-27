from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.frontend.inspectors.implementations.inspector import MarkdownInspector
from engine.planner.resolution.resolution_state import ResolutionState
from engine.planner.resolution.runtime_resolver import RuntimeResolver
from engine.planner.recipe_builder import RecipeGraphBuilder
from engine.planner.resolution.dependency_resolver import DependencyResolver
from engine.runtime.execution.context import ExecutionContext
from engine.frontend.directives.implementations.include_directive import IncludeDirectiveHandler



def test_markdown_pipeline_enriches_recipe_graph(
    temp_workspace,
    markdown_file,
    recipe_manifest,
    planning_context,
    resource_resolver
):

    markdown_file(
        "cover.md",
        """
# Cover
{{ client }}
"""
    )

    markdown_file(
        "memorial.md",
        """
---
fields_definition:
project_title:
    data_type: text
    label: Nome do Empreendimento
discipline:
    data_type: text
    label: Disciplina de projeto
fields:
  flow:
    type: number
    label: Vazão
---
@include('cover.md')
@include('image_{{logo}}.png')

# MEMORIAL TÉCNICO DE ENGENHARIA
## 1. Escopo Estrutural do Projeto: {{ project_title }}

O cálculo de dimensionamento dos pilares de sustentação, no empreendimento {{localization}}, foi executado utilizando o critério de esbeltez e tensão admissível do material, conforme a formulação clássica ({{ flow }}):

$$ \sigma = \frac{P}{A} \pm \frac{M}{W} $$

Abaixo, apresentamos o diagrama lógico que descreve o fluxo de validação da infraestrutura da obra {{classe}}:
```mermaid
graph TD
    A[Sondagem do Terreno] --> B(Análise de Carga)
    B --> C{Carga Suportada?}
    C -- Sim --> D[Fundação Direta]
    C -- Não --> E[Estacas Profundas]
```

@include("annex.md")
"""
    )

    markdown_file(
        "annex.md",
        """
# Annex
{{ project_title }}
"""
    )

    recipe_manifest.components[0].source = (
        temp_workspace / "cover.md"
    ).as_posix()

    recipe_manifest.components.append(
        recipe_manifest.components[0].model_copy(
            update={
                "id": "memorial",
                "source": (
                    temp_workspace / "memorial.md"
                ).as_posix()
            }
        )
    )

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
            'localization': 'HERE',
            'flow': 35.0,
        }
    )

    inspector_pipeline = InspectionPipeline()
    inspector_pipeline.execute(
        graph=graph,
        inspector_registry=planning_context.inspector_registry
    )
    
    inspector_pipeline = InspectionPipeline()
    inspector_pipeline.execute(
        graph=graph,
        # planning_context=planning_context
        inspector_registry=planning_context.inspector_registry
    )

    for node in graph.nodes.values():
        node.resolution = ResolutionState()

    runtime_resolver = RuntimeResolver()
    runtime_resolver.resolve(
        graph,#list(graph.nodes.values())[0],
        context=execution_context
    )

    dependency_resolver = DependencyResolver()
    # graph2 =
    dependency_resolver.resolve(
        graph=graph,
        context=planning_context
        )

    #
    # Verificações
    #
    # pprint(graph.model_dump())

    assert len(graph.nodes) == 4

    assert graph.find_by_source(
        (temp_workspace / "annex.md").as_posix()
    ) is not None

    memorial = graph.find_by_source(
        (temp_workspace / "memorial.md").as_posix()
    )

    annex = graph.find_by_source(
        (temp_workspace / "annex.md").as_posix()
    )

    # print(memorial.inspection.body)
    # print(memorial.resolution.content)
    # print(annex.resolution.content)

    assert graph.has_dependency(
        memorial.id,
        annex.id
    )

    assert "flow" in memorial.inspection.variable_names
    assert "flow" in memorial.inspection.unique_variables

    assert len(memorial.inspection.directives) == 3

    # assert False