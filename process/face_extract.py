#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 23:11

'提取人脸图片'

__author__ = 'Judgement'

import os
from multiprocessing.pool import Pool

import face_recognition
from PIL import Image
import pymongo

client = pymongo.MongoClient()
db = client.similar_star_db
collection = db.image


def extract_face(image_path, filename, save_path='../images/faces'):
    '''

    Args:
        image_path: 图片的地址，如C:/images/a.jpg
        filename: 保存的文件名称
        save_path: 保存的文件的地址

    Returns:人脸的数目

    '''
    path = f'{save_path}/{filename}'
    image = face_recognition.load_image_file(image_path)
    location = face_recognition.face_locations(image)
    if len(location) == 1:
        top, right, bottom, left = location[0]
        face = image[top:bottom, left:right]
        face_pil = Image.fromarray(face)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(path, 'wb') as f:
            face_pil.save(f)
    return len(location)


def extract_insert(images_path, filename, count):
    if collection.find({"filename": filename}).count() != 0:
        return
    if extract_face(f'{images_path}/{filename}', filename) != 1:
        return
    collection.insert_one({"filename": filename})
    print(count, filename)


if __name__ == '__main__':
    images_path = '../images'
    pool = Pool(5)
    count = 1
    for filename in os.listdir(images_path):
        pool.apply_async(extract_insert, args=(images_path, filename, count))
        count = count + 1
    pool.close()
    pool.join()
