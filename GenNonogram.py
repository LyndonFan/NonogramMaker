from Process import *
from Convert import *
import argparse
from os import *
import cv2

def main(fileName, maxDim=80, toBW = False, numColors = "", getResult = True):

    print("Processing "+fileName+"...")
    try:
        processed = cv2.imread(fileName)
    except:
        print(fileName + "is not a path to a valid image")
        sys.exit()
    processed = pixelize(processed, maxDim, toBW)
    processed = changeColors(processed, n = numColors)
    if getResult:
        cv2.imwrite("_Pic"+fileName,processed)
    print("Getting nonogram...")
    bgColor = getBackgroundColor(processed)
    clues = getClues(processed, bgColor)
    height, width = processed.shape[:2]
    product = drawGrid(clues, (width, height), bgColor)
    product = drawClues(np.float32(product), clues, (width, height))
    cv2.imwrite("_Pix"+fileName, product)
    print("Done!")

parser = argparse.ArgumentParser(description = "Make a nonogram from a picture.")
parser.add_argument("image",nargs=1,help="path to image to be processed")
parser.add_argument("-d","--maxDim",default=[80],nargs=1,type=int,help="maximum no. of squares in any dimension in the nonogram (default = 80)")
parser.add_argument("-b","--blackAndWhite",action="count",help="indicate the image should be converted to black and white")
parser.add_argument("-n","--numColor","--numColour",nargs="?",type=int,default=0,help="positive integer to denote the number of colors that should appear in your nonogram IN ADDITION to your background color.\nA 0 or negative integer means the algorithm will choose this number for you. \n (default = 0)")
parser.add_argument("-r","--getResult",nargs="?",type=bool,default=True,help="boolean to indicate whether you want the finished picture (default = True)")
args = parser.parse_args()
print(args)
main(args.image[0], args.maxDim[0], bool(args.blackAndWhite), (1 if args.blackAndWhite else args.numColor), args.getResult)