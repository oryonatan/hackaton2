import pickle
import json

def make_me_gif(image_data, emotion_data):
    """
    make a gif from an image using emotion_data 
    :param image_data: raw data of image 
    :param emotion_data: data returned from ms emotion 
    :return: raw gif file
    """
    return "this is supposed to be raw gif data"

with open('emotions_resp','rb') as emotion_response_file:
    emotion_response = pickle.load(emotion_response_file)


def test_me_gif():
    with open("sad.jpg",'rb') as image:
        image_data= image.read()
        make_me_gif(image_data, json.loads(emotion_response)[0])



if __name__ == '__main__':
    test_me_gif()