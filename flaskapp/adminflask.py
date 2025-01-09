from flask import render_template, request, session, redirect, url_for, Flask

from dbmanipulate.DBAdminDataMa import DBAdminDataMa
from dbmanipulate.DBFaceDataMa import DBFaceDataMa


class FlaskApp:
    def __init__(self):
        # Flask服务设置
        self.app = Flask(__name__)
        self.app.secret_key = '123456'
        self._setup_routes()

    def _setup_routes(self):
        # Flask路由设置
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/skipToLogin', 'skipToLogin', self.skipToLogin)
        self.app.add_url_rule('/admin/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/admin/logout', 'logout', self.logout, methods=['POST'])
        self.app.add_url_rule('/test', 'admin_main', self.admin_main, methods=['GET', 'POST'])
        self.app.add_url_rule('/skipToAddFace', 'skipToAddFace', self.skipToAddFace, methods=['POST'])

    # 欢迎界面
    def index(self):
        return render_template("welcome.html")
    # 登陆跳转
    def skipToLogin(self):
        # 获取msg的信息，如果是第一次登陆msg为None,此时为msg赋值为"".
        # 不是第一次登陆就会显示登陆失败。
        #
        msg = session.get('msg', "")
        # 获取所有人脸信息 如果人脸信息为None就给予未录入信息。
        face_msg_obj = DBFaceDataMa()
        face_msg = face_msg_obj.get_face_data()
        face_msg_obj.close()
        if len(face_msg) == 0:
            face_msg = "尚未录入人脸信息"
        else:
            # 需要对人脸数据进行部分展示，因为全部人脸数据太长了
            face_drop_part = []
        # 只有通过身份验证才能转到展示页面，否则跳回登陆
        if session.get("identity"):
            return render_template("main.html", face_msg=face_msg)
        else:
            return render_template("login.html", msg=msg)
    # 登陆功能
    def login(self):
        # 获取输入的用户名和密码
        aname = request.form.get("admin_name")
        apasswd = request.form.get("admin_passwd")
        # 开始进行身份验证
        admin_obj = DBAdminDataMa()
        if admin_obj.login(aname, apasswd):
            session['identity'] = aname
            session['msg'] = '登陆成功'
        else:
            session['msg'] = "身份验证失败!"
        admin_obj.close()
        return redirect(url_for("skipToLogin"))
    # 退出登录
    def logout(self):
        session.pop('identity', None)
        session.pop('msg', None)
        return redirect(url_for("skipToLogin"))

    # 跳转增加人脸信息界面
    def skipToAddFace(self):
        return 'addFace'

    # 增加人脸信息请求

    # 跳转修改人脸信息界面

    # 修改人脸信息请求

    # 删除人脸信息请求

    # 跳转大语言模型可视化交流界面

    # 向大语言模型发送问题内容并得到回答

    # 跳转关于我的界面

    def admin_main(self):
        return "its only a test by pyh233"

    def run(self):
        self.app.run(host='0.0.0.0', port=5000, threaded=True)
