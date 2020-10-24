# -*- coding:utf-8 -*-
import os
import xml.dom.minidom
from stop_thread import stop_thread
import threading
import socket

listIP = []
listThread = []
lock = threading.RLock()
clientEvent = []
serverEvent = threading.Event()
clientIDArray = []
threadNumber = 0


# 返回码
class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"


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
        clientEvent.pop(listThread.index(clientID))
        listThread.remove(clientID)
        for i in range(len(listIP)):
            if listIP[i][0] == addr[0]:
                listIP[i][1] -= 1
                if listIP[i][1] == 0:
                    listIP.pop(i)
                break
    finally:
        lock.release()
    serverEvent.set()


class Session(object):
    def __init__(self):
        self.data = dict()
        self.cook_file = None

    def getCookie(self, key):
        if key in self.data.keys():
            return self.data[key]
        return None

    def setCookie(self, key, value):
        self.data[key] = value

    def loadFromXML(self):
        import xml.dom.minidom as minidom
        root = minidom.parse(self.cook_file).documentElement
        for node in root.childNodes:
            if node.nodeName == '#text':
                continue
            else:
                self.setCookie(node.nodeName, node.childNodes[0].nodeValue)

    def write2XML(self):
        import xml.dom.minidom as minidom
        dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'Root', None)
        root = dom.documentElement
        for key in self.data:
            node = dom.createElement(key)
            node.appendChild(dom.createTextNode(self.data[key]))
            root.appendChild(node)
        print(self.cook_file)
        with open(self.cook_file, 'w') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')


class HttpRequest(object):
    RootDir = 'root'
    NotFoundHtml = RootDir + '/404/404.html'
    CookieDir = 'root/cookie/'

    def __init__(self, sock, addr, clientID, event, thread):
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.Cookie = None
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''
        self.session = None
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
            self.dynamicRequest(HttpRequest.RootDir + self.url)
        if self.method == 'GET':
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

    # 只提供制定类型的静态文件
    def staticRequest(self, path):
        print(path)
        if not os.path.isfile(path):
            f = open(HttpRequest.NotFoundHtml, 'rb')
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
        else:
            extension_name = os.path.splitext(path)[-1]  # 扩展名
            if extension_name == '.png':
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'image/png'
                self.response_body = f.read()
                f.close()
            elif extension_name == '.html':
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
            else:
                f = open(HttpRequest.NotFoundHtml, 'r')
                self.response_line = ErrorCode.NOT_FOUND
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
                f.close()

    def processSession(self):
        self.session = Session()
        # 没有提交cookie，创建cookie
        if self.Cookie is None:
            self.Cookie = self.generateCookie()
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            self.session.write2XML()
        else:
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            if os.path.exists(cookie_file):
                self.session.loadFromXML()
                # 当前cookie不存在，自动创建
            else:
                self.Cookie = self.generateCookie()
                cookie_file = self.CookieDir + self.Cookie
                self.session.cook_file = cookie_file
                self.session.write2XML()
        return self.session

    def generateCookie(self):
        import time
        import hashlib
        cookie = str(int(round(time.time() * 1000)))
        hl = hashlib.md5()
        hl.update(cookie.encode(encoding='utf-8'))
        return cookie

    def dynamicRequest(self, path):
        # 如果找不到或者后缀名不是py则输出404
        if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
            f = open(HttpRequest.NotFoundHtml, 'r')
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
        else:
            # 获取文件名，并且将/替换成.
            file_path = path.split('.', 1)[0].replace('/', '.')
            self.response_line = ErrorCode.OK
            m = __import__(file_path)
            m.main.SESSION = self.processSession()
            if self.method == 'POST':
                m.main.POST = self.request_data
                m.main.GET = None
            else:
                m.main.POST = None
                m.main.GET = self.request_data
            self.response_body = m.main.app()
            self.response_head['Content-Type'] = 'text/html'
            self.response_head['Set-Cookie'] = self.Cookie

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
        print("client %s:%s quit" % self.addr)

    def getResponse(self):
        headReturn = (self.response_line + dict2str(self.response_head) + '\r\n').encode('utf-8')
        bodyReturn = self.response_body
        self.sock.send(headReturn)
        self.sock.send(bodyReturn)
        print(headReturn)
        self.sock.close()
