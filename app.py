import sys
import sqlite3
import face_recognition
import numpy as np
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from werkzeug.utils import redirect

from broadcast.voice import hello_announce
from dbmanipulate.DBAdminDataMa import DBAdminDataMa
from flask import Flask, request, render_template, session, url_for
import threading
from dbmanipulate.DBFaceDataMa import DBFaceDataMa
from facerec.FaceRecognitionApp import FaceRecognitionApp
from flaskapp.adminflask import FlaskApp

if __name__ == "__main__":
    # 启动Flask Web服务
    flask_app = FlaskApp()
    flask_thread = threading.Thread(target=flask_app.run)
    flask_thread.daemon = True  # 设置为守护线程，前台人脸识别程序退出时Flask线程会随之退出
    flask_thread.start()

    # 启动 PyQt5 人脸识别应用
    app2 = QApplication(sys.argv)
    window = FaceRecognitionApp()
    hello_announce()
    window.show()
    sys.exit(app2.exec_())