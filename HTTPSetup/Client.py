# Garrett Wells
# 9-4-2018
#
# This program creates a test client
#
# The address/port of the request can be edited in config.py
# Requires Python 3.6 or higher

import os
import webbrowser
from http.client import *
from io import BytesIO

from PIL import Image

from config import *


class Client:

    def __init__(self):
        client = HTTPConnection(SERVER_ADDRESS, PORT)
        url = '/test.jpg'
        client.request('GET', url)
        response = client.getresponse()

        # if the client selected the pic
        if url == '/test.jpg':
            img_bytes = response.read()  # the image is current stored as a byte string
            Image.open(BytesIO(img_bytes)).show()  # BytesIO can be used as a file, which Image.open accepts as input

        elif url == '/test.html':
            web_page = response.read()  # web page is currently stored as a byte string
            path = os.path.abspath('temp.html')  # get path of to-be temp file
            url = 'file://' + path  # tell web browser the web page is local

            with open(path, 'w') as f:  # write html code to temp file
                f.write(web_page.decode())
            webbrowser.open(url)  # open web page
            os.remove(path)  # remove web page from storage
        elif url == '/test.txt':
            txt = response.read().decode()  # read the byte string from the response, then decode it to a normal string
            print(txt)
        else:
            print(response.read().decode())
        client.close()


Client()
