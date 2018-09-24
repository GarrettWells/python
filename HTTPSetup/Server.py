# Garrett Wells
# 9-4-2018
#
# This program creates a test server
#
# Server address/port for the test server can be tweaked in config.py
# Requires Python 3.6 or higher

import os
from http import server, HTTPStatus

from config import *


class MyHandler(server.BaseHTTPRequestHandler):

    def _set_headers(self):
        ''' take care of the headers'''
        self.send_response(HTTPStatus.OK)  # send an OK response
        self.end_headers()  # must end headers

    def do_GET(self):
        ''' Function that will be called when client.request("GET") is called'''
        self._set_headers()
        path = os.path.normpath(os.path.abspath(os.getcwd() + self.path))  # append self.path to the end of the CWD
        if self.path != '':
            file = open(path, 'rb')  # open the file in read-only mode in byte form
            str = file.read()  # the file is now stored as a byte string
            self.wfile.write(str)  # wfile.write writes a byte-object to the client
            return
        else:
            self.wfile.write('hello from GET method!'.encode())

    def do_HEAD(self):
        self._set_headers()
        return


class Server:

    def __init__(self):
        print('Started http server on port ' + str(PORT))
        self.server = server.HTTPServer((SERVER_ADDRESS, PORT), MyHandler)
        print(self.server.server_name + ':' + str(self.server.server_port), 'ready')
        self.run()

    def run(self):
        self.server.serve_forever()  # never stop waiting for connection

    def close(self):
        self.server.server_close()


if __name__ == '__main__':
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        server = Server()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
