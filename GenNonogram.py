from process import *
from convert import *
import argparse
from os import *
import cv2

def main(fileName, maxDim=80, toBW = False, numColors = "", getResult = True, getPuzzle = True):

    print("Processing "+fileName+"...")
    try:
        processed = cv2.imread(fileName)
    except:
        print(fileName + "is not a path to a valid image")
        sys.exit()
    processed = pixelize(processed, maxDim, toBW)
    processed = changeColors(processed, n = numColors)
    basePath = fileName.split("/")
    fileName = basePath[-1]
    basePath = "/".join(basePath[:-1])+"/"
    print("Generating nonogram...")
    if getResult:
        print("Saving result...")
        cv2.imwrite(basePath+"_Pic"+fileName, processed)
    if getPuzzle:
        print("Getting puzzle...")
        bgColor = getBackgroundColor(processed)
        clues = getClues(processed, bgColor)
        height, width = processed.shape[:2]
        product = drawGrid(clues, (width, height), bgColor)
        product = drawClues(np.float32(product), clues, (width, height))
        cv2.imwrite(basePath+"_Pix"+fileName, product)
    print("Done!")

parser = argparse.ArgumentParser(description = "Make a nonogram from a picture.")
parser.add_argument("image",nargs=1,help="path to image to be processed")
parser.add_argument("-d","--maxDim",default=[80],nargs=1,type=int,help="maximum no. of squares in any dimension in the nonogram (default = 80)")
parser.add_argument("-b","--blackAndWhite",action="count",help="indicate the image should be converted to black and white")
parser.add_argument("-n","--numColor","--numColour",nargs="?",type=int,default=0,help="positive integer to denote the number of colors that should appear in your nonogram IN ADDITION to your background color.\nA 0 or negative integer means the algorithm will choose this number for you. \n (default = 0)")
parser.add_argument("-p","--getPuzzle", dest='getPuzzle', action='store_true',help="boolean to indicate whether you want the puzzle with clues (add this to set to True, add -np / --no-getPuzzle to set to False)")
parser.add_argument('-np','--no-getPuzzle','--no-p', dest='getPuzzle', action='store_false')
parser.set_defaults(getPuzzle=True)
parser.add_argument("-r","--getResult", dest='getResult', action='store_true',help="boolean to indicate whether you want the finished picture (add this to set to True, add -nr / --no-getResult to set to False)")
parser.add_argument('-nr','--no-getResult','--no-r', dest='getResult', action='store_false')
parser.set_defaults(getResult=True)
# parser.add_argument("-r","--getResult",nargs="?",type=bool,default=True,help="boolean to indicate whether you want the finished picture (default = True)")
# parser.add_argument('-p','--feature', dest='feature', action='store_true')
args = parser.parse_args()
print("arguments: " + str(args))
main(args.image[0], args.maxDim[0], bool(args.blackAndWhite), (1 if args.blackAndWhite else args.numColor), args.getResult, args.getPuzzle)