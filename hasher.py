import hashlib
import numpy as np
import binascii


class Hasher:
    
    def __init__(self):
        # Hashlength is 256 (sha256)
        self.r = ''.join([str(c) for c in np.random.randint(0,high = 2, size = 256)])

    def digest(self, image):
        image_string = ''.join([str(i) for i in (np.asarray(image).reshape((-1,)))])
        hexhash = hashlib.sha256(image_string.encode('utf-8')).hexdigest()
        return hexhash

    def hex_to_bin(self, s):
        binhash = ''.join('{0:04b}'.format(int(c, 16)) for c in s)
        return binhash

    def bin_to_hex(self, str1):
        h = []
        assert len(str1) % 4 == 0
        for i in range(0, len(str1), 4):
            h.append(hex(int(str1[i:i+4], 2))[2])
        return ''.join(h)