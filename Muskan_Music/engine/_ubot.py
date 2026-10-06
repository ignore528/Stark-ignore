# © @MuskanBot

from pyrogram import Client

import config

from .._logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="MuskanAss",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistant...")

        if config.STRING:
            await self.one.start()

            assistants.append(1)

            try:
                await self.one.send_message(
                    config.LOGGER_ID,
                    "Assistant Started ✅"
                )
            except:
                LOGGER(__name__).error(
                    "Assistant has failed to access the log Group. "
                    "Make sure that you have added your assistant "
                    "to your log group and promoted as admin!"
                )
                exit()

            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username

            assistantids.append(self.one.id)

            LOGGER(__name__).info(
                f"Assistant Started as {self.one.name}"
            )

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistant...")

        try:
            if config.STRING:
                await self.one.stop()
        except:
            pass
