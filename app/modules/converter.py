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
import json
import os
import shutil
import struct
from datetime import datetime

from loguru import logger
from peewee import SqliteDatabase, Model, IntegerField, TextField, BlobField
from pyrogram.storage import Storage


class Converter:
    def __init__(self):
        self.okay = None
        self.export_dir, self.input_dir = "export", "new/session"
        self.result_data, self.global_data, self.result = {}, {}, []
        self.export_file = f"{datetime.utcnow().strftime('%d.%m.%Y_%H.%M')}.json"

    """INPUT"""

    def get_database_data(self, local_db):
        class TelethonSessions(Model):
            dc_id = IntegerField(primary_key=True)
            server_address = TextField()
            port = IntegerField()
            auth_key = BlobField()
            takeout_id = IntegerField()

            class Meta:
                db_table = 'sessions'
                database = local_db

        with local_db:
            db_ts: TelethonSessions = TelethonSessions.select().execute()[0]
        self.result_data['dc_id'] = db_ts.dc_id
        self.result_data['auth_key'] = db_ts.auth_key

    def get_json_data(self, json_data: json):
        self.result_data['phone'] = json_data['phone']
        self.result_data['user_id'] = json_data['user_id']
        self.result_data['api_id'] = json_data['app_id']
        self.result_data['api_hash'] = json_data['app_hash']
        self.result_data['date'] = json_data['register_time']

    def get_data(self, file_dir: str, filename: str):
        self.result_data = {}
        with open(f"{file_dir}/{filename}.json") as file:
            json_data = json.load(file)
        self.get_json_data(json_data)
        local_db = SqliteDatabase(f'{file_dir}/{filename}.session')
        self.get_database_data(local_db)

    """EXPORT"""

    def export_data(self):
        packed = struct.pack(
            Storage.SESSION_STRING_FORMAT, self.result_data['dc_id'], self.result_data['api_id'], 0,
            self.result_data['auth_key'], self.result_data['user_id'], 0
        )

        self.global_data[f"{self.result_data['phone']}"] = {
            'phone': self.result_data["phone"], 'user_id': self.result_data["user_id"],
            "string_session": base64.urlsafe_b64encode(packed).decode().rstrip("="),
            "api_id": self.result_data['api_id'], "api_hash": self.result_data['api_hash'],
        }

    def start(self):
        self.result = []
        for shop_name in os.listdir(self.input_dir):
            logger.info(shop_name)
            self.global_data, self.result_data = {}, {}
            shop_dir = f"{self.input_dir}/{shop_name}"
            for file_name in os.listdir(shop_dir):
                logger.info(file_name)
                file_dir = f"{shop_dir}/{file_name}"
                for file in os.listdir(file_dir):
                    logger.info(file)
                    if file.split('.')[-1] == 'json':
                        continue
                    elif file.split('.')[-1] == 'session':
                        self.get_data(file_dir, file.split('.')[0])
                        self.export_data()
                    os.remove(f"{file_dir}/{file.split('.')[0]}.session")
                    os.remove(f"{file_dir}/{file.split('.')[0]}.json")
                shutil.rmtree(file_dir)
            self.result.append({"shop_name": shop_name, "items": self.global_data})
            self.global_data = {}
            shutil.rmtree(shop_dir)
        return self.result


convert = Converter()
