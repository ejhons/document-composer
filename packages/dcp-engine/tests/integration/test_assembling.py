import os

from dcp_engine.runtime.builder import EngineBuilder
from dcp_engine.runtime.execution.context import ExecutionContext


def test_asembling_document(
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
        r"""---
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
origin: test
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
    engine.assembling.execute(session)

    file_path = 'assembled.md'
    with open(file_path, "w") as f:
        f.write(r"".join(session.fragmented_markdown.assembled_content))

    assert session.graph
    assert len(session.graph.nodes) == 4
    for node in session.graph.nodes.values():
        assert node.adapted.markdown

# import pytest

# from engine.common.models.assets import ComponentContent
# from engine.common.models.recipe import ComponentConfig
# from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown
# from engine.frontend.syntax.markdown.atomizer import MarkdownAtomizer
# from engine.modules.assembling import AssemblingModule
# from engine.planner.graph.component_node import ComponentNode, Dependency
# from engine.planner.resources.resource_resolver import LocalResourceResolver
# from engine.runtime.context import EngineContext
# from engine.runtime.execution.session import ExecutionSession


# class FakeAdapted(ComponentContent):
#     pass
#     # def __init__(self, markdown: str):
#     #     self.markdown = markdown


# class FakeGraph:

#     def __init__(self):
#         self.solved = True
#         self.nodes = {}
#         self.dependencies = {}

#     def get_root_nodes(self):
#         return [self.nodes["A"]]

#     def get_node(self, node_id):
#         return self.nodes[node_id]

#     def get_dependency(self, node_id):
#         return self.dependencies.get(node_id, [])


# @pytest.fixture
# def graph():

#     graph = FakeGraph()

#     node_a = ComponentNode(
#         component=ComponentConfig(
#             type='template',
#             source='test.md'
#             ),
#         id="A",
#         adapted=FakeAdapted(
#             markdown="""
# Texto antes

# @include("b.md")

# Texto depois
# """
#         )
#     )

#     node_b = ComponentNode(
#         component=ComponentConfig(
#             type='template',
#             source='test.md'
#             ),
#         id="B",
#         adapted=FakeAdapted(
#             markdown="""
# ## Filho

# Conteúdo do filho.
# """
#         )
#     )

#     graph.nodes = {
#         "A": node_a,
#         "B": node_b,
#     }

#     graph.dependencies["A"] = [
#         Dependency(
#             source_id="A",
#             target_id="B",
#             origin="0",
#             kind='test'
#         )
#     ]

#     return graph


# @pytest.fixture
# def session(graph):

#     return ExecutionSession(
#         graph=graph
#     )


# @pytest.fixture
# def context():

#     ctx = EngineContext(resource_resolver = LocalResourceResolver())

#     ctx.atomizer = MarkdownAtomizer()

#     return ctx


# def test_should_assemble_document(context, session):

#     assembler = AssemblingModule(context)

#     session = assembler.execute(session)

#     assert isinstance(
#         session.document,
#         AtomizedMarkdown
#     )

#     text = "".join(
#         block.content
#         for block in session.document.blocks
#         if hasattr(block, "content")
#     )

#     assert "Texto antes" in text

#     assert "Filho" in text

#     assert "Conteúdo do filho" in text

#     assert "Texto depois" in text