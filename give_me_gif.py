import pickle

def make_me_gif(image_data, emotion_data):
    """
    make a gif from an image using emotion_data 
    :param image_data: raw data of image 
    :param emotion_data: data returned from ms emotion 
    :return: raw gif file
    """
    return "this is supposed to be raw gif data"

with open('emotion_resp','rb') as emotion_response_file:
    emotion_response = pickle.load(emotion_response_file)


def test_me_gif():
    with open("delteme.jpg") as image:
        image_data= image.read()
        make_me_gif(image_data, emotion_response)



if __name__ == '__main__':
    test_me_gif()