import cv2 
from os import *
from glob import *

from sklearn.cluster import *
import numpy as np
from pprint import *

def pixelize(img, maxSize = 80, toBW = False): #img is from cv image
    width = img.shape[1]
    height = img.shape[0]
    #print(width, height, img.shape)    
    newWidth = maxSize if width >= height else width * maxSize // height
    newHeight = maxSize if height >= width else height * maxSize // width
    newImg = img
    if toBW:
        newImg = cv2.cvtColor(cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
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
            similarity = 0
            #print(kmeans.cluster_centers_)
            for c1 in kmeans.cluster_centers_:
                for c2 in kmeans.cluster_centers_:
                    c1 = tuple(c1)
                    c2 = tuple(c2)
                    if not(c1==c2):
                        similarity += 10000000 * int(max([abs(c1[i]-c2[i]) for i in range(3)]) <= 50)
            res.append((kmeans.score(clrs) - similarity)*(k+1))
        #print(res)
        #print(max(res))
        n = res.index(max(res))
        print("Best value is "+str(n))
    kmeans = KMeans(n_clusters=n+1).fit(clrs)
    clusterNumbers = list(kmeans.labels_)
    colors = list(map(tuple,list(kmeans.cluster_centers_)))
    colors = list(map(lambda t: tuple(map(int,t)), colors))
    print(colors)
    if n==1:
        def round255Tuple(t):
            return (0,0,0) if t[0] < 255/2 else (255,255,255)
        colors = list(map(lambda t: round255Tuple(t), colors))
    return (clusterNumbers, colors)

def changeColors(img, n=1):
    clusterNumbers, colors = getColors(img, n)
    width = img.shape[1]
    height = img.shape[0]
    newImg = img
    print(colors, n)
    #pprint(["".join(list(map(str,clusterNumbers[k*width:(k+1)*width]))) for k in range(height)])
    for i in range(width):
        for j in range(height):
            newImg[j,i] = colors[clusterNumbers[i+j*width]]
    return newImg

#for testing purposes
if __name__ == "__main__":

    PICNUMCLRS = {"bwPic.png": 1, "cPic.png": 2, "Izzet.png": 3}

    for f in PICNUMCLRS.keys():
        print(f[:-4])
        if not ("Res" in f or "Pix" in f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            newImg = pixelize(img)
            cv2.imwrite("Res"+f, newImg)
            altImg = changeColors(newImg, PICNUMCLRS[f])
            cv2.imwrite("zPix"+f, altImg)
            if PICNUMCLRS[f]>1:
                bwImg = changeColors(pixelize(img,toBW=True))
                cv2.imwrite("zPix_BW"+f, bwImg)
