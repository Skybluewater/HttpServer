import data_base as db
import sqlite3
import time
import threading

clientSession = []
conn = sqlite3.connect("session.db", check_same_thread=False)
connLock = threading.RLock()


def check_client_session(addr):
    for i in range(len(clientSession)):
        if clientSession[i][0] == addr[0]:
            return clientSession[i][1]
    return -1


def filter_list(excludes):
    s = set(excludes)
    return (x for x in clientSession if x[1] not in s)


def refresh_session():
    cursor = conn.cursor()
    while True:
        sql_query = """
          select sessionID from sess where ({time} - Time) >= 600;
        """.format(time=time.time())
        cursor.execute(sql_query)
        if cursor.rowcount != 0:
            query_result = cursor.fetchall()
            global clientSession
            connLock.acquire()
            clientSession = list(filter_list(query_result))
            try:
                sql_delete = """
                    delete from sess where sessionID in (select sessionID from sess where ({time} - Time) >= 600);
                """.format(time=time.time())
                cursor.execute(sql_delete)
                conn.commit()
            finally:
                connLock.release()
        time.sleep(60)


def insert_client_session(addr, sessionID):
    clientSession.append([addr[0], sessionID])
    cursor = conn.cursor()
    connLock.acquire()
    try:
        sql_insert = """
          insert into sess (clientIP, UserID, Time, SessionID) values ("{addr}",NULL,{time},{session});
        """.format(addr=addr[0], time=time.time(), session=sessionID)

        cursor.execute(sql_insert)
        conn.commit()
    finally:
        connLock.release()
    cursor.close()


def generate_session():
    import hashlib
    session = str(int(round(time.time() * 1000)))
    hl = hashlib.md5()
    hl.update(session.encode(encoding='utf-8'))
    return int(session)
