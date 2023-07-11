import base64
import json
import os
import struct
from datetime import datetime

from peewee import SqliteDatabase, Model, IntegerField, TextField, BlobField
from pyrogram.storage import Storage


class Converter:
    def __init__(self):
        self.okay = None
        self.export_dir, self.input_dir = "export/", "new/session/"
        self.result_data, self.global_data = {}, {}
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

        class UpdateState(Model):
            id = IntegerField(primary_key=True)
            date = IntegerField()

            class Meta:
                db_table = 'update_state'
                database = local_db

        with local_db:
            db_ts: TelethonSessions = TelethonSessions.select().execute()[0]
            db_us: UpdateState = UpdateState.select().execute()[0]
        self.result_data['dc_id'] = db_ts.dc_id
        self.result_data['auth_key'] = db_ts.auth_key
        self.result_data['date'] = db_us.date

    def get_json_data(self, json_data: json):
        self.result_data['phone'] = json_data['phone']
        self.result_data['user_id'] = json_data['user_id']
        self.result_data['api_id'] = json_data['app_id']
        self.result_data['api_hash'] = json_data['app_hash']

    def get_data(self, filename: str):
        self.result_data = {}
        with open(f"{self.input_dir}{filename}.json") as file:
            json_data = json.load(file)
        self.get_json_data(json_data)
        local_db = SqliteDatabase(f'{self.input_dir}{filename}.session')
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
        for filename in os.listdir(self.input_dir):
            if len(filename.split('.')) > 2:
                os.remove(f"{self.input_dir}{filename}")
                continue
            if filename.split('.')[-1] == 'json':
                continue

            self.get_data(filename.split('.')[0])
            self.export_data()
            os.remove(f"{self.input_dir}{filename.split('.')[0]}.session")
            os.remove(f"{self.input_dir}{filename.split('.')[0]}.json")
        return self.global_data


convert = Converter()
