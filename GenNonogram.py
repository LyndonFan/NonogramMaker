from Process import *
from Convert import *
import sys, getopt
from os import *
import cv2

def main(argv):

    inputImg = ""
    maxDim = 80

    try:
        opts, args = getopt.getopt(argv,"i:d:c:bw:n:t",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> [-d] [-c] [-bw] [-n]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputImg = cv2.imread(arg)
        elif opt in ("-s", "--maxDim"):
            try:
                maxDim = int(arg)
                assert maxDim>0, "The maximum dimension should be positive: "+str(maxDim)
            except:
                print("Using 80 as maximum dimension...")
                maxDim = 80
        elif 

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile