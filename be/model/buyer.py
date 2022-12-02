import sqlite3 as sqlite
import uuid
import json
import logging
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
from be.model import store
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_

class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""
        try:
            # 判断 user_id 是否存在
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id, )
            # 判断 store_id 是否存在
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id, )
            # 写一个uid
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            
            for book_id, count in id_and_count:
                cursor = None
                # 找店里有没有这本书以及这本书的id、库存、简介
                cursor = self.conn.query(store.Store.book_id, store.Store.stock_level, store.Store.book_info).filter(and_(store.Store.store_id == store_id, store.Store.book_id == book_id))  
                # cursor = self.conn.execute(
                #     "SELECT book_id, stock_level, book_info FROM store "
                #     "WHERE store_id = ? AND book_id = ?;",
                #     (store_id, book_id))
                # row = cursor.fetchone()
                row = cursor.first()
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id, )

                stock_level = row[1]
                book_info = row[2]
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")
                # 库存不够
                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)
                # 库存够，更新店里书本数目
                cursor = self.conn.query(store.Store)\
                                  .filter(and_(store.Store.store_id == store_id, store.Store.book_id == book_id, store.Store.stock_level >= count))\
                                  .update({'stock_level':store.Store.stock_level - count})
                # cursor = self.conn.execute(
                #     "UPDATE store set stock_level = stock_level - ? "
                #     "WHERE store_id = ? and book_id = ? and stock_level >= ?; ",
                #     (count, store_id, book_id, count))
                if cursor == None:
                    return error.error_stock_level_low(book_id) + (order_id, )

                # 插入新order
                self.conn.add(store.New_order_detail(order_id = uid, book_id = book_id, count = count, price = price))
                # self.conn.execute(
                #         "INSERT INTO new_order_detail(order_id, book_id, count, price) "
                #         "VALUES(?, ?, ?, ?);",
                #         (uid, book_id, count, price))
            # 插入新总order
            self.conn.add(store.New_order(order_id = uid, user_id = user_id, store_id = store_id))
            # self.conn.execute(
            #     "INSERT INTO new_order(order_id, store_id, user_id) "
            #     "VALUES(?, ?, ?);",
            #     (uid, store_id, user_id))
            self.conn.commit()
            order_id = uid
        except sqlalchemy.exc.IntegrityError as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except sqlalchemy.exc.IntegrityError as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        conn = self.conn
        try:
            cursor = conn.query(store.New_order.order_id, store.New_order.user_id, store.New_order.store_id)\
                         .filter(store.New_order.order_id == order_id)
            row = cursor.first()
            # cursor = conn.execute("SELECT order_id, user_id, store_id FROM new_order WHERE order_id = ?", (order_id,))
            # row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]

            if buyer_id != user_id:
                return error.error_authorization_fail()

            cursor = conn.query(store.Users.balance, store.Users.password)\
                         .filter(store.Users.user_id == buyer_id)
            row = cursor.first()
            # cursor = conn.execute("SELECT balance, password FROM user WHERE user_id = ?;", (buyer_id,))
            # row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_user_id(buyer_id)
            balance = row[0]
            if password != row[1]:
                return error.error_authorization_fail()

            cursor = conn.query(store.User_store.store_id, store.User_store.user_id)\
                         .filter(store.User_store.store_id == store_id)
            row = cursor.first()
            # cursor = conn.execute("SELECT store_id, user_id FROM user_store WHERE store_id = ?;", (store_id,))
            # row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = row[1]

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            cursor = conn.query(store.New_order_detail.book_id, store.New_order_detail.count,store.New_order_detail.price)\
                         .filter(store.New_order_detail.order_id == order_id)
            # cursor = conn.execute("SELECT book_id, count, price FROM new_order_detail WHERE order_id = ?;", (order_id,))
            total_price = 0
            for row in cursor:
                count = row[1]
                price = row[2]
                total_price = total_price + price * count

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)
                
            cursor = conn.query(store.Users)\
                         .filter(and_(store.Users.user_id == buyer_id, store.Users.balance >= total_price))\
                         .update({'balance': store.Users.balance - total_price})
            # cursor = conn.execute("UPDATE user set balance = balance - ?"
            #                       "WHERE user_id = ? AND balance >= ?",
            #                       (total_price, buyer_id, total_price))
            if cursor == None:
                return error.error_not_sufficient_funds(order_id)

            cursor = conn.query(store.Users)\
                         .filter(store.Users.user_id == seller_id)\
                         .update({'balance': store.Users.balance + total_price})
            # cursor = conn.execute("UPDATE user set balance = balance + ?"
            #                       "WHERE user_id = ?",
            #                       (total_price, buyer_id))
            if cursor == None:
                return error.error_non_exist_user_id(seller_id)

            cursor = conn.query(store.New_order).filter(store.New_order.order_id == order_id).delete()
            # cursor = conn.execute("DELETE FROM new_order WHERE order_id = ?", (order_id, ))
            if cursor == None:
                return error.error_invalid_order_id(order_id)

            cursor = conn.query(store.New_order_detail).filter(store.New_order_detail.order_id == order_id).delete()
            # cursor = conn.execute("DELETE FROM new_order_detail where order_id = ?", (order_id, ))
            if cursor == None:
                return error.error_invalid_order_id(order_id)

            conn.commit()

        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))

        except sqlalchemy.exc.IntegrityError as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        conn = self.conn
        try:
            cursor = conn.query(store.Users.password).filter(store.Users.user_id == user_id)
            # cursor = self.conn.execute("SELECT password  from user where user_id=?", (user_id,))
            row = cursor.first()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()

            cursor = conn.query(store.Users)\
                         .filter(store.Users.user_id == user_id)\
                         .update({'balance': store.Users.balance + add_value})
            if cursor == None:
                return error.error_non_exist_user_id(user_id)

            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except sqlalchemy.exc.IntegrityError as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
