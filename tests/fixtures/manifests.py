import pytest
from engine.common.models.recipe import ComponentConfig, RecipeManifest, StyleConfig


@pytest.fixture
def recipe_manifest():
    return RecipeManifest(
        recipe_name="Teste",
        version="1.0",
        style=StyleConfig(),
        target_format="docx",
        components=[
            ComponentConfig(
                type="template",
                source="cover.md",
                file_format='md'
            )
        ]
    )