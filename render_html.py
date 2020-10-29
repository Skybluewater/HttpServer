class base_html(object):
    head = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <!--倒入本地的BOotstrap样式, 也可以倒入网络上的；-->
        <!--<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"> -->
        <link href="css/bootstrap.css" rel="stylesheet">
        <!--<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">-->
        {style}
    </head>
    <body>
        {nav_bar}
        {body}
        {script}
    </body>
    """

    navbar = """
    <nav class="navbar navbar-default">
    <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                    data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">Todo</a>
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
                <li><a href="#">主页 <span class="sr-only">(current)</span></a></li>
                <li><a href="login.html">登陆</a></li>
                <li><a href="register.html">注册</a></li>
                <li><a href="changePass.html">更改密码</a></li>

            </ul>
            {nav_bar_right}
        </div><!-- /.navbar-collapse -->
        </div><!-- /.container-fluid -->
    </nav>
    """

    navbar_login = """
    <ul class="nav navbar-nav navbar-right">
                    <li class="dropdown">
                        <a class="dropdown-toggle" href="#" id="dropdown" role="button" data-toggle="dropdown"
                           aria-haspopup="true" aria-expanded="false">
                            <span class="caret"></span>
                            菜单栏
                        </a>
                        <ul class="dropdown-menu">
                            <li><a href="/changePass.html">密码记不住?更改密码</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="money">联系我们</a></li>
                        </ul>
                    </li>
                    <li><a href="#">当前在线：{username}</a></li>
                    <li><a href="/logout" method="POST">登出</a></li>
            </ul>
    """

    script = """
        <script src="js/jquery-3.3.1.js"></script>
        <script src="bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>
        <script src="layer/layer.js"></script>
    """

    style = """
    <style>
        .navbar {
            font-size: 130%;
            background: whitesmoke;
            margin-top: 10px;
            padding-top: 5px;
            box-shadow: 2px 2px 2px 2px lightgray;
            height: 60px;
        }
    </style>
    """


# 只涉及body
class login_html(object):
    no_user_found = """
        <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <h1>
            登录
            <small>
                没有账号？
                <a href="./news/index.html">注册</a>
            </small>
        </h1>
        <div class="alert alert-danger">用户不存在</div>
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" class="form-control" name="username" id="username" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" class="form-control" name="password" id="password" placeholder="Password">
            </div>
            <div class="checkbox">
                <label>
                    <input type="checkbox"> 记住密码
                </label>
            </div>
            <button type="submit" class="btn btn-success btn-block">登录</button>
        </form>
    </div>
    </div>
    """

    wrong_password = """
    <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <h1>
            登录
            <small>
                没有账号？
                <a href="./news/index.html">注册</a>
            </small>
        </h1>
        <div class="alert alert-danger">密码错误</div>
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" class="form-control" name="username" id="username" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" class="form-control" name="password" id="password" placeholder="Password">
            </div>
            <div class="checkbox">
                <label>
                    <input type="checkbox"> 记住密码
                </label>
            </div>
            <button type="submit" class="btn btn-success btn-block">登录</button>
        </form>
    </div>
    </div>
    """

    already_login = """
    <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <h1>
            登录
            <small>
                没有账号？
                <a href="./news/index.html">注册</a>
            </small>
        </h1>
        <div class="alert alert-danger">用户已登录</div>
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" class="form-control" name="username" id="username" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" class="form-control" name="password" id="password" placeholder="Password">
            </div>
            <div class="checkbox">
                <label>
                    <input type="checkbox"> 记住密码
                </label>
            </div>
            <button type="submit" class="btn btn-success btn-block">登录</button>
        </form>
    </div>
    </div>
    """


class changePass_html(object):
    no_login = """
    <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
            <h1>
                <div class="alert alert-danger">用户未登录</div>
            </h1>
        </div>
    </div>
    """

    no_same_password = """
    <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <div class="alert alert-danger">密码不一致</div>
        <form action="/changePass" method="POST">
            <div class="form-group">
                <label for="oldPassword">老密码</label>
                <input type="password" class="form-control" name="password" id="oldPassword" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password1">输入密码</label>
                <input type="password" class="form-control" name="password1" id="password1" placeholder="Password">
            </div>
            <div class="form-group">
                <label for="password2">确认密码</label>
                <input type="password" class="form-control" name="password2" id="password2" placeholder="PasswordAgain">
            </div>
            <button type="submit" class="btn btn-success btn-block">注册</button>
        </form>
    </div>
    </div>
    """

    false_old_password = """
    <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <div class="alert alert-danger">密码错误</div>
        <form action="/changePass" method="POST">
            <div class="form-group">
                <label for="oldPassword">老密码</label>
                <input type="password" class="form-control" name="password" id="oldPassword" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password1">输入密码</label>
                <input type="password" class="form-control" name="password1" id="password1" placeholder="Password">
            </div>
            <div class="form-group">
                <label for="password2">确认密码</label>
                <input type="password" class="form-control" name="password2" id="password2" placeholder="PasswordAgain">
            </div>
            <button type="submit" class="btn btn-success btn-block">注册</button>
        </form>
    </div>
    </div>
    """


class register_html(object):
    already_login = """
    <div class="container">
        <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
            <h1>
                <div class="alert alert-danger">用户已登录</div>
            </h1>
        </div>
    </div>
    """

    has_been_registed = """
    <div class="container">
    <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <h1>
            注册
            <small>
                已有账号？
                <a href="login.html">登陆</a>
            </small>
        </h1>
        <div class="alert alert-danger">用户名已注册</div>
        <form action="/register" method="POST">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" class="form-control" name="username" id="username" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password1">输入密码</label>
                <input type="password" class="form-control" name="password1" id="password1" placeholder="Password">
            </div>
            <div class="form-group">
                <label for="password2">确认密码</label>
                <input type="password" class="form-control" name="password2" id="password2" placeholder="PasswordAgain">
            </div>
            <div class="form-group">
                <label for="email">邮箱</label>
                <input type="email" class="form-control" name="email" id="email" placeholder="Email">
            </div>
            <button type="submit" class="btn btn-success btn-block">注册</button>
        </form>
    </div>
    </div>
    """

    password_not_same = """
    <div class="container">
    <div class="col-lg-4 col-lg-offset-4" style="margin-top: 50px">
        <h1>
            注册
            <small>
                已有账号？
                <a href="login.html">登陆</a>
            </small>
        </h1>
        <div class="alert alert-danger">密码不一致</div>
        <form action="/register" method="POST">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" class="form-control" name="username" id="username" placeholder="Username">
            </div>
            <div class="form-group">
                <label for="password1">输入密码</label>
                <input type="password" class="form-control" name="password1" id="password1" placeholder="Password">
            </div>
            <div class="form-group">
                <label for="password2">确认密码</label>
                <input type="password" class="form-control" name="password2" id="password2" placeholder="PasswordAgain">
            </div>
            <div class="form-group">
                <label for="email">邮箱</label>
                <input type="email" class="form-control" name="email" id="email" placeholder="Email">
            </div>
            <button type="submit" class="btn btn-success btn-block">注册</button>
        </form>
    </div>
    </div>
    """


def render(navbar, body="", script=base_html.script, head=base_html.head):
    return head.format(nav_bar=navbar, body=body, script=script, style=base_html.style)


def render_navbar(username=None):
    if username:
        nav_bar_right = base_html.navbar_login.format(username=username)
        return base_html.navbar.format(nav_bar_right=nav_bar_right)
    else:
        return base_html.navbar.format(nav_bar_right="")
