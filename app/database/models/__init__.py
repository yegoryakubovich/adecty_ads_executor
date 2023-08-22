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
from .country import Country
from .group import Group, GroupStates, GroupType
from .order import Order, OrderStates, OrderTypes
from .personal import Personal, PersonalTypes, PersonalSex
from .shop import Shop
from .user import User

"""SECOND"""
from .proxy import Proxy, ProxyTypes, ProxyStates
from .sessions import Session, SessionStates
from .group_country import GroupCountry
from .order_group import OrderGroup
from .country_link import CountryLink

"""THREE"""
from .sleep import Sleep, SleepStates
from .message import Message, MessageStates
from .session_group import SessionGroup, SessionGroupState
from .session_proxy import SessionProxy
from .session_task import SessionTask, SessionTaskStates, SessionTaskType
from .sessions_personals import SessionPersonal

all_models = (
    Country, Group, Order, Personal, Shop, User,
    Proxy, Session, GroupCountry, OrderGroup, CountryLink,
    Sleep, Message, SessionGroup, SessionProxy, SessionTask, SessionPersonal
)
