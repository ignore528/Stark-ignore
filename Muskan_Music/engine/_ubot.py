# © @MuskanBot

from pyrogram import Client

import config

from .._logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="MuskanAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")

        if config.STRING1:
            await self.one.start()

            assistants.append(1)

            # Log Group notification
            if config.LOGGER_ID:
                try:
                    await self.one.send_message(
                        config.LOGGER_ID,
                        "Assistant Started ✅"
                    )
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"Assistant could not access the log Group. "
                        f"Skipping log notification: {e}"
                    )

            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username

            assistantids.append(self.one.id)

            LOGGER(__name__).info(
                f"Assistant Started as {self.one.name}"
            )

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")

        try:
            if config.STRING1:
                await self.one.stop()
        except Exception:
            pass
