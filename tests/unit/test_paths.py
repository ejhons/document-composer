from engine.frontend.manifests.recipe import ComponentConfig



def test_resolve_relative_path(temp_workspace):
    

    current = ComponentConfig(
        source=str(temp_workspace / "memorial.md"),
        ...
    )

    resolved = resolver.resolve(
        current,
        "annex.md"
    )

    assert resolved == str(temp_workspace / "annex.md")