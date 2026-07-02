from engine.src.doc_engine.analysis.directives.handlers.base import BaseDirectiveHandler


class DirectiveRegistry:
    def __init__(self):
        self._handlers = {}

    def register(
        self,
        handler: BaseDirectiveHandler
    ):
        self._handlers[handler.directive_name] = handler

    def get(self, name: str) -> BaseDirectiveHandler | None:

        return self._handlers.get(name)