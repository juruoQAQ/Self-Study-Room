#! ./venv/bin/python3.9
###################################################
# server.py
# this file contains function that serve as webserver
# and communicate library camera and algorithm.
###################################################
import base64
import hashlib

from flask import Flask
from flask import request
from flask_cors import CORS
import jwt

from datetime import datetime, timedelta
from PIL import Image
import cv2

import re
import json
import os
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import db.Column, db.Integer, db.String, create_engine
# from sqlalchemy.ext.declarative import declarative_db.Model
# from sqlalchemy.orm import sessionmaker

import threading
import time

########################################
#    constant and global variable      #
########################################
app = Flask(__name__)
CORS(app, supports_credentials=True)
SECRET_KEY = 'gr_ehe^%*gbf3w*()dw&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/library.db'
# engine = create_engine('sqlite:///db/library.db')

########################################
#          datadb.Model definition         #
########################################
db = SQLAlchemy(app)


class __account__(db.Model):
    __tablename__ = '__account__'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)


class __statistics__(db.Model):
    __tablename__ = '__statistics__'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    traffic = db.Column(db.Integer)
    violation = db.Column(db.Integer)


class __violation__(db.Model):
    __tablename__ = '__violation__'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    position = db.Column(db.Integer)
    pic1 = db.Column(db.String)
    pic2 = db.Column(db.String)
    pic3 = db.Column(db.String)
    pic4 = db.Column(db.String)
    pic5 = db.Column(db.String)


########################################
#             http handler             #
#  The front end reads server data     #
#  through specific API. All data      #
#  stored in local data db.Model in ./db   #
########################################
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Welcome to Librarian System'
    # pass


@app.route('/api/login', methods=['POST'])
def login_handler():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']

    username = re.sub('[\'\"\n\r=]', '', username)
    password = re.sub('[\'\"\n\r=]', '', password)

    account = __account__.query.filter(__account__.username == username, __account__.password == password)
    if account.count() != 0:
        # generate token
        payload = {
            'exp': datetime.now() + timedelta(hours=12),
            'username': username,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        ret = {
            'code': 200,
            'msg': "请求成功",
            'token': token
        }
        return json.dumps(ret, ensure_ascii=False), 200

    else:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401


@app.route('/api/statistics', methods=['GET'])
def statistics_handler():
    date_now = datetime.now().strftime('%Y-%m-%d')

    token = request.headers.get("authorization")
    info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = info["username"]

    account = __account__.query.filter(__account__.username == username)
    if account.count() == 0:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401

    data = []

    res = __statistics__.query.filter(__statistics__.date == date_now)
    for row in res:
        t = row.time
        traffic = row.traffic
        violation = row.violation

        hour_sta = {
            "time": t,
            "traffic": traffic,
            "violation": violation
        }
        data.append(hour_sta)

    ret = {
        "code": 200,
        "msg": "请求成功",
        "date": date_now,
        "data": data
    }

    return json.dumps(ret, ensure_ascii=False), 200


@app.route('/api/violation', methods=['GET'])
def violation_handler():
    date_now = datetime.now().strftime('%Y-%m-%d')

    token = request.headers.get("authorization")
    info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = info["username"]

    account = __account__.query.filter(__account__.username == username)
    if account.count() == 0:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401

    data = []

    res = __violation__.query.filter(__violation__.date == date_now)
    for row in res:
        t = row.time
        position = row.position
        images = [
            row.pic1,
            row.pic2,
            row.pic3,
            row.pic4,
            row.pic5,
        ]

        encoded_images = []
        for i in images:
            with open(i, 'rb') as f:
                db.Model64_str = base64.b64encode(f.read())
                encoded_images.append(db.Model64_str)

        hour_sta = {
            "time": t,
            "position": position,
            "images": encoded_images
        }
        data.append(hour_sta)

    ret = {
        "code": 200,
        "msg": "请求成功",
        "date": date_now,
        "data": data
    }
    return json.dumps(ret, ensure_ascii=False), 200


@app.route('/api/history/statistics', methods=['GET'])
def his_statistics_handler():
    date_now = request.get_json(force=True)["date"]

    token = request.headers.get("authorization")

    info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = info["username"]

    account = __account__.query.filter(__account__.username == username)
    if account.count() == 0:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401

    data = []
    res = __statistics__.query.filter(__statistics__.date == date_now)
    for row in res:
        t = row.time
        traffic = row.traffic
        violation = row.violation

        hour_sta = {
            "time": t,
            "traffic": traffic,
            "violation": violation
        }

        data.append(hour_sta)

    ret = {
        "code": 200,
        "msg": "请求成功",
        "date": date_now,
        "data": data
    }
    return json.dumps(ret, ensure_ascii=False), 200


@app.route('/api/history/violation', methods=['GET'])
def his_violation_handler():
    date_now = ""
    position = ""

    try:
        date_now = request.get_json(force=True)["date"]
    except Exception as e:
        date_now = "%"

    try:
        position = request.get_json(force=True)["position"]
    except Exception as e:
        position = "%"

    token = request.headers.get("authorization")

    info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = info["username"]

    account = __account__.query.filter(__account__.username == username)
    if account.count() == 0:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401

    data = []
    res = __violation__.query.filter(__violation__.date == date_now, __violation__.position == position)
    for row in res:
        t = row.time
        position = row.position
        images = [
            row.pic1,
            row.pic2,
            row.pic3,
            row.pic4,
            row.pic5,
        ]

        encoded_images = []

        for i in images:
            with open(i, 'rb') as f:
                db.Model64_str = base64.b64encode(f.read())
                encoded_images.append(db.Model64_str)

        hour_sta = {
            "time": t,
            "position": position,
            "images": encoded_images
        }

        data.append(hour_sta)

    ret = {
        "code": 200,
        "msg": "请求成功",
        "date": date_now,
        "data": data
    }
    return json.dumps(ret, ensure_ascii=False), 200


def init():
    db.create_all()


def getPictures() -> list[Image]:
    capture = cv2.VideoCapture(os.getcwd().strip() + "/video/1.mp4")
    tp = int(time.time()) % (2 * 60)
    timer = 0
    fps = round(capture.get(5))
    while capture.isOpened():
        timer += 1
        ret, frame = capture.read()
        if timer == tp * fps:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            return image


def putPictures(pic: list) -> list[str]:
    root = os.getcwd().strip() + "/img/"
    if not os.path.exists(root):
        os.mkdir(root)

    saved = []
    m = hashlib.md5()

    for img in pic:
        date_now = time.strftime("%Y-%m-%d", time.localtime())
        time_now = time.strftime("%H-%M-%S", time.localtime())
        hashv = hashlib.sha1(img.tobytes()).hexdigest()[0:8]

        path = root + date_now + "/"
        if not os.path.exists(path):
            os.mkdir(path)

        img_name = path + time_now + "-" + hashv + ".jpg"
        img.save(img_name)
        saved.append(img_name)

    return saved


def process(imgs: list[str]):
    pass


def setResults(results):
    pass


def process_handler():
    # step1: get pictures from camera
    pic = getPictures()

    # step2: store in local folder
    saved_img_path = putPictures([pic])

    # step3: send pictures to algorithm
    # res = process(saved_img_path)

    # step4: put results to datadb.Model
    # setResults(res)

    # loop every 10 minute
    global timer
    timer = threading.Timer(600, process_handler)
    timer.start()


# for PyCharm
if __name__ == 'app':
    init()
    process_handler()

# for command line
if __name__ == '__main__':
    init()
    app.run(host="0.0.0.0", port=45786)
    process_handler()
