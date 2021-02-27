from spacer import Spacer
from hasher import Hasher
import base64
from PIL import Image
import numpy as np

class ImageSigner:

    def __init__(self):
        self.hashlen = 256
        self.sp = Spacer(256)
        self.hr = Hasher()
        pass

    def generate_keypair(self):
        pass

    def save_keypair(self):
        pass

    def load_priv_key(self):
        pass

    def load_pub_key(self):
        pass

    def sign(self, image):
        self.sp.erase(image)
        hval = self.hr.digest(image)
        self.sp.insert(hval, image)

    def verify(self, image):
        hval_expected = self.sp.extract(image)
        self.sp.erase(image)
        hval_observed = self.hr.digest(image)
        return hval_expected == hval_observed

if __name__ == "__main__":
    
    # Signing
    image = Image.open('veggies.jpg').convert('L')
    image.save("veggies-plain.png")
    sg = ImageSigner()
    sg.sign(image)
    image.save("veggies-signed.png", "PNG")
    
    # Validation
    signed_image = Image.open('veggies-signed.png')
    print((np.asarray(image) == np.asarray(signed_image)).all())
    print("Signature valid: ", str(sg.verify(signed_image)))