import logging
import os
import sqlite3 as sqlite
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
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
            
class New_order(Base):
    # 表的名字:
    __tablename__ = 'new_order'
    
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)

class New_order_detail(Base):
    # 表的名字:
    __tablename__ = 'new_order_detail'

    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)  
    count = Column(Integer)
    price = Column(Integer)

class Store:
    database: str

    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")    
        self.init_tables()

    def init_tables(self):
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
            
        class user_store(Base):
            # 表的名字:
            __tablename__ = 'user_store'
    
            # 表的结构:
            user_id = Column(Text, primary_key=True, nullable=False)
            store_id = Column(Text, primary_key=True, nullable=False)
                
        class store(Base):
            # 表的名字:
            __tablename__ = 'store'

            # 表的结构:
            store_id = Column(Text, primary_key=True, nullable=False)
            book_id = Column(Text, primary_key=True, nullable=False)  
            book_info = Column(Text)
            stock_level = Column(Integer)
            
        class new_order(Base):
            # 表的名字:
            __tablename__ = 'new_order'
    
            # 表的结构:
            order_id = Column(Text, primary_key=True, nullable=False)
            user_id = Column(Text)  
            store_id = Column(Text)

        class new_order_detail(Base):
            # 表的名字:
            __tablename__ = 'new_order_detail'

            # 表的结构:
            order_id = Column(Text, primary_key=True, nullable=False)
            book_id = Column(Text, primary_key=True, nullable=False)  
            count = Column(Integer)
            price = Column(Integer)

            
        #self.init()
        DbSession = sessionmaker(bind=engine)
        session = DbSession()
        Base.metadata.create_all(engine)
        session.commit()
        session.close()
        #except:
        #    conn.rollback()

    #def init(self) :
     #   DbSession = sessionmaker(bind=engine)
      #  session = DbSession()
       # Base.metadata.create_all(engine)
        #session.commit()
        

    #def get_db_conn(self) :
     #   engine = create_engine("postgresql://stu10205501429:Stu10205501429@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501429")
      #  DbSession = sessionmaker(bind=engine)
      #  session = DbSession() # 创建程序与数据库之间的对话
        #return session


database_instance: Store = None


def init_database(db_path):
    #global database_instance
    #database_instance = Store(db_path)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()
    Base.metadata.create_all(engine)
    session.commit()
    session.close()


#def get_db_conn():
 #   global database_instance
  #  return database_instance.get_db_conn()