from abc import ABC, abstractmethod
from typing import Union

from pydantic import BaseModel

from engine.common.exceptions import ContentNotAvaliable
from engine.planning.graph.assets import Asset
from engine.frontend.syntax.directives import DirectiveCall


class BaseMarkdownAtom(BaseModel, ABC):
    @abstractmethod
    def to_markdown(self) -> str:
        ...


class MarkdownFragment(BaseMarkdownAtom):
    content: str

    def to_markdown(self) -> str:
        return self.content


class MarkdownDirective(BaseMarkdownAtom):
    directive: DirectiveCall

    def to_markdown(self) -> str:
        raise ContentNotAvaliable("Can't convert Directive to Markdown directly")


class MarkdownImage(BaseMarkdownAtom):
    asset: Asset

    def to_markdown(self) -> str:
        return f'![{self.asset.metadata.get('title','')}]({self.asset.output})'

class MarkdownTable(BaseMarkdownAtom):
    markdown: str

    def to_markdown(self) -> str:
        return self.markdown

class MarkdownHtml(BaseMarkdownAtom):
    html: str
    
    def to_markdown(self) -> str:
        return self.html


class MarkdownPlaceholder(BaseMarkdownAtom):
    node_id: str

    def to_markdown(self) -> str:
        raise ContentNotAvaliable("Unsolved placeholder")

MarkdownAtom = Union[
    MarkdownFragment,
    MarkdownDirective,
    MarkdownImage,
    MarkdownTable,
    MarkdownHtml,
    MarkdownPlaceholder
    ]