import os

from dcp_engine.runtime.builder import EngineBuilder
from dcp_engine.runtime.execution.context import ExecutionContext


def test_engine_converges_until_no_changes(
    full_engine,
    temp_workspace,
    temp_workspace_object,
    markdown_file,
    recipe_manifest
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
        """---
fields:
  project_title:
    data_type: text
    label: Nome do Empreendimento
  discipline:
    data_type: text
    label: Disciplina de projeto
  flow:
    type: number
    label: Vazão
---
@include('cover.md')
@include('image_{{logo}}.png')

# MEMORIAL TÉCNICO DE ENGENHARIA
## 1. Escopo Estrutural do Projeto: {{ project_title }}

O cálculo de dimensionamento dos pilares de sustentação, no empreendimento {{localization}}, foi executado utilizando o critério de esbeltez e tensão admissível do material, conforme a formulação clássica ({{ flow }}):

$$ \\sigma = \\frac{P}{A} \\pm \\frac{M}{W} $$

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
                "source": (temp_workspace / "memorial.md").as_posix()
            }
        )
    )

    execution_context = ExecutionContext(
        inputs= {
            'client':'Everton',
            'logo':'generic',
            'classe':'de Infraestrutura',
            'project_title': 'Generic project',
            'discipline':'Structure',
            'localization': 'HERE',
            'flow': 35.0,
        }
    )
    # graph = RecipeGraphBuilder(context=context).build(
    #     recipe_manifest
    # )

    # inspector_pipeline = InspectionPipeline()
    # inspector_pipeline.execute(
    #     graph=graph,
    #     planning_context=full_engine.plan_context
    # )
    img_path = temp_workspace_object.root.joinpath('image_generic.png')
    os.makedirs(os.path.dirname(img_path), exist_ok=True)


    with open(img_path, 'wb') as f:
        f.write(b'ff')

    session = full_engine.create_session(
        manifest=recipe_manifest,
        context=execution_context,
        workspace=temp_workspace_object
    )
    engine = EngineBuilder.default().build()
    engine.planning.execute(session)
    engine.solving.execute(session)

    assert session.graph
    assert len(session.graph.nodes) == 4
    for node in session.graph.nodes.values():
        assert node.adapted.markdown



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
