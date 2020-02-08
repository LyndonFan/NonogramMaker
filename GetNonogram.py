import cv2 
from os import *
from glob import *
import matplotlib.pyplot as plt


def getBackgroundColor(img):
    width = img.shape[1]
    height = img.shape[0]
    clrs = {}
    clrsBoundary = {}
    clrsMiddle = {}
    for i in range(width):
        for j in range(height):
            c = img[j,i]
            k = sum([c[len(c)-1-p] * 1000**p for p in range(len(c))])
            try:    #basic
                clrs[k] += 1
            except:
                clrs[k] = 1
            try:    #is on edge
                clrsBoundary[k] += int(i*j*(width-1-i)*(height-1-j)==0)
            except:
                clrsBoundary[k] = int(i*j*(width-1-i)*(height-1-j)==0)
            try:    #center
                clrsMiddle[k] += int((i-width//2) < width//4 and (j-height//2) < height//4)
            except:
                clrsMiddle[k] = int((i-width//2) < width//4 and (j-height//2) < height//4)
    candidateClrs = list(sorted(clrs.keys(), key = lambda c: clrs[c], reverse = True))
    assert len(candidateClrs)<=11, "There are too many colors to begin with..."
    while len(candidateClrs)>0:
        h = candidateClrs[0]
        if clrs[h] >= img.size // 20 and clrsBoundary[h] >= 2*(width+height) // 10 and clrsMiddle[h] <= img.size // 4:
            break
        candidateClrs.pop(0)
    if len(candidateClrs)==0:
        raise Exception, "There doesn't seem to be a suitable background color..."
    else:
        return candidateClrs[0]
    


def toNonogram(img):
    return

if __name__ == "__main__":

    PICNUMCLRS = {"bwPic.png": 1, "cPic.png": 2, "Izzet.png": 3, "huatli.png": 10, "nahiri.png": ""}

    for f in PICNUMCLRS.keys():
        print(f[:-4])
        currpath = "/Users/lyndonf/Desktop/NonogramMaker/TestPics/"
        img = cv2.imread(currpath + "zPix" +f, cv2.IMREAD_UNCHANGED)
        '''
        try:
            b,g,r,a = cv2.split(img)
        except:
            b,g,r = cv2.split(img)
        frame_rgb = cv2.merge((r,g,b))
        plt.imshow(frame_rgb)
        plt.show()
        '''
        print(getBackgroundColor(img))