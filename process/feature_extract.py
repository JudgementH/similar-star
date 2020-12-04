#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 13:22

'利用VGG19进行特征提取https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/'

__author__ = 'Judgement'

import pymongo
import tensorflow as tf
import numpy as np

client = pymongo.MongoClient()
db = client.similar_star_db
collection = db.image


def get_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.ZeroPadding2D((1, 1), input_shape=(224, 224, 3)))
    model.add(tf.keras.layers.Convolution2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(128, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(128, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(256, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(256, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(256, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(512, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(512, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(512, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(512, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(512, (3, 3), activation='relu'))
    model.add(tf.keras.layers.ZeroPadding2D((1, 1)))
    model.add(tf.keras.layers.Convolution2D(512, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(tf.keras.layers.Convolution2D(4096, (7, 7), activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Convolution2D(4096, (1, 1), activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Convolution2D(2622, (1, 1)))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Activation('softmax'))

    return model


def preprocess_image(image_path: str):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.vgg19.preprocess_input(img)
    return img


if __name__ == '__main__':
    model = get_model()
    model.load_weights('vgg_face_weights.h5')
    vgg_face_descriptor = tf.keras.Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)

    image_datas = []
    images_path = '../images'

    for image_data in collection.find({}):
        # if "vec" not in image_data:
        image_datas.append(image_data)
    for i, image_data in enumerate(image_datas):
        img_path = f"{images_path}/faces/{image_data['filename']}"
        img = preprocess_image(img_path)

        features = vgg_face_descriptor.predict(img)
        print(i, img_path)
        feature = features[0].tolist()
        collection.update_one({"_id": image_data["_id"]}, {
            "$set": {
                "feature": feature
            }
        })
