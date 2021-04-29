from PIL import Image
import math
import numpy as np
import os

RUN_ENV = os.getenv('RUN_ENV')

def open_image(name):
    return Image.open("img_raw/{}.png".format(name)).convert("L")

def open_signed_image(name):
    root = "results" if RUN_ENV == "main" else "test_results"
    return Image.open("{}/{}-signed.png".format(root, name))

def open_plain_image(name):
    root = "img" if RUN_ENV == "main" else "test_img"
    return Image.open("{}/{}.png".format(root, name))

def save_signed_image(img, name):
    root = "results" if RUN_ENV == "main" else "test_results"
    img.save("{}/{}-signed.png".format(root, name))

def save_plain_image(img, name):
    root = "img" if RUN_ENV == "main" else "test_img"
    img.save("{}/{}.png".format(root, name))

def save_corrupted_image(img, name):
    root = "results" if RUN_ENV == "main" else "test_results"
    img.save("{}/{}-corrupted.png".format(root, name))

def calculate_psnr(image, ref_image):
    print("Calculating PSNR")
    y = np.asarray(image).reshape((-1,))
    x = np.asarray(ref_image).reshape((-1,))
    se = ((x-y)**2).astype(int).sum()
    mse = se / x.shape[0]
    print("Squared Error: {}".format(se))
    print("MSE: {}".format(mse))
    psnr = 10 * math.log10((255*255)/mse)
    print("PSNR: {}".format(psnr))
    print("-"*10)
    return psnr


