from jinja2 import Environment, meta

class ExpressionParser():
    _environment = Environment()

    @classmethod
    def parse(cls, token:str) -> str:        
        token = token.strip()
        if (
            len(token) >= 2
            and token[0] == token[-1]
            and token[0] in ("'", '"')
        ):
            token = token[1:-1]

        return token
    
    @classmethod
    def discover_inputs(cls, expression: str) -> set[str]:

        ast = cls._environment.parse(
            "{{ " + expression + " }}"
        )

        return meta.find_undeclared_variables(ast)
    