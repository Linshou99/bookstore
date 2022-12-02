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

    def logout(self, user_id: str, token: str) -> bool:
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


    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
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

