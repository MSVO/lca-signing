from PIL import Image

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

