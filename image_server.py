import cgi
import http.server
import json
import pickle
from emotion_test import send_to_emotion
from give_gif import make_me_gif
import imageio
import uuid
import os
import numpy as np
status = {}


# handles post data
class ImageHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                file_data = field_item.file.read()
                open("delteme.jpg", 'wb').write(file_data)
                temp_file_name = handle_image(file_data)

        with open(temp_file_name, 'rb') as response_gif:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response_gif.read())
            pass
            # self.wfile.write( giffile )
        os.unlink(temp_file_name)


def handle_image(image_data):
    emotion_response = send_to_emotion(image_data)
    parsed_emotion = json.loads(emotion_response)[0]
    images = make_me_gif(image_data, parsed_emotion)
    temp_file_name = str(uuid.uuid1()) + ".gif"
    imageio.mimsave(temp_file_name, images , duration=0.7)
    return temp_file_name





def run(server_class=http.server.HTTPServer,
        handler_class=ImageHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
