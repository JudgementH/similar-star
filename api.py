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
from PIL import Image


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


if __name__ == '__main__':
    img = "F:/DD/code/similar-star/images/安雅.jpg"
    face_path = get_face(img)
    feature = get_face_feature(face_path)
    stars = get_stars(feature)
    for star in stars:
        print(star)
