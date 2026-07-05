import pytest

from engine.frontend.directives.implementations.include_directive import IncludeDirectiveHandler
from engine.frontend.directives.registry import DirectiveRegistry
from engine.common.models.directives import DirectiveResolutionResult


class FakeMarkdownInspector:
    def __init__(self, inspection):
        self.inspection = inspection

    def inspect(self, component):
        return self.inspection
    
class FakeInspectorRegistry:
    def __init__(self, inspector):
        self.inspector = inspector

    def get(self, extension):
        return self.inspector
    
class FakeDirectiveHandler:
    directive_name = "include"

    def __init__(self):
        self.called = False

    def resolve(
        self,
        graph,
        node,
        directive
    ):
        self.called = True
        return DirectiveResolutionResult()