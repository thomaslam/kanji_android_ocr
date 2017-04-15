from urllib import pathname2url
from PIL import Image

# TODO: delete this
from sklearn.neural_network import MLPClassifier

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json, os, sys

def MakeHandlerFromArgv(init_args):
    class MyHandler(BaseHTTPRequestHandler, object):
        def __init__(self, *args, **kwargs):
            super(MyHandler, self).__init__(*args, **kwargs)
            self.trained_model = init_args

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=UTF-8')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            return

        def do_POST(self):
            self._set_headers()
            print "in do_POST method"
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            self.parsed_json = json.loads(self.data_string)
            photo = self.parsed_json["photo"]
            # photo_bytestr = ''.join(chr(x) for x in photo) #expect photo to be array of bytes
            # iF = Image.frombytes('F', (128, 127), photo, 'bit', 4)
            # iF.save("example.png", 'PNG', bits=4)

            # TODO: predict using photo
            predicted_code = jis2url("3021") # hard-coded for now
            print predicted_code
            result = {}
            result["parsedCode"] = predicted_code
            self.wfile.write(result)
            return

        def printStuff(self):
            print self.trained_model

    return MyHandler

class ExampleHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=UTF-8')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        return

    def do_POST(self):
        self._set_headers()
        print "in do_POST method"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.parsed_json = json.loads(self.data_string)
        photo_str = self.parsed_json["photo"]
        # photo = self.parsed_json["photo"] #expect photo to be array of bytes
        # photo_bytestr = ''.join(chr(x) for x in photo)
        photo = photo_str.encode()
        print len(photo)
        # iF = Image.frombytes('F', (128, 127), photo, 'bit', 4)
        # iP = iF.convert('P')
        # iP.save("example.png", 'PNG', bits=4)

        # TODO: predict using photo
        predicted_code = jis2url("3021") # hard-coded for now
        print predicted_code
        result = {}
        result["parsedCode"] = predicted_code
        self.wfile.write(result)
        return

def run(trained_model):
    MyHandler = MakeHandlerFromArgv(trained_model)
    http_serv = HTTPServer(('', 15675), ExampleHandler)
    print 'Starting server'
    http_serv.serve_forever()

def jis2url(code):
    b = b'\033$B' + bytes(bytearray.fromhex(code))
    c = b.decode('iso2022_jp')
    url_code = pathname2url(c.encode('utf-8'))
    return url_code

if __name__ == "__main__":
    clf = MLPClassifier(alpha=1e-5, 
                        hidden_layer_sizes=(100),
                        random_state=1)
    run(clf)
