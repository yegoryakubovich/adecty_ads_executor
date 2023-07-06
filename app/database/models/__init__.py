#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""FIRST"""
from .account import Account
from .admin import Admin
from .country import Country
from .group import Group, GroupStates
from .order import Order, OrderStates
from .shop import Shop, ShopTypes
from .tag import Tag

"""SECOND"""
from .proxy import Proxy, ProxyTypes, ProxyStates
from .session import Session, SessionStates

"""THREE"""
from .message import Message, MessageStates
from .group_country import GroupCountry
from .group_tag import GroupTag
from .order_group import OrderGroup
from .session_group import SessionGroup
from .session_proxy import SessionProxy
from .session_task import SessionTask

__all__ = (
    # Main
    Account, Admin, Country, Tag, Order, Shop,

    # Proxies
    Proxy,

    # Groups
    Group, GroupCountry, GroupTag,

    # Sessions
    Session,

    # Messages
    Message,

    # States
    SessionGroup, SessionProxy, OrderGroup
)

all_models = (
    Account,
    Admin,
    Country,
    Tag,
    Order,
    Shop,
    Proxy,
    Group,
    GroupTag,
    Session,
    Message,
    GroupCountry,
    SessionGroup,
    SessionProxy,
    SessionTask,
    OrderGroup,
)
