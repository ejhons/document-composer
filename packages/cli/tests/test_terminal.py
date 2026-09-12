import typer
from unittest.mock import Mock

from dcp_cli.interaction.terminal import TerminalInteraction
from dcp_engine.solving.resolution.resolution_collector import PendingResolution

def test_terminal_resolves_pending_values(monkeypatch):
    prompt = Mock(side_effect=["Everton", "Fortaleza"])

    monkeypatch.setattr(
        typer,
        "prompt",
        prompt,
    )

    request_name = Mock()
    request_name.name = "author"
    request_name.description = "Document author"
    request_name.default = None

    request_city = Mock()
    request_city.name = "city"
    request_city.description = "Project city"
    request_city.default = "Fortaleza"

    interaction = TerminalInteraction()

    result = interaction.resolve(
        [request_name, request_city]
    )

    assert result == {
        "author": "Everton",
        "city": "Fortaleza",
    }

    assert prompt.call_count == 2


def test_terminal_resolves_empty_pending():
    interaction = TerminalInteraction()

    result = interaction.resolve(PendingResolution(
        resolved=False,
        unchanged=True
    ))

    assert result == {}

def test_terminal_passes_description_and_default(monkeypatch):
    prompt = Mock(return_value="Fortaleza")

    monkeypatch.setattr(
        typer,
        "prompt",
        prompt,
    )

    request = Mock()
    request.name = "city"
    request.description = "Project city"
    request.default = "Fortaleza"

    interaction = TerminalInteraction()

    result = interaction.resolve([request])

    assert result == {
        "city": "Fortaleza",
    }

    prompt.assert_called_once_with(
        "city (Project city)",
        default="Fortaleza",
        show_default=True,
    )