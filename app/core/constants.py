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
from database.models import GroupType, OrderAttachmentTypes


def min2sec(minutes: int):
    return minutes * 60


def hour2sec(hours: int):
    return min2sec(hours * 60)


NEW_SESSION_SLEEP_SEC = min2sec(120)
URL_FOR_TEST_PROXY = 'https://ifconfig.me/all.json'
avatar_path = 'media/bot/personals/avatars/'

BOT_SLEEP_MIN_SEC = min2sec(10)  # sleep min
BOT_SLEEP_MAX_SEC = min2sec(15)  # sleep max
BOT_SLEEP_ANSWER_SEC = min2sec(2)  # sleep max
ASSISTANT_SLEEP_SEC = min2sec(15)  # assistant sleep
ASSISTANT_RARELY_SLEEP_SEC = min2sec(60)  # assistant sleep
ASSISTANT_OFTEN_SLEEP_SEC = min2sec(15)  # assistant sleep
MAX_TASKS_COUNT = 10  # max count tasks by one session

SEND_MSG_DELAY_MSG = 30  # msg delay
SEND_MSG_DELAY_SEC = min2sec(10)  # msg delay

KEY_WORDS = ["Обмен", "Обменник"]

GROUPS_ORDERS_TEXT_TYPES = {
    GroupType.link: OrderAttachmentTypes.text_common,
    GroupType.no_link: OrderAttachmentTypes.text_no_link,
    GroupType.short: OrderAttachmentTypes.text_short,
    GroupType.replace: OrderAttachmentTypes.text_short
}

LATTERS = {
    "А": ["A", "丹", "a"], "Б": ["石", "右", "五"], "В": ["B", "归", "乃", "日"], "Г": ["厂", "广"], "Д": ["亼"],
    "Е": ["E", "e", "仨"], "Ё": [], "Ж": ["兴", "米"], "З": ["3", "乡"], "И": ["U", "u"], "Й": [],
    "К": ["K", "k", "长"], "Л": ["几", "人", "入"], "М": ["M", "m", "从"], "Н": ["H", "廾", "卄"],
    "О": ["O", "o", "口"], "П": ["冂", "穴"], "Р": ["P", "p", "卩", "户", "尸"], "С": ["C", "c", "匚", "亡"],
    "Т": ["T", "丅", "丁"], "У": ["Y", "y", "丫"], "Ф": ["中"], "Х": ["X", "x", "乂"], "Ц": ["凵"], "Ч": ["4", "丩"],
    "Ш": ["山", "山"], "Щ": ["山", "山"], "Ъ": [], "Ы": [], "Ь": [], "Э": ["彐"], "Ю": [], "Я": ["牙", "兑"],

    "A": ["А", "а", "丹"], "B": ["В", "в", "归", "乃", "日"], "C": ["С", "с", "匚", "亡"], "D": [],
    "E": ["Е", "е", "仨"], "F": [], "G": [], "H": ["Н", "н", "廾", "卄"], "I": ["丨", "工", "1"], "J": ["亅"],
    "K": ["К", "к", "长"], "L": ["乚"], "M": ["М", "м", "从"], "N": [], "O": ["О", "о", "口"],
    "P": ["Р", "р", "卩", "户", "尸"], "Q": [], "R": ["尺"], "S": [], "T": ["Т", "т", "丅", "丁"],
    "U": ["И", "и", "凵"], "V": [], "W": ["山"], "X": ["Х", "х", "乂"], "Y": ["У", "у", "丫"], "Z": ["乙"],

}

SPAM_REPLY_ANSWERS = {
    "[['OK'], ['What is spam?'], ['I was wrong, please release me'], ['This is a mistake']]": "This is a mistake",
    "[['Yes'], ['No']]": "Yes",
    "[['No! Never did that!'], ['Well… In fact I did.']]": "No! Never did that!",
    "[['Cool, thanks'], ['But I can’t message non-contacts!']]": "Cool, thanks"
}

SPAM_MESSAGE_ANSWERS = {
    "Great! I’m very sorry if your account was limited by mistake. "
    "Please write me some details about your case, "
    "I will forward it to the supervisor. "
    "Why do you think your account was limited, what went wrong?": "An error occurred, I did not do such actions. "
                                                                   "Unblock me.",
    "Thank you! Your complaint has been successfully submitted. "
    "Our team’s supervisors will check it as soon as possible. "
    "If this was a mistake, all limitations will be lifted from your account soon.": "/start"

}

SPAM_STOP_MESSAGE = [
    "You've already submitted a complaint recently. "
    "Our team’s supervisors will check it as soon as possible. "
    "Thank you for your patience.",
]
SPAM_FREE_MESSAGE = [
    "Good news, no limits are currently applied to your account. You’re free as a bird!",
]
