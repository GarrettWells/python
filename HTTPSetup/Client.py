# Garrett Wells
# 9-4-2018
#
# This program creates a test client
#
# The address/port of the request can be edited in config.py
# Requires
#   - Python >= 3.6
#   - Pillow >= 5.2.0


import webbrowser
from http.client import *
from io import BytesIO
import tempfile
from time import sleep

from PIL import Image

from config import *


class Client:

    def __init__(self):
        client = HTTPConnection(SERVER_ADDRESS, PORT)
        url = '/test.html'
        client.request('GET', url)
        response = client.getresponse()

        # if the client selected the pic
        if url == '/test.jpg':
            img_bytes = response.read()  # the image is current stored as a byte string
            Image.open(BytesIO(img_bytes)).show()  # BytesIO can be used as a file, which Image.open accepts as input

        elif url == '/test.html':
            time_to_wait = 1

            web_page = response.read()  # web page is currently stored as a byte string
            with tempfile.TemporaryFile(mode='w+', suffix='.html') as temp_file:  # create a temp file
                path = temp_file.name  # get the path of the temp file
                temp_file.write(web_page.decode())  # write html code to temp file
                temp_file.seek(0)
                webbrowser.open(path)  # open web page
                sleep(time_to_wait)  # give time for the web browser to open
        elif url == '/test.txt':
            txt = response.read().decode()  # read the byte string from the response, then decode it to a normal string
            print(txt)
        else:
            print(response.read().decode())
        client.close()


Client()
