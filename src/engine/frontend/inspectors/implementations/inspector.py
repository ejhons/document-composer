from pprint import pprint

from engine.frontend.inspectors.base import BaseOjbjectInspector
from engine.frontend.parser import MarkdownParser
from engine.common.models.inspection import InspectionResult
from engine.common.models.recipe import ComponentConfig

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
    