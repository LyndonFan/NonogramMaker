import cv2 
from os import *
from glob import *

from sklearn.cluster import *
import numpy as np

def pixelize(img, maxSize = 80, toBW = False): #img is from cv image
    width = img.shape[1]
    height = img.shape[0]
    print(width, height, img.shape)    
    newWidth = maxSize if width >= height else width * maxSize // height
    newHeight = maxSize if height >= width else height * maxSize // width
    newImg = img
    if toBW:
        newImg = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)
    newImg = cv2.resize(newImg, dsize = (newWidth, newHeight), interpolation = cv2.INTER_NEAREST)
    return newImg

def getColors(img, n=1):
    width = img.shape[1]
    height = img.shape[0]
    clrs = [img[i//width, i%width] for i in range(width*height)]
    clrs = np.array(clrs)

    if not (type(n) == int):
        print("Using best value of n from 1 to 10...")
        res = []
        for k in range(11):
            kmeans = KMeans(n_clusters=k+1).fit(clrs)
            res.append(kmeans.score(clrs))
        print(res)
        print(max(res))
        n = res.index(max(res))
        print("Best value is "+str(n))
    kmeans = KMeans(n_clusters=n+1).fit(clrs)
    clusterNumbers = list(kmeans.labels_)
    colors = list(map(tuple,list(kmeans.cluster_centers_)))
    colors = list(map(lambda t: tuple(map(int,t)), colors))
    return (img, clusterNumbers, colors)

def changeColors(img, n=1):
    newImg, clusterNumbers, colors = getColors(img, n)
    width = img.shape[1]
    height = img.shape[0]
    for i in range(width):
        for j in range(height):
            newImg[j,i] = colors[clusterNumbers[i+j*width]]
    return newImg

#for testing purposes
if __name__ == "__main__":
    for ext in ["png","jpg"]:
        for f in glob("*."+ext):
            print(f[:-4])
            if not ("Res" in f or "Pix" in f):
                img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
                newImg = pixelize(img)
                cv2.imwrite(f[:-4] + "Res."+ext, newImg)
                rgbImg, clusterNumbers, colors = getColors(newImg, "best")
                if len(colors)==2:
                    newImg = pixelize(img, toBW = True)
                altImg = changeColors(newImg, 3)
                cv2.imwrite(f[:-4] + "Pix."+ext, altImg)