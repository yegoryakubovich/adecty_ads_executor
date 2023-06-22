import requests
from loguru import logger

from database import repo
from database.models import ProxyTypes, ProxyStates


def check_proxy(proxy) -> bool:
    proxies = None
    logger.info(proxy.id)
    if proxy.type == ProxyTypes.socks5:
        proxies = {
            'http': f'socks5://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
            'https': f'socks5://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
        }
    elif proxy.type == ProxyTypes.http:
        proxies = {
            'http': f'https://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
            'https': f'https://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
        }
    if proxies:
        try:
            r = requests.get("https://ifconfig.me/all.json", proxies=proxies, timeout=5)
            if r.status_code == 200:
                return True
        except:
            pass
    return False


def check_new_proxy():
    for proxy in repo.proxies.get_all_by_state(state=ProxyStates.wait):
        if not check_proxy(proxy):
            repo.proxies.move_state(proxy, ProxyStates.disable)
            continue
        repo.proxies.move_state(proxy, ProxyStates.enable)
