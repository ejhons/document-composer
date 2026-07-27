from pathlib import Path
from unittest.mock import Mock

import pytest

from engine.compilation.module import CompilationModule
from engine.execution.execution_session import ExecutionSession

@pytest.fixture
def compiler():
    return Mock()


@pytest.fixture
def registry(compiler):
    registry = Mock()
    registry.get_compiler.return_value = compiler
    return registry


@pytest.fixture
def module(registry):
    return CompilationModule(registry)


@pytest.fixture
def session():
    session = Mock(spec=ExecutionSession)

    session.manifest.target_format = "docx"
    session.fragmented_markdown = Mock()

    return session


def test_compile_should_get_compiler(
    module,
    registry,
    session,
    tmp_path,
):
    module.compile(
        session=session,
        output_path=tmp_path / "output.docx",
    )

    registry.get_compiler.assert_called_once_with(
        "docx"
    )


def test_compile_should_call_compiler(
    module,
    compiler,
    session,
    tmp_path,
):
    output = tmp_path / "document.docx"

    module.compile(
        session=session,
        output_path=output,
    )

    compiler.compile.assert_called()


def test_compile_should_forward_fragmented_document(
    module,
    compiler,
    session,
    tmp_path,
):
    output = tmp_path / "result.docx"

    module.compile(
        session=session,
        output_path=output,
    )

    compiler.compile.assert_called_with(
        fragmented=session.fragmented_markdown,
        output_path=output,
    )


def test_compile_should_return_compiler_result(
    module,
    compiler,
    session,
    tmp_path,
):
    expected = Path("generated.docx")

    compiler.compile.return_value = expected

    result = module.compile(
        session=session,
        output_path=tmp_path / "result.docx",
    )

    assert result == expected


def test_compile_should_propagate_exception(
    module,
    compiler,
    session,
    tmp_path,
):
    compiler.compile.side_effect = RuntimeError(
        "Compilation failed"
    )

    with pytest.raises(RuntimeError):
        module.compile(
            session=session,
            output_path=tmp_path / "out.docx",
        )

def compile(
    self,
    session: ExecutionSession,
    output_path,
):
    compiler = self.compilers.get_compiler(
        session.manifest.target_format
    )

    return compiler.compile(
        fragmented=session.fragmented_markdown,
        output_path=output_path,
    )


