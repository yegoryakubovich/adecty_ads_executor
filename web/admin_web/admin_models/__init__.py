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
def registration_load():
    from . import SessionAdmin, UserAdmin, GroupAdmin, OrderAdmin, ProxyAdmin, PersonalAdmin
    from . import SessionTaskAdmin, MessageAdmin, SleepAdmin, ShopAdmin, CounryAdmin

    """addon"""
    from . import SessionProxyAdmin, SessionGroupAdmin, SessionPersonalAdmin, SessionOrderAdmin
    from . import GroupCountryAdmin
    from . import OrderGroupAdmin, OrderPersonalAdmin, OrderUserAdmin
    from . import CountryLinkAdmin


max_rows = 10
max_rows_inline = 50
