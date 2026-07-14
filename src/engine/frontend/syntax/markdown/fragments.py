from pydantic import BaseModel

from engine.common.models.assets import Asset
from engine.frontend.syntax.directives import DirectiveCall


class MarkdownBlock(BaseModel):
    pass


class MarkdownFragment(MarkdownBlock):
    content: str


class MarkdownDirective(MarkdownBlock):
    directive: DirectiveCall


class MarkdownImage(MarkdownBlock):
    asset: Asset


class MarkdownTable(MarkdownBlock):
    markdown: str


class MarkdownHtml(MarkdownBlock):
    html: str


class MarkdownPlaceholder(MarkdownBlock):
    node_id: str