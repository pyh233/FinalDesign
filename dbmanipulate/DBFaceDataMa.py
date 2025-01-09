"""数据库操作模块"""
import sqlite3

class DBFaceDataMa:
    def __init__(self):
        # self.conn = sqlite3.connect('../face_recognition.db')
        self.conn = sqlite3.connect('/home/pyh233/PycharmProjects/PythonProject/face_recognition.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS faces (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        encoding BLOB NOT NULL
                    )
                ''')

        self.conn.commit()
    def get_face_data(self):
        sql = "SELECT name, encoding FROM faces"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
    def insert_face_data(self):
        pass
    def update_face_data(self):
        pass
    def delete_face_data(self):
        pass
    def close(self):
        # 不需要关闭cursor,因为conn会自动关闭cursor
        # self.cursor.close()
        self.conn.close()
if __name__ == '__main__':
    d = DBFaceDataMa()
    print(d.get_face_data())
    d.close()