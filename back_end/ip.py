# 接受并执行来自允许IP的POST请求
ALLOWED_IP = ['172.26.69.174']
from webapp2 import RequestHandler


class PostHandler(RequestHandler):
    def post(self):

        # 读取访问ip
        ip = self.request.remote_addr

        # ip在白名单内
        if ip in ALLOWED_IP:
            print('hello')  # 后续操作

        # ip不在白名单内
        else:
            self.error(403)
