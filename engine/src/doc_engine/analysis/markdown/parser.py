

import os
import re
from typing import Any, Dict, Tuple

import yaml

from engine.src.doc_engine.analysis.syntax.directives import DirectiveArgument, DirectiveCall, Expression
from engine.src.doc_engine.analysis.syntax.fields import FieldDefinition
from engine.src.doc_engine.analysis.syntax.parsed_markdown import ParsedMarkDown
from engine.src.doc_engine.analysis.syntax.variables import VariableReference


DIRECTIVE_START = re.compile(
    r'^\s*@([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
    re.MULTILINE
)

class MarkdownParser:
    '''
    Cumpre a função de converter o markdown em ParsedMarkdown.
    A partir do arquivo, identifica:
    - fields
    - variables
    - directives
    - metadata
    Cria o objeto ParsedMarkdown
    '''
    @staticmethod
    def read_markdown(file_path:str) -> str:
        """Extracts YAML front matter and the raw Markdown body from a component file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File {file_path} not found.')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
        
    @staticmethod
    def parse(file_path: str) -> ParsedMarkDown:
        content = MarkdownParser.read_markdown(file_path)
        
        metadata, body = MarkdownParser.parse_front_matter(content)
        fields = MarkdownParser.extract_fields(metadata)
        variables = MarkdownParser.extract_variables(body)
        directives = MarkdownParser.extract_directives(body)

        return ParsedMarkDown(
            metadata=metadata,
            fields=fields,
            variables=variables,
            directives=directives,
            body=body
        )

    @staticmethod
    def parse_front_matter(content: str) -> Tuple[Dict[str, Any], str]:
        # Match YAML block bounded by --- at the start of the file
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if match:
            front_matter_text, body_content = match.groups()
            metadata = yaml.safe_load(front_matter_text) or {}

            return metadata, body_content
        
        return {}, content

    @staticmethod
    def extract_fields(metadata: dict[str, Any]) -> dict[str, FieldDefinition]:
        # Extrai o campo 'fields' do dicionário
        fields = metadata.pop('fields')

        return {
            key: FieldDefinition(**field)
            for key, field 
            in fields.items()
            }


    @staticmethod
    def extract_variables(content: str) -> list[VariableReference]:
        """Scans raw text to discover all Jinja2 placeholders like {{ variable_name }}."""
        found_tokens = re.findall(r'\{\{\s*(.*?)\s*\}\}', content)

        return [VariableReference(name=token) for token in found_tokens]



    @staticmethod
    def extract_directives(content: str) -> list[DirectiveCall]:
        directives: list[DirectiveCall] = []
        for match in DIRECTIVE_START.finditer(content):
            name = match.group(1)
            start = match.start()
            open_paren = content.find("(", match.end() - 1)
            end = MarkdownParser._find_matching_parenthesis(
                content,
                open_paren
            )

            if end == -1:
                # posteriormente pode gerar um Diagnostic
                continue

            raw = content[start:end + 1]
            arguments_text = content[
                open_paren + 1:end
            ]

            line = content.count("\n", 0, start) + 1
            column = start - content.rfind("\n", 0, start)
            directives.append(
                DirectiveCall(
                    name=name,
                    raw=raw,
                    arguments=MarkdownParser.extract_directive_parameters(
                        arguments_text
                    ),
                    line=line,
                    column=column
                )
            )
        return directives
    
    
    @staticmethod
    def _find_matching_parenthesis(text: str, start: int) -> int:
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
    
    @staticmethod
    def extract_directive_parameters(text: str) -> list[DirectiveArgument]:
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
                MarkdownParser._append_parameter(
                    parameters,
                    "".join(current).strip()
                )

                current.clear()
                continue

            current.append(c)

        MarkdownParser._append_parameter(
            parameters,
            "".join(current).strip()
        )

        return parameters
    
    @staticmethod
    def _append_parameter(parameters: list[DirectiveArgument], token: str):#Remoevr aspas de strings
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

        parameters.append(
            DirectiveArgument(
                name=name,
                expression = Expression(source=value)
            )
        )
    # @staticmethod
    # def parse_front_matter(file_path: str) -> Tuple[Dict[str, Any], str]:
    #     """Extracts YAML front matter and the raw Markdown body from a component file."""
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         content = file.read()
    #     return MarkdownParser.parse_front_matter_from_content(content)