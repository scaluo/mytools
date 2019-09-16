#选照片工具
#按s键保存选中照片，l键 上一张 j键 下一张 选中照片目录默认在choosepic里
#需安装cv2

#! /usr/bin/env python3
import os
import cv2
from shutil import copyfile

CHOOSE_DIR = 'choosepic'
MAX_LENGTH = 800

def getPicFiles():
    retlist = []
    files = os.listdir('./')
    for f in files:
        if os.path.isfile(f):
            ext = os.path.splitext(f)[1]
            if (ext.lower() == '.jpg'):
                retlist.append(f)
    return retlist

def showImage(filename):
    img = cv2.imread(filename)
    sp = img.shape
    height = sp[0]
    width = sp[1]
    if width>height:
        newwidth = MAX_LENGTH
        newheight = int(newwidth*height/width)
    else:
        newheight = MAX_LENGTH
        newwidth = int(newheight*width/height)
    img2 = cv2.resize(img,(newwidth,newheight))
    cv2.imshow('image',img2)

def choosePic(filename):
    if not os.path.exists(CHOOSE_DIR):
        os.mkdir(CHOOSE_DIR)
    copyfile(filename,CHOOSE_DIR+'/'+filename)

def showPics(piclist):
    picCount = len(piclist)
    if len(piclist)==0:
        return
    index = 0
    showImage(piclist[index])
    while True:
        key = cv2.waitKey(0)
        if  key == 27:
            cv2.destroyAllWindows()
            break
        if key == ord('j'):
            if index == picCount-1:
                index = 0
            else:
                index +=1
            showImage(piclist[index])
        if key == ord('l'):
            if index == 0:
                index = picCount-1
            else:
                index -=1
            showImage(piclist[index])
        if key == ord('s'):
            choosePic(piclist[index])

if __name__== '__main__':
    piclist = getPicFiles()
    showPics(piclist)
