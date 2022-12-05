import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid

import time


class TestAutoCancelOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_auto_cancel_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_auto_cancel_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_auto_cancel_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.buyer_id
        self.wait_time = 10#10s后自动取消订单
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

    def test_ok_overtime(self):
        code, self.order_id = self.buyer.new_order(self.store_id, self.buy_book_id_list)
        assert code == 200
        time.sleep(self.wait_time+1)
        code = self.buyer.is_order_cancelled(self.order_id)
        assert code == 200

    #在自动取消前，订单已经被买家取消
    def test_ok_not_overtime_cancel_by_buyer(self):
        code, self.order_id = self.buyer.new_order(self.store_id, self.buy_book_id_list)
        assert code == 200
        code = self.buyer.cancel_order(self.buyer_id, self.order_id)
        assert code == 200
        time.sleep(self.wait_time+1)
        code = self.buyer.is_order_cancelled(self.order_id)
        assert code == 200

    #在自动取消前，订单已付款(不在已取消订单中)
    def test_ok_not_overtime_paid(self):
        code, self.order_id = self.buyer.new_order(self.store_id, self.buy_book_id_list)
        assert code == 200
        code = self.buyer.payment(self.order_id)
        assert code == 200
        time.sleep(self.wait_time+1)
        code = self.buyer.is_order_cancelled(self.order_id)
        assert code != 200
