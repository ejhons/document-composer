import os
from pathlib import Path

from pydantic import BaseModel, Field, PrivateAttr

from dcp_engine.common.generator import IdGenerator
from dcp_engine.language.manifests.recipe import RecipeManifest
from dcp_engine.runtime.execution.metadata import Metadata
from dcp_engine.runtime.logging.log import logger


class Workspace(BaseModel):
    '''
    Represents physical environment of document assembling.
    Project of document composition.
    '''
    root: Path
    id: str = Field(default_factory=lambda:
        IdGenerator.generate('w')
    )

    # Atributos privados com valores padrão (Pydantic v2)
    _recipe_name: str = PrivateAttr('recipe.json')
    _metadata_name: str = PrivateAttr('metadata.json')
    _generated_name: str = PrivateAttr('document')

    _relative_components_dir: str = PrivateAttr('components')
    _relative_outputs_dir: str = PrivateAttr('output')
    _relative_build_dir: str = PrivateAttr('build')
            
    _relative_assets_dir: str = PrivateAttr('output/assets')
    _relative_images_dir: str = PrivateAttr('img')
    _relative_documents_dir: str = PrivateAttr('docs')
    _relative_spreadsheets_dir: str = PrivateAttr('sheets')

    _relative_temp_dir: str = PrivateAttr('tmp')

    @property
    def components_dir(self) -> Path:
        return self.root / self._relative_components_dir

    @property
    def assets_dir(self) -> Path:
        return self.root / self._relative_assets_dir

    @property
    def images_dir(self) -> Path:
        return self.root / self._relative_assets_dir / self._relative_images_dir

    @property
    def documents_dir(self) -> Path:
        return self.root / self._relative_assets_dir / self._relative_documents_dir

    @property
    def spreadsheets_dir(self) -> Path:
        return self.root / self._relative_assets_dir / self._relative_spreadsheets_dir
    
    @property
    def build_dir(self) -> Path:
        return self.root / self._relative_build_dir

    @property
    def outputs_dir(self) -> Path:
        return self.root / self._relative_outputs_dir

    @property
    def temp_dir(self) -> Path:
        return self.root / self._relative_temp_dir

    @property
    def recipe_path(self) -> Path:
        return self.root / self._recipe_name
    
    @property
    def metadata_path(self) -> Path:
        return self.root / self._metadata_name

    def generated_path(self, extension: str) -> Path:
        filename = self._generated_name + '.' + extension
        return self.outputs_dir / filename 


    def load_recipe(self) -> RecipeManifest:
        recipe = RecipeManifest.from_file(self.recipe_path)
        return recipe
    
    def reload_metadata(self) -> Metadata:
        metadata =  Metadata.from_json_file(self.metadata_path)
        return metadata

    

    def dir_from_root(
            self,
            relative_dir:str,
            exists_ok:bool = False
    ) -> Path:
        path = self.root / relative_dir
        path_dir = path if path.is_dir() else path.parent

        if exists_ok:
            os.makedirs(path_dir, exist_ok=exists_ok)
            
        return path

    def dir_from_temp(
        self,
        relative_dir:str,
        exists_ok:bool = False
    ) -> Path:
        path = self.temp_dir / relative_dir
        path_dir = path if path.is_dir() else path.parent
        
        if exists_ok:
            path_dir.mkdir(parents=True, exist_ok=True)
            # os.makedirs(path_dir, exist_ok=exists_ok)
            
        return path
    
    def dir_from_temp(
        self,
        relative_dir:str,
        exists_ok:bool = False
    ) -> Path:
        path = self.temp_dir / relative_dir
        path_dir = path if path.is_dir() else path.parent
        
        if exists_ok:
            path_dir.mkdir(parents=True, exist_ok=True)
            # os.makedirs(path_dir, exist_ok=exists_ok)
            
        return path

    
    def exists(self) -> bool:
        return self._root.exists()

    def is_initialized(self) -> bool:
        return (
            self._root.is_dir()
            and self.recipe_path.exists()
            and self.components_dir.is_dir()
            and self.outputs_dir.is_dir()
        )

    
    def init(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.components_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.recipe_path.touch(exist_ok=True)
        self.metadata_path.touch(exist_ok=True)
        logger.info(f'Workspace created in "{self.root}"')


