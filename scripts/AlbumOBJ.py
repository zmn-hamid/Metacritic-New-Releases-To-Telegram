import datetime
from typing import Type


class Album:
    NAME: str
    ARTIST: str
    DATE: str
    URL: str

    def __init__(
        self, name: str, artist: str, date: datetime.datetime, url: str = None
    ) -> None:
        self.NAME = name
        self.ARTIST = artist
        self.DATE = date
        self.URL = url

    def to_appendable_dict(self):
        """is used to save the album. no url needed to save"""
        return {
            "name": self.NAME,
            "artist": self.ARTIST,
            "date": (
                str(self.DATE.strftime("%Y-%m-%d"))
                if type(self.DATE) != str
                else self.DATE
            ),
        }

    @staticmethod
    def to_album(*args, **kwargs):
        return Album(*args, **kwargs)

    @staticmethod
    def albums_equal(album_1: Type["Album"], album_2: Type["Album"]):
        return (
            album_1.NAME == album_2.NAME
            and album_1.ARTIST == album_2.ARTIST
            and album_1.DATE == album_2.DATE
        )
