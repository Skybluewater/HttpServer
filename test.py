import threading


class ezf():

    def __init__(self):
        pass

    def abc(self):
        print(threading.current_thread())


def abc():
    print(str(threading.current_thread()) + ' abc ')
    edf()


def edf():
    print(str(threading.current_thread()) + ' edf ')
    cla = ezf()
    cla.abc()


abc()

