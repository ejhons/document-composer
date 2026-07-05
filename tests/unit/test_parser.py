
from engine.frontend.parser import MarkdownParser


def test_read(dummy_markdown):
    parser = MarkdownParser()
    content = parser.read_markdown(dummy_markdown)
    assert content is not None
    assert len(content) > 0

def test_parse_markdown(dummy_markdown):
    parser = MarkdownParser()
    parsed_markdwon = parser.parse_file(file_path=dummy_markdown)

    assert parsed_markdwon is not None
    assert len(parsed_markdwon.fields) == 1
    assert len(parsed_markdwon.variables) == 2
    assert len(parsed_markdwon.directives) == 1