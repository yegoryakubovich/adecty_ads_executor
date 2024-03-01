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


from .answers import Answer
from .countries import Country
from .devices import Device
from .groups import Group, GroupStates, GroupType, GroupCaptionType
from .orders import Order, OrderStates, OrderTypes
from .ours_groups import OurGroup, OurGroupStates
from .personals import Personal, PersonalTypes, PersonalSex
from .settings import Setting, SettingTypes
from .shops import Shop
from .users import User

from .countries_links import CountryLink
from .proxies import Proxy, ProxyTypes, ProxyStates
from .sessions import Session, SessionStates

from .groups_countries import GroupCountry
from .messages import Message, MessageStates
from .orders_attachments import OrderAttachment, OrderAttachmentTypes
from .orders_groups import OrderGroup
from .orders_personals import OrderPersonal
from .orders_users import OrderUser, OrderUserStates
from .sessions_devices import SessionDevice
from .sessions_groups import SessionGroup, SessionGroupState
from .sessions_links import SessionLink
from .sessions_orders import SessionOrder
from .sessions_ours_groups import SessionOurGroup
from .sessions_personals import SessionPersonal
from .sessions_proxies import SessionProxy
from .sessions_tasks import SessionTask, SessionTaskStates, SessionTaskType
from .sleeps import Sleep, SleepStates


all_models = (
    Answer, Country, Device, Group, Order, OurGroup, Personal, Setting, Shop, User,
    CountryLink, Proxy, Session,
    GroupCountry, Message, OrderAttachment, OrderGroup, OrderPersonal, OrderUser, SessionDevice, SessionGroup,
    SessionLink, SessionOrder, SessionOurGroup,  SessionPersonal, SessionProxy, SessionTask, Sleep,
)
