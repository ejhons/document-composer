from pathlib import Path


from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.planning.loaders.resource_resolver import LocalResourceResolver


def test_resolve_relative_path(temp_workspace):
    resolver = LocalResourceResolver()
    current = ComponentConfig(
        type='external',
        source=str(temp_workspace / "memorial.md")
    )

    resolved = resolver.resolve(
        current,
        "annex.md"
    )

    assert resolved == (temp_workspace / "annex.md").as_posix()