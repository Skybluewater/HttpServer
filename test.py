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

import sqlite3

conn = sqlite3.connect("session.db", check_same_thread=False)
sql_insert = """
                  insert into sess(sessionID) values(1234);
                """
cursor = conn.cursor()
cursor.execute(sql_insert)
cursor.close()
conn.commit()
conn.close()