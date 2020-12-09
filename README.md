# similar-star

找到相似的明星脸

Find the most similar star





## project images



![image-20201205215315144](.\note_images\image-20201205215315144.png)



**search for similar stars**

![image-20201205215607819](.\note_images\image-20201205215607819.png)

![image-20201205215622775](.\note_images\image-20201205215622775.png)



## Get start

### 1) Installation

**Requirements**

+ Python 3.8
+ pymongo
+ requests
+ beautifulsuop4
+ dlib
+ face_recognition
+ pillow
+ TensorFlow
+ elasticsearch
+ flask
+ flask_cors



**Installation**

```
pip install -r requirement.txt
```



### 2) Download Resources

+ **Pre-trained weights** of model
  [Google Drive](https://drive.google.com/file/d/1CPSeum3HpopfomUEK1gybeuIVoeJT_Eo/view?usp=sharing])
  move **Pre-trained weights** into `./process`
+ Increase the number of elasticsearch's vector **dims to 4096**
  [baidu](https://pan.baidu.com/s/1KCTSuCL5hXtvHGSSN3hMxQ) 
  password:4l0i
+ **MongoDB**
  [MongoDB](https://www.mongodb.com/)



### 3) Craw Data

Launch **MongoDB** and create **datebase** named similar_star_db with **collection** named star

```
//cd ./crawler
python ./star_crawler.py
python ./download_image.py
```



### 4) Create Index

Ensure your ElasticSearch support 2622-dimension vector

Launch `ElasticSearch.bat`

```
//cd ./process
python ./index_create.py
python ./feature_extract.py
```



### 5) Setup Backend

```
//cd ./backend
python ./main.py
```



### 6) Setup Web

```
cd ./web
```



**project setup**

```
npm install
```



**Compiles and hot-reloads for development**

```
npm run serve
```