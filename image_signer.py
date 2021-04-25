from spacer import Spacer
from Hasher import ImageHasher
import base64
from PIL import Image
import numpy as np
from cryptosystem import FDM_CA_Cryptosystem, create_string_message, create_2D_message
import json
import libnum
import random

class ImageSigner:

    def __init__(self):
        self.hashlen = 256
        self.sp = Spacer(256)
        self.cr = FDM_CA_Cryptosystem()
        self.hr = None
        self.num_gen = 200
        pass

    def generate_keys(self):
        print("Generating keys")
        self.cr.generate_keys(2, list("0123456789abcdef"), [(1,0),(0,1)], 250, 0.5, 0.5)
        self.hash_params = {
            "iv1": format(libnum.randint_bits(self.hashlen),'0256b'),
            "iv2": format(libnum.randint_bits(self.hashlen),'0256b'),
            "prime": libnum.generate_prime(13),
            "rand_ind": random.randint(0, 1000)
        }
        print("-"*10)

    def save_keys(self, identifier):
        print("Saving keys")
        pub_keyfile = "keys/{}.pub.xml".format(identifier)
        priv_keyfile = "keys/{}.xml".format(identifier)
        hash_paramfile = "keys/{}.hash_params.json".format(identifier)
        self.cr.write_key(pub_keyfile, "public")
        self.cr.write_key(priv_keyfile, "private")
        with open(hash_paramfile, "w") as fp:
            json.dump(self.hash_params, fp)
        print("-"*10)

    def load_priv_key(self):
        pass

    def load_pub_key(self):
        pass

    def load_keys(self, identifier):
        print("Loading keys")
        pub_keyfile = "keys/{}.pub.xml".format(identifier)
        priv_keyfile = "keys/{}.xml".format(identifier)
        hash_paramfile = "keys/{}.hash_params.json".format(identifier)
        self.cr.read_key(pub_keyfile, "public")
        self.cr.read_key(priv_keyfile, "private")
        with open(hash_paramfile, "r") as fp:
            self.hash_params = json.load(fp)
        print("-"*10)

    def sign(self, image):
        # self.cr.read_key(private_key_file, "private")
        print("Signing an image")
        iv1, iv2, prime, rand_ind = map(self.hash_params.get, ["iv1", "iv2", "prime", "rand_ind"])
        image = self.sp.erase(image)
        hval = ImageHasher(image, iv1=iv1, iv2=iv2, prime=prime, rand_ind=rand_ind).digest()
        print("Hash:\t\t", hval)
        msg2d = create_2D_message(list(hval),list(str("0123456789abcdef")),8,8)
        signature = create_string_message(self.cr.decrypt(msg2d, self.num_gen),8,8)
        print("Sign:\t\t", signature)
        signature_bin = self.hex_to_bin(signature)
        print("-"*10)
        return self.sp.insert(signature_bin, image)

    def verify(self, image):
        # self.cr.read_key(public_key_file, "public")
        print("Verifying a signed image")
        iv1, iv2, prime, rand_ind = map(self.hash_params.get, ["iv1", "iv2", "prime", "rand_ind"])
        signature_bin = self.sp.extract(image)
        signature = self.bin_to_hex(signature_bin)
        print("Sign:\t\t", signature)
        sig2d = create_2D_message(list(signature),list(str("0123456789abcdef")),8,8)
        hval_expected = create_string_message(self.cr.encrypt_with_composed_CA(sig2d, self.num_gen),8,8)
        print("Hash expected:\t", hval_expected)
        image = self.sp.erase(image)
        hval_observed = ImageHasher(image, iv1=iv1, iv2=iv2, prime=prime, rand_ind=rand_ind).digest()
        print("Hash_found:\t", hval_observed)
        response = hval_expected == hval_observed
        print("Success?:{}".format(response))
        print("-"*10)
        return response
    
    def bin_to_hex(self, str1):
        h = []
        assert len(str1) % 4 == 0
        for i in range(0, len(str1), 4):
            h.append(hex(int(str1[i:i+4], 2))[2])
        return ''.join(h)
    
    def hex_to_bin(self, s):
        binhash = ''.join('{0:04b}'.format(int(c, 16)) for c in s)
        return binhash

if __name__ == "__main__":
    
    # Signing
    iv1 = '1010010110001011011011110011010010011101000111100100101110000001011101011011000011100110001101011110001000010110100100001010010000000110001000011100100001000011100100111011101101101010100010110010000011111000000101110110000001101001110100111100101101011011'
    iv2 = '1001011011000101001111010101000111110110110111010001010000101010001001100010110100011001101001111100000001010011010101110101011100001100011101001111000011101011000001110101001111011111101111110001011110100000111101001000000010011110001000100110001011011110'
    prime = 5441
    rand_ind = 4390

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