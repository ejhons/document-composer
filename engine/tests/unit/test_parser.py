
from engine.src.doc_engine.analysis.markdown.parser import MarkdownParser


def test_read(dummy_markdown):
    content = MarkdownParser.read_markdown(dummy_markdown)
    assert content is not None
    assert len(content) > 0

def test_parse_markdown(dummy_markdown):
    parsed_markdwon = MarkdownParser.parse(dummy_markdown)

    assert parsed_markdwon is not None
    assert len(parsed_markdwon.fields) == 1
    assert len(parsed_markdwon.variables) == 2
    assert len(parsed_markdwon.directives) == 1