from pprint import pprint

from engine.solving.inspection.base import BaseOjbjectInspector
from engine.frontend.parser import MarkdownParser
from engine.solving.inspection.result import InspectionResult
from engine.frontend.manifests.recipe import ComponentConfig

class MarkdownInspector(BaseOjbjectInspector):
    def __init__(
            self,
            markdown_parser: MarkdownParser | None = None
        ):
        self.parsed_markdown = None
        self.markdown_parser = markdown_parser or MarkdownParser()
        
    def inspect(self, component:ComponentConfig)  -> InspectionResult:
        '''
        task.format_type = md
        '''
        parsed = self.markdown_parser.parse_file(
            component.source
        )
        self.parsed_markdown = parsed

        result = InspectionResult(
            body = parsed.body,
            fields=parsed.fields,
            variables=parsed.variables,
            directives=parsed.directives,
            metadata=parsed.metadata
        )

        return result
    