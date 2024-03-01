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


import base64
import os
import shutil
import struct

from loguru import logger
from opentele.td import TDesktop
from pyrogram.storage import Storage


class TdataConverter:
    result: list
    input_dir = "new/tdata_session"
    results = []
    global_data = {}

    def convert(self, tdata_path: str, filename: str, name: str):
        tdesk = TDesktop(f"{tdata_path}/{filename}")
        assert tdesk.isLoaded()
        packed = struct.pack(
            Storage.SESSION_STRING_FORMAT, tdesk.mainAccount.authKey.dcId,
            tdesk.mainAccount.api.api_id, 0, tdesk.mainAccount.authKey.key, tdesk.mainAccount.UserId, 0
        )
        _str = base64.urlsafe_b64encode(packed).decode().rstrip("=")

        self.global_data[f"{name}"] = {
            'session_name': name, 'api_id': tdesk.mainAccount.api.api_id, 'api_hash': tdesk.mainAccount.api.api_hash,
            'user_id': tdesk.mainAccount.UserId, 'string': _str
        }
        print(self.global_data)

    def start(self):
        self.results = []
        for shop_name in os.listdir(self.input_dir):
            logger.info(shop_name)
            self.global_data = {}
            shop_dir = f"{self.input_dir}/{shop_name}"
            for file_name in os.listdir(shop_dir):
                logger.info(file_name)
                file_dir = f"{shop_dir}/{file_name}"
                for file in os.listdir(file_dir):
                    if file == 'tdata':
                        self.convert(file_dir, file, file_name)
                        shutil.rmtree(f"{file_dir}/{file}")
                    else:
                        os.remove(f"{file_dir}/{file}")
                shutil.rmtree(file_dir)
            self.results.append({"shop_name": shop_name, "items": self.global_data})
            self.global_data = {}
            shutil.rmtree(shop_dir)
        return self.results


tdata_converter = TdataConverter()
