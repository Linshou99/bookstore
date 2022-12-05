import requests
from urllib.parse import urljoin


class Auth:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "auth/")#"http://127.0.0.1:5000/auth/"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str):
        json = {"user_id": user_id, "password": password, "terminal": terminal}
        url = urljoin(self.url_prefix, "login")#"http://127.0.0.1:5000/auth/login"，测试在 be/view/auth.py 文件中的访问后端接口的函数 /login
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("token")

    def register(
        self,
        user_id: str,
        password: str
    ) -> int:
        json = {
            "user_id": user_id,
            "password": password
        }
        url = urljoin(self.url_prefix, "register")
        r = requests.post(url, json=json)
        return r.status_code

    def password(self, user_id: str, old_password: str, new_password: str) -> int:
        json = {
            "user_id": user_id,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        url = urljoin(self.url_prefix, "password")
        r = requests.post(url, json=json)
        return r.status_code

    def logout(self, user_id: str, token: str) -> int:
        json = {"user_id": user_id}
        headers = {"token": token}
        url = urljoin(self.url_prefix, "logout")
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def unregister(self, user_id: str, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "unregister")
        r = requests.post(url, json=json)
        return r.status_code

    def search_all(self, input_str: str, page: int) -> int:
        json = {"input_str": input_str, "page": page}
        url = urljoin(self.url_prefix, "search_all")
        r = requests.post(url, json=json)
        return r.status_code

    def search_in_store(self, store_id: str, input_str: str, page: int) -> int:
        json = {"store_id": store_id, "input_str": input_str, "page": page}
        url = urljoin(self.url_prefix, "search_in_store")
        r = requests.post(url, json=json)
        return r.status_code
