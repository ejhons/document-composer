import pytest
from pydantic import ValidationError

from dcp_engine.language.manifests.recipe import ComponentConfig, RecipeManifest, StyleConfig



# Inferência de DOCX
def test_should_infer_docx_file_format():
    component = ComponentConfig(
        type="external",
        source="arquivo.docx",
    )

    assert component.file_format == "docx"

# Infere MARKDOwN
def test_should_infer_markdown_file_format():
    component = ComponentConfig(
        type="external",
        source="template.md",
    )

    assert component.file_format == "md"

# Infere HTML
def test_should_infer_html_file_format():
    component = ComponentConfig(
        type="external",
        source="pagina.html",
    )

    assert component.file_format == "html"

# Infere Imagens
@pytest.mark.parametrize("filename", [
    "imagem.png",
    "imagem.jpg",
    "imagem.jpeg",
    "imagem.webp",
    "imagem.svg",
])
def test_should_infer_image_file_format(filename):
    component = ComponentConfig(
        type="external",
        source=filename,
    )

    assert component.file_format == "image"

# Deve respeitar file_format informado
def test_should_not_override_explicit_file_format():
    component = ComponentConfig(
        type="external",
        source="arquivo.qualquer",
        file_format="pdf",
    )

    assert component.file_format == "pdf"


# Deve lançar erro para extensão desconhecida
def test_should_raise_when_extension_is_unknown():
    with pytest.raises(ValidationError):
        ComponentConfig(
            type="external",
            source="arquivo.xyz",
        )
# Template é sempre solvable
def test_template_should_be_solvable():
    component = ComponentConfig(
        type="template",
        source="template.docx",
    )

    assert component.solvable is True

# Markdown é sempre solvable
def test_markdown_should_be_solvable():
    component = ComponentConfig(
        type="external",
        source="arquivo.md",
    )

    assert component.solvable is True

# PDF externo não é solvable
def test_style_config_defaults():
    style = StyleConfig()

    assert style.include_header is True
    assert style.include_footer is True
    assert style.primary_color == "#003366"
    assert style.header_text_left == "Memorial Descritivo Técnico"

# RecipeManifest deve possuir target_format padrão
def test_recipe_manifest_default_target_format():
    manifest = RecipeManifest(
        recipe_name="Teste",
        version="1.0",
        style=StyleConfig(),
        components=[],
    )

    assert manifest.target_format == "docx"
    assert manifest.inputs == {}