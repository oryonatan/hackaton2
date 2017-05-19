import uuid

from PIL import Image
import numpy as np
import os
import io
import binascii

import pickle
import json
import cv2
import math
import InsertFace

HeightWidthGif = {
    'SAD': (144,193),
    'ANGRY': (135,185),
    'SURPRISED': (150,200),
    'HAPPY': (141,193)
}

def convertEmotionStrFile(strEmotion):
    if (strEmotion == 'happiness'):
        return 'HAPPY'
    if (strEmotion == 'sadness'):
        return 'SAD'
    if (strEmotion == 'anger'):
        return 'ANGRY'
    if (strEmotion == 'surprise'):
        return 'SURPRISED'


def findEmotion(emotion_data):
    max_score = 0
    # 'anger'   'contempt'    'surprise'   'disgust'   'fear'   'happiness'   'neutral'   'sadness'
    emotion_data.pop('neutral')
    emotion_data.pop('contempt')
    emotion_data.pop('disgust')
    emotion_data.pop('fear')

    for mood, value in emotion_data.items():
        if value > max_score:
            max_score = value
            max_mood = mood
    return convertEmotionStrFile(max_mood)


def findlocation(emotion_data):
    locations = []
    for loc, value in emotion_data.items():
        locations.append(value)
    return locations


def convertBinaryImToJPG(image_data):
    #image = Image.open(StringIO.S(rimage_data))

    image = Image.open(io.BytesIO(image_data))
    xsize, ysize = image.size

    r, g, b = image.split()
    r_data = np.array(r.getdata())  # data is now an array of length ysize*xsize
    g_data = np.array(g.getdata())
    b_data = np.array(b.getdata())

    data = np.zeros((ysize,xsize,3))
    data[:,:, 0] = r_data.reshape(ysize, xsize)
    data[:,:, 1] = g_data.reshape(ysize, xsize)
    data[:,:, 2] = b_data.reshape(ysize, xsize)
    return data



def make_me_gif(image_data, emotion_data):
    """
    make a gif from an image using emotion_data
    :param image_data: raw data of image
    :param emotion_data: data returned from ms emotion
    :return: raw gif file
    """

    emotionType = findEmotion(emotion_data['scores'])

    locations = emotion_data['faceRectangle']
    imFaceHeightR = locations.get('height')
    imFaceWidthC = locations.get('width')
    imFaceCTopLeft = locations.get('left')
    imFaceRTopLeft = locations.get('top')

    """
    emotionType = 'ANGRY'
    imFaceRTopLeft = 320
    imFaceCTopLeft = 180
    imFaceWidthC = 156
    imFaceHeightR = 108"""

    ####  take care for image  ####

    # take only the face
    startC = imFaceCTopLeft
    endC = imFaceCTopLeft + imFaceWidthC
    startR = imFaceRTopLeft
    endR = imFaceRTopLeft + imFaceHeightR

    temp_file_name = str(uuid.uuid1()) + ".jpg"
    with open(temp_file_name, 'wb') as temp_file:
        temp_file.write(image_data)
        temp_file.close()

    imagecv = cv2.imread(temp_file_name,1)

    imOnlyFace = imagecv[startR:endR,startC:endC, :]
    os.unlink(temp_file_name)

    # resize face
    resizedImFace = cv2.resize(imOnlyFace,(HeightWidthGif[emotionType]))
    # cv2.imshow('ImageWindow', resizedImFace)
    # cv2.waitKey()
    return InsertFace.insertFaceToGIFSeries(emotionType, resizedImFace)


def test_me_gif(imFace):
    with open('happy_emotion_resp', 'rb') as emotion_response_file:
        emotion_response = pickle.load(emotion_response_file)

    # with open(imFace, 'rb') as image:
    #     image_data = image.read()
    image_data = cv2.imread(imFace, 1)
    # return make_me_gif(image_data, json.loads(emotion_response.decode("utf-8"))[0])
    return make_me_gif(image_data, emotion_response)


if __name__ == '__main__':
    # face = '/cs/grad/ng6767535/Desktop/111/11.png'
    face = 'happy.jpg'
    finalSeriesGIF = test_me_gif(face )

    print ("Done")