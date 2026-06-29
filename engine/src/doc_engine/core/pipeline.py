import os
import logging
import datetime
from traceback import print_exc
from typing import Dict, Any
import pypandoc
import subprocess

from engine.src.doc_engine.core.engine import DocumentEngine
from engine.src.doc_engine.core.models import AssembledManifest

# Configuração do Logger local do módulo
logger = logging.getLogger("doc_engine.pipeline")

class DocumentPipeline:
    """
    Orchestrates the lifecycle of document discovery, setup, assembly, 
    and compilation into polymorphic target formats.
    """
    def __init__(self, manifest_path: str, output_root: str = "engine/src/doc_engine/output"):
        self.manifest_path = manifest_path
        self.output_root = output_root
        self.engine = None
        
        if not os.path.exists(self.manifest_path):
            logger.error(f"Assembly recipe manifest not found at: {self.manifest_path}")
            raise FileNotFoundError(f"Recipe manifest missing: {self.manifest_path}")

    def setup_environment(self) -> bool:
        """Ensures system dependencies like Pandoc are available and valid."""
        logger.info("Checking for Pandoc installation state...")
        try:
            pandoc_path = pypandoc.get_pandoc_path()
            pandoc_version = pypandoc.get_pandoc_version()
            logger.info(f"Pandoc executable detected at: {pandoc_path}")
            logger.info(f"Pandoc system version: {'.'.join(map(str, pandoc_version))}")
            
            # Subprocess verification check
            result = subprocess.run([pandoc_path, '--version'], capture_output=True, text=True, check=True)
            logger.debug(f"Direct system verification code output: {result.stdout.splitlines()[0]}")
            
            # Force update context for legacy versions
            if int(pandoc_version[0]) < 2:
                logger.warning("Detected Pandoc version is outdated. Upgrading core binaries...")
                pypandoc.download_pandoc(force_dl=True)
            return True
            
        except Exception as error:
            logger.warning(f"Initial Pandoc resolution failed: {error}. Attempting automated recovery download...")
            try:
                pypandoc.download_pandoc(force_dl=True)
                logger.info(f"Pandoc recovered successfully. Version: {'.'.join(map(str, pypandoc.get_pandoc_version()))}")
                return True
            except Exception as system_error:
                logger.critical(f"Critical environment initialization failure: {system_error}")
                return False

    def initialize_engine(self):
        """Boots up the underlying polymorphic document engine framework."""
        logger.info(f"Initializing structural rendering engine using manifest recipe...")
        self.engine = DocumentEngine(self.manifest_path)
        logger.info(f"Loaded Recipe Specification: {self.engine.manifest.recipe_name} (v{self.engine.manifest.version})")

    def scan_fields(self) -> Dict[str, Any]:
        """Discovers dynamic input variables required across selected template blocks."""
        if not self.engine:
            self.initialize_engine()
        logger.info("Scanning document components to extract schema fields definition...")
        return self.engine.discover_required_fields()

    def run(self, input_data: Dict[str, Any]) -> str:
        """
        Executes the compilation pipeline: links blocks, applies input parameters,
        caches markdown structures, and triggers format compilation adapters.
        """
        if not self.engine:
            self.initialize_engine()

        os.makedirs(self.output_root, exist_ok=True)
        resource_dir = os.path.join(self.output_root, "resources")
        
        # 1. Block Stitching and Jinja Variable Injection
        logger.info("Executing text segment rendering and parameter injection mapping...")
        assembled_markdown = self.engine.assemble_document(input_data, output_resource_dir=resource_dir)

        # 2. Intermediate Representation (Transpilation Stage)
        logger.info("Intercepting layout tags and translating graphical diagram code blocks...")
        final_markdown = self.engine.pre_process_markdown_diagrams(assembled_markdown, resource_dir)

        dist_markdown_path = os.path.join(self.output_root, "document_distribution.md")
        with open(dist_markdown_path, 'w', encoding='utf-8') as file:
            file.write(final_markdown)
        logger.info(f"Intermediate standalone Markdown source generated at: {dist_markdown_path}")

        # 3. Create Distribution Manifest Record Log
        generated_assets = []
        if os.path.exists(resource_dir):
            generated_assets = [os.path.join(resource_dir, f) for f in os.listdir(resource_dir)]

        format_type = self.engine.manifest.target_format
        final_manifest = AssembledManifest(
            document_name=self.engine.manifest.recipe_name,
            generation_timestamp=datetime.datetime.now().isoformat(),
            engine_version=self.engine.manifest.version,
            target_format=format_type,
            injected_parameters=input_data,
            compiled_markdown_source=dist_markdown_path,
            generated_resources=generated_assets
        )

        manifest_delivery_path = os.path.join(self.output_root, "document_manifest_delivery.json")
        with open(manifest_delivery_path, 'w', encoding='utf-8') as file:
            file.write(final_manifest.model_dump_json(indent=2))
        logger.info(f"Delivery audit logging manifest written to: {manifest_delivery_path}")

        # 4. Binary Adapter Compilation Output Pipeline
        final_output_path = os.path.join(self.output_root, f"final_report.{format_type}")
        
        try:
            compiler = self.engine.compiler_registry.get_compiler(format_type)
            compiler.compile(dist_markdown_path, final_output_path, self.engine.manifest)
            
            # Post-compilation steps exclusive to Microsoft Word ecosystems
            if format_type == "docx":
                logger.info("Executing post-compile subdocument binary structural binding merge...")
                for component in self.engine.manifest.components:
                    if component.type == "external" and component.file_format == "docx":
                        docx_adapter = self.engine.registry.get_adapter("docx")
                        docx_adapter.execute_binary_merge(final_output_path, component.source)
                        
            logger.info(f"SUCCESS! Distribution ready artifact successfully compiled at: {final_output_path}")
            return final_output_path
            
        except Exception as compilation_error:
            print_exc()
            logger.error(f"Compilation adapter pipeline execution failure: {compilation_error}")
            raise compilation_error