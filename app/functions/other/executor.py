from database import repo
from database.models import Proxy, ProxyStates, Shop, Session
from functions.base_executor import BaseExecutorAction


class AssistantExecutorAction(BaseExecutorAction):

    async def proxy_disable(self, proxy: Proxy):
        proxy_shop: Shop = repo.shops.get(proxy.shop_id)
        for sp in repo.sessions_proxies.get_all(proxy=proxy):
            repo.sessions_proxies.remove(sp.id)
        repo.proxies.update(proxy, state=ProxyStates.disable)

        await self.proxy_disable_log(proxy_id=proxy.id, proxy_shop_id=proxy_shop.id, proxy_shop_name=proxy_shop.name)

    async def proxy_new(self, session: Session):
        proxy_shop: Shop = repo.shops.get(proxy.shop_id)
        for sp in repo.sessions_proxies.get_all(proxy=proxy):
            repo.sessions_proxies.remove(sp.id)
        repo.proxies.update(proxy, state=ProxyStates.disable)

        await self.proxy_disable_log(proxy_id=proxy.id, proxy_shop_id=proxy_shop.id, proxy_shop_name=proxy_shop.name)
