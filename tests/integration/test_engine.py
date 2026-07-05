import pytest

from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.planner.recipe_builder import RecipeGraphBuilder
from engine.runtime.context import ExecutionContext
from engine.runtime.engine import Engine


# def test_engine_resolves_runtime_and_dependencies(engine):
#     graph = engine.plan(
#         component=NodeComponent.from_file("tests/resources/main.md"),
#         inputs={
#             "name": "Everton",
#             "type": "person"
#         }
#     )

#     assert len(graph.nodes) == 2

#     main = graph.root
#     dependency = graph.find_by_path(
#         "contracts/person.md"
#     )

#     assert dependency is not None

#     assert main.resolution.content == (
#         "Olá Everton\n\n"
#         '@include("contracts/person.md")'
#     )

#     assert not main.resolution.pending_inputs
#     assert not main.resolution.pending_dependencies

#     assert main.resolution.resolved

#     assert dependency.resolution.resolved

# def test_engine_keeps_unresolved_directive(engine):
#     graph = engine.plan(
#         component=Component.from_file("tests/resources/main.md"),
#         inputs={
#             "name": "Everton"
#         }
#     )

#     root = graph.root

#     assert root.resolution.content == (
#         "Olá Everton\n\n"
#         '@include("contracts/{{ type }}.md")'
#     )

#     assert root.resolution.pending_inputs == {
#         "type"
#     }

#     assert len(graph.nodes) == 1

# def test_engine_converges_after_new_input(engine):
#     graph = engine.plan(
#         component=Component.from_file("tests/resources/main.md"),
#         inputs={
#             "name": "Everton"
#         }
#     )

#     graph = engine.resolve(
#         graph,
#         {
#             "name": "Everton",
#             "type": "person"
#         }
#     )

#     assert len(graph.nodes) == 2

#     assert graph.root.resolution.resolved

def test_engine_converges_until_no_changes(
    full_engine,
    temp_workspace,
    markdown_file,
    recipe_manifest,
    context
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

    execution_context = ExecutionContext(
        inputs= {
            'logo':'generic',
            'project_title': 'Generic project',
            'localization': 'HERE',
            'flow': 35.0,
        }
    )
    graph = RecipeGraphBuilder(context=context).build(
        recipe_manifest
    )
    previous_revision = -1

    inspector_pipeline = InspectionPipeline()
    inspector_pipeline.execute(
        graph=graph,
        planning_context=full_engine.plan_context
    )
    while True:

        changed = full_engine.plan(
            graph,
            execution_context)

        current_revision = sum(
            node.resolution.revision
            for node in graph.nodes.values()
        )

        assert current_revision >= previous_revision

        if not changed:
            break

        previous_revision = current_revision

    assert all(
        node.resolution.resolved
        for node in graph.nodes.values()
    )