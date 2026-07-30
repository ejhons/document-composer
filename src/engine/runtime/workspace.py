import os
from pathlib import Path

from pydantic import BaseModel, PrivateAttr


class Workspace(BaseModel):
    root: Path

    # Atributos privados com valores padrão (Pydantic v2)
    _relative_assets_dir: str = PrivateAttr('assets')
    _relative_images_dir: str = PrivateAttr('img')
    _relative_documents_dir: str = PrivateAttr('docs')
    _relative_spreadsheets_dir: str = PrivateAttr('sheets')
    _relative_temp_dir: str = PrivateAttr('tmp')

    @property
    def assets_dir(self) -> Path:
        return self.root / self._relative_assets_dir

    @property
    def images_dir(self) -> Path:
        return self.root / self._relative_images_dir

    @property
    def documents_dir(self) -> Path:
        return self.root / self._relative_documents_dir

    @property
    def spreadsheets_dir(self) -> Path:
        return self.root / self._relative_spreadsheets_dir

    @property
    def temp_dir(self) -> Path:
        return self.root / self._relative_temp_dir

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