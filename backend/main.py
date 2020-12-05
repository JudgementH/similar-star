#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/5 13:15

'flask后台'

__author__ = 'Judgement'

import base64
import os
import time

from flask import Flask, request, make_response
from flask_cors import CORS

import sys

sys.path.append('..')
from api import get_similar_stars

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r"/*")


@app.route('/', methods=['POST'])
def hello():
    return "Hello,World!"


@app.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':
        param = request.form.to_dict()
        image_base64 = param['imageData']
        b64_data = image_base64.split(';base64,')[1]
        data = base64.b64decode(b64_data)
        image_url = save_image_file("../images/upload", data)
        stars = get_similar_stars(image_url,
                                  save_path='../images/temp',
                                  model_path='../process/vgg_face_weights.h5',
                                  size=9)
        return {'stars': stars}
    return "error"


def save_image_file(image_url, data):
    if not os.path.exists(image_url):
        os.makedirs(image_url)
    t = int(time.time())
    image_url = f"{image_url}/{t}.jpg"
    with open(image_url, 'wb') as f:
        f.write(data)
    return image_url


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
