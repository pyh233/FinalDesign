from PyQt5.QtCore import QTimer

from broadcast.voice import close_announce, open_announce


# 门控类
class DoorControl:
    def __init__(self):
        self.door_open = False

    def open_door(self):
        if not self.door_open:
            open_announce()
            print("开门")
            self.door_open = True
            # 3 秒后自动关门
            QTimer.singleShot(3000, self.close_door)

    def close_door(self):
        if self.door_open:
            close_announce()
            print("关门")
            self.door_open = False
