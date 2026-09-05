import os
from pathlib import Path

from pydantic import BaseModel, PrivateAttr


class Workspace(BaseModel):
    '''
    Represents physical environment of document assembling.
    Project of document composition.
    '''
    root: Path

    # Atributos privados com valores padrão (Pydantic v2)
    _relative_recipe_name: str = PrivateAttr('recipe.json')
    _relative_generated_name: str = PrivateAttr('document')

    _relative_assets_dir: str = PrivateAttr('assets')
    _relative_components_dir: str = PrivateAttr('components')
    _relative_outputs_dir: str = PrivateAttr('outputs')
    _relative_build_dir: str = PrivateAttr('build')
            
    _relative_images_dir: str = PrivateAttr('img')
    _relative_documents_dir: str = PrivateAttr('docs')
    _relative_spreadsheets_dir: str = PrivateAttr('sheets')

    _relative_temp_dir: str = PrivateAttr('tmp')


    @property
    def images_dir(self) -> Path:
        return self.root / self._relative_components_dir / self._relative_images_dir

    @property
    def documents_dir(self) -> Path:
        return self.root / self._relative_components_dir / self._relative_documents_dir

    @property
    def spreadsheets_dir(self) -> Path:
        return self.root / self._relative_components_dir / self._relative_spreadsheets_dir

    @property
    def components_dir(self) -> Path:
        return self.root / self._relative_components_dir

    @property
    def assets_dir(self) -> Path:
        return self.root / self._relative_assets_dir
    
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
        return self.root / self._relative_recipe_name

    def generated_path(self, extension: str):
        filename = self._relative_generated_name + '.' + extension
        return self.outputs_dir / filename 

    # @property
    # def components_path(self) -> Path:
    #     return self.root / "components"

    # @property
    # def assets_path(self) -> Path:
    #     return self.root / "assets"

    # @property
    # def output_path(self) -> Path:
    #     return self.root / "output"
    

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
    
    # _relative_assets_dir: str = 'assets'
    # _relative_images_dir: str = 'img'
    # _relative_documents_dir: str = 'docs'
    # _relative_spreadsheets_dir: str = 'sheets'
    # _relative_temp_dir: str = 'tmp'

    # @property
    # def assets_dir(self) -> Path:
    #     # root / _relative_assets_dir

    # @property
    # def images_dir(self) -> Path:
    #     # root / _relative_images_dir

    # @property
    # def documents_dir(self) -> Path:
    #     # root / _relative_documents_dir

    # @property
    # def spreadsheets_dir(self) -> Path:
    #     # root / _relative_spreadsheets_dir

    # @property
    # def temp_dir(self) -> Path:
    #     # root / _relative_temp_dir