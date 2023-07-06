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


MAX_SESSION2ONE_PROXY = 3
NEW_SESSION_SLEEP_SEC = min2sec(1)
DAY_OLD = 5
URL_FOR_TEST_PROXY = 'https://ifconfig.me/all.json'
BOT_SLEEP_MIN_SEC = min2sec(0)  # sleep min
BOT_SLEEP_MAX_SEC = min2sec(1)  # sleep max
ASSISTANT_SLEEP_SEC = min2sec(1)  # assistant sleep
SEND_MSG_DELAY_MSG = 3  # msg delay
SEND_MSG_DELAY_SEC = min2sec(10)  # msg delay
