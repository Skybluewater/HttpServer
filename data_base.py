import sqlite3

conn = sqlite3.connect("data_base.db", check_same_thread=False)


def check_password(username,password):
    sql_query = """
        select password from BaseInfo where username = {username}
    """.format(username=username)
    cursor=conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    cursor.close()
    assert cursor.rowcount != 0, "no exists user"
    if result[0][0] == password:
        return True
    else:
        return False
