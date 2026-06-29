import logging
from rich.logging import RichHandler
from traceback import print_exc
from engine.src.doc_engine.core.pipeline import DocumentPipeline

def configure_structured_logging():
    """Initializes standard application stream loggers with consistent formats."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

def run_mvp_cli_application():
    configure_structured_logging()
    
    logger = logging.getLogger("doc_engine.cli")
    logger.info("Starting Technical Documentation Assembly Engine Console UI Context...")

    root_path = 'engine/src/doc_engine/'
    manifest_target = root_path + "storage/recipes/engineering_manifest.json"
    
    try:
        # Initialize the decoupled high-level Pipeline abstraction abstraction layer
        pipeline = DocumentPipeline(manifest_path=manifest_target, output_root=root_path + "output")
        
        # Step 1: Handle system environment setup
        if not pipeline.setup_environment():
            logger.critical("Aborting document pipeline pipeline. Environment configuration failure.")
            return

        # Step 2: Dynamic input fields parameter extraction scan
        form_fields = pipeline.scan_fields()
        
        # Step 3: Map user console data collection loops
        captured_data = {}
        if form_fields:
            print("\n" + "="*40)
            print("  MANDATORY PROJECT DATA SPECIFICATIONS")
            print("="*40)
            for field_id, properties in form_fields.items():
                label = properties.get("label", field_id)
                data_type = properties.get("data_type", "text")
                
                user_value = input(f"-> {label} [{data_type}]: ")
                captured_data[field_id] = user_value
            print("="*40 + "\n")
        else:
            logger.info("No interactive token fields detected across source layout blocks.")

        # Step 4: Run compilation block orchestration
        pipeline.run(input_data=captured_data)
        
    except Exception as general_error:
        print_exc()#general_error)
        logger.error(f"Application runtime failed to process target sequence pipeline: {general_error}")

if __name__ == "__main__":
    run_mvp_cli_application()

# import os
# import pypandoc
# from engine.src.doc_engine.core.engine import DocumentEngine
# from engine.src.doc_engine.core.models import AssembledManifest

# def run_mvp_pipeline():
#     print("=" * 65)
#     print("    TECHNICAL DOCUMENTATION ASSEMBLY ENGINE - CORE MVP")
#     print("=" * 65)

#     root = 'engine/src/doc_engine/'

#     manifest_path = root + "storage/recipes/engineering_manifest.json"
    
#     if not os.path.exists(manifest_path):
#         print(f"[Error] Assembly recipe not found at: {manifest_path}")
#         print("Please configure your seed assets under storage/ paths first.")
#         return


#     # Adicionar o download do Pandoc aqui
#     print("[Setup] Checking for Pandoc installation...")
#     try:
#         pypandoc.get_pandoc_path()
#         print("[Setup] Pandoc found.")
#         pandoc_path = pypandoc.get_pandoc_path()
#         pandoc_version = pypandoc.get_pandoc_version()
#         debug_pandoc_path = pypandoc.get_pandoc_path()
#         debug_pandoc_version = pypandoc.get_pandoc_version()
#         print(f"[Setup] Pandoc found at: {pandoc_path}")
#         print(f"[Setup] Pandoc version: {'.'.join(map(str, pandoc_version))}")
#         import subprocess
#         try:
#             result = subprocess.run([debug_pandoc_path, '--version'], capture_output=True, text=True, check=True)
#             print("Direct Pandoc --version output:\n", result.stdout)
#         except Exception as e:
#             print(f"Could not run pandoc --version directly: {e}")
#             print("This might indicate an issue with the executable or permissions.")
#         # Opcional: Verificar se a versão é suficientemente nova (ex: 2.0 ou superior)
#         if int(pandoc_version[0]) < 2: # Se a versão principal for menor que 2
#             print("[Warning] Detected Pandoc version is old. Attempting to download a newer version.")
#             pypandoc.download_pandoc(force_dl=True)
#             pandoc_version = pypandoc.get_pandoc_version() # Re-check version after download
#             print(f"[Setup] New Pandoc version after download: {'.'.join(map(str, pandoc_version))}")

#     except Exception as e:
#         print(str(e))
#         print("[Setup] Pandoc not found. Attempting to download...")
#         try: 
#             pypandoc.download_pandoc(force_dl=True) # Força o download
#             pandoc_version = pypandoc.get_pandoc_version()
#             print(f"[Setup] Pandoc downloaded successfully. Version: {'.'.join(map(str, pandoc_version))}")
#         except Exception as e:
#             print(f"[Setup Error] Failed to download Pandoc: {e}")
#             print("Please install Pandoc manually or check your internet connection.")
#             return
        
#     # 1. Initialize Document Engine
#     engine = DocumentEngine(manifest_path)
#     print(f"Loaded Recipe: {engine.manifest.recipe_name} (v{engine.manifest.version})\n")

#     # 2. Extract Fields Map
#     print("[Scanning] Extracting variables and metadata from components...")
#     form_fields = engine.discover_required_fields()
    
#     # 3. Dynamic Console Form Generation
#     captured_data = {}
#     if form_fields:
#         print("\n--- Mandatory Project Data Specifications ---")
#         for field_id, properties in form_fields.items():
#             label = properties.get("label", field_id)
#             data_type = properties.get("data_type", "text")
            
#             user_value = input(f"-> {label} [{data_type}]: ")
#             captured_data[field_id] = user_value
#     else:
#         print("\n[Info] No dynamic parameters detected across components.")

#     # 4. Content Compilation Loop
#     print("\n[Assembling] Stitching blocks and executing engine parsing...")
#     assembled_markdown = engine.assemble_document(captured_data, output_resource_dir=root+"output/resources")

#     # 5. Output Temporary Markdown Management
#     output_dir = root +  "output"
#     os.makedirs(output_dir, exist_ok=True)
#     # Este é o seu arquivo Markdown autônomo, equivalente ao .js transpilado do TypeScript!
#     dist_markdown_path = os.path.join(output_dir, "document_distribution.md")
#     with open(dist_markdown_path, 'w', encoding='utf-8') as file:
#         file.write(final_markdown)

#     # Criamos o Manifesto Final de Entrega (Metadata de Auditoria)
#     import datetime
    
#     # Varre a pasta de recursos para mapear o que o motor gerou (como os diagramas png)
#     resource_dir = os.path.join(output_dir, "resources")
#     generated_assets = []
#     if os.path.exists(resource_dir):
#         generated_assets = [os.path.join(resource_dir, f) for f in os.listdir(resource_dir)]

#     final_manifest = AssembledManifest(
#         document_name=engine.manifest.recipe_name,
#         generation_timestamp=datetime.datetime.now().isoformat(),
#         engine_version=engine.manifest.version,
#         target_format=format_type,
#         injected_parameters=captured_data,
#         compiled_markdown_source=dist_markdown_path,
#         generated_resources=generated_assets
#     )

#     # Salva o arquivo JSON do manifesto de entrega ao lado do Markdown final
#     manifest_delivery_path = os.path.join(output_dir, "document_manifest_delivery.json")
#     with open(manifest_delivery_path, 'w', encoding='utf-8') as file:
#         file.write(final_manifest.model_dump_json(indent=2))

#     print(f"[Transpiler] Intermediate Markdown source generated at: {dist_markdown_path}")
#     print(f"[Transpiler] Delivery Manifest log written to: {manifest_delivery_path}")

#     # 4.5. Diagram Interception Phase (NEW STEP)
#     print("[Processing] Intercepting code structures and rendering diagrams...")
#     resources_dir = os.path.join(output_dir, "resources")
#     final_markdown = engine.pre_process_markdown_diagrams(assembled_markdown, resources_dir)
    
#     # temp_markdown_path = os.path.join(output_dir, "assembled_document.md")
#     # with open(temp_markdown_path, 'w', encoding='utf-8') as file:
#     #     file.write(final_markdown)

#     # 6. Stylized Binary Compilation Phase (Pandoc Pipeline)
#     # final_docx_path = os.path.join(output_dir, "final_report.docx")
#     # compiler = DocumentCompiler(engine.manifest)
#     # compiler = engine.compiler_registry.get_compiler(format_type)
#     format_type = engine.manifest.target_format  # Resgata do JSON (docx ou pdf)
    
#     final_output_path = os.path.join(output_dir, f"final_report.{format_type}")
    
#     try:
#         # O motor recupera o adaptador correto baseado na string do formato e executa o contrato
#         compiler = engine.compiler_registry.get_compiler(format_type)
#         compiler.compile(dist_markdown_path, final_output_path, engine.manifest)
#         # compiler.compile(temp_markdown_path, final_output_path, engine.manifest)
        
#         # Pós-processamento condicional exclusivo do ecossistema do Word
#         if format_type == "docx":
#             # Executa a costura de arquivos Word apenas se o destino for docx
#             for component in engine.manifest.components:
#                 if component.type == "external" and component.file_format == "docx":
#                     docx_adapter = engine.registry.get_adapter("docx")
#                     docx_adapter.execute_binary_merge(final_output_path, component.source)
                    
#         print("=" * 65)
#         print(f"SUCCESS! Integrated modular artifact saved to: {final_output_path}")
#         print("=" * 65)
        
#     except Exception as error:
#         print(f"\n[Compilation Failure] Processing error: {error}")
#     # try:
#     #     compiler.compile_to_docx(temp_markdown_path, final_docx_path)
#     #     # Pós-processamento polimórfico usando o adaptador recuperado do Registro
#     #     for component in engine.manifest.components:
#     #         if component.type == "external" and component.file_format == "docx":
#     #             docx_adapter = engine.registry.get_adapter("docx")
#     #             docx_adapter.execute_binary_merge(final_docx_path, component.source)

#     #     print("=" * 65)
#     #     print(f"SUCCESS! Distribution ready file compiled to: {final_docx_path}")
#     #     print("=" * 65)
#     # except Exception as error:
#     #     print(str(error))
#     #     print(f"\n[Compilation Failure] Pandoc processing error: {error}")
#     #     print("Markdown artifact preserved for structural inspection.")

# if __name__ == "__main__":
#     run_mvp_pipeline()