import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
from be.model import store
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Seller(db_conn.DBConn):

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)
            self.conn.add(store.Store(store_id = store_id, book_id = book_id, book_info = book_json_str, stock_level = stock_level))
            # self.conn.execute("INSERT into store(store_id, book_id, book_info, stock_level)"
            #                   "VALUES (?, ?, ?, ?)", (store_id, book_id, book_json_str, stock_level))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        except sqlalchemy.exc.IntegrityError as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)
            cursor = self.conn.query(store.Store).filter(store.Store.store_id == store_id).update({'stock_level':store.Store.stock_level + add_stock_level})   
            if cursor == None:
                return error.error_authorization_fail() + ("", )
            # self.conn.execute("UPDATE store SET stock_level = stock_level + ? "
            #                   "WHERE store_id = ? AND book_id = ?", (add_stock_level, store_id, book_id))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except sqlalchemy.exc.IntegrityError as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            self.conn.add(store.User_store(user_id = user_id, store_id = store_id))
            # self.conn.execute("INSERT into user_store(store_id, user_id)"
            #                   "VALUES (?, ?)", (store_id, user_id))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except sqlalchemy.exc.IntegrityError as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def send_books(self, user_id: str, order_id: str) -> (int, str):
        conn = self.conn
        cursor = conn.query(store.New_order_paid)\
                     .filter(store.New_order_paid.order_id == order_id)
        if cursor == None:
            return error.error_invalid_order_id(order_id)   
        row = cursor.first()
        store_id = row[2]
        cursor_store = conn.query(store.User_store.user_id)\
                     .filter(store.User_store.store_id == store_id)
        row_store = cursor_store.first()
        if row_store[0] != user_id:
            return error.error_authorization_fail()
        if row[4] == 1 or row[4] == 2:
            return error.error_books_duplicate_sent()      
        cursor = self.conn.query(store.New_order_paid)\
                                  .filter(store.New_order_paid.order_id == order_id)\
                                  .update({'status':1}) 
        self.conn.commit()
        return 200, "ok"
