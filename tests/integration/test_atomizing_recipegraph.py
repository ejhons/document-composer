from engine.common.models.assets import ComponentContent
from engine.planner.recipe_builder import RecipeGraphBuilder
from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.frontend.syntax.markdown.atomizer import MarkdownAtomizer
from engine.planner.resolution.resolution_state import ResolutionState
from engine.planner.resolution.dependency_resolver import DependencyResolver
from engine.frontend.inspectors.implementations.inspector import MarkdownInspector
from engine.frontend.syntax.markdown.atom import MarkdownDirective, MarkdownFragment
from engine.frontend.directives.implementations.include_directive import IncludeDirectiveHandler


def test_markdown_pipeline_atomizes_resolved_document(
    temp_workspace,
    markdown_file,
    recipe_manifest,
    planning_context,
    resource_resolver,
):
    markdown_file(
        "cover.md",
        """
# Cover

Texto

@include("annex.md")

Fim
"""
    )

    markdown_file(
        "annex.md",
        """
# Annex
"""
    )

    recipe_manifest.components[0].source = (
        temp_workspace / "cover.md"
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

    InspectionPipeline().execute(
        graph=graph,
        inspector_registry=planning_context.inspector_registry,
    )

    for node in graph.nodes.values():
        node.resolution = ResolutionState()

    DependencyResolver().resolve(
        graph=graph,
        context=planning_context,
    )

    #
    # Simula adaptação concluída
    #

    cover = graph.find_by_source(
        (temp_workspace / "cover.md").as_posix()
    )

    cover.adapted = ComponentContent(
        markdown=cover.resolution.content
    )

    atomizer = MarkdownAtomizer()

    fragmented = atomizer.atomize(
        cover.adapted.markdown
    )

    assert len(fragmented.blocks) == 3

    assert isinstance(
        fragmented.blocks[0],
        MarkdownFragment
    )

    assert isinstance(
        fragmented.blocks[1],
        MarkdownDirective
    )

    assert isinstance(
        fragmented.blocks[2],
        MarkdownFragment
    )

    # parsed = MarkdownParser().parse(cover.adapted.body)
    # assert parsed.variables == []


