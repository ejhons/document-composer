from engine.backend.ir.block import ComponentIRBlock
from engine.backend.ir.document import DocumentIR
from engine.frontend.parser import MarkdownParser
from engine.frontend.syntax.parsed_markdown import ParsedMarkdown
from engine.planner.graph.graph import RecipeGraph


class MarkdownAssembler:
    def assemble(
        self,
        graph: RecipeGraph,
        document: DocumentIR,
        parser: MarkdownParser
    ) -> ParsedMarkdown:
        chunks: list[str] = []
        for block in document.walk():
            if not isinstance(block, ComponentIRBlock):
                continue

            node = graph.nodes.get(block.node_id)#. block.node.adapted
            parsed = node.adapted


            if parsed is None:
                continue

            chunks.append(parsed.markdown.rstrip())

        return parser.parse(content="\n\n".join(chunks))
    

class MarkdownAssembler:

    def assemble(
        self,
        block: ComponentIRBlock,
    ) -> ParsedMarkdown:

        output = ParsedMarkdown()

        self._append(
            output,
            block
        )

        return output

    def _append(
        self,
        output: ParsedMarkdown,
        block: ComponentIRBlock
    ):

        parsed = block.node.adapted

        for item in parsed.blocks:

            if isinstance(item, MarkdownPlaceholder):

                child = document.find_by_node(
                    item.node_id
                )

                self._append(
                    output,
                    child
                )

                continue

            output.blocks.append(
                item.model_copy(deep=True)
            )


class MarkdownRenderer:

    def render(
        self,
        parsed: ParsedMarkdown
    ) -> str:

        parts = []

        for block in parsed.blocks:

            if isinstance(block, MarkdownText):
                parts.append(block.text)

            elif isinstance(block, MarkdownImage):
                parts.append(
                    f"![]({block.path})"
                )

            elif isinstance(block, MarkdownTable):
                parts.append(block.markdown)

        return "".join(parts)