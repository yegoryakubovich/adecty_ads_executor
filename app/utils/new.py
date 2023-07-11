import json


class New:
    def __init__(self):
        self.proxy_file = "new/proxy.json"

    async def get_proxy(self):
        with open(f"{self.proxy_file}") as file:
            json_data = json.load(file)
        with open(f"{self.proxy_file}", 'w') as file:
            file.write("{}")

        return json_data


new = New()
