from random import randint
from typing import List

import socks

import repo
from core.constants import proxies_list
from db.session import SessionLocal
from models import Proxy
from models.proxies import ProxyTypes, ProxyStates

model = Proxy


class ProxyRepository:
    def __init__(self):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal

    def add_new_proxy(self, ):
        for item in proxies_list:
            item_data = item.split("@")
            with self.get_session():
                self.model.get_or_create(
                    type="socks5", host=item_data[1].split(':')[0], port=item_data[1].split(':')[1],
                    user=item_data[0].split(':')[0], password=item_data[0].split(':')[1], country=repo.countries.get(1)
                )

    def get_count(self) -> int:
        with self.get_session():
            result = self.model.select().count()
        return result

    def get(self, id: int) -> model:
        with self.get_session():
            result = self.model.get_by_id(id)
        return result

    def get_all_by_state(self, state: ProxyStates) -> List[model]:
        with self.get_session():
            result = self.model.select().filter(state=state).execute()
        return result

    def get_all(self) -> List[model]:
        with self.get_session():
            result = self.model.select().execute()
        return result

    def get_dict(self, proxy_id: int) -> tuple:
        proxy = self.get(proxy_id)
        result = (
            socks.HTTP if proxy.type == ProxyTypes.http else socks.SOCKS5,
            proxy.host, proxy.port, proxy.user, proxy.password
        )
        return result

    def get_random_dict(self):
        return self.get_dict(randint(1, self.get_count()))

    def move_state(self, proxy: Proxy, state: ProxyStates):
        with self.get_session():
            proxy.state = state
            proxy.save()


proxies = ProxyRepository()
