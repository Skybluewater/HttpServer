import sqlite3
import threading
import session

conn = sqlite3.connect("data_base.db", check_same_thread=False)
dataBaseLock = threading.RLock()


def check_password(username, password):
    sql_query = """
        select Password from BaseInfo where Username = "{username}"
    """.format(username=username)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return "WrongUsername"
    # print("check result = " + str(result))
    if result[0][0] == password:
        return "Pass"
    else:
        return "WrongPassword"


def check_username(username):
    sql_query = """
        select * from BaseInfo where Username = "{username}"
    """.format(username=username)
    cursor = conn.cursor()
    result = cursor.execute(sql_query).fetchall()
    if len(result) == 0:
        return 0
    return 1


def user_register(username, password, email, sessionID):
    sql_insert = """
        insert into BaseInfo (Username, Password, Email) values ("{username}","{password}","{email}")   
    """.format(username=username, password=password, email=email)
    cursor = conn.cursor()
    dataBaseLock.acquire()
    try:
        cursor.execute(sql_insert)
    finally:
        conn.commit()
    dataBaseLock.release()
    session.set_client_name(username, sessionID)


def update_pass(username, password):
    sql_update = """
        update BaseInfo Set Password = "{password}" where Username = "{username}"
    """.format(password=password, username=username)
    cursor = conn.cursor()
    dataBaseLock.acquire()
    try:
        cursor.execute(sql_update)
    finally:
        conn.commit()
    dataBaseLock.release()
    cursor.close()
