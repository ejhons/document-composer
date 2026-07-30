from engine.solving.inspection.implementations.markdown_inspector import BaseOjbjectInspector


class StaticInspectorRegistry():
    '''
    Relaciona o formato do arquivo com o Inspetor adequado.
    '''
    def __init__(self):
        self._inpectors: dict[str, BaseOjbjectInspector] = {}
    
    def register(
        self,
        format_data: str,
        inspector: BaseOjbjectInspector
    ):
        self._inpectors[format_data] = inspector

    def get(self, format_data) -> BaseOjbjectInspector:
        return self._inpectors.get(format_data)