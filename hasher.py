import hashlib
import numpy as np

class Hasher:
    
    def __init__(self):
        # Hashlength is 256 (sha256)
        self.r = ''.join([str(c) for c in np.random.randint(0,high = 2, size = 256)])

    def digest(self, image):
        hexhash = hashlib.sha256(str(np.asarray(image)).encode('utf-8')).hexdigest()
        binhash = ''.join('{0:04b}'.format(int(c, 16)) for c in hexhash)
        return self.r
        # return binhash