from spacer import Spacer
from hasher import Hasher
import base64
from PIL import Image
import numpy as np
from cryptosystem import FDM_CA_Cryptosystem, create_string_message, create_2D_message

class ImageSigner:

    def __init__(self):
        self.hashlen = 256
        self.sp = Spacer(256)
        self.hr = Hasher()
        self.cr = FDM_CA_Cryptosystem()
        self.num_gen = 200
        pass

    def generate_keypair(self):
        pass

    def save_keypair(self):
        pass

    def load_priv_key(self):
        pass

    def load_pub_key(self):
        pass

    def sign(self, image, private_key_file):
        self.cr.read_key(private_key_file, "private")
        self.sp.erase(image)
        hval = self.hr.digest(image)
        print("Hash:", hval)
        msg2d = create_2D_message(list(hval),list(str("0123456789abcdef")),8,8)
        signature = create_string_message(self.cr.decrypt(msg2d, self.num_gen),8,8)
        print("Sign:", signature)
        signature_bin = self.hr.hex_to_bin(signature)
        self.sp.insert(signature_bin, image)

    def verify(self, image, public_key_file):
        self.cr.read_key(public_key_file, "public")
        signature_bin = self.sp.extract(image)
        signature = self.hr.bin_to_hex(signature_bin)
        print("Sign:", signature)
        sig2d = create_2D_message(list(signature),list(str("0123456789abcdef")),8,8)
        hval_expected = create_string_message(self.cr.encrypt_with_composed_CA(sig2d, self.num_gen),8,8)
        print("Hash_e:", hval_expected)
        self.sp.erase(image)
        hval_observed = self.hr.digest(image)
        print("Hash_f:", hval_observed)
        return hval_expected == hval_observed

if __name__ == "__main__":
    
    # Signing
    print("Signing image")
    image = Image.open('veggies.jpg').convert('L')
    image.save("veggies-plain.png")
    sg = ImageSigner()
    sg.sign(image, "priv_key_2.xml")
    image.save("veggies-signed.png", "PNG")
    
    # Corrupting
    data = image.load()
    data[10,10] = (data[10,10] + 9) % 256
    image.save("veggies-corrupted.png", "PNG")

    # Validation
    signed_image = Image.open('veggies-signed.png')
    print("Verifying authentic image")
    print("Signature valid: ", str(sg.verify(signed_image, "public_key_2.xml")))

    print("Verifying corrupted image")
    corrupted_image = Image.open("veggies-corrupted.png")
    data3 = corrupted_image.load()
    print("Signature valid: ", str(sg.verify(corrupted_image, "public_key_2.xml")))