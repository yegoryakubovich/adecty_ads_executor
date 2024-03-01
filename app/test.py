import asyncio

from pyrogram import Client


async def start():
    client = Client(
        'lol',
        session_string='AgAAB_gABn4ZCosXClTBK1PjzAy6KogbzNhmw_LdUoKN5McWWqip_I9EnVFJ320Pq0M1i5Z1e6d5bvuVhs-6QtX4U_b3Qh5bUOxrO0mffjfZMTIjKzMPPKI8ftvetWPW1M7pFi4sxKTVv1BrrJ0BZO84M16A-FcDNDhKv9FYz0MAwGc9-mjbeCrD_TVs2kabzrqnH0FI9t0IghtAHo3KotdT0NosMTH2GXLYnguNVypZum_CSWOwtNS4BnVqZON6zJytdq3CSPvjCEexBISbNnyGxU_AWdrAzFdNwkhMUL2XqW1K98KBmDj1wLu5JDPElpzugul_aabv_N-iNF71QsU4c1AolwAAAAFEpfzaAA',
        proxy={
            "scheme": 'http',
            "hostname": '85.143.45.20', "port": 63272,
            "username": '18PSkbwQ', "password": 'ngPiajzG'
        },
    )
    await client.start()
    print(await client.get_users(user_ids='arthur_air'))
    await client.stop()


asyncio.run(start())
