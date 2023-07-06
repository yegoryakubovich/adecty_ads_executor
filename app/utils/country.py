import phonenumbers
import pycountry as pycountry
import requests


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
    response = requests.get(f"http://ip-api.com/json/{ip}")
    code = response.json()['countryCode']
    return CountryType(code=code, name=pycountry.countries.get(alpha_2=code).name)


def get_by_code(code: str) -> CountryType:
    return CountryType(code=code, name=pycountry.countries.get(alpha_2=code).name)
