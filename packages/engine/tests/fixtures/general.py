import os
from pathlib import Path
import shutil
import pytest

from dcp_engine.language.syntax.fields import InputDefinition
from dcp_engine.planning.loaders.resource_resolver import LocalResourceResolver


# @pytest.fixture
# def temp_workspace(tmp_path: Path) -> Path:
#     """
#     Cria um workspace temporário para cada teste.
#     """
#     return tmp_path


# @pytest.fixture
# def markdown_file(temp_workspace: Path):
#     def _factory(name: str, content: str):

#         path = temp_workspace / name
#         path.write_text(content, encoding="utf8")

#         return path

#     return _factory

@pytest.fixture
def resource_resolver():
    return LocalResourceResolver()


@pytest.fixture
def text_field_definition():
    return InputDefinition(
        type='text',
        name='test text field',
        description='a simple tag field text',
        default='dummy value'
    )

@pytest.fixture
def number_field_definition():
    return InputDefinition(
        type='number',
        name='test number field',
        description='a simple tag field number',
        default=1.05
    )

@pytest.fixture
def date_field_definition():
    return InputDefinition(
        type='date',
        name='test date field',
        description='a simple tag field date',
        default='dummy date'
    )

@pytest.fixture
def tabele_field_definition():
    return InputDefinition(
        type='table',
        name='test table field',
        description='a simple tag field table',
        default='dummy table'
    )

@pytest.fixture(scope="session")
def dummy_markdown():
    """
    Sets up a temporary sandbox environment for document assembly tests.
    Cleans up all generated files automatically after testing finishes.
    """
    test_dir = "storage_test"
    base_dir = os.path.join(test_dir, "components")
    
    os.makedirs(base_dir, exist_ok=True)
    
    # 1. Create a mock Markdown template component
    md_path = os.path.join(base_dir, "test_specs.md")
    md_content = (
        '---\n'
        'title: Memorial\n'
        'fields:\n'
        '   flow:\n'
        '       type: number\n'
        '       label: Vazão\n'
        '   city_idf:\n'
        '       type: text\n'
        '       label: IDF do Local\n'
        '---\n'
        '# Memorial\n'
        'Cliente: {{ client.name }}\n'
        'Vazão: {{ flow }}\n'

        '@include(\n'
        '    "tabela.xlsx",\n'
        '    optional=True\n'
        ')'
        )
    # (
    #     "---\n"
    #     "fields_definition:\n"
    #     "  project_title:\n"
    #     "    data_type: 'text'\n"
    #     "    label: 'Nome do Projeto'\n"
    #     "---\n"
    #     "# SECTION: {{ project_title }}\n\n"
    #     "```mermaid\n"
    #     "graph LR\n"
    #     "    A --> B\n"
    #     "```\n"
    # )
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # Yield control to the test function
    yield md_path

    # Teardown phase: Delete temporary sandbox data execution files
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
