import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
from fe.access import auth
from fe import conf
import uuid

import random


class TestSearchInStore:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_in_store_store_id_{}".format(str(uuid.uuid1()))
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=10)
        self.book_info_list = gen_book.buy_book_info_list
        assert ok
        len_list = len(self.book_info_list)
        bk_index1 = random.randint(0,len_list-1)
        bk_index2 = random.randint(0,len_list-1)
        bk_index3 = random.randint(0,len_list-1)
        self.input_str = self.book_info_list[bk_index1][0].title+" "+\
                            self.book_info_list[bk_index2][0].author+" "+\
                            " ".join(self.book_info_list[bk_index3][0].tags) 
        print("self.input_str\n",self.input_str)
        print("self.book_info_list\n",[i[0].title for i in self.book_info_list])
        #self.page = random.randint(0,1)
        self.page = 0
        yield

    def test_ok(self):
        code = self.auth.search_in_store(self.store_id, self.input_str, self.page)
        assert code == 200

    #测试找不到书的情况
    def test_no_(self):
        code = self.auth.search_in_store(self.store_id, "xxx", self.page)
        assert code != 200
