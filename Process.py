from PIL import Image
from PIL import *
from os import *

def pixelize(img, maxSize): #img is from PIL.Image
    width, height = img.size
    maxDim = max(width, height)
    newWidth = int(width*maxSize/maxDim)
    newHeight = int(height*maxSize/maxDim)
    img.resize((newWidth, newHeight))
    return img

if __name__ = "__init__":
    img = Image.open("testPic.jpg")
    pixelize(img).save("testRes.jpg")