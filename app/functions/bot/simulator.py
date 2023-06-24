from pyrogram import Client


class SimulatorAction:
    def __init__(self, client: Client):
        self.client: Client = client
