import threading

from flask import render_template, request, session, redirect, url_for, Flask

from dbmanipulate.DBAdminDataMa import DBAdminDataMa
from dbmanipulate.DBFaceDataMa import DBFaceDataMa
from log.log4p.GenerateLog import generate


class FlaskApp:
    def __init__(self):
        # Flask服务设置
        self.app = Flask(__name__)
        self.app.secret_key = '123456'
        self._setup_routes()

    def _setup_routes(self):
        # Flask路由设置
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/skipToLogin', 'skipToLogin', self.skipToLogin,methods=['GET'])
        self.app.add_url_rule('/mainPage', 'mainPage', self.mainPage,methods=['GET'])
        self.app.add_url_rule('/loginPage', 'loginPage', self.loginPage,methods=['GET'])
        self.app.add_url_rule('/admin/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/admin/logout', 'logout', self.logout, methods=['POST'])
        self.app.add_url_rule('/test', 'admin_main', self.admin_main, methods=['GET', 'POST'])
        self.app.add_url_rule('/skipToAddFace', 'skipToAddFace', self.skipToAddFace, methods=['GET'])
        self.app.add_url_rule('/addFacePage', 'addFacePage', self.addFacePage, methods=['GET'])
        self.app.add_url_rule('/addFace', 'addFace', self.addFace, methods=['POST'])

        self.app.add_url_rule('/delFace', 'delFace', self.deleteFace, methods=['POST'])

    # 欢迎界面
    def index(self):
        return render_template("welcome.html")
    # 登陆跳转(各功能实现后跳转到此，唯一入口)
    def skipToLogin(self):
        # 获取msg的信息，如果是第一次登陆msg为None,此时为msg赋值为"".
        # 不是第一次登陆就会显示登陆失败。
        # TODO：？
        msg = session.get("msg", "")
        # 只有通过身份验证才能转到展示页面，否则跳回登陆页面，记录msg
        # 身份验证通过才会查询信息，否则不查询
        if session.get("identity"):
            # # 获取所有人脸信息 如果人脸信息为None就给予未录入信息。
            # face_msg_obj = DBFaceDataMa()
            # face_msg = face_msg_obj.get_face_data()
            # face_msg_obj.close()
            # # 需要对人脸数据进行部分展示，因为全部人脸数据太长了，页面无法展示
            # face_msg = [(name, data[:20]) for name, data in face_msg]
            face_msg = self.load_face_data()
            if len(face_msg) == 0:
                face_msg = "尚未录入人脸信息"
            session['face_msg'] = face_msg
            # return render_template("main.html",face_msg=face_msg)
            return redirect(url_for("mainPage"))
        else:
            return redirect(url_for("loginPage",msg=msg))
    # 跳转登陆页面，请求参数为登陆成功或失败信提示
    def loginPage(self):
        msg = request.args.get("msg")
        return render_template("login.html",msg=msg)
    # 跳转主界面
    def mainPage(self):
        face_msg = session.get("face_msg","")
        msg = session.get("msg","发生了一个未知错误")
        return render_template("main.html", face_msg=face_msg, msg=msg)
    # 登陆功能
    def login(self):
        # 获取输入的用户名和密码
        aname = request.form.get("admin_name")
        apasswd = request.form.get("admin_passwd")
        # 开始进行身份验证 身份验证数据库对象不需要持续开启
        admin_obj = DBAdminDataMa()
        if admin_obj.login(aname, apasswd):
            session['identity'] = aname
            session['msg'] = '登陆成功, 欢迎进入人脸管理界面'
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
        return redirect(url_for("addFacePage"))
    def addFacePage(self):
        return render_template("addFaceMsg.html")
    # 增加人脸信息请求
    def addFace(self):
        if session['identity']=="pyh":
            name = request.form.get("add_name")
            face_data = request.form.get("add_face_data")
            face_msg_obj = DBFaceDataMa()
            res = face_msg_obj.insert_face_data(name, face_data)
            face_msg_obj.close()
            # TODO：Res判断
            if True:
                session['msg'] = "成功添加一条人脸数据"
            else:
                session['msg'] = "添加失败"
        return redirect(url_for("skipToLogin"))
    # 删除人脸信息请求
    def deleteFace(self):
        if session['identity'] == "pyh":
            name = request.form.get("del_name")
            face_data = request.form.get("del_face_data")
            face_msg_obj = DBFaceDataMa()
            res = face_msg_obj.delete_face_data(name, face_data)
            face_msg_obj.close()
            # TODO：res判断
            # 检查如果删除数据日志记录，方便恢复数据
            if True:
                # 同时做记录，删除的数据获得,考虑使用单独的一个线程
                log_thread = threading.Thread(
                    # TODO:路径
                    target=lambda: generate("../log/logs/deletedFaceDate.txt", name + "---" + face_data)
                )
                log_thread.start()
                session['msg'] = "成功删除一条人脸数据"
            else:
                session['msg'] = "删除失败"
        return redirect(url_for("skipToLogin"))
    # 跳转大语言模型可视化交流界面

    # 向大语言模型发送问题内容并得到回答

    # 跳转关于我的界面

    # 测试勿动
    def admin_main(self):
        return "its only a test by pyh233"

    def run(self):
        self.app.run(host='0.0.0.0', port=5000, threaded=True)

    def load_face_data(self):
        # 获取所有人脸信息 如果人脸信息为None就给予未录入信息。
        face_msg_obj = DBFaceDataMa()
        face_msg = face_msg_obj.get_face_data()
        face_msg_obj.close()
        # 需要对人脸数据进行部分展示，因为全部人脸数据太长了，页面无法展示
        face_msg = [(name, data[:20]) for name, data in face_msg]
        return face_msg
