#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 22:19

'一些方便使用的api'

__author__ = 'Judgement'

import os


from process.face_extract import extract_face
from process.feature_extract import get_model, preprocess_image
from process.feature_query import feature_query

import tensorflow as tf
import pymongo

client = pymongo.MongoClient()
db = client.similar_star_db
star_coll = db.star


def get_face(image: str, save_path):
    filename = os.path.basename(image)
    if extract_face(image, filename, save_path=save_path) != 1:
        raise Exception("必须仅为一人")
    face_path = f'{save_path}/{filename}'
    return face_path


def get_face_feature(face_image: str, model_path) -> list:
    model = get_model()
    model.load_weights(model_path)
    vgg_face_descriptor = tf.keras.Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)
    img = preprocess_image(face_image)
    features = vgg_face_descriptor.predict(img)[0]
    return features


def get_stars(features: list, size=10) -> list:
    return feature_query(features, size)


def get_src_by_name(stars: list) -> list:
    for star in stars:
        name = star['name']
        item = list(star_coll.find({"name": name}))[0]
        star['src'] = item['src']
    return stars


def get_similar_stars(image_path: str, save_path, model_path, size=10):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    face_path = get_face(image_path, save_path)
    feature = get_face_feature(face_path, model_path)
    stars = get_stars(feature, size)
    stars = get_src_by_name(stars)
    return stars


if __name__ == '__main__':
    img = "F:/DD/code/similar-star/images/upload/1607154743.jpg"
    stars = get_similar_stars(img, save_path='./images/temp', model_path='./process/vgg_face_weights.h5')
    for star in stars:
        print(star['name'], star['score'], star['src'])
