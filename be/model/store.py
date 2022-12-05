import logging
import os
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

import sqlite3 as sqlite
import random
import base64
import simplejson as json


engine = create_engine("postgresql://stu10205501429:Stu10205501429@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501429")
Base = declarative_base()


class Users(Base):
    # 表的名字:
    __tablename__ = 'user'    
    # 表的结构:
    user_id = Column(Text, primary_key=True, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(Text)
    terminal = Column(Text)
            
class User_store(Base):
    # 表的名字:
    __tablename__ = 'user_store'
    
    # 表的结构:
    user_id = Column(Text, primary_key=True, nullable=False)
    store_id = Column(Text, primary_key=True, nullable=False)
              
class Store(Base):
    # 表的名字:
    __tablename__ = 'store'

    # 表的结构:
    store_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)  
    book_info = Column(Text)
    stock_level = Column(Integer)

#新建未付款订单          
class New_order(Base):
    # 表的名字:
    __tablename__ = 'new_order'
    
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)
    price = Column(Integer)#订单总价
    time_ = Column(DateTime, nullable=False)#下单时间

#已付款订单
class New_order_paid(Base):
    # 表的名字:
    __tablename__ = 'new_order_paid'
    
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)
    price = Column(Integer)
    status = Column(Integer)#0,1,2分别代表未发货，已发货和已收货

#用户取消或超时自动取消的订单
class New_order_cancel(Base):
    # 表的名字:
    __tablename__ = 'new_order_cancel'
    
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)
    price = Column(Integer)


class New_order_detail(Base):
    # 表的名字:
    __tablename__ = 'new_order_detail'

    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)  
    count = Column(Integer)
    price = Column(Integer)

#记录所有书的信息
class Book(Base):
    # 表的名字:
    __tablename__ = 'book'

    # 表的结构:
    book_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    price = Column(Integer)
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    picture = Column(LargeBinary)

#不是表，用于将data/book.db数据导入表book
class BookDB:
    def __init__(self, large: bool = False):
        parent_path = os.path.dirname(os.path.dirname(__file__))
        """
        self.db_s = os.path.join(parent_path, "data/book.db")
        self.db_l = os.path.join(parent_path, "data/book_lx.db")
        if large:
            self.book_db = self.db_l
        else:
            self.book_db = self.db_s
        """
        self.book_db = os.path.join(parent_path, "../fe/data/book.db")
        

    def get_book_count(self):
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT count(id) FROM book")
        row = cursor.fetchone()
        return row[0]

    def send_db_to_table(self, start, size):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT id, title, author, "
            "publisher, original_title, "
            "translator, pub_year, pages, "
            "price, currency_unit, binding, "
            "isbn, author_intro, book_intro, "
            "content, tags, picture FROM book ORDER BY id "
            "LIMIT ? OFFSET ?", (size, start))
        for row in cursor:
            book = Book()
            book.id = row[0]
            book.title = row[1]
            book.author = row[2]
            book.publisher = row[3]
            book.original_title = row[4]
            book.translator = row[5]
            book.pub_year = row[6]
            book.pages = row[7]
            book.price = row[8]

            book.currency_unit = row[9]
            book.binding = row[10]
            book.isbn = row[11]
            book.author_intro = row[12]
            book.book_intro = row[13]
            book.content = row[14]
            tags = row[15]

            picture = row[16]

            taglist = []
            for tag in tags.split("\n"):
                if tag.strip() != "":
                    # book.tags.append(tag)
                    taglist.append(tag)
            book.tags = " ".join(taglist)#将列表转换为字符串
            #?
            for i in range(0, random.randint(0, 9)):
                if picture is not None:
                    encode_str = base64.b64encode(picture).decode('utf-8')
                    book.pictures.append(encode_str)
            session.add(book)
        session.commit()
        session.close()
        

def init_table_book():
    bookdb = BookDB()
    size = bookdb.get_book_count()
    bookdb.send_db_to_table(0,size)  

def init_database(db_path):
    #global database_instance
    #database_instance = Store(db_path)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()# 创建程序与数据库之间的对话
    Base.metadata.create_all(engine)
    #将data/book.db数据导入表book
    init_table_book()

    session.commit()
    session.close()



