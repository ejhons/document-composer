import json
import os
import logging
from warnings import deprecated

from dcp_engine.language.manifests.recipe import RecipeManifest


# Configuração do Logger local do módulo
logger = logging.getLogger("doc_engine.pipeline")

@deprecated('Use RecipeManifest.from_file()')
class ManifestLoader:
    """
    Orchestrates the lifecycle of document discovery, setup, assembly, 
    and compilation into polymorphic target formats.
    """
    def __init__(self):
            # self, 
            # manifest_path: str
            # ):
        self._manifest_path = None
        self.generated_manifest = None
        
    def load_manifest(
        self,
        manifest_path: str
    ) -> RecipeManifest:
        
        if not os.path.exists(manifest_path):
            logger.error(f"Assembly recipe manifest not found at: {manifest_path}")
            raise FileNotFoundError(f"Recipe manifest missing: {manifest_path}")
                
        with open(manifest_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)

        self._manifest_path = manifest_path
        self.generated_manifest = RecipeManifest(**raw_data)

        return self.generated_manifest