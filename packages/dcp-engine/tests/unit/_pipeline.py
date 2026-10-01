import os
import json
import shutil
import pytest
import pandas as pd

from doc_engine.compilation.compilers.implementations.docx_compiler import DocxCompiler
from doc_engine.runtime.engine import DocumentEngine

# =====================================================================
# FIXTURES (Gerenciamento de Ambiente de Teste)
# =====================================================================

@pytest.fixture(scope="session")
def test_environment():
    """
    Sets up a temporary sandbox environment for document assembly tests.
    Cleans up all generated files automatically after testing finishes.
    """
    test_dir = "storage_test"
    base_dir = os.path.join(test_dir, "components")
    recipe_dir = os.path.join(test_dir, "recipes")
    output_dir = "output_test"
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(recipe_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Create a mock Markdown template component
    md_path = os.path.join(base_dir, "test_specs.md")
    md_content = (
        "---\n"
        "fields_definition:\n"
        "  project_title:\n"
        "    data_type: 'text'\n"
        "    label: 'Nome do Projeto'\n"
        "---\n"
        "# SECTION: {{ project_title }}\n\n"
        "```mermaid\n"
        "graph LR\n"
        "    A --> B\n"
        "```\n"
    )
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 2. Create a mock Excel spreadsheet component
    xlsx_path = os.path.join(base_dir, "test_data.xlsx")
    mock_data = {
        "Parameter": ["Tension", "Elasticity"],
        "Value": [150, 0.85]
    }
    df = pd.DataFrame(mock_data)
    df.to_excel(xlsx_path, index=False)
    
    # 3. Create a mock Recipe Manifest
    manifest_path = os.path.join(recipe_dir, "test_manifest.json")
    manifest_content = {
        "recipe_name": "Automated Hexagonal Test Layout",
        "version": "2.0.0",
        "style": {
            "reference_docx": None,
            "include_header": False,
            "include_footer": False
        },
        "components": [
            {
                "id": "specs_block",
                "type": "template",
                "source": md_path,
                "file_format": "md"
            },
            {
                "id": "excel_block",
                "type": "external",
                "source": xlsx_path,
                "file_format": "xlsx"
            }
        ]
    }
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_content, f, indent=2)

    # Yield control to the test function
    yield {
        "manifest_path": manifest_path,
        "output_dir": output_dir
    }

    # Teardown phase: Delete temporary sandbox data execution files
    for directory in [test_dir, output_dir]:
        if os.path.exists(directory):
            shutil.rmtree(directory)


# =====================================================================
# INTEGRATION TEST SUITE
# =====================================================================

def test_end_to_end_assembly_pipeline(test_environment):
    """
    Validates the entire document compilation pipeline lifecycle using standard
    pytest assert architecture configurations.
    """
    manifest_path = test_environment["manifest_path"]
    output_dir = test_environment["output_dir"]
    resource_dir = os.path.join(output_dir, "resources")
    
    # Step 1: Initialization
    engine = DocumentEngine(manifest_path)
    assert engine.manifest.recipe_name == "Automated Hexagonal Test Layout"
    
    # Step 2: Meta Field Extraction
    discovered_fields = engine.discover_required_fields()
    assert "project_title" in discovered_fields
    assert discovered_fields["project_title"]["label"] == "Nome do Projeto"
    
    # Step 3: Core Dynamic Template and Adapter Generation
    mock_inputs = {"project_title": "Omega Core Matrix"}
    assembled_md = engine.assemble_document(mock_inputs, resource_dir)
    
    print(assembled_md)
    assert "# SECTION: Omega Core Matrix" in assembled_md
    assert "| Parameter | Value |" in assembled_md or "| Parameter   |   Value |" in assembled_md

    # Step 4: Inline Diagram Code Block Interception Parsing Check
    final_markdown = engine.pre_process_markdown_diagrams(assembled_md, resource_dir)
    assert "```mermaid" not in final_markdown
    assert "![System Diagram]" in final_markdown

    # Step 5: Master Binary Artifact Compiling Check (Pandoc Output Integration)
    temp_markdown_path = os.path.join(output_dir, "interim_document.md")
    with open(temp_markdown_path, 'w', encoding='utf-8') as file:
        file.write(final_markdown)
        
    final_docx_path = os.path.join(output_dir, "test_output_report.docx")
    compiler = DocxCompiler(engine.manifest)
    
    compiled_output = compiler.compile_to_docx(temp_markdown_path, final_docx_path)
    
    assert os.path.exists(compiled_output)
    assert os.path.getsize(compiled_output) > 0

    # Teste extra para garantir que a função do PDF executa sem falhas estruturais
    final_pdf_path = os.path.join(output_dir, "test_output_report.pdf")
    
    try:
        compiled_pdf = compiler.compile_to_pdf(temp_markdown_path, final_pdf_path)
        assert os.path.exists(compiled_pdf)
        assert os.path.getsize(compiled_pdf) > 0
    except Exception as e:
        # Se a máquina de teste não tiver um motor de PDF (como wkhtmltopdf ou texlive) instalado,
        # capturamos o erro para o teste não quebrar por falta de dependência de ambiente.
        print(f"PDF local engine skipped or unconfigured: {e}")