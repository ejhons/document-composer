from typing import Any
from jinja2 import Environment, StrictUndefined, Undefined

from dcp_engine.language.syntax.expressions.parser import ExpressionParser
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.common.generator import IdGenerator
from dcp_engine.planning.graph.component_node import ComponentNode


class PreserveUndefined(Undefined):
    def __str__(self):
        return "{{" + self._undefined_name + "}}"
    __repr__ = __str__

class RuntimeResolver:
    '''
    Recebe ComponentNode e ExecutionContext
    Modifica a resolution apenas.
    '''
    def __init__(self):
        self._environment = Environment(
            undefined=StrictUndefined,
            autoescape=False
        )

    def resolve(
        self,
        graph: RecipeGraph,
        context: ExecutionContext
    ):
        # print(type(graph))
        for node in graph.nodes.values():
            self.resolve_node(node, context)

    def resolve_node(
        self,
        node: ComponentNode,
        context: ExecutionContext
    ) -> None: 
        # if node.component.file_format != 'md':
        #     return
        if node.inspection is None:
            return
        
        resolution = node.resolution
        if not resolution.content:
            resolution.content = node.inspection.body
            
        # content = node.inspection.body
        unresolved_variables = []

        # original_content = resolution.content
        # placeholders: dict[str, str] = {}
        # Descobre quais expressões NÃO podem ser avaliadas
        for variable in node.inspection.variables:
            required_inputs = ExpressionParser.discover_inputs(variable.name)
            unresolved = False

            for input_name in required_inputs:
                value = context.inputs.get(input_name)
                if value is None:
                    unresolved = True
                    break
                resolution.resolved_inputs[input_name] = value

            if unresolved:
                unresolved_variables.append(variable)
        
        rendered = self._render_with_placeholders(
            content=node.inspection.body,
            resolved_inputs=resolution.resolved_inputs,
            unresolved_variables=unresolved_variables,
        )

        resolution.changed = rendered != resolution.content
        resolution.content = rendered


    def _render_with_placeholders(
        self,
        content: str,
        resolved_inputs: dict[str, Any],
        unresolved_variables: list,
    ) -> str:
        placeholders: dict[str, str] = {}

        for variable in unresolved_variables:
            placeholder = (
                "__DOC_COMPOSER_PLACEHOLDER__"
                f"{IdGenerator.generate()}__"
            )

            placeholders[placeholder] = variable.raw
            content = content.replace(variable.raw, placeholder)

        template = self._environment.from_string(content)
        rendered = template.render(**resolved_inputs)

        for placeholder, raw in placeholders.items():
            rendered = rendered.replace(placeholder, raw)

        return rendered
    

        #         continue

        #     placeholder = (
        #         "__DOC_COMPOSER_PLACEHOLDER__"
        #         + IdGenerator.generate()
        #         + "__"
        #     )

        #     placeholders[placeholder] = variable.raw

        #     content = content.replace(
        #         variable.raw,
        #         placeholder
        #     )

        # # Renderiza somente as expressões resolvíveis
        # template = self._environment.from_string(content)
        # rendered = template.render(**resolution.resolved_inputs)

        # # Restaura expressões pendentes
        # for placeholder, raw in placeholders.items():
        #     rendered = rendered.replace(placeholder, raw)