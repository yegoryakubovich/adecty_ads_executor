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
from .personal import Personal
from .shop import Shop
from .tag import Tag

"""SECOND"""
from .proxy import Proxy, ProxyTypes, ProxyStates
from .session import Session, SessionStates
from .group_country import GroupCountry
from .group_tag import GroupTag
from .order_group import OrderGroup
from .country_link import CountryLink

"""THREE"""
from .sleep import Sleep, SleepStates
from .message import Message, MessageStates
from .session_group import SessionGroup
from .session_proxy import SessionProxy
from .session_task import SessionTask

all_models = (
    Account, Admin, Country, Group, Order, Shop, Tag, Personal,
    Proxy, Session, GroupCountry, GroupTag, OrderGroup, CountryLink,
    Sleep, Message, SessionGroup, SessionProxy, SessionTask,
)
