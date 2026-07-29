import re
from typing import Any, Dict, Optional, Tuple
from numpy import block
from pydantic import Field
from pydantic import BaseModel
from engine.frontend.parser import MarkdownParser
from engine.frontend.syntax.expressions.parser import ExpressionParser
from engine.frontend.syntax.fields import InputDefinition
from engine.frontend.syntax.directives import DirectiveArgument, DirectiveCall, TextSpan
from engine.frontend.syntax.markdown.atom import MarkdownAtom, MarkdownDirective, MarkdownFragment
from engine.frontend.syntax.inputs import InputReference

        
class AtomizedMarkdown(BaseModel):
    body: Optional[str] = None
    blocks: list[MarkdownAtom] = Field(default_factory=list)

    @property
    def assembled_content(self):
        '''
        Markdown completo a partir dos fragmentos.
        '''
        return [
            block.to_markdown()
            for block  in self.blocks
        ]



    
    # def parse_front_matter(self, content: str) -> Tuple[Dict[str, Any], str]:
    #     # Match YAML block bounded by --- at the start of the file
    #     match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    #     if match:
    #         front_matter_text, body_content = match.groups()
    #         metadata = yaml.safe_load(front_matter_text) or {}

    #         return metadata, body_content
        
    #     return {}, content

    
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

    #         line_start = content.count("\n", 0, start) + 1
    #         column_start = start - content.rfind("\n", 0, start)
    #         line_end = content.count("\n", 0, end) + 1
    #         column_end = end - content.rfind("\n", 0, end)

    #         directives.append(
    #             DirectiveCall(
    #                 index=idx,
    #                 name=name,
    #                 raw=raw,
    #                 arguments=self.extract_directive_parameters(
    #                     arguments_text
    #                 ),
    #                 start=TextSpan(
    #                     line=line_start, 
    #                     column=column_start, 
    #                     index=start
    #                 ),
    #                 end=TextSpan(
    #                     line=line_end,
    #                     column=column_end,
    #                     index=end
    #                 )
    #                 # line=line,
    #                 # column=column
    #             )
    #         )
    #     return directives  
    
    # def _find_matching_parenthesis(self, text: str, start: int) -> int:
    #     depth = 0
    #     in_string = False
    #     quote = None
    #     escape = False

    #     for i in range(start, len(text)):
    #         c = text[i]

    #         if escape:
    #             escape = False
    #             continue

    #         if c == "\\":
    #             escape = True
    #             continue

    #         if in_string:
    #             if c == quote:
    #                 in_string = False
    #             continue

    #         if c in ("'", '"'):
    #             in_string = True
    #             quote = c
    #             continue

    #         if c == "(":
    #             depth += 1

    #         elif c == ")":
    #             depth -= 1
    #             if depth == 0:
    #                 return i

    #     return -1
    
    
    # def extract_directive_parameters(self, text: str) -> list[DirectiveArgument]:
    #     parameters = []
    #     current = []
    #     depth = 0
    #     in_string = False
    #     quote = None
    #     escape = False

    #     for c in text:
    #         if escape:
    #             current.append(c)
    #             escape = False
    #             continue

    #         if c == "\\":
    #             current.append(c)
    #             escape = True
    #             continue

    #         if in_string:
    #             current.append(c)
    #             if c == quote:
    #                 in_string = False
    #             continue

    #         if c in ("'", '"'):
    #             in_string = True
    #             quote = c
    #             current.append(c)
    #             continue

    #         if c == "(":
    #             depth += 1
    #             current.append(c)
    #             continue

    #         if c == ")":
    #             depth -= 1
    #             current.append(c)
    #             continue

    #         if c == "," and depth == 0:
    #             self._append_parameter(
    #                 parameters,
    #                 "".join(current).strip()
    #             )

    #             current.clear()
    #             continue

    #         current.append(c)

    #     self._append_parameter(
    #         parameters,
    #         "".join(current).strip()
    #     )

    #     return parameters
    
    
    # def _append_parameter(self, parameters: list[DirectiveArgument], token: str):#Remoevr aspas de strings
    #     if not token:
    #         return

    #     depth = 0
    #     name = None
    #     quote = None
    #     value = token
    #     in_string = False

    #     for i, c in enumerate(token):
    #         if in_string:
    #             if c == quote:
    #                 in_string = False
    #             continue

    #         if c in ("'", '"'):
    #             in_string = True
    #             quote = c
    #             continue

    #         if c == "(":
    #             depth += 1
    #             continue

    #         if c == ")":
    #             depth -= 1
    #             continue

    #         if c == "=" and depth == 0:
    #             name = token[:i].strip()
    #             value = token[i + 1:].strip()
    #             break

        
    #     # token = token.strip()
    #     # if (
    #     #     len(token) >= 2
    #     #     and token[0] == token[-1]
    #     #     and token[0] in ("'", '"')
    #     # ):
    #     #     token = token[1:-1]
        
    #     value = self.expression_parser.parse(value)

    #     parameters.append(
    #         DirectiveArgument(
    #             name=name,
    #             expression =  Expression(source=value)
    #         )
    #     )
