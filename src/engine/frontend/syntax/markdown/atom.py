from typing import Union

from pydantic import BaseModel

from engine.common.models.assets import Asset
from engine.frontend.syntax.directives import DirectiveCall


class BaseMarkdownAtom(BaseModel):
    pass


class MarkdownFragment(BaseMarkdownAtom):
    content: str


class MarkdownDirective(BaseMarkdownAtom):
    directive: DirectiveCall


class MarkdownImage(BaseMarkdownAtom):
    asset: Asset


class MarkdownTable(BaseMarkdownAtom):
    markdown: str


class MarkdownHtml(BaseMarkdownAtom):
    html: str


class MarkdownPlaceholder(BaseMarkdownAtom):
    node_id: str

MarkdownAtom = Union[
    MarkdownFragment,
    MarkdownDirective,
    MarkdownImage,
    MarkdownTable,
    MarkdownHtml,
    MarkdownPlaceholder
    ]