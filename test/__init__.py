import json
import os.path

data = []
result = []

for filename in os.listdir():
    if filename.split('.')[-1] != 'json':
        continue
    if filename == 'export.json':
        continue
    with open(filename, 'r', encoding="UTF-8") as f:
        json_file = json.load(f)
    if not json_file.get('app_version'):
        continue
    if not json_file.get('device'):
        continue
    if f"{json_file.get('app_version')}|{json_file.get('device')}" in data:
        continue
    data.append(f"{json_file.get('app_version')}|{json_file.get('device')}")
    result.append({'app_version': json_file.get('app_version'), 'device': json_file.get('device')})

with open('export.json', 'w', encoding="UTF-8") as f:
    json.dump(result, f)
