'''
Gera os identificadores.
'''
import shortuuid
from uuid import uuid4

class IdGenerator:
    @staticmethod
    def generate_hex(prefix: str | None = None ) -> str:
        uid = str(uuid4().hex)
        if prefix:
            return f'{prefix}_{uid}'
        
        return uid
    
    @staticmethod
    def generate(prefix: str | None = None ) -> str:
        gerador = shortuuid.ShortUUID(alphabet="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")#str(uuid4().hex)
        uid = gerador.random(length=4)
        if prefix:
            return f'{prefix}_{uid}'
        
        return uid