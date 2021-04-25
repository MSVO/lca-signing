from util import *
import numpy as np

# Main Module

from image_signer import ImageSigner        # Image Signer

if __name__ == "__main__":
    
    # Instantiate
    signer = ImageSigner()
    image_name = "pic_1"

    # Generate key pair
    signer.generate_keys()
    signer.save_keys("key1")

    # Processing raw image
    img = open_image(image_name)
    save_plain_image(img, image_name)
    img = open_plain_image(image_name)

    # Signing
    signed_img = signer.sign(img)
    save_signed_image(signed_img, image_name)

    # Verifying signature
    # signed_img = open_signed_image(image_name)
    signer.verify(signed_img)