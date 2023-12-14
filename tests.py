import asyncio

from pyrogram import Client

a = "BAAAB_gAB27M8u3knIVt1Irs7G1m_xBYSHSjUCT5ZdXlF03uMFpaHCbsWAZlqrkRk2Fv92X4dAlw8ahmBZ9FCHR78WUqV8_3aH5Nk7KfKxOr6ZPLjZLtbdaRmhqz0bXk0qtf5eJbuO65OuPji40hIhKf4VazZIkD8ypza6mC-IZ20AXckIenGOUh6VL5VmU_qgotlY_il2R-3A4EuPWpFmX673jtYbNKKTLczSpZpjzPOUfn1hGAfEBMIH2OvxbRmjy7Nl87exB4m-_JfPzv_SKP1YDoKmJ460aLotut5u625Fldmk6iww1WVLEnDB2IzXLs39bEZG5pQcGCVMJ1cdVJWK0_9QAAAAGdhJToAA"
telegram_id = 6847771178


async def main(client):
    @client.on_message()
    async def on_message(client, message):
        print(message.text)
    await client.start()
    print(await client.get_messages(chat_id="newyorkeusa", message_ids=19399))
    await client.send_message(chat_id="arthur_air", text="РАБОТАЕТ")


client = Client("LOL", session_string=a)
loop = asyncio.get_event_loop()
loop.run_until_complete(main(client))
loop.run_forever()
