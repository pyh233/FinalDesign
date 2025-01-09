import numpy as np
import sqlite3
import face_recognition

# 创建一个模拟的人脸特征编码（128 维的浮点数）
# image经过face库的处理得到一个ndarray数组表示图片
image = face_recognition.load_image_file("/flaskapp/static/img/R-C.jpg")
encoding = face_recognition.face_encodings(image)[0]  # 获取第一个人脸的特征编码

# 打印特征的长度
print("Encoding length (in bytes):", encoding.nbytes)

# 将 encoding 转换为二进制（BLOB）格式
encoding_blob = encoding.tobytes()

# 打印二进制数据的长度，确保是 np.float64 大小的倍数
print(f"Blob length (in bytes): {len(encoding_blob)}")

# 数据库连接
conn = sqlite3.connect('/home/pyh233/PycharmProjects/PythonProject/face_recognition.db')
cursor = conn.cursor()

# 插入数据
cursor.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", ('Test User', encoding_blob))
conn.commit()

# 查询插入的数据
cursor.execute("SELECT name, encoding FROM faces")
print(cursor.fetchall())  # 打印长度，确认数据格式

conn.close()
