import sqlite3 as sqlite
import uuid
import json
import logging
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
from be.model import store
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from datetime import datetime,timedelta
from threading import Timer
from apscheduler.schedulers.background import BackgroundScheduler



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
            total_price = 0
            
            for book_id, count in id_and_count:
                cursor = None
                c = self.conn.query(store.Store.book_id).filter(store.Store.store_id == store_id,).all()
                print("store_book_id:",c)
                # 找店里有没有这本书以及这本书的id、库存、简介
                cursor = self.conn.query(store.Store.book_id, store.Store.stock_level, store.Store.book_info)\
                                  .filter(and_(store.Store.store_id == store_id, store.Store.book_id==int(book_id) ))  
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
                total_price += price*count
                # self.conn.execute(
                #         "INSERT INTO new_order_detail(order_id, book_id, count, price) "
                #         "VALUES(?, ?, ?, ?);",
                #         (uid, book_id, count, price))
            # 插入新总order
            time_ = datetime.utcnow()#暂存
            self.conn.add(store.New_order(order_id = uid, user_id = user_id, store_id = store_id, price = total_price, time_ = time_))
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
            cursor = conn.query(store.New_order.order_id, store.New_order.user_id, store.New_order.store_id, store.New_order.price)\
                         .filter(store.New_order.order_id == order_id)
            row = cursor.first()
            # cursor = conn.execute("SELECT order_id, user_id, store_id FROM new_order WHERE order_id = ?", (order_id,))
            # row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            total_price = row[3]

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
            #在new_order时已计算总价，无需再计算，暂时注释掉
            """
            cursor = conn.query(store.New_order_detail.book_id, store.New_order_detail.count,store.New_order_detail.price)\
                         .filter(store.New_order_detail.order_id == order_id)
            # cursor = conn.execute("SELECT book_id, count, price FROM new_order_detail WHERE order_id = ?;", (order_id,))
            total_price = 0
            for row in cursor:
                count = row[1]
                price = row[2]
                total_price = total_price + price * count
            """
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
            #付款后将该订单移至new_order_paid，status初设为0，表示未发货
            cursor = conn.query(store.New_order).filter(store.New_order.order_id == order_id).delete()
            # cursor = conn.execute("DELETE FROM new_order WHERE order_id = ?", (order_id, ))
            if cursor == None:
                return error.error_invalid_order_id(order_id)
            self.conn.add(store.New_order_paid(order_id = order_id, user_id = user_id, store_id = store_id, price = total_price, status = 0))

            #为查看历史订单，不删除new_order_detail
            """
            cursor = conn.query(store.New_order_detail).filter(store.New_order_detail.order_id == order_id).delete()
            # cursor = conn.execute("DELETE FROM new_order_detail where order_id = ?", (order_id, ))
            if cursor == None:
                return error.error_invalid_order_id(order_id)
            """

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

    
    def receive_books(self, user_id: str, order_id: str) -> (int, str):
        conn = self.conn
        cursor = conn.query(store.New_order_paid.user_id,store.New_order_paid.status)\
                     .filter(store.New_order_paid.order_id == order_id)
        if cursor == None:
            return error.error_invalid_order_id(order_id)   
        row = cursor.first()
        if row[0] != user_id:
            return error.error_authorization_fail()
        if row[1] == 0:
            return error.error_books_not_sent()      
        if row[1] == 2:
            return error.error_books_duplicate_receive() 
        cursor = self.conn.query(store.New_order_paid)\
                                  .filter(store.New_order_paid.order_id == order_id)\
                                  .update({'status':2}) 
        self.conn.commit()
        return 200, "ok"

    #分为取消未付款订单和已付款订单,移入New_order_cancel表，已付款订单需要退款
    def cancel_order(self, user_id: str, order_id: str) -> (int, str):
        conn = self.conn
        cursor = conn.query(store.New_order.order_id,store.New_order.user_id,store.New_order.store_id,store.New_order.price)\
                     .filter(store.New_order.order_id == order_id).all()
        #取消未付款订单
        if len(cursor) != 0:
            row = cursor[0]
            if row[1] != user_id:
                return error.error_authorization_fail()
            order_id = row[0]
            user_id = row[1]
            store_id = row[2]
            price = row[3]
            cursor_del = conn.query(store.New_order)\
                             .filter(store.New_order.order_id == order_id)\
                             .delete()
            if cursor_del == None:
                return error.error_invalid_order_id(order_id)
        else:
            cursor = conn.query(store.New_order_paid.order_id,store.New_order_paid.user_id,store.New_order_paid.store_id,store.New_order_paid.price)\
                         .filter(store.New_order_paid.order_id == order_id).all()
            #取消已付款订单
            if len(cursor) != 0:
                row = cursor[0]
                if row[1] != user_id:
                    return error.error_authorization_fail()
                order_id = row[0]
                user_id = row[1]
                store_id = row[2]
                price = row[3]
                cursor_seller = conn.query(store.User_store.user_id)\
                             .filter(store.User_store.store_id == store_id)
                if cursor_seller == None:
                    return error.error_non_exist_store_id(store_id)
                row_seller = cursor_seller.first()
                seller_id = row_seller[0]
                #暂不考虑退款后卖家账户为负
                """
                cursor = conn.query(store.Users)\
                         .filter(and_(store.Users.user_id == seller_id, store.Users.balance >= price))\
                         .update({'balance': store.Users.balance - price})
                if cursor == None:
                    return error.error_seller_not_sufficient_funds(order_id)
                """
                cursor = conn.query(store.Users)\
                         .filter(store.Users.user_id == seller_id)\
                         .update({'balance': store.Users.balance - price})
                if cursor == None:
                    return error.error_non_exist_user_id(seller_id)

                cursor = conn.query(store.Users)\
                             .filter(store.Users.user_id == user_id)\
                             .update({'balance': store.Users.balance + price})
                if cursor == None:
                    return error.error_non_exist_user_id(user_id)
                
                cursor_del = conn.query(store.New_order_paid)\
                                 .filter(store.New_order_paid.order_id == order_id)\
                                 .delete()
                if cursor_del == None:
                    return error.error_invalid_order_id(order_id)

            #既不是未付款订单也不是已付款订单
            else:
                return error.error_invalid_order_id(order_id)  
              
        conn.add(store.New_order_cancel(order_id = order_id, user_id = user_id, store_id = store_id, price = price))

        self.conn.commit()
        return 200, "ok"

    def auto_cancel_order(self) -> (int, str):
        #print('time3333333auto: ', datetime.utcnow())
        wait_time = 20#10s后自动取消订单
        conn = self.conn
        now = datetime.utcnow()
        cursor_all = conn.query(store.New_order.order_id)\
                     .all()
        if(len(cursor_all)) != 0:
            cursor = conn.query(store.New_order.order_id,store.New_order.user_id,store.New_order.store_id,store.New_order.price,store.New_order.time_)\
                            .filter(store.New_order.time_ <= now-timedelta(seconds=wait_time)).all()
            #未查到订单说明已付款或已被买家自行取消，无需做出动作
            if len(cursor) != 0:
                for row in cursor:
                    cursor_del = conn.query(store.New_order)\
                        .filter(store.New_order.order_id == row[0])\
                        .delete()
                    if cursor_del == None:
                        self.conn.commit()
                        return error.error_invalid_order_id(row[0])
                    conn.add(store.New_order_cancel(order_id = row[0], user_id = row[1], store_id = row[2], price = row[3]))
        self.conn.commit()
        return 200, "ok"


    #为测试auto_cancel_order作的函数
    def is_order_cancelled(self, order_id: str) -> (int, str):
        conn = self.conn
        cursor = conn.query(store.New_order_cancel.order_id)\
                        .filter(store.New_order_cancel.order_id == order_id) 
        row = cursor.first()
        if row == None:
            self.conn.commit()
            return error.error_auto_cancel_fail(order_id)#超时前已付款
        else:
            self.conn.commit()
            return 200, "ok"

    def check_hist_order(self, user_id: str):
        conn = self.conn
        if not self.user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        res = []
        #查询未付款订单
        cursor = conn.query(store.New_order.order_id,store.New_order.user_id,store.New_order.store_id,store.New_order.price)\
                    .filter(store.New_order.user_id == user_id)\
                    .all()
        if len(cursor) != 0:
            for row in cursor:
                details = []
                order_id = row[0]
                cursor_detail = conn.query(store.New_order_detail.book_id,store.New_order_detail.count,store.New_order_detail.price)\
                                    .filter(and_(store.New_order_detail.order_id == order_id))\
                                    .all()
                if len(cursor_detail) != 0:
                    for i in cursor_detail:
                        details.append({'book_id':i[0],'count':i[1],'price':i[2]})
                else:
                    return error.error_invalid_order_id(order_id)
                res.append({'status':"not paid",'order_id':row[0],'buyer_id':row[1],'store_id':row[2],'total_price':row[3],'details':details})
        #查询已付款订单
        books_status=["not send","already send","already receive"]
        cursor = conn.query(store.New_order_paid.order_id,store.New_order_paid.user_id,store.New_order_paid.store_id,store.New_order_paid.price,store.New_order_paid.status)\
                    .filter(store.New_order_paid.user_id == user_id)\
                    .all()
        if len(cursor) != 0:
            for row in cursor:
                details = []
                order_id = row[0]
                cursor_detail = conn.query(store.New_order_detail.book_id,store.New_order_detail.count,store.New_order_detail.price)\
                                    .filter(and_(store.New_order_detail.order_id == order_id))\
                                    .all()
                if len(cursor_detail) != 0:
                    for i in cursor_detail:
                        details.append({'book_id':i[0],'count':i[1],'price':i[2]})
                else:
                    return error.error_invalid_order_id(order_id)
                res.append({'status':"already paid",'order_id':row[0],'buyer_id':row[1],'store_id':row[2],'total_price':row[3],'books_status':books_status[row[4]],'details':details})
        #查询已取消订单
        cursor = conn.query(store.New_order_cancel.order_id,store.New_order_cancel.user_id,store.New_order_cancel.store_id,store.New_order_cancel.price)\
                    .filter(store.New_order_cancel.user_id == user_id)\
                    .all()
        if len(cursor) != 0:
            for row in cursor:
                details = []
                order_id = row[0]
                cursor_detail = conn.query(store.New_order_detail.book_id,store.New_order_detail.count,store.New_order_detail.price)\
                                    .filter(and_(store.New_order_detail.order_id == order_id))\
                                    .all()
                if len(cursor_detail) != 0:
                    for i in cursor_detail:
                        details.append({'book_id':i[0],'count':i[1],'price':i[2]})
                else:
                    return error.error_invalid_order_id(order_id)
                res.append({'status':"cancelled",'order_id':row[0],'buyer_id':row[1],'store_id':row[2],'total_price':row[3],'details':details})
        
        self.conn.commit()
        if len(res)==0:
            return 200, "ok", " "
        else:
            return 200, "ok", res




sched = BackgroundScheduler()
sched.add_job(Buyer().auto_cancel_order, 'interval', id='5_second_job', seconds=5)
sched.start()
            
                            
            
    
    
    







        

        
