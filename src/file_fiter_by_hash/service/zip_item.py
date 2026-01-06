from ..config.salt import salt
from dowhen import when
import pyzipper


def zip_item():
    with when(pyzipper.zipfile_aes.AESZipEncrypter,'pwd_verify_length = 2').do(add_self_salt):
        pass
