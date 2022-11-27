from be.model import store
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DBConn:
    def __init__(self):
        engine = create_engine("postgresql://stu10205501429:Stu10205501429@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501429")
        Base = declarative_base()
        DbSession = sessionmaker(bind=engine)
        self.conn = DbSession() # 创建程序与数据库之间的对话

    def user_id_exist(self, user_id):
        cursor = self.conn.execute("SELECT user_id FROM user WHERE user_id = ?;", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cursor = self.conn.execute("SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;", (store_id, book_id))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cursor = self.conn.execute("SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
