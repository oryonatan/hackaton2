import cgi
import http.server
import json
import pickle
from emotion_test import send_to_emotion

status ={}

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
                open("delteme.jpg",'wb').write(file_data)
                # response = handle_image(file_data)


        with open('laser.gif','rb') as dummy_gif_file:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(dummy_gif_file.read())
            pass
        # self.wfile.write( giffile )



def handle_image(image_data):
    emotion_response = send_to_emotion(image_data)
    parsed_data = json.loads(emotion_response)[0]
    pickle.dump(parsed_data, open('emotion_resp','wb'))
    ###
    #TODO: here goes ronen and naama code
    ###



    return emotion_response

def run(server_class=http.server.HTTPServer,
        handler_class=ImageHandler):
    server_address = ('', 8001)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()

