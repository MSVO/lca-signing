from PIL import Image
import math
import numpy as np

def open_image(name):
    return Image.open("img_raw/{}.png".format(name)).convert("L")

def open_signed_image(name):
    return Image.open("results/{}-signed.png".format(name))

def open_plain_image(name):
    return Image.open("img/{}.png".format(name))

def save_signed_image(img, name):
    img.save("results/{}-signed.png".format(name))

def save_plain_image(img, name):
    img.save("img/{}.png".format(name))

def save_corrupted_image(img, name):
    img.save("results/{}-corrupted.png".format(name))

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


