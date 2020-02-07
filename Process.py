from PIL import Image
from PIL import *
from os import *
from glob import *

from sklearn.cluster import *
import numpy as np

def pixelize(img, maxSize = 80, toBW = False): #img is from PIL.Image
    width, height = img.size
    maxDim = max(width, height)
    newWidth = int(width*maxSize/maxDim)
    newHeight = int(height*maxSize/maxDim)
    print(img.size,"to",(newWidth, newHeight),"B&W" if toBW else "")
    newImg = img
    if toBW:
        newImg = newImg.convert("L")
    newImg = newImg.resize((newWidth, newHeight), Image.LANCZOS)
    return newImg

def changeColors(img, n=1):
    rgbImg = img.convert("RGB")
    width, height = rgbImg.size
    clrs = list(rgbImg.getdata())
    clrs = np.array(clrs)
    kmeans = KMeans(n_clusters=n+1).fit(clrs)
    pixels = rgbImg.load()
    clusterNumbers = list(kmeans.labels_)
    colors = list(map(tuple,list(kmeans.cluster_centers_)))
    colors = list(map(lambda t: tuple(map(int,t)), colors))
    print(clusterNumbers[:10])
    print(colors)
    for i in range(width):
        for j in range(height):
            pixels[i,j] = colors[clusterNumbers[i+j*width]]
    return rgbImg

#for testing purposes
if __name__ == "__main__":
    for ext in ["png","jpg"]:
        for f in glob("*."+ext):
            print(f[:-4])
            if not ("Res" in f or "Pix" in f):
                img = Image.open(f)
                newImg = pixelize(img)
                newImg.save(f[:-4] + "Res."+ext)
                altImg = changeColors(newImg, 3)
                altImg.save(f[:-4] + "Pix."+ext)
                newImg = pixelize(img, toBW = True)
                newImg.save(f[:-4] + "BWRes."+ext)
                altImg = changeColors(newImg)
                altImg.save(f[:-4] + "BWPix."+ext)