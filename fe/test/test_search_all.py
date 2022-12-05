import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
from fe.access import auth
from fe import conf
import uuid

import random


class TestSearchALL:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.input_str = "平凡的世界 小说 路遥"
        self.page = random.randint(1,2)
        yield

    def test_ok(self):
        code = self.auth.search_all(self.input_str, self.page)
        assert code == 200


