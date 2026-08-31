import json
import os
import logging
from warnings import deprecated

from dcp_engine.language.manifests.recipe import RecipeManifest


# Configuração do Logger local do módulo
logger = logging.getLogger("doc_engine.pipeline")

@deprecated(message='not implemented yet.')
class ManifestLoader:
    """
    Orchestrates the lifecycle of document discovery, setup, assembly, 
    and compilation into polymorphic target formats.
    """
    def __init__(
            self, 
            manifest_path: str
            ):
        self.manifest_path = manifest_path
        self.generated_manifest = None
        
        if not os.path.exists(self.manifest_path):
            logger.error(f"Assembly recipe manifest not found at: {self.manifest_path}")
            raise FileNotFoundError(f"Recipe manifest missing: {self.manifest_path}")
        
    def load_manifest(self) -> RecipeManifest:
        with open(self.manifest_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)

        self.generated_manifest = RecipeManifest(**raw_data)

        return self.generated_manifest