import cv2 
from os import *
from glob import *
import matplotlib.pyplot as plt
import numpy as np

def hashColor(c):
    try:
        return sum([c[p] * 1000**p for p in range(len(c))])
    except:
        return sum([c[p] * 1000**p for p in range(c.size())])

def unhashColor(c):
    ans = c
    anstup = []
    for i in range(3):
        anstup.append(ans%1000)
        ans = ans//1000
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
    if len(candidateClrs)==2:
        print(candidateClrs)
        if candidateClrs[0] < candidateClrs[1]:
            candidateClrs = candidateClrs[::-1]
        print("Main color(BGR): " + str(unhashColor(candidateClrs[1])))
        print("Background color: " + str(unhashColor(candidateClrs[0])))
        return unhashColor(candidateClrs[0])
    while len(candidateClrs)>0:
        h = candidateClrs[0]
        if clrs[h] >= img.size // 20 and clrsBoundary[h] >= 2*(width+height) // 10 and clrsMiddle[h] <= img.size // 4:
            break
        candidateClrs.pop(0)
    if len(candidateClrs)==0:
        raise Exception("There doesn't seem to be a suitable background color...")
    else:
        remainingClrs = list(map(unhashColor,clrs.keys()))
        remainingClrs.pop(remainingClrs.index(unhashColor(candidateClrs[0])))
        print("{} colors(BGR): ".format(len(remainingClrs)) + ", ".join(str(x) for x in remainingClrs))
        print("Background color: " + str(unhashColor(candidateClrs[0])))
        return unhashColor(candidateClrs[0])
        

def getClues(img, bgColor):
    width = img.shape[1]
    height = img.shape[0]
    hRead = [[list(img[j,i]) for i in range(width)] for j in range(height)]
    vRead = [[list(img[j,i]) for j in range(height)] for i in range(width)]
    #print(hRead[:5])
    def groupColors(inp):
        arr = inp
        #print(arr)
        i = 0
        clues = []
        count = 0
        if len(arr)==0:
            return []
        curr = arr[0]
        while i < len(arr):
            while i < len(arr) and str(arr[i])==str(curr):
                i += 1
                count += 1
            clues.append((curr, count))
            if i < len(arr):
                count = 0
                curr = arr[i]
        assert sum([t[1] for t in clues]) == len(inp), "We aren't getting all the colors...\n" + str(clues) + str(len(inp))
        
        res = []
        for x in clues:
            if not(hashColor(x[0]) == hashColor(bgColor)):
                res.append(x)
        return res
    
    hClues = list(map(groupColors,hRead))
    vClues = list(map(groupColors,vRead))
    #print(hClues[:5])
    #print(vClues[:5])
    return (hClues, vClues)

def drawGrid(clues, imgShape, bgColor, SQUARESIZE = 40):
    hClues, vClues = clues
    maxHClues = max([len(r) for r in hClues])
    maxVClues = max([len(c) for c in vClues])
    width, height = imgShape
    img = np.full(((maxVClues+height)*SQUARESIZE + height + 1,(maxHClues+width)*SQUARESIZE + width + 1, len(bgColor)), 255)
    img[maxVClues*SQUARESIZE:,maxHClues*SQUARESIZE:] = bgColor
    img[:,[ maxHClues*SQUARESIZE + (SQUARESIZE+1)*k for k in range(width+1)]] = (0,0,0) if sum(x for x in bgColor)>=30 else (100,100,100)
    img[[maxVClues*SQUARESIZE + (SQUARESIZE+1)*k for k in range(height+1)],:] = (0,0,0) if sum(x for x in bgColor)>=30 else (100,100,100)
    return img

def drawClues(img, clues, imgShape):
    hClues, vClues = clues
    maxHClues = max([len(r) for r in hClues])
    maxVClues = max([len(c) for c in vClues])
    width = img.shape[1]
    height = img.shape[0]
    SQUARESIZE = (width - imgShape[0] - 1) // (imgShape[0] + maxHClues)
    assert (imgShape[1] + maxVClues) * SQUARESIZE + imgShape[1] + 1 == height, "SQUARESIZE isn't "+str(SQUARESIZE)
    for i in range(len(hClues)):
        startX = (maxHClues-len(hClues[i]))*SQUARESIZE
        startY = (maxVClues+i)*SQUARESIZE+i+1
        for j in range(len(hClues[i])):
            clr = hClues[i][j][0]
            compClr = [(k+122)%255 for k in clr] if sum(clr[:3])>=30 else [255,255,255]
            #print(clr,compClr)
            xOffset = SQUARESIZE//3 if hClues[i][j][1]<10 else 0
            img[startY:startY+SQUARESIZE, startX:startX+SQUARESIZE] = clr
            cv2.putText(img,str(hClues[i][j][1]),(startX+xOffset,startY+4*SQUARESIZE//5),cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=compClr,thickness=2)
            startX += SQUARESIZE
    for i in range(len(vClues)):
        startY = (maxVClues-len(vClues[i]))*SQUARESIZE
        startX = (maxHClues+i)*SQUARESIZE+i+1
        for j in range(len(vClues[i])):
            clr = vClues[i][j][0]
            compClr = [(k+100)%255 for k in clr] if sum(clr[:3])>=30 else [255,255,255] 
            #(clr,compClr)
            xOffset = SQUARESIZE//3 if vClues[i][j][1]<10 else 0
            img[startY:startY+SQUARESIZE, startX:startX+SQUARESIZE] = clr
            cv2.putText(img,str(vClues[i][j][1]),(startX+xOffset,startY+4*SQUARESIZE//5),cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=compClr,thickness=2)
            startY += SQUARESIZE
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
        img = drawGrid(res,(width,height),bgColor)
        cv2.imwrite("Grid"+f, drawClues(np.float32(img), res, (width,height)))


    