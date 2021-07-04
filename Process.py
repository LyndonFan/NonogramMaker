import cv2
from os import *
from glob import *

from skimage import color
from sklearn.cluster import *
import numpy as np
from pprint import *
import matplotlib.pyplot as plt


def pixelize(img, maxSize=80, minSize=20, toBW=False):  # img is from cv image
    width = img.shape[1]
    height = img.shape[0]
    # print(width, height, img.shape)
    newWidth = maxSize if width >= height else (width * maxSize) // height
    newHeight = maxSize if height >= width else (height * maxSize) // width
    if min(newWidth, newHeight) < minSize:
        newWidth = minSize if width <= height else (width * minSize) // height
        newHeight = minSize if height <= width else (height * minSize) // width
    newImg = img
    if toBW:
        print("Converting to black and white...")
        newImg = cv2.cvtColor(
            cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR
        )
    if newImg.shape[2] == 4:
        newImg = np.delete(newImg, 3, axis=0)
    print("Resizing to ({},{})...".format(newWidth, newHeight))
    newImg = cv2.resize(
        newImg,
        dsize=(newWidth, newHeight),
        interpolation=cv2.INTER_NEAREST,  # cv2.INTER_AREA
    )
    return newImg


def getColors(img, n=1):
    width = img.shape[1]
    height = img.shape[0]
    clrs = img.reshape(width * height, img.shape[-1])
    if not (type(n) == int) or n == 0:
        print("Using best value of n from 1 to 10...")
        res = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k + 1).fit(clrs)
            similarity = 0
            centers = kmeans.cluster_centers_
            for i in range(k):
                c1 = color.rgb2lab(centers[i])
                for j in range(i + 1, k + 1):
                    c2 = color.rgb2lab(centers[j])
                    dist = color.deltaE_cie76(c1, c2)
                    # similarity += (dist / 23) ** 2
                    similarity += 10 ** 11 / ((dist / 2.3) ** 2)
            # https://en.wikipedia.org/wiki/Color_difference#CIE76
            # difference of 2.3 corresponds to just noticeable difference
            # so dist < 2.3 --> much more similar
            print(k, -kmeans.score(clrs), similarity)
            res.append(-kmeans.score(clrs) + similarity)
        plt.plot(range(1, 11), res)
        plt.show()
        improvements = [(res[i] - res[i + 1]) / res[i] for i in range(9)]
        n = 1
        # pseudo-like elbow method: increases num colors until no sig improvement
        while n - 1 < len(improvements) and improvements[n - 1] >= 0.05:
            n += 1
        print(improvements)
        print("Best value is " + str(n))
    kmeans = KMeans(n_clusters=n + 1).fit(clrs)
    clusterNumbers = list(kmeans.labels_)
    colors = list(map(tuple, list(kmeans.cluster_centers_)))
    colors = list(map(lambda t: tuple(map(int, t)), colors))
    # print(colors)
    if n == 1:
        colors = (
            [(0, 0, 0), (255, 255, 255)]
            if colors[0][0] < colors[1][0]
            else [(255, 255, 255), (0, 0, 0)]
        )
    return (clusterNumbers, colors)


def changeColors(img, n=1):
    clusterNumbers, colors = getColors(img, n)
    width = img.shape[1]
    height = img.shape[0]
    # print(str(n)+" colors (BGRA): " + ", ".join(str(x) for x in colors))
    assert not (type(n) == int) or n == 0 or len(colors) == n + 1, (
        "There are " + str(len(colors)) + " but I wanted " + str(n + 1) + "..."
    )
    # pprint(["".join(list(map(str,clusterNumbers[k*width:(k+1)*width]))) for k in range(height)])
    newImg = [colors[k] for k in clusterNumbers]
    newImg = np.array(newImg)
    newImg = newImg.reshape(height, width, len(colors[0])).astype("float32")

    # # In case you want to preview the picture in your terminal...
    # if len(colors)<10:
    #     print("\n".join(["".join(list(map(str,clusterNumbers[i*width:(i+1)*width]))) for i in range(height)]))

    # # To see the colors
    # if len(colors)>2:
    #     clrsImg = [[[x for asdf in range(100)] for x in colors] for qwer in range(100)]
    #     clrsImg = np.array(clrsImg)
    #     clrsImg = clrsImg.reshape(100, len(colors)*100, len(colors[0]))
    #     cv2.imwrite(str(hash(colors[0]))+"_"+str(len(colors))+"Colors.png", clrsImg)

    return newImg


# for testing purposes
if __name__ == "__main__":

    PICNUMCLRS = {
        "bwPic.png": 1,
        "cPic.png": 2,
        "Izzet.png": 3,
        "huatli.png": "",
        "nahiri.png": "",
    }

    for f in PICNUMCLRS.keys():
        print(f[:-4])
        currpath = "/Users/lyndonf/Desktop/NonogramMaker/TestPics/"
        img = cv2.imread(currpath + f, cv2.IMREAD_UNCHANGED)
        newImg = pixelize(img)
        cv2.imwrite(currpath + "Res" + f, newImg)
        altImg = changeColors(newImg, PICNUMCLRS[f])
        cv2.imwrite(currpath + "zPix" + f, altImg)
        if PICNUMCLRS[f] > 1:
            bwImg = changeColors(pixelize(img, toBW=True))
            cv2.imwrite(currpath + "zPix_BW" + f, bwImg)
