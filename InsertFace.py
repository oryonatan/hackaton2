import math
import cv2
import os
import numpy as np
from os import listdir
from os.path import isfile, join

#import os
#from PIL import Image

GifSizeR = 1080
gifSizeC = 1080


LocationDictForEachEmotionAtndEachFrame = {
    'SAD': [[372,519],[372,519],[372,519],[372,519],[372,519],[372,519]],
    'ANGRY': [[540,540], [540,540], [278,564],[303,619],[344,651],[790,505],[625,601],[675,721],[796,793],[865,876],[540,540]],
    'SURPRISED': [[350,370],[350,370],[350,370],[350,370],[350,370],[350,370],[350,370],[350,370],[350,370],[350,370]],
    'HAPPY': [[291,739],[293,736],[399,655],[545,270],[540,271]]

}

def getColRowForEachEmotionAndEachFrame(emotionType, frameIdx):
    return

def blendImagesWithMask(imFace,imGif,imMask):
    imMask = imMask / 255
    x= (imFace*imMask + imGif*(1-imMask)).astype(np.uint8)
    return x

def locateFaceInMaskArea(CGif,RGif, resizedImFace):
    targetWidth, targetHeight, depth = resizedImFace.shape
    startC = CGif - math.floor(targetWidth / 2)
    endC = CGif + math.ceil(targetWidth / 2)
    startR = RGif - math.floor(targetHeight / 2)
    endR = RGif + math.ceil(targetHeight / 2)
    imGifWithFace = np.zeros((GifSizeR,gifSizeC, 3),dtype=np.uint8) # maybe the opposite direction
    imGifWithFace[startC:endC, startR:endR, :] = resizedImFace
    return imGifWithFace

def insertFaceToGIFSeries(emotionType, resizedImFace):
    emotionGifDirPath =  'GIFimages/' + emotionType + '/GIF_images'
    emotionMaskDirPath = 'GIFimages/' + emotionType + '/mask_images'

    #GIF_images = os.listdir(EmotionGifDirPath)
    #mask_images = os.listdir(EmotionMaskDirPath)
    #EmotionGifDirPath = 'GIFimages/' + emotionType
    #GIF_images = os.listdir(EmotionGifDirPath)

    # outputPath = '/cs/grad/ng6767535/PycharmProjects/untitled/GIFimages/HAPPY'
    finalSeries = []
    frameIdx=0
    GifFiles = [f for f in listdir(emotionGifDirPath) if isfile(join(emotionGifDirPath, f))]
    MaskFiles = [f for f in listdir(emotionMaskDirPath) if isfile(join(emotionMaskDirPath, f))]
    GifFiles.sort()
    MaskFiles.sort()
    for i in range(len(GifFiles)):
        imGif = cv2.imread(join(emotionGifDirPath,GifFiles[i]))
        imMask = cv2.imread(join(emotionMaskDirPath, MaskFiles[i]))
        #initialize according to emmotion
        CGif, RGif = LocationDictForEachEmotionAtndEachFrame[emotionType][frameIdx]
        # locate
        imGifWithFace = locateFaceInMaskArea(CGif, RGif, resizedImFace)
        print(join(emotionGifDirPath,GifFiles[i]))
        print(join(emotionGifDirPath, MaskFiles[i]))
        blendIm= blendImagesWithMask(imGifWithFace,imGif,imMask)
        cvtblendIm = cv2.cvtColor(blendIm,cv2.COLOR_BGR2RGB)
        finalSeries.append(cvtblendIm)
        frameIdx=frameIdx+1
        # cv2.imwrite(join(outputPath,str(frameIdx)+'.jpg'),blendIm)

    return finalSeries

##############################################################
"""
imFacePath = '/cs/grad/ng6767535/Desktop/111/11.png'
imFace = cv2.imread(imFacePath, 1)
imGifPath = '/cs/grad/ng6767535/Desktop/111/1.JPG'
imGif = cv2.imread(imGifPath, 1)
imFaceRTopLeft = 320
imFaceCTopLeft = 180
imFaceWidthC = 156
imFaceHeightR = 108

startC = imFaceCTopLeft
endC = imFaceCTopLeft + imFaceWidthC

startR = imFaceRTopLeft
endR = imFaceRTopLeft + imFaceHeightR

imGif = cv2.imread(imGifPath, 1)
heightGif = 470-350
RGif = 410
CGif = 590
imGifSmall = imGif[350:470, 540:600, :]
cv2.imshow('ImageWindow', imGifSmall)
cv2.waitKey()
"""