# -*- coding=utf-8 -*-
import socket
import threading
import HttpHead as HH
import session as sess

numConnect = 20

''''# 每个任务线程
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):  # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))  '''


def find() -> int:
    for i in range(numConnect):
        if HH.clientIDArray[i] == 0:
            return i


def ifNeed2Block(addr):
    flag = 0
    IPIndex = 0
    HH.lock.acquire()
    for IPIndex in range(len(HH.listIP)):
        if HH.listIP[IPIndex][0] == addr[0]:
            flag = 1
            HH.listIP[IPIndex][1] += 1
            break
    if flag == 0:
        HH.listIP.append([addr[0], 1])
        IPIndex = len(HH.listIP) - 1
    HH.lock.release()
    return IPIndex


def tcp_link(sock, addr, clientID, event):
    # print('Accept new connection from %s:%s...' % addr)
    print('client IP is: %s' % addr[0])
    print('client PORT is: %s' % addr[1])
    IPIndex = ifNeed2Block(addr)
    ret = sess.check_client_session(addr)
    # print("the value returns from sess: " + str(ret))
    if ret == -1:
        sess.insert_client_session(addr, sess.generate_session())
    else:
        sess.update_client_session(ret)
    request = sock.recv(1024)
    http_req = HH.HttpRequest(sock, addr, clientID, event, threading.current_thread())
    http_req.passRequest(request)
    http_req.getResponse()
    http_req.lastHandle()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threading.Thread(target=sess.refresh_session).start()
    s.bind(('127.0.0.1', 9999))
    s.listen(128)
    # thread_pool = ThreadPoolManger(numConnect)
    print('listen in %s:%d' % ('127.0.0.1', 9999))
    while True:
        sock, addr = s.accept()
        clientID = find()
        HH.clientIDArray[clientID] = 1
        HH.listThread.append(clientID)
        print("The Thread Running now is: " + str(HH.listThread))
        if len(HH.listThread) > numConnect:
            HH.lock.acquire()
            try:
                HH.threadNumber = HH.listThread[0]
                print("Find conflict and the conflict ThreadNumber is: " + str(HH.threadNumber))
                event = HH.clientEvent[0]
                event.set()
            finally:
                HH.lock.release()
            HH.serverEvent.wait()
            HH.serverEvent.clear()
        HH.clientEvent.append(threading.Event())
        client = threading.Thread(target=tcp_link, args=(sock, addr, clientID, HH.clientEvent[-1]))
        client.start()


if __name__ == '__main__':
    for i in range(0, numConnect + 1):
        HH.clientIDArray.append(0)
    start_server()
    pass
