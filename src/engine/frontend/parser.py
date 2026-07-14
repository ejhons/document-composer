import os
import re
import yaml
from typing import Any, Dict, Tuple

from engine.frontend.syntax.directives import DirectiveArgument, DirectiveCall, Expression, TextSpan
from engine.frontend.syntax.expressions.parser import ExpressionParser
from engine.frontend.syntax.fields import FieldDefinition
from engine.frontend.syntax.parsed_markdown import ParsedMarkdown
from engine.frontend.syntax.variables import VariableReference


DIRECTIVE_START = re.compile(
    r'^\s*@([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
    re.MULTILINE
)

class MarkdownParser:    
    def __init__(self, expression_parser: ExpressionParser | None = None):
        self.expression_parser = expression_parser or ExpressionParser()

    '''
    Cumpre a função de converter o markdown em ParsedMarkdown.
    A partir do arquivo, identifica:
    - fields
    - variables
    - directives
    - metadata
    Cria o objeto ParsedMarkdown
    '''
    
    def read_markdown(self, file_path:str) -> str:
        """Extracts YAML front matter and the raw Markdown body from a component file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File {file_path} not found.')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
        
    
    def parse_file(self, file_path:str) -> ParsedMarkdown:
        content = self.read_markdown(file_path)
        
        metadata, body = self.parse_front_matter(content)
        fields = self.extract_fields(metadata)
        variables = self.extract_variables(body)
        directives = self.extract_directives(body)

        return ParsedMarkdown(
            metadata=metadata,
            fields=fields,
            variables=variables,
            directives=directives,
            body=body
        )

    def parse(self, content:str) -> ParsedMarkdown:
        # content = self.read_markdown(file_path)
        
        metadata, body = self.parse_front_matter(content)
        fields = self.extract_fields(metadata)
        variables = self.extract_variables(body)
        directives = self.extract_directives(body)

        return ParsedMarkdown(
            metadata=metadata,
            fields=fields,
            variables=variables,
            directives=directives,
            body=body
        )

    
    def parse_front_matter(self, content: str) -> Tuple[Dict[str, Any], str]:
        # Match YAML block bounded by --- at the start of the file
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if match:
            front_matter_text, body_content = match.groups()
            metadata = yaml.safe_load(front_matter_text) or {}

            return metadata, body_content
        
        return {}, content

    
    def extract_fields(self, metadata: dict[str, Any]) -> dict[str, FieldDefinition]:
        # Extrai o campo 'fields' do dicionário
        fields = metadata.pop('fields', {})

        return {
            key: FieldDefinition(**field)
            for key, field 
            in fields.items()
            }


    
    # def extract_variables(self, content: str) -> list[VariableReference]:
    #     """Scans raw text to discover all Jinja2 placeholders like {{ variable_name }}."""
    #     found_tokens = re.findall(r'\{\{\s*(.*?)\s*\}\}', content)
    #     return [VariableReference(name=token) for token in found_tokens]

    
    def extract_variables(self, content: str) -> list[VariableReference]:
        """
        Scans the Markdown content looking for Jinja expressions.
        Examples:
            {{ client }}
            {{ area | round(2) }}
            {{ width * height }}
        """
        variables: list[VariableReference] = []
        pattern = re.compile(r"(\{\{\s*(.*?)\s*\}\})")

        for idx, match in enumerate(pattern.finditer(content)):
            raw = match.group(1)          # "{{ area | round(2) }}"
            expression = match.group(2)   # "area | round(2)"

            variables.append(
                VariableReference(
                    name=expression,
                    raw=raw,
                    index=idx
                    # start=match.start(),
                    # end=match.end(),
                )
            )

        return variables



    
    def extract_directives(self, content: str) -> list[DirectiveCall]:
        directives: list[DirectiveCall] = []
        for idx, match in enumerate(DIRECTIVE_START.finditer(content)):
            name = match.group(1)
            start = match.start()
            open_paren = content.find("(", match.end() - 1)
            end = self._find_matching_parenthesis(
                content,
                open_paren
            )

            if end == -1:
                # posteriormente pode gerar um Diagnostic
                continue

            raw = content[start:end + 1]
            arguments_text = content[open_paren + 1:end]

            line_start = content.count("\n", 0, start) + 1
            column_start = start - content.rfind("\n", 0, start)
            line_end = content.count("\n", 0, end) + 1
            column_end = end - content.rfind("\n", 0, end)

            directives.append(
                DirectiveCall(
                    index=idx,
                    name=name,
                    raw=raw,
                    arguments=self.extract_directive_parameters(
                        arguments_text
                    ),
                    start=TextSpan(
                        line=line_start, 
                        column=column_start, 
                        index=start
                    ),
                    end=TextSpan(
                        line=line_end,
                        column=column_end,
                        index=end
                    )
                    # line=line,
                    # column=column
                )
            )
        return directives  
    # def extract_directives(self, content: str) -> list[DirectiveCall]:
    #     directives: list[DirectiveCall] = []
    #     for idx, match in enumerate(DIRECTIVE_START.finditer(content)):
    #         name = match.group(1)
    #         start = match.start()
    #         open_paren = content.find("(", match.end() - 1)
    #         end = self._find_matching_parenthesis(
    #             content,
    #             open_paren
    #         )

    #         if end == -1:
    #             # posteriormente pode gerar um Diagnostic
    #             continue

    #         raw = content[start:end + 1]
    #         arguments_text = content[open_paren + 1:end]

    #         line = content.count("\n", 0, start) + 1
    #         column = start - content.rfind("\n", 0, start)
    #         directives.append(
    #             DirectiveCall(
    #                 index=idx,
    #                 name=name,
    #                 raw=raw,
    #                 arguments=self.extract_directive_parameters(
    #                     arguments_text
    #                 ),
    #                 line=line,
    #                 column=column
    #             )
    #         )
    #     return directives
    
    
    
    def _find_matching_parenthesis(self, text: str, start: int) -> int:
        depth = 0
        in_string = False
        quote = None
        escape = False

        for i in range(start, len(text)):
            c = text[i]

            if escape:
                escape = False
                continue

            if c == "\\":
                escape = True
                continue

            if in_string:
                if c == quote:
                    in_string = False
                continue

            if c in ("'", '"'):
                in_string = True
                quote = c
                continue

            if c == "(":
                depth += 1

            elif c == ")":
                depth -= 1
                if depth == 0:
                    return i

        return -1
    
    
    def extract_directive_parameters(self, text: str) -> list[DirectiveArgument]:
        parameters = []
        current = []
        depth = 0
        in_string = False
        quote = None
        escape = False

        for c in text:
            if escape:
                current.append(c)
                escape = False
                continue

            if c == "\\":
                current.append(c)
                escape = True
                continue

            if in_string:
                current.append(c)
                if c == quote:
                    in_string = False
                continue

            if c in ("'", '"'):
                in_string = True
                quote = c
                current.append(c)
                continue

            if c == "(":
                depth += 1
                current.append(c)
                continue

            if c == ")":
                depth -= 1
                current.append(c)
                continue

            if c == "," and depth == 0:
                self._append_parameter(
                    parameters,
                    "".join(current).strip()
                )

                current.clear()
                continue

            current.append(c)

        self._append_parameter(
            parameters,
            "".join(current).strip()
        )

        return parameters
    
    
    def _append_parameter(self, parameters: list[DirectiveArgument], token: str):#Remoevr aspas de strings
        if not token:
            return

        depth = 0
        name = None
        quote = None
        value = token
        in_string = False

        for i, c in enumerate(token):
            if in_string:
                if c == quote:
                    in_string = False
                continue

            if c in ("'", '"'):
                in_string = True
                quote = c
                continue

            if c == "(":
                depth += 1
                continue

            if c == ")":
                depth -= 1
                continue

            if c == "=" and depth == 0:
                name = token[:i].strip()
                value = token[i + 1:].strip()
                break

        
        # token = token.strip()
        # if (
        #     len(token) >= 2
        #     and token[0] == token[-1]
        #     and token[0] in ("'", '"')
        # ):
        #     token = token[1:-1]
        
        value = self.expression_parser.parse(value)

        parameters.append(
            DirectiveArgument(
                name=name,
                expression =  Expression(source=value)
            )
        )
    # 
    # def parse_front_matter(file_path: str) -> Tuple[Dict[str, Any], str]:
    #     """Extracts YAML front matter and the raw Markdown body from a component file."""
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         content = file.read()
    #     return MarkdownParser.parse_front_matter_from_content(content)