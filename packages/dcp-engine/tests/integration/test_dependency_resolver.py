from dcp_engine.language.directives.implementations.include_directive import (
    IncludeDirectiveHandler,
)
from dcp_engine.planning.graph.builder import RecipeGraphBuilder
from dcp_engine.planning.resolution.dependency_resolver import DependencyResolver
from dcp_engine.solving.inspection.implementations.markdown_inspector import (
    MarkdownInspector,
)
from dcp_engine.solving.inspection.pipeline import InspectionPipeline
from dcp_engine.solving.resolution.resolution_state import ResolutionState


def test_markdown_pipeline_enriches_recipe_graph(
    temp_workspace,
    markdown_file,
    recipe_manifest,
    planning_context,
    resource_resolver
):
    """
    Pipeline completo:

    Manifest
        ↓
    RecipeGraphBuilder
        ↓
    MarkdownInspector
        ↓
    DependencyResolver
        ↓
    RecipeGraph enriquecido
    """

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
fields:
  flow:
    type: number
    label: Vazão
---
# Memorial
{{ flow }}
@include("annex.md")
"""
    )

    markdown_file(
        "annex.md",
        """
# Annex
{{ project_name }}
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

    graph = RecipeGraphBuilder(resource_resolver).build(#context=planning_context
        recipe_manifest
    )

    # inspectors = StaticInspectorRegistry()

    planning_context.inspector_registry.register(
        "md",
        MarkdownInspector()
    )

    # directives = DirectiveRegistry()
    # directives

    planning_context.directive_registry.register(
        IncludeDirectiveHandler()
    )

    inspector_pipeline = InspectionPipeline()
    inspector_pipeline.execute(
        graph=graph,
        inspector_registry=planning_context.inspector_registry
        # planning_context=planning_context
    )

    resolver = DependencyResolver()
    # DependencyResolver(
    #     # expression_parser=ExpressionParser()
    #     # inspector_registry=inspectors,
    #     # directive_registry=directives
    # )
    for node in graph.nodes.values():
        node.resolution = ResolutionState()

    # graph2 = 
    resolver.resolve(
        graph=graph,
        context=planning_context
        )

    #
    # Verificações
    #
    # pprint(graph.model_dump())

    assert len(graph.nodes) == 3

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

    assert graph.has_dependency(
        memorial.id,
        annex.id
    )

    assert "flow" in memorial.inspection.variable_names
    assert "flow" in memorial.inspection.unique_variables

    assert len(memorial.inspection.directives) == 1

    # assert False