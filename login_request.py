import session as sess
import data_base as db
import render_html as html


def login_check(username, password, sessionID):
    ret = sess.check_client_login(username=username)
    print("ret: " + str(ret))
    if ret == 1:
        check_result = db.check_password(username, password)
        if check_result == "Pass":
            sess.set_client_name(username, sessionID)
            return html.render(html.render_navbar(username))
        elif check_result == "WrongPassword":
            return html.render(html.render_navbar(), html.login_html.wrong_password)
        elif check_result == "WrongUsername":
            return html.render(html.render_navbar(), html.login_html.no_user_found)
    elif ret == 0:
        return html.render(html.render_navbar(), html.login_html.already_login)


def change_pass_check(password, newPassword1, newPassword2, sessionID):
    ret = sess.check_login(sessionID)
    if newPassword1 != newPassword2:
        return html.render(html.render_navbar(ret), html.changePass_html.no_same_password)
    if db.check_password(ret, password) == "WrongPassword":
        return html.render(html.render_navbar(username=ret), html.changePass_html.false_old_password)
    db.update_pass(ret, newPassword1)
    return html.render(html.render_navbar(username=ret))


def register_check(username, password1, password2, email, sessionID):
    result = db.check_username(username)
    if result == 1:
        return html.render(html.render_navbar(), html.register_html.has_been_registed)
    if password1 != password2:
        return html.render(html.render_navbar(), html.register_html.password_not_same)
    db.user_register(username, password1, email, sessionID)
    return html.render(html.render_navbar(username))


def forget_pass_check(username, password1, password2):
    pass


def send_mail():
    pass


def register_request(username):
    return html.render(html.render_navbar(username), html.register_html.already_login)


def changePass_request():
    return html.render(html.render_navbar(), html.changePass_html.no_login)


def login_request(username):
    return html.render(html.render_navbar(username), html.register_html.already_login)
