
from engine.frontend.parser import MarkdownParser
from engine.frontend.syntax.markdown.atom import MarkdownDirective, MarkdownFragment
from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown


class MarkdownAtomizer:    
    def __init__(
        self, 
        parser: MarkdownParser | None = None
    ):
        self.parser = parser or MarkdownParser()
        

    def atomize(self, markdown:str) -> AtomizedMarkdown:
        '''
        Nesse ponto o markdown já deve ter sido tratado
        sem a existência de variáveis.
        '''        
        parsed = self.parser.parse(markdown)

        body = parsed.body
        directives = parsed.directives

        fragmented = AtomizedMarkdown()

        if not directives:
            fragmented.blocks.append(MarkdownFragment(content=body))
            return fragmented

        cursor = 0
        for directive in directives:
            directive.arguments
            start = directive.start.index
            end = directive.end.index + 1

            # Texto anterior
            if start > cursor:
                fragmented.blocks.append(MarkdownFragment(content=body[cursor:start]))
            # Diretiva
            fragmented.blocks.append(MarkdownDirective(directive=directive))

            cursor = end

        # Restante
        if cursor < len(body):
            fragmented.blocks.append(MarkdownFragment(content=markdown[cursor:]))

        return fragmented
    
