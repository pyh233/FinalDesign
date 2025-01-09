import datetime
import time
from xmlrpc.client import DateTime

# 日志选择使用文本文件存储，不使用数据库。
def generate(log_name, log_content):
    with open(log_name,"a+",encoding='utf-8') as fp:
        fp.write(str(datetime.datetime.now())+" ")
        fp.write(log_content + "\n")