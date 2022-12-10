# <center>华东师范大学数据科学与工程学院实验报告</center>


课程名称：当代数据管理系统 &emsp; &emsp;上机作业：书店 &emsp; &emsp;年级：大三 &emsp; &emsp;上机实践时间：2022.12.8

组号：2022_CDMS_PJ2_第6组&emsp; &emsp; 成员：许瑞琪、汪思远、陈沁文&emsp;&emsp;&emsp;学号：10205501450/29/09

## 实验任务
### 实现功能
实现一个提供网上购书功能的网站后端。网站支持书商在上面开商店，购买者可以通过网站购买。买家和卖家都可以注册自己的账号。一个卖家可以开一个或多个网上商店，买家可以为自已的账户充值，在任意商店购买图书。支持 下单->付款->发货->收货 流程。

1. 实现对应接口的功能，见项目的 doc 文件夹下面的.md 文件描述 （60%）。其中包括：
   
   1)用户权限接口，如注册、登录、登出、注销；

   2)买家用户接口，如充值、下单、付款；

   3)卖家用户接口，如创建店铺、填加书籍信息及描述、增加库存；

   通过对应的功能测试，所有 test case 都 pass。

2. 为项目添加其它功能（40%）：
   
   1)实现后续的流程：发货 -> 收货；

   2)搜索图书：
   用户可以通过关键字搜索，参数化的搜索方式；如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。如果显示结果较大，需要分页（使用全文索引优化查找）；

   3)订单状态，订单查询和取消定单：
   用户可以查自已的历史订单，用户也可以取消订单。取消定单可由买家主动地取消定单，或者买家下单后，经过一段时间超时仍未付款，定单也会自动取消。

### 实验要求
三人一组，做好分工，完成下述内容：

1. bookstore 文件夹是该项目的 demo，采用 flask 后端框架与 sqlite 数据库，实现了前 60% 功能以及对应的测试用例代码。要求利用 ORM 使用 postgreSQL 数据库实现前 60% 功能，可以在 demo 的基础上进行修改，也可以采用其他后端框架重新实现。需要通过 fe/test/ 下已有的全部测试用例。

2. 在完成前 60% 功能的基础上，继续实现后 40% 功能，要有接口、后端逻辑实现、数据库操作、代码测试。对所有接口都要写 test case，通过测试并计算测试覆盖率（尽量提高测试覆盖率）。

3. 尽量使用索引、事务处理等关系数据库特性，对程序与数据库执行的性能有考量。

4. 尽量使用 git 等版本管理工具。

5. 不需要实现界面，通过代码测试体现功能与正确性。
   
## 实验分工
1. 许瑞琪（学号：10205501450）
   
   修改数据库连接方式（修改 be/model/store.py、be/model/db_conn.py）；
   
   用户权限接口代码修改（修改 be/model/user.py）；

   实验报告的撰写；

2. 汪思远（学号：10205501429）
   
   买家用户接口代码修改（修改 be/model/buyer.py）；

   卖家用户接口代码修改（修改 be/model/seller.py）；

   协助后 40% 功能实现的代码测试；

3. 陈沁文（学号：10205501409）
   
   后 40% 功能实现，包括接口、后端逻辑实现、数据库操作，调整前 60% 的部分 .py 文件使其能够实现后 40% 的功能。

关于关系数据库如何设计、后 40% 功能的实现逻辑都经由我们小组组员共同商讨；完成前面部分的组员会将自己的代码经验分享到工作群或者 github 平台，以供后面部分的组员更快速理解代码编写方式和测试实现的整体架构，在实现分工紧密合作的同时提高工作效率。

## bookstore目录结构
```
bookstore
  |-- be                            后端
        |-- model                     后端逻辑代码
        |-- view                      访问后端接口
        |-- ....
  |-- doc                           JSON API 规范说明
  |-- fe                            前端访问与测试代码
        |-- access
        |-- bench                     效率测试
        |-- data                    
            |-- book.db                 sqlite 数据库(book.db，较少量的测试数据)
            |-- scraper.py              从豆瓣爬取的图书信息数据的代码
        |-- test                      功能性测试
        |-- conf.py                   测试参数
        |-- conftest.py               pytest 初始化配置
        |-- ....
  |-- ....
```

## 实验过程
### 安装配置：
安装 python (需要 python3.6 以上)

进入 bookstore 文件夹下安装依赖：

`pip install -r requirements.txt`

ORM：Object Relation Mapping，最初主要描述的是程序中的 Object 对象和关系型数据库中 Relation 关系(表)之间的映射关系，目前来说也是描述程序中对象和数据库中数据记录之间的映射关系的统称，是一种进行程序和数据库之间数据持久化的一种编程思想。特点是操纵 Python 对象而不是 SQL 查询，也就是在代码层面考虑的是对象，而不是 SQL，体现的是一种程序化思维，这样使得 Python 程序更加简洁易读。通过[ORM]核心模块增删改查的函数定义进行数据库数据的修改。

SQLAlchemy 是一个 Python 的 SQL 工具包以及数据库对象映射框架。它包含整套企业级持久化模式，专门为高效和高性能的数据库访问。实验要求利用 ORM 使用 postgreSQL 数据库，因此需要在本地安装，使用以下语句：

`pip install SQLAlchemy`

`pip install psycopg2`

### 关系数据库设计：
画 ER 图之前，这里介绍一些课外学到的关于更完备地构建 ER 图的知识，有助于更完善完美地画 ER 图。

用 ER 图方法构建一个项目的模型时，经常会遇到某些实体型是某个实体型的子类型。例如，在本次作业中买家 buyer 和卖家 seller 是用户 user 的子类型，用户是父类型。这种父类-子类联系称为 ISA 联系，表示 “is a” 的语义，可以理解为买家 “is a” 用户，卖家 “is a” 用户。ISA 联系用三角形来表示。如果父类中的一个实体能同时属于多个子类中的实体集，则称为可重叠约束，子类符号中没有叉号表示是可重叠的。完备性约束描述父类中的一个实体是否必须是某一个子类中的实体，如果是，则叫做完全特化(total specialization)，否则叫做部分特化(partial specialization)。完全特化用父类到子类的双线连接来表示，单线连接则表示部分特化。假设用户只有两类，要么是买家，要么是卖家，二者必居其一，这就是完全特化的例子。

ER 图绘制如下：

![avatar](img/ER.png)

下面介绍关系数据库的概念设计：

从 ER 图中看出，实体类涉及用户、商铺、订单和书籍，其中，用户实体有子类买家和卖家，订单实体有子类未付款订单、已付款订单和已取消订单。

接下来探究各个实体类之间的联系：

- 买家和订单：一个买家可以对应多笔订单，但一笔订单只能对应一个买家。
- 卖家和订单：一个卖家可以对应多笔订单，但一笔订单只能对应一个卖家。
- 卖家和商铺：一个卖家可以拥有多个书店，但一家书店只能对应一个卖家。
- 书店和书籍：一家书店可以存有多款书籍，一款书也可以被多家书店持有。这里的一款书指的不是一本书，而是每本同样的书都共用一个 book_id，book_id 一样的书统称为一款书。
- 订单和书籍：一个订单可以购买多款书籍，一款书也可以被多笔订单所购买。
- 订单和书店：一家书店可以拥有多笔订单，但一笔订单只能对应一家书店。

为了实现书店功能逻辑，我根据 ER 图中实体和联系一对一、一对多、多对多的创建原则，创建了八个关系数据表，分别是用户（user）、卖家店铺信息（user_store）、书店（store）、未付款订单（new_order）、已付款订单（new_order_paid）、已取消订单（new_order_cancel）、订单需求详情（new_order_detail）和书表（book）。而这八个数据表分别有如下属性及关系模式：

- 用户（user）：
  
  唯一属性用户 id user_id，单值属性密码 password、余额 balance、终端 teminal 和身份令牌 token。
  ```python
  class Users(Base):
    # 表的名字:
    __tablename__ = 'user'    
    # 表的结构:
    user_id = Column(Text, primary_key=True, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(Text)
    terminal = Column(Text)
  ```
  user_id 是主键，不再添加额外索引，基本都是通过 user_id 进行数据查询的。终端 terminal 用于标识登录的设备，而身份令牌 token 是登陆后在客户端缓存的令牌，在用户登录时由服务端生成，用户在接下来的访问请求时就无需密码。登录的用户 token 不会重复，但未登录的用户 token 均为空。
  
- 卖家店铺信息（user_store）：
  
  单值属性卖家 id user_id，卖家拥有书店 id store_id。
  ```python
  class User_store(Base):
    # 表的名字:
    __tablename__ = 'user_store'
    # 表的结构:
    user_id = Column(Text, primary_key=True, nullable=False)
    store_id = Column(Text, primary_key=True, nullable=False)
  ```
  (user_id, store_id) 是复合主键，不再添加额外索引，通过 user_id 或 store_id 查询书店与卖家的附属关系。

- 书店（store）：

  单值属性书店 id store_id、书籍 id book_id、书籍信息 book_info、库存量 stock_level。
  ```python
  class Store(Base):
    # 表的名字:
    __tablename__ = 'store'
    # 表的结构:
    store_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Integer, primary_key=True, nullable=False,index=True)  
    book_info = Column(Text)
    stock_level = Column(Integer)
  ```
  其中 store_id 和 book_id 组成复合主键，对 book_id 建立索引，加快搜索时根据书籍找到对应的书店和根据书店找到书店内的书。

- 未付款订单（new_order）：
  
  唯一属性订单 id order_id，单值属性买家 id user_id、书店 id store_id、订单应付款金额 price 和订单创建时间 time_。
  ```python
  class New_order(Base):
    # 表的名字:
    __tablename__ = 'new_order' 
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)
    price = Column(Integer)#订单总价
    time_ = Column(DateTime, nullable=False)#下单时间
  ```
  其中 order_id 是主键，由于订单表会频繁的插入删除，不适合在唯一标识订单的属性 order_id 上索引的创建，因此不再添加额外索引。

- 已付款订单（new_order_paid）：
  
  唯一属性订单 id order_id，单值属性买家 id user_id、书店 id store_id、订单应付款金额 price 和订单物流状态 status。
  ```python
  class New_order_paid(Base):
    # 表的名字:
    __tablename__ = 'new_order_paid'    
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)
    price = Column(Integer)
    status = Column(Integer)#0,1,2分别代表未发货，已发货和已收货
  ```
  由于订单实体被拆分成 3 个子类，未付款和已取消订单的物流状态已经确定，只有已付款订单需要添加状态属性，明确是待发货、已发货还是已收货。和未付款订单一样，设置 order_id 为主键，不再添加额外索引。

- 已取消订单（new_order_cancel）：
  
  唯一属性订单 id order_id，单值属性买家 id user_id、书店 id store_id、订单应付款金额 price。
  ```python
  class New_order_cancel(Base):
    # 表的名字:
    __tablename__ = 'new_order_cancel'   
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Text)  
    store_id = Column(Text)
    price = Column(Integer)
  ```
  和未付款、已付款订单一样，设置 order_id 为主键，不再添加额外索引。

- 订单需求详情（new_order_detail）：

  单值属性订单 id order_id、书籍 id book_id、购买书籍数量 count、书籍单价 price。
  ```python
  class New_order_detail(Base):
    # 表的名字:
    __tablename__ = 'new_order_detail'
    # 表的结构:
    order_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)  
    count = Column(Integer)
    price = Column(Integer)
  ```
  其中 order_id 和 book_id 组成复合主键，由于订单和书本是多对多关系，因此我们需要建立一张额外的订单需求详情表，由于会频繁的插入，因此不再添加额外索引。

- 书表（book）：

  唯一属性 book_id，单值属性标题 title、作者 author、出版商 publisher、原价 price、书籍简介 book_intro 等。
  ```python
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
  ```
  其中 book_id 是主键，不再添加额外索引，通过 book_id 查询书籍相关信息。

### 数据库连接：
为了完成书店功能，我连接的是我们组一个成员的阿里云数据库。本地链接阿里云 postgresql 要用公网地址：`dase-cdms-2022-pub.pg.rds.aliyuncs.com`，公网端口：5432。

数据库连接及数据表初始化函数在 be/model/store.py 和 be/model/init_book_db.py 里。建立本地与阿里云数据库连接，并创建对象的基类 Base：
```python
engine = create_engine("postgresql://stu10205501429:Stu10205501429@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501429")
Base = declarative_base()
```
其中 declarative_base() 是 sqlalchemy 内部封装的一个方法，通过其构造一个基类，这个基类和它的子类，可以将 Python 类和数据库表关联映射起来。后续也可以看到每个文件要使用数据表需要在文件头插入 `from be.model import init_book_db,store`，就可以对数据表进行各项操作，比如要用到用户表即运用类 store.Users 进行增删改查。

数据库表模型类通过 tablename 和表关联起来，Column 表示数据表的列。继承于 Base 的类对应的表为上述八个表，在介绍关系数据库设计时已随之给出，不再赘述。

当启动 app.py 文件并运行 serve.be_run() 函数，将调用 be/model/store.py 中的 init_database() 函数对数据库做初始化：
```python
def init_database(db_path):
    #Base.metadata.drop_all(engine)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()# 创建程序与数据库之间的对话
    Base.metadata.create_all(engine)
    session.commit()
    session.close()
```
创建程序与数据库之间的对话、创建所有继承于 Base 的类对应的表，提交事务后关闭对话窗口。这样一来，我们创建了八个空表，后面我们在运行测试的时候会进行数据操作。

但书籍的数据有些微差别，我们需要事先插入数据才能进行书籍查找。fe/data/scraper.py 已经写好爬虫将豆瓣网抓取的图书信息存入 sqlite 数据库 bookstore/fe/data/book.db 中，其 DDL 为：

    create table book
    (
        id TEXT primary key,
        title TEXT,
        author TEXT,
        publisher TEXT,
        original_title TEXT,
        translator TEXT,
        pub_year TEXT,
        pages INTEGER,
        price INTEGER,
        currency_unit TEXT,
        binding TEXT,
        isbn TEXT,
        author_intro TEXT,
        book_intro text,
        content TEXT,
        tags TEXT,
        picture BLOB
    );

于是添加了额外的 be/model/init_book_db.py 文件，用于将 sqlite 数据库 fe/data/book.db 中的数据导入 postgreSQL 数据库中的表 book。BookDB 类中的 __init__() 确定与 /fe/data/book.db 数据库的连接路径，send_db_to_table() 函数用于两个数据库之间的数据导入。

设计好数据库后，观察 be/model 文件夹下的各个功能函数，发现每个类的初始化都用到一条语句：
```python
def __init__(self):
    db_conn.DBConn.__init__(self)
```
到 be/model/db_conn.py 文件中查看，这个函数是用于连接数据库，创建程序与数据库之间的对话。由于我们把数据库换成了 postgreSQL 数据库，因此要采用新的连接方式：
```python
class DBConn:
    def __init__(self):
        engine = create_engine("postgresql://stu10205501429:Stu10205501429@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501429")
        Base = declarative_base()
        DbSession = sessionmaker(bind=engine)
        self.conn = DbSession() # 创建程序与数据库之间的对话
```
因此，上面提到的类初始化正是进入这样的代码，执行上述代码后便可以和数据库交互了。后续功能实现语句中的 self.conn 就充当一般查询语句中的 session 的功能。

所有表格创建好并在书表中插入完数据后，建立与 postgreSQL 数据库的连接会话，便可开始编写函数实现书店的各项功能。

### 后端逻辑的功能实现：
前 60% 的功能原本已采用 flask 后端框架与 sqlite 数据库实现。现要求利用 ORM 使用 postgreSQL 数据库实现前 60% 功能，可以直接在 demo 的基础上进行修改。通过查看 doc 里的 .md 文件知道修改 be/model/ 中的功能文件的要求，明确功能实现结果要传什么样的执行码和执行信息，用于与之后的测试结果匹配。

其中用到了 jwt 模块，它的 encode 功能用于配合密钥将字典格式的数据编码成字符串，即 token；它的 decode 功能用于配合密钥将字符串 token 还原成字典个数数据。这个模块用于在没有前端的情况下方便测试时的用户访问，即在 token 有效的时间段内，用户每次访问不需要密码。而 token 为由 user_id、登录设备 terminal、当前时间 timestamp 组合成的字符串。token 会定期地失效，对于不同的设备，token 是不同的。token 只对特定的时期特定的设备是有效的。

此外，很多功能执行失败的相关返回信息存在文件 be/model/error.py 中，后面将根据需要调用它。

先介绍原有的 60% 的功能分别做了什么：

参考 doc/auth.md 文件，auth 行为身份下有以下功能：

1. 注册用户（register 函数）：
   
   注册新用户，即插入 user_id、password、balance、token、termial 信息至 user 表。直接尝试插入数据，根据唯一属性 user_id 判断该用户名是否已经存在，若唯一属性 user_id 已存在，为了维持该属性的唯一标识性，数据将不能成功插入，发生数据库操作执行错误 sqlalchemy.exc.IntegrityError。user_id 不存在且语句书写正确则插入成功，返回执行码 200 和执行信息 'ok'；插入失败则返回定义在 be/model/error.py 中的用户 id 存在的报错信息 `error.error_exist_user_id(user_id)`，执行码 512。
  ```python
  def register(self, user_id: str, password: str):
      try:
          terminal = "terminal_{}".format(str(time.time()))
          token = jwt_encode(user_id, terminal)
          self.conn.add(store.Users(user_id=user_id, password=password,balance=0, token=token, terminal=terminal))
          self.conn.commit()
      except sqlalchemy.exc.IntegrityError:
          return error.error_exist_user_id(user_id)
      return 200, "ok"
  ```

2. 登录（login 函数）：

   利用同样位于 user.py 中 User 类的 check_password() 函数，根据 user_id 查询 user 数据表获取用户密码与用户输入密码对比，不相同则报身份权限错误，执行码 401，相同则下接。

   用 jwt 生成并更新 token，更改用户登录设备 terminal，操作正确则返回执行码 200、执行信息 'ok' 和 token；无更新结果，即没找到对应 user_id （在 check_password() 后正常不会出现这样的情况）报身份权限错误，更新操作失败则报执行码 528 和相应的错误信息。
  ```python
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
  ```
3. 登出（logout 函数）：
   
   利用同样位于 user.py 中 User 类的 check_token() 函数，根据 user_id 查询该 user 是否处于登陆状态，即检查 token 是否过期，过去则报身份权限错误，执行码 401，相同则下接。

   用 jwt 生成并更新 token，更改用户登录设备 terminal，操作正确则返回执行码 200 和执行信息 'ok'；无更新结果，即没找到对应 user_id （在 check_token() 后正常不会出现这样的情况）报身份权限错误，更新操作失败则报执行码 528 和相应的错误信息。
  ```python
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
  ```      
4. 注销用户（unregister 函数）：

   根据 user_id 查询待注销的用户是否存在，不存在或查询到用户但输入的密码错误，不能证明是用户本人操作，则报身份权限错误，执行码 401，不允许注销；存在则删除对应 user 表中要注销的表项并返回执行码 200 和执行信息 'ok'。
  ```python
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
  ```
5. 更改密码（change_password 函数）：

   利用同样位于 user.py 中 User 类的 check_password() 函数，根据 user_id 获取用户原有密码与用户输入的旧密码对比，不相同则报身份权限错误，执行码 401，不允许修改；若相同，则更新用户密码。
   
   用 jwt 生成并更新 token，更新用户登录设备 terminal，更新操作正确则返回执行码 200 和执行信息 'ok'；无更新结果，即没找到对应 user_id （在 check_password() 后正常不会出现这样的情况）报身份权限错误，更新操作失败则报执行码 528 和相应的错误信息。
  ```python
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
  ```
接下来要介绍的 buyer 和 seller 功能函数都会用到 be/model/db_conn.py 中判断用户、书籍、书店存在的函数。如 be/model/buyer.py 中的 `self.user_id_exist(user_id)` 就是调用了判断用户存在的函数，因为 self 经历了 `db_conn.DBConn.__init__(self)` 的初始化，因此也可以调用 DBConn 类中定义的 user_id_exist() 函数。

参考 doc/buyer.md 文件，buyer 行为身份下有以下功能：

1. 买家下单（new_order 函数）：
   
   判断 user_id 是否存在，不存在则返回错误类型 error_non_exist_user_id，执行码 511。判断 store_id 是否存在，不存在则返回错误类型 error_non_exist_store_id，执行码 513。
   
   确认买家 id 和书店 id 都存在之后，该用户可以在目标书店进行下单了。生成一个由user_id、store_id 和基于时间戳生成的唯一标识码组合而成的 uid，后续将作为订单 id order_id 用于唯一标识订单。
   
   根据订单信息（包括 book_id、购买数量 count、store_id）在 store 表中查找商户中是否存在对应书籍和足够的库存。如果没找到想要买的书，返回错误类型 error_non_exist_book_id，执行码 515。若库存不够，返回错误类型 error_stock_level_low，执行码 517。

   若满足订单查询条件且该书籍拥有足够的库存，则更新店里书籍数目，并在 new_order_detail 表中插入对应的 order_id、book_id、购买价格 price、购买数量 count。计算总价格，为 id_and_count 数组中每本书的单价和购买数量的乘积相加。然后在 new_order 表中插入对应的 order_id、买家 id、store_id、订单总价 price（为我们刚才计算得到的总价格）、下单时间 time_。操作正确且满足下单成功的逻辑则返回执行码 200、执行信息 'ok' 和订单 id order_id。若出现数据库操作失败则报执行码 528 和相应的错误信息。
  ```python
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
              # 找店里有没有这本书以及这本书的id、库存、简介
              cursor = self.conn.query(store.Store.book_id, store.Store.stock_level, store.Store.book_info)\
                                .filter(and_(store.Store.store_id == store_id, store.Store.book_id==int(book_id) ))                  
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
              if cursor == None:
                  return error.error_stock_level_low(book_id) + (order_id, )

              # 插入新order
              self.conn.add(store.New_order_detail(order_id = uid, book_id = book_id, count = count, price = price))
              total_price += price*count
          # 插入新总order
          time_ = datetime.utcnow()#暂存
          self.conn.add(store.New_order(order_id = uid, user_id = user_id, store_id = store_id, price = total_price, time_ = time_))           
          self.conn.commit()
          order_id = uid
      except sqlalchemy.exc.IntegrityError as e:
          logging.info("528, {}".format(str(e)))
          return 528, "{}".format(str(e)), ""
      return 200, "ok", order_id
  ```
注意：这里生成下单时间用到了 datetime.utcnow() 返回当前 UTC 时间，将在后面自动取消订单有所帮助。

2. 买家付款（payment 函数）：
   
   用 order_id 查询在 new_order 表中是否存在符合订单号的代付订单，不存在则返回错误类型 error_invalid_order_id，执行码 518。若存在对应订单，但查询得到的该订单下单者 id buyer_id 不等于预付款的 user_id，报身份权限错误，执行码 401，授权失败。

   通过 user_id 确认预付款用户有权限操作后，获取用户余额与用户密码，与用户输入密码对比。查询没能获得结果，即没找到对应 user_id （在之前判断授权后正常不会出现这样的情况），返回错误类型 error_non_exist_user_id，执行码 511。若密码不正确，报身份权限错误，执行码 401；密码正确则接下去判断。
   
   第一个查询已根据订单号查询到 store_id，接着再由 store_id 查询书店所属卖家 id。若没找到则证明 store_id 有误，返回错误类型 error_non_exist_store_id，执行码 513。找到卖家后，确定卖家 id 在用户表里存在，即证明卖家是真实存在可与买家进行交易的，且买家用户余额大于待付价格，则能够成功付款，根据买家 id 在 user 表中给买家减少余额，若更新失败返回错误类型 error_not_sufficient_funds，执行码 519；根据卖家 id 在 user 表中给卖家增加余额。

   付款后，将该订单移至 new_order_paid 表，将 status 初始化为 0，表示未发货；从未付款订单表 new_order 中删除对应订单信息。操作正确且满足付款成功的逻辑则返回执行码 200 和执行信息 'ok'。若出现数据库操作失败则报执行码 528 和相应的错误信息。
  ```python
  def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
      conn = self.conn
      try:
          cursor = conn.query(store.New_order.order_id, store.New_order.user_id, store.New_order.store_id, store.New_order.price)\
                       .filter(store.New_order.order_id == order_id)
          row = cursor.first()
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
          if row is None:
              return error.error_non_exist_user_id(buyer_id)
          balance = row[0]
          if password != row[1]:
              return error.error_authorization_fail()

          cursor = conn.query(store.User_store.store_id, store.User_store.user_id)\
                       .filter(store.User_store.store_id == store_id)
          row = cursor.first()
          if row is None:
              return error.error_non_exist_store_id(store_id)

          seller_id = row[1]

          if not self.user_id_exist(seller_id):
              return error.error_non_exist_user_id(seller_id)
          
          if balance < total_price:
              return error.error_not_sufficient_funds(order_id)
                
          cursor = conn.query(store.Users)\
                       .filter(and_(store.Users.user_id == buyer_id, store.Users.balance >= total_price))\
                       .update({'balance': store.Users.balance - total_price})
          if cursor == None:
              return error.error_not_sufficient_funds(order_id)

          cursor = conn.query(store.Users)\
                       .filter(store.Users.user_id == seller_id)\
                       .update({'balance': store.Users.balance + total_price})
          if cursor == None:
              return error.error_non_exist_user_id(seller_id)
          #付款后将该订单移至new_order_paid，status初设为0，表示未发货
          cursor = conn.query(store.New_order).filter(store.New_order.order_id == order_id).delete()
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
      return 200, "ok"
  ```
注意：为实现后 40% 查看历史订单的功能，这里去掉了原代码里删除 new_order_detail 表中关于该订单表项的操作。

3. 买家充值（add_funds 函数）：
    
   根据 user_id 获取用户密码与用户输入密码对比。没查到对应用户或密码错误报身份权限错误，执行码 401，授权失败；若密码正确，在 user 表中更新用户余额。操作正确且满足充值成功的逻辑则返回执行码 200 和执行信息 'ok'。若出现数据库操作失败则报执行码 528 和相应的错误信息证明充值失败。
  ```python
  def add_funds(self, user_id, password, add_value) -> (int, str):
      conn = self.conn
      try:
          cursor = conn.query(store.Users.password).filter(store.Users.user_id == user_id)
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
      return 200, "ok"
  ```
参考 doc/seller.md 文件，seller 行为身份下有以下功能：

1. 商家添加书籍信息（add_book 函数）：
   
   检查 user_id 和 store_id 是否已存在。不存在则分别报错卖家用户不存在或书店不存在，执行码 511、513。
   
   根据 book_id 从 book 表查询是否存在对应书籍，存在报错 error_exist_book_id，执行码 516，表示书籍已在该书店存在无法添加；若不存在，就将 store_id、book_id、书籍信息 book_info 和初始库存量 stock_level 插入 store 表。操作正确且满足添加书籍成功的逻辑则返回执行码 200 和执行信息 'ok'。若出现数据库操作失败则报执行码 528 和相应的错误信息证明添加失败。
  ```python
  def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
      try:
          if not self.user_id_exist(user_id):
              return error.error_non_exist_user_id(user_id)
          if not self.store_id_exist(store_id):
              return error.error_non_exist_store_id(store_id)
          if self.book_id_exist(store_id, book_id):
              return error.error_exist_book_id(book_id)
          self.conn.add(store.Store(store_id = store_id, book_id = book_id, book_info = book_json_str, stock_level = stock_level))
          self.conn.commit()
      except sqlalchemy.exc.IntegrityError as e:
          return 528, "{}".format(str(e))
      return 200, "ok"
  ```
2. 商家添加书籍库存（add_stock_level 函数):
   同样先检查 user_id、store_id 和 book_id 是否已存在，不存在则报错。

   根据 store_id 更新对应书店 store 表中待进货书籍库存。无更新结果即没找到对应书店（执行上面的书店 store_id 查询后正常不会出现这种现象）则报权限错误，执行码 401。操作正确且满足添加书籍库存成功的逻辑则返回执行码 200 和执行信息 'ok'。若出现数据库操作失败则报执行码 528 和相应的错误信息证明添加库存失败。
  ```python
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
          self.conn.commit()
      except sqlalchemy.exc.IntegrityError as e:
          return 528, "{}".format(str(e))
      return 200, "ok" 
  ```

3. 创建商铺（create_store 函数）：
   
   检查 user_id 是否已存在，不存在返回用户不存在的报错，执行码 511；检查 store_id 是否已存在，存在返回书店已存在的报错，执行码 514，书店已存在意味着不能再用该 store_id 创建新书店了。

   用户存在且 store_id 不存在时，插入用户 id 和新建书店 id store_id 至 user_store 表，代表着该用户开了一家 id 为 store_id 的新书店。操作正确且满足创建书店成功的逻辑则返回执行码 200 和执行信息 'ok'。若出现数据库操作失败则报执行码 528 和相应的错误信息证明创建失败。
  ```python
  def create_store(self, user_id: str, store_id: str) -> (int, str):
      try:
          if not self.user_id_exist(user_id):
              return error.error_non_exist_user_id(user_id)
          if self.store_id_exist(store_id):
              return error.error_exist_store_id(store_id)
          self.conn.add(store.User_store(user_id = user_id, store_id = store_id))
          self.conn.commit()
      except sqlalchemy.exc.IntegrityError as e:
          return 528, "{}".format(str(e))
      return 200, "ok"
  ```

以上是前 60% 包含的所有功能。接下来介绍后 40% 的功能是在完成前 60% 功能的基础上实现的，对前 60% 作了微调。

首先介绍订单的后续流程实现。订单的后续发货流程是由卖家决定的，因此将发货功能添加到 be/model/seller.py 文件中，为 seller 行为身份增添了以下功能：

4. 卖家发货（send_books 函数）：
   
   根据 order_id 在已付款订单 new_order_paid 表中查询对应的订单状态和书店 id。没找到则返回错误类型 error_invalid_order_id，执行码 518，订单号不正确不能发货。

   通过书店 id 获取其拥有者 id，比较其与输入的卖家 id 是否对应，不对应则返回权限错误，执行码 401。权限无误后，检查订单状态是否为待发货，不是则返回错误类型 error_books_duplicate_sent（为实现后 40% 添加的错误类型），执行码 522。若符合条件，则更新订单状态为已发货，即将物流状态码更新为 1，返回执行码 200 和执行信息 'ok'。
  ```python
  def send_books(self, user_id: str, order_id: str) -> (int, str):
      conn = self.conn
      cursor = conn.query(store.New_order_paid.store_id,store.New_order_paid.status)\
                   .filter(store.New_order_paid.order_id == order_id)
      if cursor == None:
          return error.error_invalid_order_id(order_id)   
      row = cursor.first()
      store_id = row[0]
      cursor_store = conn.query(store.User_store.user_id)\
                         .filter(store.User_store.store_id == store_id)
      row_store = cursor_store.first()
      if row_store[0] != user_id:
          return error.error_authorization_fail()
      if row[1] == 1 or row[1] == 2:
          return error.error_books_duplicate_sent()     
      cursor = self.conn.query(store.New_order_paid)\
                        .filter(store.New_order_paid.order_id == order_id)\
                        .update({'status':1}) 
      self.conn.commit()
      return 200, "ok"
  ```
测试用例写在 fe/test/test_send_books.py，测试的情况有四种：发货正常情况、订单号 order_id 不存在、权限错误 user_id 与 store_id 不对应、订单已发货不可重复发货。

订单发货后物流最终是否成功送达给买家卖家难以跟踪，因此是否把订单标记为成功收货是由买家决定的，将收货功能添加到 be/model/buyer.py 文件中，为 buyer 行为身份增添以下功能：

4. 买家收货（receive_books 函数）：

   根据 order_id 在 new_order_paid 表中查询对应的订单状态和买家 id。没找到则返回错误类型 error_invalid_order_id，执行码 518，订单号不正确无法修改状态。

   找到对应订单后，检查输入的用户 user_id 与下单用户是否一致，不是同一个人的话返回权限错误，执行码 401，没有资格修改物流状态。

   检查订单状态是否为已发货，若物流状态为未发货，返回错误类型 error_books_not_sent（为实现后 40% 添加的错误类型），执行码 520；若物流状态为已收货，返回错误类型 error_books_duplicate_receive（为实现后 40% 添加的错误类型），执行码 521。若物流状态正好为已发货，则更新订单状态为已收货，即将物流状态码更新为 2，返回执行码 200 和执行信息 'ok'。
  ```python
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
  ```
测试用例写在 fe/test/test_receive_books.py，测试的情况有五种：收货正常情况、订单号 order_id 不存在、权限错误 user_id 与 order_id 不对应、订单未发货不可能收货、订单已收货不可重复收货。

然后介绍更多订单相关功能。取消定单可由买家主动地取消定单，或者买家下单后，经过一段时间超时仍未付款，定单也会自动取消。将取消订单功能添加到 be/model/buyer.py 文件中，为 buyer 行为身份增添以下功能：

5. 买家主动取消订单（cancel_order 函数）：
   
   买家可以取消未付款订单和已付款订单，移入 new_order_cancel 表，已付款订单需要退款，默认卖家都是允许退款的。
   
   先处理未付款订单的取消，根据 order_id 在未付款订单 new_order 表中中获取买家 id、书店 id、订单价格 price。如果用户输入 id 与该订单买家 id 不匹配，返回权限错误，执行码 401，不支持非本人取消订单。确定为本人操作后，未付款订单可直接从未付款订单 new_order 表中删除。

   然后处理已付款订单的取消。根据 order_id 在已付款订单 new_order_paid 表中获取买家 id、书店 id、订单价格 price。如果用户输入 id 与该订单买家 id 不匹配，返回权限错误，执行码 401，同样不支持非本人取消订单。确定为本人操作后，查询被取消订单的书店的拥有者 id，让卖家将钱退还给买家，在 user 表中更新买家和卖家余额。做完这些才能从已付款订单 new_order_paid 表中删除取消的订单表项。

   既不是未付款也不是已付款的订单无法取消。

   最后将订单信息加入 new_order_cancel 表中，方便以后对历史订单查询。
  ```python
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
  ```
测试用例写在 fe/test/test_cancel_order.py，测试的情况有八种：已付款订单的取消、未付款订单的取消、已付款订单号 order_id 不存在、未付款订单号 order_id 不存在、取消已付款订单权限错误、取消未付款订单权限错误、已付款订单不可重复取消、未付款订单不可重复取消。

6. 定单自动取消（auto_cancel_order 函数）：
   
   设置为 20 秒后取消订单，检查所有未付款订单 id，未查询到任何订单即没有未付款订单，则无需自动取消，直接返回执行码 200 和执行消息 'ok'。若查到则接下去判断，查询未付款订单中所有当前时间与订单的下单时间差在 20 秒内的订单。未查到订单说明已付款或已被买家自行取消，无需做出动作；查到则依次自动取消订单，即将到期未付款订单从 new_order 中删除，删除失败返回错误类型 error_invalid_order_id。

   最后，将自动取消的订单信息也加入 new_order_cancel 表中，方便以后对历史订单查询。
  ```python
  def auto_cancel_order(self) -> (int, str):
      wait_time = 20#20s后自动取消订单
      conn = self.conn
      now = datetime.utcnow()
      cursor_all = conn.query(store.New_order.order_id).all()
      if(len(cursor_all)) != 0:
          cursor = conn.query(store.New_order.order_id,store.New_order.user_id,store.New_order.store_id,store.New_order.price,store.New_order.time_)\
                       .filter(store.New_order.time_ <= now-timedelta(seconds=wait_time)).all()
          #未查到订单说明已付款或已被买家自行取消，无需做出动作
          if len(cursor) != 0:
              for row in cursor:
                  cursor_del = conn.query(store.New_order)\
                                   .filter(store.New_order.order_id == row[0]).delete()
                  if cursor_del == None:
                      self.conn.commit()
                      return error.error_invalid_order_id(row[0])
                  conn.add(store.New_order_cancel(order_id = row[0], user_id = row[1], store_id = row[2], price = row[3]))
      self.conn.commit()
      return 200, "ok"
  ```
7. 检查订单是否取消（is_order_cancelled 函数）：
   
   为测试 auto_cancel_order 作的函数，判断订单没有自动取消的原因。根据 order_id 查询已取消的订单中是否有与该订单号相匹配的，若没找到则证明在超时前已付款无法再对订单自动取消，返回错误类型 error_auto_cancel_fail，执行码 524；找到说明订单以成功取消（要么超时前已经由用户取消要么到时间自动取消，取决于测试时的线程休眠时间），则返回执行码 200 和执行消息 'ok'。
  ```python
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
  ```
测试用例写在 fe/test/test_auto_cancel_order.py，测试的情况有三种：订单超时正常自动取消情况、在自动取消前订单已经被买家取消、在自动取消前订单已付款。

订单相关功能还有支持用户查询历史订单。同样将查询历史订单功能添加到 be/model/buyer.py 文件中，为 buyer 行为身份增添以下功能：

8. 历史订单查询（check_hist_order 函数）：
   
   先检查用户 id 是否存在，存在才能进行订单查询，不存在则报权限错误。一共有三种历史订单，分别是未付款订单、已付款订单、已取消订单，为了让用户所有的历史订单都能查询到，需要对三张表都进行查询。
   
   先查询所有未付款订单，根据买家 id 在未付款订单 new_order 表中筛选记录，然后根据查询得到的每个订单号 order_id 对 new_order_detail  表查询对应订单详细信息，获取该订单买的所有书籍的 book_id、购买该书籍数量 count、单价 price 的信息并将它们合并为一个字典类型。然后将这笔订单设置订单状态为 not paid'，加上订单号 order_id、买家 id、书店 id、订单总价 total_price、订单详情 details（刚才生成的字典类型数据）插入 res 字典类型。

   在已付款和已取消订单表中进行相同的操作，已付款订单还会多查询出订单物流状态信息。最终得到的 res 就是用户希望查到的所有历史订单，将它和执行码 200、执行消息 'ok' 一起返回。如果 res 长度为 0，即用户无购买记录，则返回执行码 200、执行消息 'ok' 和一个空值。
  ```python
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
                                  .filter(store.New_order_detail.order_id == order_id).all()
              if len(cursor_detail) != 0:
                  for i in cursor_detail:
                      details.append({'book_id':i[0],'count':i[1],'price':i[2]})
              else:
                  return error.error_invalid_order_id(order_id)
              res.append({'status':"not paid",'order_id':row[0],'buyer_id':row[1],'store_id':row[2],'total_price':row[3],'details':details})
      #查询已付款订单
      books_status=["not send","already send","already receive"]
      cursor = conn.query(store.New_order_paid.order_id,store.New_order_paid.user_id,store.New_order_paid.store_id,store.New_order_paid.price,store.New_order_paid.status)\
                   .filter(store.New_order_paid.user_id == user_id).all()
      if len(cursor) != 0:
          for row in cursor:
              details = []
              order_id = row[0]
              cursor_detail = conn.query(store.New_order_detail.book_id,store.New_order_detail.count,store.New_order_detail.price)\
                                  .filter(store.New_order_detail.order_id == order_id).all()
              if len(cursor_detail) != 0:
                  for i in cursor_detail:
                      details.append({'book_id':i[0],'count':i[1],'price':i[2]})
              else:
                  return error.error_invalid_order_id(order_id)
              res.append({'status':"already paid",'order_id':row[0],'buyer_id':row[1],'store_id':row[2],'total_price':row[3],'books_status':books_status[row[4]],'details':details})
      #查询已取消订单
      cursor = conn.query(store.New_order_cancel.order_id,store.New_order_cancel.user_id,store.New_order_cancel.store_id,store.New_order_cancel.price)\
                   .filter(store.New_order_cancel.user_id == user_id).all()
      if len(cursor) != 0:
          for row in cursor:
              details = []
              order_id = row[0]
              cursor_detail = conn.query(store.New_order_detail.book_id,store.New_order_detail.count,store.New_order_detail.price)\
                                  .filter(store.New_order_detail.order_id == order_id).all()
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
  ```
测试用例写在 fe/test/test_check_hist_order.py，测试的情况有三种：历史订单正常查询情况、user_id 不存在导致的权限错误、用户无购买记录。

最后介绍图书搜索功能。用户可以通过关键字搜索，搜索范围包括：书名、作者名、标签、书简介和出版社，全站搜索或是当前店铺搜索。显示结果较大，需要分页 (使用全文索引优化查找)。将书籍搜索功能添加到 be/model/user.py 文件中，为 user 行为身份增添以下功能：

6. 全站搜索（search_all 函数）：

   制定搜索规则 rule：利用正则化匹配的方法通过搜索关键词查找图书，关键词按空格隔开，进行模糊查询。搜索范围包括书名 title、作者 author、标签 tags、书籍简介 book_intro、出版社 publisher。

   在书表 book 中根据搜索规则查询关键词匹配结果。关键词可能会带来巨大的查询结果，为了简洁地呈现我们希望查到的书籍并希望通过分页查询减少数据库与程序之间 IO 的负担，实现了分页查询，可查询第 page+1 页的所有结果，每页有五个返回结果。如果没能查到任何匹配关键词的书籍，返回错误类型 error_no_matching_books_in_all（为实现后 40% 添加的错误类型），执行码 525 和 "can not find" 的提示语。若找到匹配书籍，将每条查找结果插入 res 字典类型，返回执行码 200、执行消息 'ok' 和搜索结果 res。
  ```python
  def search_all(self, input_str: str, page: int):
      conn = self.conn
      #一页有5个返回结果
      num_of_books_page = 5
      input_list = set(re.sub('[^\w\u4e00-\u9fff]+', ' ', input_str.lower()).split(' '))
      rule = or_( *[init_book_db.Book.title.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.author.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.tags.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.book_intro.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.publisher.like("%"+input+"%") for input in input_list])
      cursor = conn.query(init_book_db.Book.book_id,init_book_db.Book.title,init_book_db.Book.author,init_book_db.Book.publisher,init_book_db.Book.book_intro)\
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
          return error.error_no_matching_books_in_all(),"can not find"
  ```
测试用例写在 fe/test/test_search_all.py，测试的情况有两种：正常搜索情况、关键词无匹配结果。

7. 书店内搜索（search_in_store 函数）：
   
   同样制定搜索规则 rule：利用正则化匹配的方法通过搜索关键词查找图书，关键词按空格隔开，进行模糊查询。搜索范围包括书名 title、作者 author、标签 tags、书籍简介 book_intro、出版社 publisher。

   搜索该书店中所有书籍 book_id，在书表 book 中根据搜索规则查询关键词匹配且 id 在搜索书店中存在的书籍结果。还是实现分页查询，可查询第 page+1 页的所有结果，每页有十个返回结果。如果没能查到任何匹配关键词的书籍，返回错误类型 error_no_matching_books_in_store（为实现后 40% 添加的错误类型），执行码 526 和 "can not find" 的提示语。若找到匹配书籍，将每条查找结果插入 res 字典类型，返回执行码 200、执行消息 'ok' 和搜索结果 res。
  ```python
  def search_in_store(self, store_id: str, input_str: str, page: int):
      conn = self.conn
      input_list = set(re.sub('[^\w\u4e00-\u9fff]+', ' ', input_str.lower()).split(' '))
      rule = or_( *[init_book_db.Book.title.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.author.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.tags.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.book_intro.like("%"+input+"%") for input in input_list],
                  *[init_book_db.Book.publisher.like("%"+input+"%") for input in input_list])
      cursor_store = conn.query(store.Store.book_id)\
                         .filter(store.Store.store_id == store_id).all()
      res=[]
      if len(cursor_store) != 0:
          cursor = conn.query(init_book_db.Book.book_id,init_book_db.Book.title,init_book_db.Book.author,init_book_db.Book.publisher,init_book_db.Book.book_intro)\
                       .filter(and_(init_book_db.Book.book_id.in_([i[0] for i in cursor_store]),rule))\
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
          return error.error_no_matching_books_in_store(),"can not find"
  ```

测试用例写在 fe/test/test_search_in_store.py，测试的情况有两种：正常搜索情况、关键词在该书店无匹配结果。

至此，我介绍完了本次作业书店包含的所有功能。

### 访问后端接口：
本次作业使用 flask 构建实现书店功能的应用程序。访问后端接口的文件被写在 be/view 文件夹里，在这里对其中一个 40% 附加功能的接口做介绍。

使用 Blueprint 分离前后端开发的代码，以不同的 url 前缀来隔离不同的功能，达到每个功能分开测试的效果，不仅可以使入口文件变得很干净，更重要的是实现了很好的模块化。这里我创建了 auth（认证模块）：
```python
bp_auth = Blueprint("auth", __name__, url_prefix="/auth")
```
然后在 be/serve.py 中注册了这个蓝图：
```python
    app = Flask(__name__)
    app.register_blueprint(auth.bp_auth)
```
因此，这里以 bp_auth.route 注册的函数都会自带 /auth，以 be/view/auth.py 中的全局搜索 search_all 的功能接口为例，url 是 /auth/search_all。

完成测试与后端的划分代码实现框架后，开始编写接口函数功能。后端接收测试例数据：在 search_all() 函数中使用 flask 中的 `request.json.get("input_str", "")` 可以获得测试例向后端传递的 “关键词” 数据，然后就可以进行相应的处理。令 u 等效于 be/model/user.py 中的 User 类，调用类函数 search_all() 并将获取的测试例参数随函数传给后端逻辑运行。由于测试是模拟前端发送一个请求然后跳转到后端接口的 search_all() 函数，返回值为后端逻辑功能函数执行得到的，由执行消息和执行结果组合而成的 json 类型返回值和执行码 code。
```python
@bp_auth.route("/search_all", methods=["POST"])
def search_all():
    input_str = request.json.get("input_str", "")
    page = request.json.get("page", "")
    u = user.User()
    code, message, res = u.search_all(input_str=input_str, page=page)
    return jsonify({"message": message, "res": res}), code
```
所有的功能接口其实都大同小异，就不再对其他接口进行介绍了。

### 接口测试：
接口测试文件均放在文件夹 fe 中，要实现测试至少需要 __init__.py、conftest.py（测试头部）、fe/test/test_func.py（各个测试函数）文件。一个包是一个带有特殊文件 __init__.py 的目录。__init__.py 文件定义了包的属性和方法，它可以什么也不定义；也可以只是一个空文件，但是必须存在，否则这个目录就仅仅是一个目录，而不是一个可以用于测试的包。conftest.py 文件用于启动测试、pytest 初始化配置，conf.py 包含测试参数。

测试使用了 python 库 threading，其开启线程后主线程会等待所有的子线程结束后才结束。它实例化了 serve.be_run() 线程对象，然后开始执行线程进行测试。

进入 bookstore 文件夹右键 Git Bash Here，输入 `bash script/test.sh` 执行测试。前 60% 测试代码没有改动，后 40% 代码测试函数添加在 fe/test 文件夹中。测试结果与测试覆盖率如下，可以看到针对不同功能的 60 个测试全部通过：

![avatar](img/test.png)

所有测试全部通过，符合我们的预期。代码覆盖率达到 91%，且核心组件 buyer.py、seller.py 和 user.py 的覆盖率均大于等于 86%，算是一个比较可观的覆盖率。

接下来详细介绍一下代码测试。我们注意到 fe/test 文件夹中有一个不是以 test_ 开头命名的文件 gen_book_data.py，这个文件所包含代码被封装为 GenBook 类，是用于根据输入的 user_id 和 store_id 生成一个卖家书店，并在书店里随机插入一些书；还为买家随机生成一份欲购买书籍清单 buy_book_id_list。在测试代码中我们将经常能看到它。

还是以一份测试代码为例，我选择的是 test_auto_cancel_order.py，测试自动取消订单功能。先为自动取消订单创建一个类 TestAutoCancelOrder，比较好奇测试数据的初始化：测试文件前面先生成测试要用的数据，将稍后要用到的测试数据统一在 pre_run_initialization 函数生成里。可以看到下面的数据生成中，共生成了一笔订单的卖家、书店、买家和要买书籍的信息。还给买家账户里充钱，保证交易的正常资金流动。
```python
class TestAutoCancelOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_auto_cancel_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_auto_cancel_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_auto_cancel_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.buyer_id
        self.wait_time = 20 # 自动取消订单间隔时长
        gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = gen_book.seller
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        self.buy_book_id_list = buy_book_id_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b

        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price+1000000)
        assert code == 200
        yield
```
fe/test 中的文件还链接着 fe/access 中的文件，注意看其中的 url 可以得知测试被链接到哪。比如自动取消订单被链接到 fe/access/new_buyer.py，调用其中的 register_new_buyer 函数将由 "http://127.0.0.1:5000/auth/register" 跳转到 be/view/auth.py 文件中的访问后端接口的函数 /register 进行买家用户注册。

生成完测试要用的数据后便可以开始测试，每个测试例为定义在 TestAutoCancelOrder 类中的方法。订单超时正常自动取消情况：
```python
def test_ok_overtime(self):
    code, self.order_id = self.buyer.new_order(self.store_id, self.buy_book_id_list)
    assert code == 200
    time.sleep(self.wait_time+5)
    code = self.buyer.is_order_cancelled(self.order_id)
    assert code == 200
```
先生成新的未付款订单，执行成功返回执行码 200；接着让线程休眠一次未付款订单自动取消周期加五秒后，查询订单是否被取消，若返回的执行码是 200 则说明自动取消成功。当执行码返回的都是期望中的值，则不发生断言，程序正常执行；否则断言错误，测试不通过。

在自动取消前订单已经被买家取消：
```python
def test_ok_not_overtime_cancel_by_buyer(self):
    code, self.order_id = self.buyer.new_order(self.store_id, self.buy_book_id_list)
    assert code == 200
    code = self.buyer.cancel_order(self.buyer_id, self.order_id)
    assert code == 200
    time.sleep(self.wait_time+5)
    code = self.buyer.is_order_cancelled(self.order_id)
    assert code == 200
```
生成新的未付款订单，执行成功返回执行码 200；接着买家手动取消订单，取消成功返回执行码 200；然后让线程休眠一次未付款订单自动取消周期加五秒后，查询订单是否被取消，若返回的执行码是 200 则说明未付款订单已被买家取消。执行过程中未发生断言错误则测试通过。

在自动取消前订单已付款：
```python
def test_ok_not_overtime_paid(self):
    code, self.order_id = self.buyer.new_order(self.store_id, self.buy_book_id_list)
    assert code == 200
    code = self.buyer.payment(self.order_id)
    assert code == 200
    time.sleep(self.wait_time+5)
    code = self.buyer.is_order_cancelled(self.order_id)
    assert code != 200
```
生成新的未付款订单，执行成功返回执行码 200；接着买家付款，付款成功返回执行码 200；然后让线程休眠一次未付款订单自动取消周期加五秒后，查询订单是否被取消，若返回的执行码不是 200 则说明未付款订单已被买家取消。执行过程中未发生断言错误则测试通过。

这是一个比较特殊的测试，比起其他测试代码，自动取消订单设置了让线程休眠的代码行，为的是让线程运行时停下，等待自动取消订单后再判断订单状态是否被自动取消、手动取消、已付款。这里用到了 python 定时器库 apscheduler，需要在命令行输入 `pip install apscheduler` 下载。

自动取消订单功能在 be/model/buyer.py 文件中，为了实现定时器的效果，在文件最后插入以下语句：
```python
sched = BackgroundScheduler()
sched.add_job(Buyer().auto_cancel_order, 'interval', id='5_second_job', seconds=5)
sched.start()
```
设置 BackgroundScheduler 类定时器，调用 start 后主线程不会阻塞并可以持久化任务。它能实现每隔 5s 就调度 Buyer().auto_cancel_order 运行一次，而 Buyer().auto_cancel_order 是自动取消订单功能函数，即每隔五秒自动搜索并取消一次过期未付款订单。通过修改 add_job() 的参数 seconds，就可以改变任务调度的间隔时间，每个任务都会以线程的方式被调度。

功能的测试代码也大同小异，就不再介绍其他功能的测试用例了。

### 大作业亮点
我们小组的作业使用了 git 版本管理工具，方便多人协调工作、上传或查看代码、有效监听谁修改代码、获取工作的历史版本、本地及远程操作。我们在 github.com/Linshou99 下建仓库并添加合作者直接 clone 我们的项目，以及 fork 到另两位组员的仓库并向该仓库发起 pull request 请求三种方式，最终采用三者地位都平等的方式。当有需要组员修改后的代码时，自行拉取至本地即可。

大作业 github 网址：https://github.com/Linshou99/bookstore 。可以在上面回溯我们的工作历史。

![avatar](img/git.png)

本次作业我们还使用 pgAdmin 4 工具操作 PostgreSQL。pgAdmin4 是一个可视化界面，可代替 SQL Shell 对关系数据库进行操作。我们正是看中了该工具的可视化功能，在上面连接阿里云数据库，利用 pgAdmin 中的 SQL 执行脚本进行 DML 操作，查看插入表的全部记录。在 pgAdmin 上我们能通过表查询结果方便地判断数据插入正误及数据库操作语句执行正误，填补本次实验没有前端要求，不方便直观判断代码书写正误的缺点。

![avatar](img/pgAdmin.png)

以上就是我们组大作业的所有内容，若有代码问题或者其他需求，请联系我们！