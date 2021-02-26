import numpy as np
from PIL import Image
from numpy import asarray
# load the image
image = Image.open('kolala.jpg').convert('L')

# convert image to numpy array
image.show()

data = asarray(image)
print(type(data))
# summarize shape
print(data.shape)
width, height = data.shape
print(width, height)
data = data.copy()
print(data)
lim = (image.size[0]*image.size[1])


def erase(image):
    data = image.load()
    k = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            chk = data[i,j] & 1
            if chk == 1:
                data[i,j] = data[i,j] - 1
            k = k + 1
            if k == lim:
                break
        if k == lim:
            break

erase(image)
data = asarray(image)
print(data)
# image.show()

def insert(has, image):
    data = image.load()
    k = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            data[i,j] = data[i,j] + int(has[k])
            k = k + 1
            if k == lim:
                break
        if k == lim:
            break

has = np.random.randint(0,high = 2, size = lim)
print(has)
insert(has,image)
data = asarray(image)
print(data)
image.show()

def extract(image):

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
            if k == lim:
                break
        if k == lim:
            break
    
    return chash

chas = extract(image)

print((np.asarray(chas) == has).all())
