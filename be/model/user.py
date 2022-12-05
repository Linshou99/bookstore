import jwt
import time
import logging
from be.model import error
from be.model import db_conn
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from be.model import store
import re
from sqlalchemy import or_, and_

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 身份将被记录 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.conn.add(store.Users(user_id=user_id, password=password, balance=0, token=token, terminal=terminal))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        cursor = self.conn.query(store.Users.token).filter(store.Users.user_id == user_id)
        row = cursor.first()
        if row is None:
            return error.error_authorization_fail()
        db_token = row[0]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        cursor = self.conn.query(store.Users.password).filter(store.Users.user_id == user_id)
        row = cursor.first()
        if row is None:
            return error.error_authorization_fail()
        if password != row[0]:
            return error.error_authorization_fail()
        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            cursor = self.conn.query(store.Users).filter(store.Users.user_id == user_id).update({'token':token,'terminal':terminal})   
            if cursor == None:
                return error.error_authorization_fail() + ("", )
            self.conn.commit()# 提交即保存到数据库
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str):
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)
            cursor = self.conn.query(store.Users).filter(store.Users.user_id == user_id).update({'token':dummy_token,'terminal':terminal})
            if cursor == None:
                return error.error_authorization_fail()
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> (int, str):
        user = self.conn.query(store.Users).filter(store.Users.user_id == user_id).first()
        if user == None:
            code, message = error.error_authorization_fail()
            return code, message
        if password != user.password:
            code, message = error.error_authorization_fail()
            return code, message
        self.conn.query(store.Users).filter(store.Users.user_id == user_id).delete()
        self.conn.commit()
        return 200, "ok"


    def change_password(self, user_id: str, old_password: str, new_password: str):
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            cursor = self.conn.query(store.Users).filter(store.Users.user_id == user_id).update({'password':new_password,'token':token,'terminal':terminal})
            if cursor == None:
                return error.error_authorization_fail()
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        return 200, "ok"

    #字符串input中的关键词按空格隔开，模糊查询
    def search_all(self, input_str: str, page: int):
        conn = self.conn
        #一页有5个返回结果
        num_of_books_page = 5
        input_list = set(re.sub('[^\w\u4e00-\u9fff]+', ' ', input_str.lower()).split(' '))
        #在书名、作者名、书简介和出版社上做关键词匹配
        rule = or_( *[store.Book.title.like("%"+input+"%") for input in input_list],
                    *[store.Book.author.like("%"+input+"%") for input in input_list],
                    *[store.Book.tags.like("%"+input+"%") for input in input_list],
                    *[store.Book.book_intro.like("%"+input+"%") for input in input_list],
                    *[store.Book.publisher.like("%"+input+"%") for input in input_list])
        cursor = conn.query(store.Book.book_id,store.Book.title,store.Book.author,store.Book.publisher,store.Book.book_intro)\
                     .filter(rule)\
                     .limit(num_of_books_page)\
                     .offset(page*num_of_books_page)\
                     .all()
        if len(cursor) != 0:
            res=[]
            for i in cursor:
                res.append({'book_id':i[0],'title':i[1],'author':i[2],'publisher':i[3],'book_intro':i[4]})
            self.conn.commit()
            return 200, "ok",res
        else:
            self.conn.commit()
            return 200, "ok"," "



    def search_in_store(self, store_id: str, input_str: str, page: int):
        conn = self.conn
        input_list = set(re.sub('[^\w\u4e00-\u9fff]+', ' ', input_str.lower()).split(' '))
        #在书名、作者名、书简介和出版社上做关键词匹配
        rule = or_( *[store.Book.title.like("%"+input+"%") for input in input_list],
                    *[store.Book.author.like("%"+input+"%") for input in input_list],
                    *[store.Book.tags.like("%"+input+"%") for input in input_list],
                    *[store.Book.book_intro.like("%"+input+"%") for input in input_list],
                    *[store.Book.publisher.like("%"+input+"%") for input in input_list])
        cursor_store = conn.query(store.Store.book_id)\
                           .filter(store.Store.store_id == store_id)\
                           .all()
        res=[]
        if len(cursor_store) != 0:
            cursor = conn.query(store.Book.book_id,store.Book.title,store.Book.author,store.Book.publisher,store.Book.book_intro)\
                        .filter(and_(store.Book.book_id.in_(cursor_store), rule))\
                        .limit(10)\
                        .offset(page*10)\
                        .all()
            if len(cursor) != 0:
                for i in cursor:
                    res.append({'book_id':i[0],'title':i[1],'author':i[2],'publisher':i[3],'book_intro':i[4]})
        self.conn.commit()           
        if len(res) != 0:
            return 200, "ok",res
        else:
            return 200, "ok"," "


            
        

