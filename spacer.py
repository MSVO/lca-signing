import numpy as np
from PIL import Image
from numpy import asarray


class Spacer:
    def __init__(self, spacelength):
        self.lim = spacelength

    def erase(self, image):
        assert image.size[0] * image.size[1] > self.lim
        data = image.load()
        k = 0
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                chk = data[i,j] & 1
                if chk == 1:
                    data[i,j] = data[i,j] - 1
                k = k + 1
                if k == self.lim:
                    break
            if k == self.lim:
                break

    def insert(self, has, image):
        assert image.size[0] * image.size[1] > self.lim
        data = image.load()
        k = 0
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                data[i,j] = data[i,j] + int(has[k])
                k = k + 1
                if k == self.lim:
                    break
            if k == self.lim:
                break

    def extract(self, image):
        assert image.size[0] * image.size[1] > self.lim
        data = image.load()
        k = 0
        chash = []
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                chk = data[i,j] & 1
                if chk == 1:
                    data[i,j] = data[i,j] - 1
                    chash.append(1)
                else:
                    chash.append(0)
                k = k + 1
                if k == self.lim:
                    break
            if k == self.lim:
                break
        
        return ''.join([str(c) for c in chash])


if __name__ == "__main__":
# load the image
    image = Image.open('veggies.jpg').convert('L')
    hlen = 128

    # convert image to numpy array
    image.save("veggies-before.png", "PNG")

    sp = Spacer(hlen)

    data = asarray(image)
    print(type(data))
    # summarize shape
    print(data.shape)
    width, height = data.shape
    print(width, height)
    data = data.copy()
    print(data)

    sp.erase(image)
    data = asarray(image)
    print(data)
    image.save("veggies-erased.png", "PNG")

    has = ''.join([str(c) for c in np.random.randint(0,high = 2, size = hlen)])
    print(has)
    sp.insert(has,image)
    data = asarray(image)
    print(data)
    image.save("veggies-after.png", "PNG")

    after_image = Image.open("veggies-after.png").convert("L")
    print(np.asarray(image) == np.asarray(after_image))
    chas = sp.extract(after_image)
    print(type(chas))
    print(chas)
    print(has)
    print(chas == has)
