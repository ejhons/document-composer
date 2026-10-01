import json
import pickle
from pathlib import Path
from typing import Union

class Metadata(dict):
    """Classe de metadados com suporte a campos arbitrários e sintaxe de atributo."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Converte dicionários aninhados em instâncias de Metadata recursivamente
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = Metadata(value)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'Metadata' não possui o atributo '{item}'")

    def __setattr__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, Metadata):
            value = Metadata(value)
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError:
            raise AttributeError(f"'Metadata' não possui o atributo '{item}'")

    @classmethod
    def from_json(cls, json_str: str):
        """Cria uma instância de Metadata a partir de uma string JSON."""
        data = json.loads(json_str)
        return cls(data)

    def to_json(self, **kwargs) -> str:
        """Exporta a instância diretamente para uma string JSON."""
        return json.dumps(self, **kwargs)

    @classmethod
    def from_json_file(cls, filepath: Union[str, Path], encoding: str = 'utf-8'):
        """Lê os metadados diretamente de um arquivo JSON."""
        with open(filepath, 'r', encoding=encoding) as f:
            data = json.load(f)
        return cls(data)

    def to_json_file(self, filepath: Union[str, Path], indent: int = 4, encoding: str = 'utf-8'):
        """Salva os metadados diretamente em um arquivo JSON."""
        with open(filepath, 'w', encoding=encoding) as f:
            json.dump(self, f, indent=indent, ensure_ascii=False)

    # --- MÉTODOS PICKLE (Para salvar o objeto Python diretamente em arquivo binário) ---

    def to_pickle_file(self, filepath: Union[str, Path]):
        """Salva a instância em um arquivo binário (.pickle)."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle_file(cls, filepath: Union[str, Path]):
        """Carrega a instância a partir de um arquivo binário (.pickle)."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)