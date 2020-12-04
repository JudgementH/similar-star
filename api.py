#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 22:19

'一些方便使用的api'

__author__ = 'Judgement'

import os

import requests

from process.face_extract import extract_face
from process.feature_extract import get_model, preprocess_image
from process.feature_query import feature_query

import tensorflow as tf
import pymongo
from PIL import Image
import cv2

client = pymongo.MongoClient()
db = client.similar_star_db
star_coll = db.star


def get_face(image: str):
    filename = image.split('/')[-1]
    save_path = "./"
    if extract_face(image, filename, save_path=save_path) != 1:
        raise Exception("必须仅为一人")
    face_path = f'{save_path}/{filename}'
    return face_path


def get_face_feature(face_image: str) -> list:
    model = get_model()
    model.load_weights('./process/vgg_face_weights.h5')
    vgg_face_descriptor = tf.keras.Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)
    img = preprocess_image(face_image)
    features = vgg_face_descriptor.predict(img)[0]
    return features


def get_stars(features: list) -> list:
    return feature_query(features)


def get_src_by_name(names: list) -> list:
    srcs = []
    for name in names:
        item = list(star_coll.find({"name": name}))[0]
        srcs.append(item['src'])
    return srcs


if __name__ == '__main__':
    img = "F:/1.jpg"
    origin = cv2.imread(img)

    face_path = get_face(img)
    feature = get_face_feature(face_path)
    stars = get_stars(feature)
    print(stars)
    list_ = get_src_by_name(stars)

    for i, item in enumerate(list_):
        filename = item.split('/')[-1]
        path = os.path.join('./temp', filename)
        req = requests.get(item, timeout=60)
        req.raise_for_status()
        with open(path, 'wb') as f:
            f.write(req.content)
        req.close()
        img_ = cv2.imread(path)
        cv2.imshow(str(i), img_)

    cv2.imshow('origin', origin)
    cv2.waitKey()
    cv2.destroyAllWindows()
