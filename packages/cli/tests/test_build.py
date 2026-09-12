from dcp_cli.cli import app
from pathlib import Path
from unittest.mock import Mock
from typer.testing import CliRunner



runner = CliRunner()


def test_build_help():
    result = runner.invoke(app, ["build", "--help"])

    assert result.exit_code == 0
    assert "workspace" in result.stdout.lower()

def test_build_uses_current_directory():
    result = runner.invoke(app, ["build"])

    assert result.exit_code == 0


def test_build_uses_current_directory_by_default(
    monkeypatch,
    tmp_path: Path,
):
    use_case = Mock()
    use_case.compile.return_value = Mock(
        output_path=tmp_path / "output.pdf"
    )

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "dcp_application.use_cases.build_document.BuildDocument",
        # "dcp_application.commands.build.build",
        lambda **kwargs: use_case,
    )

    result = runner.invoke(app, ["build"])

    # assert result.exit_code == 0

    use_case.execute.assert_called_once_with(
        root=tmp_path,
        target_format="default",
    )


def test_build_accepts_explicit_root(
    monkeypatch,
    tmp_path: Path,
):
    project = tmp_path / "project"
    project.mkdir()

    use_case = Mock()
    use_case.execute.return_value = Mock(
        output_path=project / "output.pdf"
    )

    monkeypatch.setattr(
        "doc_composer_cli.commands.build.BuildDocument",
        lambda **kwargs: use_case,
    )

    result = runner.invoke(
        app,
        ["build", str(project)],
    )

    assert result.exit_code == 0

    use_case.execute.assert_called_once_with(
        root=project,
        target_format="default",
    )


def test_build_accepts_target_format(
    monkeypatch,
    tmp_path: Path,
):
    use_case = Mock()
    use_case.execute.return_value = Mock(
        output_path=tmp_path / "output.pdf"
    )

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "doc_composer_cli.commands.build.BuildDocument",
        lambda **kwargs: use_case,
    )

    result = runner.invoke(
        app,
        ["build", "--format", "pdf"],
    )

    assert result.exit_code == 0

    use_case.execute.assert_called_once_with(
        root=tmp_path,
        target_format="pdf",
    )


def test_build_reports_success(
    monkeypatch,
    tmp_path: Path,
):
    output = tmp_path / "output.pdf"

    use_case = Mock()
    use_case.execute.return_value = Mock(
        output_path=output
    )

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "doc_composer_cli.commands.build.BuildDocument",
        lambda **kwargs: use_case,
    )

    result = runner.invoke(app, ["build"])

    assert result.exit_code == 0
    assert "Document successfully built." in result.stdout
    assert str(output) in result.stdout


def test_build_reports_failure(
    monkeypatch,
    tmp_path: Path,
):
    use_case = Mock()
    use_case.execute.side_effect = RuntimeError("Compilation failed")

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "doc_composer_cli.commands.build.BuildDocument",
        lambda **kwargs: use_case,
    )

    result = runner.invoke(app, ["build"])

    assert result.exit_code == 1
    assert "Build failed" in result.stdout
    assert "Compilation failed" in result.stdout