import threading

import cv2
import face_recognition
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel

from otherinterface.DoorControl import DoorControl
from dbmanipulate.DBFaceDataMa import DBFaceDataMa
from log.log4p.GenerateLog import generate

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化摄像头
        self.capture = cv2.VideoCapture(0)

        # 初始化窗口
        self.setWindowTitle("人脸识别")
        self.setGeometry(100, 100, 800, 600)

        # 创建 QLabel 来显示视频
        self.image_label = QLabel(self)
        self.setCentralWidget(self.image_label)

        # 定时器，每隔一定时间更新视频帧
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # 每 20 毫秒获取一帧

        # 检查并创建数据库表
        self.db_obj = DBFaceDataMa()
        # 加载数据库中的人脸特征
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_face_data()

        # 创建门控对象
        self.door_control = DoorControl()

        # 启动人脸识别线程
        self.face_recognition_thread = threading.Thread(target=self.run_face_recognition)
        self.face_recognition_thread.daemon = True
        self.face_recognition_thread.start()


    def load_face_data(self):
        """从数据库中获取人脸数据，只需要在启动的时候读取一次就够了"""
        rows = self.db_obj.get_face_data()

        for row in rows:
            name = row[0]
            encoding = np.frombuffer(row[1], dtype=np.float64)
            self.known_face_names.append(name)
            self.known_face_encodings.append(encoding)

    def run_face_recognition(self):
        """单独线程处理人脸识别，需要一直运行"""
        while True:
            self.update_frame()

    def update_frame(self):
        """获取视频流的一帧并进行人脸识别，被人脸识别任务调用"""
        ret, frame = self.capture.read()

        if ret:
            # 转换为 RGB 格式
            rgb_frame = frame[:, :, ::-1]

            # 查找所有人脸
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # 绘制人脸框并进行人脸比对
            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, encoding)
                name = "未知"

                # 如果找到匹配的脸，打印 "开门"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                    # 同时做记录，xxx开门,我考虑使用单独的一个线程
                    # TODO：路径
                    log_thread = threading.Thread(
                        target=lambda: generate("../log/logs/open_door_mark.txt", "-"+name[0] + "---open the door")
                    )
                    log_thread.start()

                    self.door_control.open_door()  # 调用门控函数打开门
                # 在人脸周围画矩形框并显示名字
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # 将 OpenCV 图像转换为 PyQt 图像
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)

            # 显示图像
            self.image_label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        """关闭窗口时释放摄像头"""
        self.capture.release()
        event.accept()
