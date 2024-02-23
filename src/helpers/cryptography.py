from typing import final
from base64 import b64encode, b64decode

@final
class Cryptography:
    @staticmethod
    def encode_base64(text: str) -> str:
        return b64encode(text.encode("ascii")).decode("ascii")
    
    @staticmethod
    def decode_base64(text: str) -> str:
        return b64decode(text.encode("ascii")).decode("ascii")