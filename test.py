import os
os.environ['RUN_ENV'] = "test" # Setting environment as test
import unittest
from sheet import Sheet 
import numpy as np
ts = Sheet()
from image_signer import ImageSigner        # Image Signer
from util import *

class TestImageSigner(unittest.TestCase):
    
    def test_1_Validation(self):
        ts.title("Validation Tests")
        signer = ImageSigner()
        image_names = ["{}".format(i) for i in range(1, 50)]
        key_identifier = "key1"

        # Generate key pair
        # signer.generate_keys()
        signer.load_keys(key_identifier)

        verify_outputs = []
        psnrs = []
        for image_name in image_names:
            ts.subtitle("Case {}".format(image_name))
            img = open_plain_image(image_name)
            hval = signer.get_digest(img)
            signature = signer.get_signature(hval)
            signed_img = signer.insert(signature, img)
            save_signed_image(signed_img, image_name)

            signed_img = open_signed_image(image_name)
            v = signer.verify(signed_img)
            verify_outputs.append(v)

            psnr = calculate_psnr(signed_img, img)
            ts.union_1(image_name, hval, signature, v, psnr)
            psnrs.append(psnr)

        success = np.asarray(verify_outputs).all()
        self.assertTrue(success)
        if success:
            ts.paragraph("All validation test cases passed")


if __name__ == "__main__":
    ts.clear()
    unittest.main()