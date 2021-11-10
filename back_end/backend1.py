import os

from flask import Flask
from flask import request



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    def query_db(query, args=(), one=False):
        cur = db.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/user name')
    def user_name():
        return 'user name'


    @app.route('/user password')
    def uesr_password():
        return 'user password'
#登录界面
    @app.route('/name', methods=['GET', 'POST'])
    def get_name():
        if request.method == 'POST':
            return 'x from POST'
        else:
            return 'x from GET'
#x 用户名
    @app.route('/untermined1')
    def get_attr():
        return 'attribute1'
#待定信息与相关属性

    ## 用户资料endpoint
    #将每个数据看成用户资料
    # R: Read 读取创建的user profile /GET
    # C: Create 创建一个user profile /POST
    # U: Update 更新创建的user profile /PUT
    # D: Delete 删除创建的user profile /DELETE
    @app.route('/userProfile', methods=["GET","POST","PUT","DELETE"])
    def userProfile():
        if request.method == 'GET':
            # name = request.args.get('name', '')
            uid = request.args.get('uid',7)
            # 3. 写sql
            query = "SELECT * FROM userProfile WHERE id = {}".format(uid)
            # 通过用户的id来查询用户资料
            result = query_db(query,one=True)
            # 1. 获取数据库连接
            # 2. 获取一个数据库的游标 cursor
            # 4. 执行sql
            # not robust at all !
            # 别学我！
            if result is None:
                return dict(message="user doesn't exist")
            else:
                username=result['username']
                fans=result['attr']
                print(result['username'])
                print(result['fans'])
                return dict(username=username,arrt=arrt)
            # 5. 处理从数据库里读取的数据
            # 6. 将数据返回给调用者
        elif request.method =='POST':

            print(request.json)
            name = request.json.get('name')
            fans = request.json.get('arrt')
            # 获取post body中的name和arrt
            # 插入新的数据到数据库
            #1. 获取数据库连接
            connection = db.get_db()
            query = "INSERT INTO userProfile (username,arrt) values('{}',{})".format(name,arrt)
            print(query)
            #2. 执行
            try:
                cursor = connection.execute(query)
                # 3. DML data manipulate language 没关系
                # 当你对数据库的数据有改动的时候，需要commit，否则改动不会生效
                # execute的时候就回去数据库里执行这条sql，如果有错误，会报错
                connection.commit()
                print(cursor.lastrowid)
                # select * from userProfile where id =5
                return dict(success=True)
            except:
                return dict(success=False,message="username exist",errorCode=1)
        elif request.method == 'PUT':
            # update
            return '1'
        elif request.method =='DELETE':
            # delete
            uid=request.args.get('uid',1)
            connection = db.get_db()
            query = "delete from userProfile where id = {}".format(uid)
            connection.execute(query)
            connection.commit()
            return dict(success=True)
    return app

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


#通信测试用
from socket import *
import threading
from time import ctime


def Recv(sock, BUFSIZE=1024):
    print('Recver is UP!')
    while True:
        try:
            data, addr = sock.recvfrom(BUFSIZE)
        except OSError:
            break
        print('%s [%s]' % (addr[0], ctime()), data.decode())


def main(targetHost, targetPost=21567):
    HOST = ''
    POST = 21567
    BUFSIZ = 1024
    ADDR = (HOST, POST)

    targetADDR = (targetHost, targetPost)

    UdpSock = socket(AF_INET, SOCK_DGRAM)
    UdpSock.bind(ADDR)
    # 开启新线程，获取信息
    threadrev = threading.Thread(target=Recv, args=(UdpSock, BUFSIZ))
    threadrev.start()
    # 主线程开始传输信息~
    while True:
        data = input('')
        UdpSock.sendto(data.encode(), targetADDR)
        if not data:
            print('End of Chat')
            break
    UdpSock.close()


if __name__ == '__main__':
    IP = input('输入目标机器的IP地址: ')
    main(IP)

#可以建立通信，后续考虑ip限定问题