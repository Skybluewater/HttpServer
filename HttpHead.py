# -*- coding:utf-8 -*-
import os
from stop_thread import stop_thread
import threading
import socket
import login_request as login
import session as sess
import log

listIP = []
listThread = []
lock = threading.RLock()
clientEvent = []
serverEvent = threading.Event()
clientIDArray = []
threadNumber = 0

f = open("root/index.html", 'rb')
index_html = f.read()


# 返回码
class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
    FORBIDDEN = "HTTP/1.1 403 Forbidden\r\n"
    UNAUTHORIZED = "HTTP/1.1 401 Unauthorized Access\r\n"
    BAD_REQUEST = "HTTP/1.1 400 Bad Request\r\n"


# 将字典转成字符串
def dict2str(d):
    s = ''
    for i in d:
        s = s + i + ': ' + d[i] + '\r\n'
    return s


def daemon_client(client_socket: socket.socket, clientID, fatherThread: threading.Thread, event, addr):
    event.wait()
    lock.acquire()
    try:
        # try 2 shut down the fatherThread in case that it continues transporting data
        stop_thread(fatherThread)
        client_socket.close()
        clientIDArray[clientID] = 0
        try:
            clientEvent.pop(listThread.index(clientID))
        except Exception as er:
            log.log_list.append("RaiseError: %s\n" % str(er))
        try:
            listThread.remove(clientID)
        except Exception as er:
            log.log_list.append("RaiseError: %s\n" % str(er))
        for i in range(len(listIP)):
            if listIP[i][0] == addr[0]:
                listIP[i][1] -= 1
                if listIP[i][1] == 0:
                    listIP.pop(i)
                break
    finally:
        lock.release()
    serverEvent.set()


class HttpRequest(object):
    RootDir = 'root'
    NotFoundHtml = RootDir + '/404/404.html'
    CookieDir = 'root/cookie/'

    def __init__(self, sock, addr, clientID, event, sess, thread):
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.Cookie = None
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''.encode('utf-8')
        self.session = sess
        self.sock = sock
        self.addr = addr
        self.clientID = clientID
        self.event = event
        self.thread = thread

    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        if self.url == '/':
            self.url = '/index.html'
        self.protocol = header_list[2]

    def passRequestHead(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val
            # print key, val
        if 'Cookie' in self.head:
            self.Cookie = self.head['Cookie']

    def passRequest(self, request):
        deamon = threading.Thread(target=daemon_client,
                                  args=(self.sock, self.clientID, threading.current_thread(), self.event, self.addr))
        deamon.start()
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)
        log.log_list.append(request_line + "\n" + request_head + "\n")
        # 所有post视为动态请求
        # get如果带参数也视为动态请求
        # 不带参数的get视为静态请求
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('&')  # 每一行是一个字段
            for i in parameters:
                if i == '':
                    continue
                key, val = i.split('=', 1)
                self.request_data[key] = val
            self.dynamicRequest(self.url)
        elif self.method == 'GET' or self.method == 'HEAD':
            if self.url.find('?') != -1:  # 含有参数的get
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val
                self.dynamicRequest(HttpRequest.RootDir + s_url)
            else:
                self.staticRequest(HttpRequest.RootDir + self.url)
        else:
            self.response_line = ErrorCode.BAD_REQUEST
            self.response_head['Content-Type'] = 'text/html'
            path = HttpRequest.RootDir + '/400.html'
            f = open(path, 'rb')
            self.response_body = f.read()
            f.close()

    # 只提供制定类型的静态文件
    def staticRequest(self, path):
        if not os.path.isfile(path):
            f = open(HttpRequest.NotFoundHtml, 'rb')
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
            f.close()
        else:
            extension_name = os.path.splitext(path)[-1]  # 扩展名
            tail = path.split('/')[-1]
            if extension_name == '.png':
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'image/png'
                self.response_body = f.read()
                f.close()
            elif extension_name == '.html':
                if self.url == "/index.html":
                    self.response_line = ErrorCode.OK
                    self.response_head['Content-Type'] = 'text/html'
                    self.response_body = index_html
                    return
                if self.url == "/register.html":
                    result = sess.check_login(self.session)
                    if result is not None:
                        self.response_line = ErrorCode.FORBIDDEN
                        self.response_head['Content-Type'] = 'text/html'
                        self.response_body = login.register_request(result).encode('utf-8')
                        return
                elif self.url == "/changePass.html":
                    result = sess.check_login(self.session)
                    if result is None:
                        self.response_line = ErrorCode.UNAUTHORIZED
                        self.response_head['Content-Type'] = 'text/html'
                        self.response_body = login.changePass_request().encode('utf-8')
                        return
                elif self.url == "/login.html":
                    result = sess.check_login(self.session)
                    if result is not None:
                        self.response_line = ErrorCode.FORBIDDEN
                        self.response_head['Content-Type'] = 'text/html'
                        self.response_body = login.login_request(result).encode('utf-8')
                        return
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
                f.close()
            elif extension_name == '.css':
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'text/css'
                self.response_body = f.read()
                f.close()
            elif extension_name == '.js':
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'application/x-javascript'
                self.response_body = f.read()
                f.close()
            elif extension_name == '.py':
                self.dynamicRequest(path)
            elif extension_name == '.ico':
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'image/x-icon'
                self.response_body = f.read()
                f.close()
            elif tail == 'logout':
                ret = sess.check_login(self.session)
                if ret is None:
                    self.response_line = ErrorCode.FORBIDDEN
                    self.response_head['Content-Type'] = 'text/html'
                    self.response_body = login.logout_request().encode('utf-8')
                else:
                    self.response_line = ErrorCode.OK
                    self.response_head['Content-Type'] = 'text/html'
                    self.response_body = login.logout_check(self.session).encode('utf-8')
            else:
                f = open(HttpRequest.NotFoundHtml, 'rb')
                self.response_line = ErrorCode.NOT_FOUND
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
                f.close()

    def dynamicRequest(self, path):
        if path == '/login':
            self.response_body = login.login_check(self.request_data['username'], self.request_data['password'],
                                                   self.session).encode('utf-8')
            self.response_line = ErrorCode.OK
            self.response_head['Content-Type'] = 'text/html'
        elif path == '/changePass':
            self.response_body = login.change_pass_check(self.request_data['password'], self.request_data['password1'],
                                                         self.request_data['password2'], self.session).encode('utf-8')
            self.response_line = ErrorCode.OK
            self.response_head['Content-Type'] = 'text/html'
        elif path == '/register':
            self.response_line = ErrorCode.OK
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = login.register_check(self.request_data['username'], self.request_data['password1'],
                                 self.request_data['password2'], self.request_data['email'], self.session)\
                .encode('utf-8')
        elif path == '/logout':
            ret = sess.check_login(self.session)
            if ret is None:
                self.response_line = ErrorCode.FORBIDDEN
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = login.logout_request().encode('utf-8')
            else:
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = login.logout_check(self.session).encode('utf-8')

    def lastHandle(self):
        lock.acquire()
        try:
            clientIDArray[self.clientID] = 0
            clientEvent.pop(listThread.index(self.clientID))
            listThread.remove(self.clientID)
            for i in range(len(listIP)):
                if listIP[i][0] == self.addr[0]:
                    listIP[i][1] -= 1
                    if listIP[i][1] == 0:
                        listIP.pop(i)
                    break
        finally:
            lock.release()
        # print("client %s:%s quit" % self.addr)
        log.log_list.append("client %s:%s quited\n" % self.addr)

    def getResponse(self):
        headReturn = (self.response_line + dict2str(self.response_head) + '\r\n').encode('utf-8')
        log.log_list.append(headReturn.decode() + "\n")
        bodyReturn = self.response_body
        self.sock.send(headReturn)
        if self.method != 'HEAD':
            try:
                self.sock.send(bodyReturn)
            except Exception as br:
                log.log_list.append("RaiseError: %s\n" % str(br))
        self.sock.close()
