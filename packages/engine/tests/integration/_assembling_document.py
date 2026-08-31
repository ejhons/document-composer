import pytest
from dcp_engine.assembly.atomizer import MarkdownAtomizer
from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.language.syntax.markdown.atomized_markdown import AtomizedMarkdown
from dcp_engine.pipeline.assembling import AssemblingModule
from dcp_engine.planning.graph.assets import ComponentContent
from dcp_engine.planning.graph.component_node import ComponentNode, Dependency
from dcp_engine.planning.loaders.resource_resolver import LocalResourceResolver
from dcp_engine.runtime.context import EngineContext
from dcp_engine.runtime.execution.session import ExecutionSession


class FakeAdapted(ComponentContent):
    pass
    # def __init__(self, markdown: str):
    #     self.markdown = markdown


class FakeGraph:

    def __init__(self):
        self.solved = True
        self.nodes = {}
        self.dependencies = {}

    def get_root_nodes(self):
        return [self.nodes["A"]]

    def get_node(self, node_id):
        return self.nodes[node_id]

    def get_dependency(self, node_id):
        return self.dependencies.get(node_id, [])


@pytest.fixture
def graph():

    graph = FakeGraph()

    node_a = ComponentNode(
        component=ComponentConfig(
            type='template',
            source='test.md'
            ),
        id="A",
        adapted=FakeAdapted(
            markdown="""
Texto antes

@include("b.md")

Texto depois
"""
        )
    )

    node_b = ComponentNode(
        component=ComponentConfig(
            type='template',
            source='test.md'
            ),
        id="B",
        adapted=FakeAdapted(
            markdown="""
## Filho

Conteúdo do filho.
"""
        )
    )

    graph.nodes = {
        "A": node_a,
        "B": node_b,
    }

    graph.dependencies["A"] = [
        Dependency(
            source_id="A",
            target_id="B",
            origin="0",
            kind='test'
        )
    ]

    return graph


@pytest.fixture
def session(graph):

    return ExecutionSession(
        graph=graph
    )


@pytest.fixture
def context():

    ctx = EngineContext(resource_resolver = LocalResourceResolver())

    ctx.atomizer = MarkdownAtomizer()

    return ctx


def test_should_assemble_document(context, session):

    assembler = AssemblingModule(context)

    session = assembler.execute(session)

    assert isinstance(
        session.document,
        AtomizedMarkdown
    )

    text = "".join(
        block.content
        for block in session.document.blocks
        if hasattr(block, "content")
    )

    assert "Texto antes" in text

    assert "Filho" in text

    assert "Conteúdo do filho" in text

    assert "Texto depois" in text