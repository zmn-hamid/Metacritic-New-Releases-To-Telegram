from scripts.AlbumOBJ import Album
from scripts.JSON_handler import CJSON
from scripts.Log import logger
from telegram.error import TelegramError
from telegram.ext import Application, ContextTypes, ApplicationBuilder

from config import BOT_TOKEN, CHAT_ID


class TelgramHandler:
    def __init__(self) -> None:
        self.application = ApplicationBuilder().token(BOT_TOKEN).build()
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

    def add_album_to_queue(self, album: Album):
        self.job_queue.run_once(
            self._send_album,
            0,
            data={"album": album},
            job_kwargs={"misfire_grace_time": 15 * 60},
        )

    def run(self):
        self.application.run_polling()


thandler = TelgramHandler()
