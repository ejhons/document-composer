import pytest

from dcp_engine.language.directives.implementations.include_directive import IncludeDirectiveHandler
from dcp_engine.language.directives.registry import DirectiveRegistry
from dcp_engine.language.syntax.directives import DirectiveArgument, DirectiveCall


# from doc_engine.models.directives import (
#     DirectiveCall,
#     DirectiveArgument
# )


@pytest.fixture
def directive_registry():
    registry = DirectiveRegistry()
    registry.register(
        IncludeDirectiveHandler()
    )
    return registry

@pytest.fixture
def include_directive():

    return DirectiveCall(
        name="include",
        raw='@include("cover.md")',
        arguments=[
            DirectiveArgument(
                value="cover.md"
            )
        ],
        line=1,
        column=1
    )

@pytest.fixture
def include_dynamic():
    return DirectiveCall(
        name="include",
        raw='@include("{{img}}")',
        arguments=[
            DirectiveArgument(
                value="{{img}}"
            )
        ],
        line=1,
        column=1
    )

@pytest.fixture
def include_optional():
    return DirectiveCall(
        name="include",
        raw='@include("cover.md", optional=True)',
        arguments=[
            DirectiveArgument(
                value="cover.md"
            ),
            DirectiveArgument(
                name="optional",
                value="True"
            )
        ],
        line=1,
        column=1
    )

