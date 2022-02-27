import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='./discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


mail = 'tefilorofi@hotmail.com'
password = 'Teoroca1998$'


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, **kwargs)

    async def on_ready(self):
        servers = list(self.servers)
        print('Logged on as {0}!'.format(self.user))
        print('Printing servers for {0}...'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print("Creando cliente discord...")
    dc = DiscordClient()
    dc.close()
    print('Cliente creado...')

    loop.run_until_complete(
        dc.login('SSayaxidM2sT29K4fZJPLcD4te2GqLgz'))
    loop.run_until_complete(dc.close())
