import cv2 
from os import *
from glob import *
import matplotlib.pyplot as plt
import numpy as np
import turtle

def hashColor(c):
    return sum([c[len(c)-1-p] * 1000**p for p in range(len(c))])

def unhashColor(c):
    ans = c
    anstup = []
    while ans>=1000:
        anstup.insert(0, ans%1000)
        ans = ans//1000
    anstup.insert(0, ans)
    anstup = tuple(anstup)
    return anstup

def getBackgroundColor(img):
    width = img.shape[1]
    height = img.shape[0]
    clrs = {}
    clrsBoundary = {}
    clrsMiddle = {}
    for i in range(width):
        for j in range(height):
            c = img[j,i]
            k = hashColor(c)
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
        return unhashColor(candidateClrs[0])
        

def getClues(img, bgColor):
    width = img.shape[1]
    height = img.shape[0]
    hRead = [[img[j,i] for i in range(width)] for j in range(height)]
    vRead = [[img[j,i] for j in range(height)] for i in range(width)]
    def groupColors(arr):
        for x in arr:
            while str(bgColor) in list(map(str,x)):
                x.pop(x.index(bgColor))
        i = 1
        res = []
        count = 1
        curr = arr[0]
        while i < len(arr):
            while i < len(arr) and str(arr[i])==str(curr):
                i += 1
                count += 1
            res.append((curr, count))
            if i < len(arr):
                count = 0
                curr = arr[i]
        assert sum(list([ t[1] for t in res])) == len(arr), "We're missing a few elements here..."
        return res
    hClues = list(map(groupColors,hRead))
    vClues = list(map(groupColors,vRead))
    return (hClues, vClues)

def drawGrid(clues, gridShape, bgColor):
    SQUARESIZE = 40
    hClues, vClues = clues
    maxHClues = max([len(r) for r in hClues])
    maxVClues = max([len(c) for c in vClues])
    width, height = gridShape
    img = np.full(((maxVClues+height)*SQUARESIZE + height + 1,(maxHClues+width)*SQUARESIZE + width + 1, len(bgColor)), 255)
    if bgColor
    img[maxVClues*SQUARESIZE:,maxHClues*SQUARESIZE:] = bgColor
    img[:,[ maxHClues*SQUARESIZE + (SQUARESIZE+1)*k for k in range(width)]] = (0,0,0,0) if len(bgColor)==4 else (0,0,0)
    img[[maxVClues*SQUARESIZE + (SQUARESIZE+1)*k for k in range(height)],:] = (0,0,0,0) if len(bgColor)==4 else (0,0,0)
    return img



if __name__ == "__main__":

    PICNUMCLRS = {"bwPic.png": 1, "cPic.png": 2, "Izzet.png": 3, "huatli.png": 10, "nahiri.png": ""}

    for f in PICNUMCLRS.keys():
        print(f[:-4])
        currpath = "/Users/lyndonf/Desktop/NonogramMaker/TestPics/"
        img = cv2.imread(currpath + "zPix" +f, cv2.IMREAD_UNCHANGED)
        width = img.shape[1]
        height = img.shape[0]
        '''
        try:
            b,g,r,a = cv2.split(img)
        except:
            b,g,r = cv2.split(img)
        frame_rgb = cv2.merge((r,g,b))
        plt.imshow(frame_rgb)
        plt.show()
        '''
        bgColor = getBackgroundColor(img)
        res = getClues(img, bgColor)
        hClues, vClues = res
        print(max([len(x) for x in hClues]), max([len(x) for x in vClues]))
        cv2.imwrite("Grid"+f, drawGrid(res,(width,height),bgColor))


    