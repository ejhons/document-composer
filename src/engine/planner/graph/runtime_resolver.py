from typing import Any

from jinja2 import Environment, StrictUndefined, Undefined
from engine.planner.graph.graph import RecipeGraph
from engine.runtime.context import ExecutionContext
from engine.frontend.syntax.expressions.parser import ExpressionParser
from engine.runtime.result import RuntimeResolutionResult
from engine.planner.graph.component_node import ComponentNode
from engine.common.utils.generator import IdGenerator

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
        for node in graph.nodes.values():
            self.resolve_node(node, context)

    def resolve_node(
        self,
        node: ComponentNode,
        context: ExecutionContext
    ) -> None: 
        if node.component.file_format != 'md':
            return
        
        resolution = node.resolution
        if not resolution.content:
            resolution.content = node.inspection.body

        original_content = resolution.content
        content = original_content
        placeholders: dict[str, str] = {}
        resolution.resolved_inputs.clear()

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

            if not unresolved:
                continue

            placeholder = (
                "__DOC_COMPOSER_PLACEHOLDER__"
                + IdGenerator.generate()
                + "__"
            )

            placeholders[placeholder] = variable.raw

            content = content.replace(
                variable.raw,
                placeholder
            )

        # Renderiza somente as expressões resolvíveis
        template = self._environment.from_string(content)
        rendered = template.render(
            **resolution.resolved_inputs
            )

        # Restaura expressões pendentes
        for placeholder, raw in placeholders.items():
            rendered = rendered.replace(placeholder, raw)

        resolution.changed |= rendered != original_content
        resolution.content = rendered
        


        # if node.inspection is None:
        #     return result
        # # Cria um objeto jinja
        # template = self._environment.from_string(node.inspection.body)
        # # Vasculha as variáveis presentes no template
        # ast = self._environment.parse(node.inspection.body)
        # undeclared = meta.find_undeclared_variables(ast)

        # missing = {}
        # inputs = dict(context.inputs)
        # unique_variables = node.inspection.unique_variables

        # # Cria os placeholders para realizar futura substituição
        # placeholders = {
        #     IdGenerator.generate():name
        #     for name in undeclared
        #     if name not in unique_variables
        # }


        # for variable in node.inspection.variables:
        #     if context.values.get(variable.name) is None:
        #         placeholder = IdGenerator.generate()
        #         placeholders[placeholder] = variable.name

        #         inputs = inputs.replace(
        #             variable.raw,
        #             placeholder
        #         )
        #         placeholders[placeholder] = variable.raw


        # for variable in node.inspection.unique_variables():
        #     value = context.values.get(variable.name)

        #     if value is None:
        #         missing[variable.name] = ""
        #         result.pending_inputs.add(variable.name)

        # render_context = {**context.values, **missing}

        # rendered = template.render(render_context)

        # if rendered != node.resolved_content:

        #     node.resolved_content = rendered
        #     node.resolved = False
        #     result.changed = True

        # else:
        #     node.resolved = True

        
        # for placeholder, raw in placeholders.items():
        #     content = content.replace(
        #         placeholder,
        #         raw
        #     )

        # return result