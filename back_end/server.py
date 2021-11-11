#! ./venv/bin/python3.9
###################################################
# server.py
# this file contains function that serve as webserver
# and communicate library camera and algorithm.
###################################################

from flask import Flask
from flask import Response
from flask import request

import jwt
from datetime import datetime, timedelta

import re
import json
import sqlite3

import threading
import time

########################################
#    constant and global variable      #
########################################
app = Flask(__name__)
SECRET_KEY = 'gr_ehe^%*gbf3w*()dw&^'
DBNAME = "db/librarian.db"


########################################
#             http handler             #
#  The front end reads server data     #
#  through specific API. All data      #
#  stored in local data base in ./db   #
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

    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    cursor = c.execute("""
        SELECT * FROM __account__
        WHERE username=:username AND password=:password;
    """, {"username": username, "password": password})

    if len(list(cursor)) != 0:
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

        c.close()
        conn.close()

        return json.dumps(ret, ensure_ascii=False), 200
    else:
        c.close()
        conn.close()

        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401


@app.route('/api/statistics', methods=['GET'])
def statistics_handler():
    date_now = datetime.now().strftime('%Y-%m-%d')

    token = request.headers.get("authorization")

    try:
        info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = info["username"]

        conn = sqlite3.connect(DBNAME)
        c = conn.cursor()
        cursor = c.execute("""
            SELECT * FROM __account__
            WHERE username=?
        """, [username])

        if len(list(cursor)) == 0:
            c.close()
            conn.close()
            ret = {
                'code': 401,
                'msg': "用户不存在或密码错误",
            }
            return json.dumps(ret, ensure_ascii=False), 401

        cursor = c.execute("""
            SELECT [time], [traffic], [violation] FROM __statistics__
            WHERE date=?
        """, [date_now])

        data = []

        for row in cursor:
            t = row[0]
            traffic = row[1]
            violation = row[2]

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

        c.close()
        conn.close()
        return json.dumps(ret, ensure_ascii=False), 200

    except Exception as e:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401


@app.route('/api/violation', methods=['GET'])
def violation_handler():
    date_now = datetime.now().strftime('%Y-%m-%d')

    token = request.headers.get("authorization")

    try:
        info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = info["username"]

        conn = sqlite3.connect(DBNAME)
        c = conn.cursor()
        cursor = c.execute("""
                SELECT * FROM __account__
                WHERE username=?
            """, [username])

        if len(list(cursor)) == 0:
            c.close()
            conn.close()
            ret = {
                'code': 401,
                'msg': "用户不存在或密码错误",
            }
            return json.dumps(ret, ensure_ascii=False), 401

        cursor = c.execute("""
                SELECT [time], [position], [pic1], [pic2], [pic3], [pic4], [pic5] FROM __violation__
                WHERE date=?
            """, [date_now])

        data = []

        for row in cursor:
            t = row[0]
            position = row[1]
            images = [
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
            ]

            # TODO:读取图片并转化为base64编码

            hour_sta = {
                "time": t,
                "position": position,
                "images": images
            }

            data.append(hour_sta)

        ret = {
            "code": 200,
            "msg": "请求成功",
            "date": date_now,
            "data": data
        }

        c.close()
        conn.close()
        return json.dumps(ret, ensure_ascii=False), 200

    except Exception as e:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401


@app.route('/api/history/statistics', methods=['GET'])
def his_statistics_handler():
    date_now = request.get_json(force=True)["date"]

    token = request.headers.get("authorization")

    try:
        info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = info["username"]

        conn = sqlite3.connect(DBNAME)
        c = conn.cursor()
        cursor = c.execute("""
            SELECT * FROM __account__
            WHERE username=?
        """, [username])

        if len(list(cursor)) == 0:
            c.close()
            conn.close()
            ret = {
                'code': 401,
                'msg': "用户不存在或密码错误",
            }
            return json.dumps(ret, ensure_ascii=False), 401

        cursor = c.execute("""
            SELECT [time], [traffic], [violation] FROM __statistics__
            WHERE date=?
        """, [date_now])

        data = []

        for row in cursor:
            t = row[0]
            traffic = row[1]
            violation = row[2]

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

        c.close()
        conn.close()
        return json.dumps(ret, ensure_ascii=False), 200

    except Exception as e:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401

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

    try:
        info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = info["username"]

        conn = sqlite3.connect(DBNAME)
        c = conn.cursor()
        cursor = c.execute("""
                SELECT * FROM __account__
                WHERE username=?
            """, [username])

        if len(list(cursor)) == 0:
            c.close()
            conn.close()
            ret = {
                'code': 401,
                'msg': "用户不存在或密码错误",
            }
            return json.dumps(ret, ensure_ascii=False), 401

        cursor = c.execute("""
                SELECT [time], [position], [pic1], [pic2], [pic3], [pic4], [pic5] FROM __violation__
                WHERE date LIKE ? AND position LIKE ?;
            """, [date_now, position])

        data = []

        for row in cursor:
            t = row[0]
            position = row[1]
            images = [
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
            ]

            # TODO:读取图片并转化为base64编码

            hour_sta = {
                "time": t,
                "position": position,
                "images": images
            }

            data.append(hour_sta)

        ret = {
            "code": 200,
            "msg": "请求成功",
            "date": date_now,
            "data": data
        }

        c.close()
        conn.close()
        return json.dumps(ret, ensure_ascii=False), 200

    except Exception as e:
        ret = {
            'code': 401,
            'msg': "用户不存在或密码错误",
        }
        return json.dumps(ret, ensure_ascii=False), 401

def init():
    sql_create_account = """
        CREATE TABLE IF NOT EXISTS __account__(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username CHAR(20) NOT NULL,
            password CHAR(30) NOT NULL
        )
    """

    sql_create_statistics = """
        CREATE TABLE IF NOT EXISTS __statistics__(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date CHAR(10) NOT NULL,
            time CHAR(10) NOT NULL,
            traffic INT,
            violation INT
        )
    """

    sql_create_violation = """
        CREATE TABLE IF NOT EXISTS __violation__(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date CHAR(10) NOT NULL,
        time CHAR(10) NOT NULL,
        position INT NOT NULL,
        pic1 CHAR(50),
        pic2 CHAR(50),
        pic3 CHAR(50),
        pic4 CHAR(50),
        pic5 CHAR(50)
    )
    """

    connection = sqlite3.connect("db/librarian.db", )
    cursor = connection.cursor()

    print("database connected")

    cursor.execute(sql_create_account)
    cursor.execute(sql_create_violation)
    cursor.execute(sql_create_statistics)
    connection.commit()

    print("query commit")

    connection.close()

def getPictures():
    pass

def putPictures(pic: list):
    pass

def process():
    pass

def setResults():
    pass

def process_handler():
    # step1: get pictures from camera
    pic = getPictures()
    # step2: store in local folder
    putPictures(pic)
    # step3: send pictures to algorithm
    res = process()
    # step4: put results to database
    setResults(res)

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
