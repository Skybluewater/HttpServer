import session as sess


def login_request(username, password):
    ret = sess.check_client_login(username=username)
    if ret == 1:
        check_result = sess.db.check_password(username, password)
        if check_result:
            pass
        else:
            pass
    elif ret == 0:
        pass
