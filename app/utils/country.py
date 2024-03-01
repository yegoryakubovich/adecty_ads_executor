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


import httpx
import phonenumbers
import pycountry as pycountry


class CountryType:
    code: str
    name: str

    def __init__(self, code: str, name: str):
        self.code, self.name = code, name


def get_by_phone(phone: str) -> CountryType:
    number = phonenumbers.parse(f"+{phone}")
    code = phonenumbers.region_code_for_number(number)
    return CountryType(code=code, name=pycountry.countries.get(alpha_2=code).name)


def get_by_ip(ip: str) -> CountryType:
    response = httpx.get(f"http://ip-api.com/json/{ip}")
    code = response.json()['countryCode']
    return CountryType(code=code, name=pycountry.countries.get(alpha_2=code).name)


def get_by_code(code: str) -> CountryType:
    return CountryType(code=code, name=pycountry.countries.get(alpha_2=code).name)
