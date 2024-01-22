import asyncio

from pyrogram import Client


async def start():
    client = Client('lol',
                    session_string='BAAAB_gAW7rCChmyNXDDkl9vj2DeBlRQWvTUyzN4NKrc-pGXhIXYcW0vhcSYHFzGOQTRJJjclyr19oRSa_-1ViN73HjUyNZCRMCpgnWdN32FLMw3KysGNFDjIdHkzd8uYIM3fWgdao75MzhRW_vWPbWBYahtYqNzVyRZhy7FTkWkfK-p2HdyMIuWkPX0hYi1SyrIdyo-xAVcbTmK06AE7Vx3byeCoeuOCsCtP89EYw27jHkD71h9EInzxIK1rx7xJ2NdRfQhU_He1zToy5r_3-y_rMDAfJARH7tXn0fT2pa9T7o3kx-hvpIfUmd0b7-0vI_r0L_xDl9VCr3KggdgIejXJYPtcwAAAAGVSZKcAA')
    await client.start()
    print(await client.get_users(user_ids='arthur_air'))
    await client.stop()


asyncio.run(start())
