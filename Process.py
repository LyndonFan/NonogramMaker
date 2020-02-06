from PIL import Image
from PIL import *
from os import *

def pixelize(img, maxSize): #img is from PIL.Image
    width, height = img.size
    print(img.size)
    maxDim = max(width, height)
    newWidth = int(width*maxSize/maxDim)
    newHeight = int(height*maxSize/maxDim)
    print(newWidth, newHeight)
    newImg = img.resize((newWidth, newHeight), Image.ANTIALIAS)
    #img.show()
    return newImg

if __name__ == "__main__":
    bwimg = Image.open("bwPic.png")
    newbwImg = pixelize(bwimg, 30)
    newbwImg.save("bwRes.png","PNG")
    cimg = Image.open("cPic.png")
    newCImg = pixelize(cimg, 30)
    newCImg.save("cRes.png","PNG")