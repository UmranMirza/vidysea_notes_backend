import base64
from application.configuration.auth_config import AuthConfig
from Crypto.Cipher import AES


iv = "@@@@&&&&####$$$$"
BLOCK_SIZE = 16

__pad__ = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
    BLOCK_SIZE - len(s) % BLOCK_SIZE
)
__unpad__ = lambda s: s[0 : -ord(s[-1])]

class Encryption:
    def __init__(self):
        self.key = AuthConfig.ENCRYPTION_KEY[:32]

    def encrypt(self,to_encode):    
        to_encode = __pad__(to_encode)
        c = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
        to_encode = c.encrypt(to_encode.encode("utf8"))
        to_encode = base64.b64encode(to_encode)
        return to_encode.decode("UTF-8")

    def decrypt(self,to_decode):
        to_decode = base64.b64decode(to_decode)
        c = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
        to_decode = c.decrypt(to_decode)
        if type(to_decode) == bytes:
            # convert bytes array to str.
            to_decode = to_decode.decode()
        # remove pad
        return __unpad__(to_decode)
        