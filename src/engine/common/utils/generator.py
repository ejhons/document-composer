'''
Gera os identificadores.
'''
from uuid import uuid4

class IdGenerator:
    @staticmethod
    def generate(prefix: str | None = None ) -> str:
        uid = str(uuid4())
        if prefix:
            return f'{prefix}_{uid}'
        
        return uid