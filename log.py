import time
log_list = []

f = open("server.log", 'w')


def append_file():
    while True:
        time.sleep(30)
        global log_list
        f.writelines(log_list)
        log_list = []
    f.close()
