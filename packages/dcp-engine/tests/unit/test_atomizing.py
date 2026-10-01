from dcp_engine.assembly.atomizer import MarkdownAtomizer
from dcp_engine.language.syntax.markdown.atom import MarkdownDirective, MarkdownFragment


def test_atomizer_should_create_single_fragment_when_no_directives(
    markdown_file,
    temp_workspace,
):
    markdown = """
# Título

Texto simples.

Mais texto.
"""

    atomizer = MarkdownAtomizer()

    fragmented = atomizer.atomize(markdown)

    assert len(fragmented.blocks) == 1

    block = fragmented.blocks[0]

    assert isinstance(block, MarkdownFragment)
    assert "# Título" in block.content


def test_atomizer_should_split_markdown_around_single_directive():

    markdown = """
# Memorial

Texto antes.

@include("annex.md")

Texto depois.
"""

    atomizer = MarkdownAtomizer()

    fragmented = atomizer.atomize(markdown)

    assert len(fragmented.blocks) == 3

    assert isinstance(fragmented.blocks[0], MarkdownFragment)
    assert isinstance(fragmented.blocks[1], MarkdownDirective)
    assert isinstance(fragmented.blocks[2], MarkdownFragment)

    assert "Texto antes" in fragmented.blocks[0].content
    assert fragmented.blocks[1].directive.name == "include"
    assert "Texto depois" in fragmented.blocks[2].content


def test_atomizer_should_preserve_directive_order():

    markdown = """
Antes

@include("a.md")

Meio

@include("b.md")

Fim
"""

    atomizer = MarkdownAtomizer()

    fragmented = atomizer.atomize(markdown)

    assert len(fragmented.blocks) == 5

    assert isinstance(fragmented.blocks[0], MarkdownFragment)
    assert isinstance(fragmented.blocks[1], MarkdownDirective)
    assert isinstance(fragmented.blocks[2], MarkdownFragment)
    assert isinstance(fragmented.blocks[3], MarkdownDirective)
    assert isinstance(fragmented.blocks[4], MarkdownFragment)