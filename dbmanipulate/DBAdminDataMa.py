import sqlite3
from oauthlib.uri_validate import query

class DBAdminDataMa:
    def __init__(self):
        # self.conn = sqlite3.connect('../face_recognition.db')
        self.conn = sqlite3.connect('/home/pyh233/PycharmProjects/PythonProject/face_recognition.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS admin (name TEXT, password TEXT)")
        self.conn.commit()
    def login(self,name,passwd):
        query="select * from admin where name=? and password=?"
        self.cursor.execute(query, (name, passwd))
        data = self.cursor.fetchall()
        return data
    def close(self):
        self.conn.close()
    # def test(self):
        # name = 'pyh'
        # pw = 'b889546949b8db301fc659fa69989be7'
        # query="select * from admin where name=? and password=?"
        # self.cursor.execute(query,(name,pw))
        # date = self.cursor.fetchall()
        # return date
        # self.cursor.execute("insert into admin values('pyh233','49b8db301fc659fa')")
        # self.conn.commit()
# if __name__ == '__main__':
#     d = DBAdminDataMa()
#     # res = d.test()
#     res = d.login('pyh','b889546949b8db301fc659fa69989be7')
#     print(res)

