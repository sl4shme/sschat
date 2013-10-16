#!/usr/bin/python
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import base64


class Crypt:
        def __init__(self, password):
                self.key = hashlib.sha256(password).digest()
		BS = 16
		self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
		self.unpad = lambda s : s[0:-ord(s[-1])]

        def encrypt(self, data):
                data = self.pad(data)
                iv = Random.new().read(AES.block_size)
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                return base64.b64encode(iv + cipher.encrypt(data))

        def decrypt(self, enc):
                enc = base64.b64decode(enc)
                iv = enc[:16]
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
		dec = self.unpad(cipher.decrypt(enc[16:]))
		if dec != '':
			return dec
		else:
			return '<Encrypted>'
