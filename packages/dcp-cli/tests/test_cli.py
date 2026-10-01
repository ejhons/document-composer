from dcp_cli.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_without_arguments_shows_help():
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Document Composer command-line interface." in result.stdout


def test_build_help():
    result = runner.invoke(app, ["build", "--help"])

    assert result.exit_code == 0
    assert "workspace" in result.stdout.lower()
    assert "--format" in result.stdout