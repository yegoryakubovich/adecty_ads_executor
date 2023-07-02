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

def min2sec(minutes: int):
    return minutes * 60


def hour2sec(hours: int):
    return min2sec(hours * 60)


NEW_PROXY_FILE = "new/proxy.txt"
SESSIONS_DIR = 'sessions'
NEW_SESSION_DIR = f"{SESSIONS_DIR}/wait"
MAX_SESSION2ONE_PROXY = 1
DAY_OLD = 5
URL_FOR_TEST_PROXY = 'https://ifconfig.me/all.json'
BOT_SLEEP_MIN_SEC = min2sec(1)  # sleep min
BOT_SLEEP_MAX_SEC = min2sec(2)  # sleep max
SEND_MSG_DELAY_MSG = 30  # msg delay
ASSISTANT_SLEEP_SEC = min2sec(1)  # assistant sleep

groups_list = ["@kekajangroup"]  # "adaptaciyausa", "adaptaciya_ua_usa"]
# "ads_new_york", "calosangeles", "ca_miami_chat", "chatamerika",
# "chatinnj", "chatinSeattle", "chatinsf", "chatnewyork1", "chchatua", "chicagoil", "la_services",
# "losangeles2021immigrants", "los_angeles_avito", "los_angeles_ca", "los_angeles_california_usa",
# "miamichatik", "miamichatru", "movingsf", "multinational_group", "nashaphiladelphia", "nashlosangeles",
# "nashmiami", "nashny", "newyorkchatru", "nyjobsusa", "philadelphiachat", "phillychat", "russianlo",
# "sacramentocity", "telemarketus", "ukrnewyorkgroup", "usachatru", "usaforuz", "usagreen", "usarmenians",
# "usa_360", "usb_mexico_usa", "uzbeksinusalup", "vatandoshimuzbus", "vatandoshim_usa_50_state",
# "vatandoshim_uz", "vatandoshimusa", "yagonadarchausany", "nomadsfamilyusa", "kg_america", "nashchicago",
# "nomadschicago", "sfnomad", "mahallanewyorkjobs", "nomadssd", "mexicousa21", "newyorknash1",
# "rentcarnomad", "rusoenmexico", "workersnomads", "ads_california", "america_new_york",
# "canada_work_life", "creditmebel908203131", "dogbanusa", "freeshipping", "horizont24", "housingnomad",
# "jobinmoving", "jobs_usa24", "jobsinny", "la_california", "liveintheusa", "mextous", "miamihotchat",
# "nomadsboston", "nomadsmiami", "nomadsdc", "nomadsfamily", "poputchiki_usa", "rent_miami_rusrek",
# "russianclassifieds", "teachbkusa", "trucker_cargo", "usa_benefit", "usa_exchange", "usa_job_help",
# "usa_job_helper", "usamexico", "used21cars", "biznesdvigusa", "miamiarea", "newyorkchat24",
# "newyork_job", "vhi7f", "mayami_360", "nomadsfamilyla", "nyjobs_usa", "in_miami"]

proxies_list = ["zrZ1na:vzSPV8@38.170.95.174:9504", "zrZ1na:vzSPV8@38.153.57.132:9851", "zrZna:vzSPV8@38.12.57.11:9851",
                "zrZ1na:vzSPV8@38.170.95.62:9805", "zrZ1na:vzSPV8@38.170.243.82:9329", "zrZ1na:vzSPV8@38.170.95.7:9460"]

strings = {
    "573213524152": {"phone": "573213524152", "user_id": 5619122397,
                     "string_session": "AQAAB_gAik9fS8Hf3Ubk7_FfHMKaXzGX2BnISq3OZHp2xwFBhAE33Lj9VGNvBB4uirpwZDEWRglrQF6pNDhfZNNUJLcdp5RAklOF6qdIhnBKgnwAAvjg1iSEtNdEC2ClxHZAIMstCgcEnrnxtieEn3fYGVss12quMdzIwmheUnWaNGiHpLc-4jXrVHmW9DCIUI8j4CyN8sqYEf8IS8EAT2grLPwSemT3tRwfD1wmGi8l5ZsmBpu8nikMaGYHILxJltuPJfinTFzRX231sk2gAFiR8KZIOob83eDFwT2T6Vn9cLtF_ReGyA5cCOP4tlNZxydaXr1D0DwdbVOsVqpMvFdP_VR-HwAAAAFO7QDdAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.2 x64", "system_version": "Windows 11"},
    "573213815626": {"phone": "573213815626", "user_id": 6067370896,
                     "string_session": "AQAAB_gAk9dBnBQzGHb7f6NHE0G0wdKPhhJMod1jhZ4khtryRuhNffhgtFZXhfLi2rurkbtgiP-d4m25UTGq1vi72TR9yw3u9xmKeOEudAaZYJonY5fhyzcpeMajgUxfjA3OnIDVM3cU-N78w6es5Eir9V2QcctA0Mj4OSkkSgf3k1vLcwTl_0-yvswlfGBI60aIsIRlLkQb6oVK06BtTjtast0NynS_3ZQmsAtmwUgYwJOgdLVMTSFGDW9q6mpRcjRBh4Tzocj0k2RqWoQ4ioKExbDQuI9YV1ZnaC9qkjAOLRJc28tbxpL1sOCT4eyKae1D_-d5cxsLAoKyKolzIy4B7rq3twAAAAFppLuQAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.3 x64", "system_version": "Windows 11"},
    "573214578014": {"phone": "573214578014", "user_id": 6235508623,
                     "string_session": "AQAAB_gAkz1jBBy8fSksA1mtZMlNN0hiG4-hf6xenhzKgQgjxhan494tXm-Cx-6zB1aPVsEeyg180vOYjTbSXvbilMbglGKrm8evFQ-8ZMFE7AEF1pPhG5lc9WJ84ssUMAEjmSKnTBIXj-J2nz6MRb75gpugKnxVqC8THeqnpIxhjjum7kCuCnDni-QamxNAckeA1Jl_UcTVRLRbupS797wkpKFPTnEPVR_omy5HJhRzsCD8pmitFWl_DXmvyilPViUNaCGuLqNTWerdcphkPKMDBdYpB99AtUSLZr0s0452wIrbyHXxzLMlx0Oye93wdzn7wN9g6oindcV0VWuS80G4UYTe1AAAAAFzqk-PAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.2 x64", "system_version": "Windows 10"}
}
