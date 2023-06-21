import requests

import repo
from models.proxies import ProxyStates, ProxyTypes


def check_proxy(proxy) -> bool:
    proxies = None
    if proxy.type == ProxyTypes.http:
        proxies = {
            'http': f"http://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}/"
        }
    elif proxy.type == ProxyTypes.socks5:
        proxies = {
            'http': f"socks5://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}/"
        }
    if proxies:
        r = requests.get("https://ya.ru", proxies=proxies)
        print(r.status_code)
        if r.status_code == 200:
            return True
    return False


def check_new_proxy():
    for proxy in repo.proxies.get_all_by_state(state=ProxyStates.wait):
        if not check_proxy(proxy):
            repo.proxies.move_state(proxy, ProxyStates.disable)
            continue
        repo.proxies.move_state(proxy, ProxyStates.enable)
