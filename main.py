#!/usr/bin/python3

import numpy as np
from PIL import Image
import cv2
import sys
import pyocr
import pyocr.builders


def main(image_name):
    moji = []
    string = []
    num = 1
    j = -1
    high_line = 10000

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)

    tool = tools[0]
    imgname = image_name
    img = cv2.imread(imgname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mser = cv2.MSER_create()
    mser.setMinArea(100)
    mser.setMaxArea(800)

    coordinates = mser.detectRegions(gray, None)

    for coord in coordinates:
        bbox = cv2.boundingRect(coord)
        x,y,w,h = bbox
        aspect_ratio = w / h
        if w < 10 or h < 10 or w/h > 5:
            continue
        moji.append([x, y, h, w])

    moji_sort = sorted(moji, key=lambda x: x[1])
    for i in range(len(moji_sort)):
        if high_line >= moji_sort[i][1]-10 and high_line <= (moji_sort[i][1] + moji_sort[i][3]+10):
            string[j].append(moji_sort[i])
        else:
            high_line = moji_sort[i][1]+moji_sort[i][3]/2
            string.append([])
            j = j + 1
            string[j].append(moji_sort[i])

    for i in range(len(string)):
        if len(string[i]) < 30:
            continue
        string_sort = sorted(string[i], key=lambda x: x[0])

        string_sort = np.array(string_sort)

        im = img[string_sort.min(axis=0)[1]-2:string_sort.min(axis=0)[1]+(string_sort.min(axis=0)[1]+string_sort.max(axis=0)[3]-string_sort.min(axis=0)[1]), string_sort.min(axis=0)[0]-2:string_sort.min(axis=0)[0]+(string_sort.max(axis=0)[0]-string_sort.min(axis=0)[0]+string_sort.max(axis=0)[2])]
    
        cv2.imwrite("result"+str(num)+".png", im)
    
        txt = tool.image_to_string(Image.open('result'+str(num)+'.png'), lang="eng", builder=pyocr.builders.TextBuilder(tesseract_layout=6))
        print(txt)

    num = num + 1
    cv2.imwrite("result"+str(num)+".png", img)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python main.py")
        quit()
    
    main(sys.argv[1])

