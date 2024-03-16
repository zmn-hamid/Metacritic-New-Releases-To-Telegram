from config import BOT_TOKEN, CHAT_ID, NEW_RELEASES_FILENAME
from telegram.ext import Application
from telegram.ext import ContextTypes, Application
from Log import logger
from JSON_handler import CJSON
from AlbumOBJ import Album
from telegram.error import TelegramError


class TelgramHandler:
    def __init__(self) -> None:
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.job_queue = self.application.job_queue

    async def _send_album(self, context: ContextTypes.DEFAULT_TYPE):
        album: Album = context.job.data["album"]
        try:
            await context.bot.send_message(
                chat_id=CHAT_ID, text=f"{album.ARTIST} - {album.NAME}\n{album.URL}"
            )
            logger.info(f'sending "{album.ARTIST}" - "{album.NAME}"...')
        except TelegramError as e:
            logger.critical(f"TelegramError:{e}")

    def send_album(self, album: Album):
        self.job_queue.run_once(
            self._send_album,
            0,
            data={"album": album},
            job_kwargs={"misfire_grace_time": 15 * 60},
        )

    def run(self):
        self.application.run_polling()


thandler = TelgramHandler()
