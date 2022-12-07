import logging
import os
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, DateTime, LargeBinary,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

import sqlite3 as sqlite
import random
import base64
import simplejson as json
from be.model import init_book_db


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
    book_id = Column(Integer, primary_key=True, nullable=False,index=True)  
    book_info = Column(Text)
    stock_level = Column(Integer)

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
        

def init_database(db_path):
    #global database_instance
    #database_instance = Store(db_path)
    #Base.metadata.drop_all(engine)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()# 创建程序与数据库之间的对话
    Base.metadata.create_all(engine)
    session.commit()
    session.close()



