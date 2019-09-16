#选照片工具
#按s键保存选中照片，按d键删除选中照片，右键 下一张 左键 上一张 选中照片目录默认在choosepic里，选过的图片显示为黑白
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
    #选过的图片灰化
    if os.path.exists(CHOOSE_DIR+'/'+filename):
        img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',img2)

def choosePic(filename):
    if not os.path.exists(CHOOSE_DIR):
        os.mkdir(CHOOSE_DIR)
    if not os.path.exists(CHOOSE_DIR+'/'+filename):
        copyfile(filename,CHOOSE_DIR+'/'+filename)

def unchoosePic(filename):
    if os.path.exists(CHOOSE_DIR+'/'+filename):
        os.remove(CHOOSE_DIR+'/'+filename)

def showPics(piclist):
    picCount = len(piclist)
    if len(piclist)==0:
        return
    index = 0
    showImage(piclist[index])
    while True:
        key = cv2.waitKeyEx(0)  #用waitkey捕捉不到左右键
        if  key == 27:
            cv2.destroyAllWindows()
            break
        if key == 2555904:  #右键
            if index == picCount-1:
                index = 0
            else:
                index +=1
            showImage(piclist[index])
        if key == 2424832:  #左键
            if index == 0:
                index = picCount-1
            else:
                index -=1
            showImage(piclist[index])
        if key == ord('s'):
            choosePic(piclist[index])
            showImage(piclist[index])
        if key == ord('d'):
            unchoosePic(piclist[index])
            showImage(piclist[index])

if __name__== '__main__':
    piclist = getPicFiles()
    showPics(piclist)
