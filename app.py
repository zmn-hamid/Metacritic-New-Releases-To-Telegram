import datetime
import os
from typing import List
from urllib import request

import click
from bs4 import BeautifulSoup
from scripts.AlbumOBJ import Album
from scripts.JSON_handler import CJSON
from scripts.Log import logger
from scripts.Spotify_handler import shandler

from config import (
    HISTORY_FILENAME,
    READ_WEBPAGE_FROM_FILE,
    SAVE_TO_WEBPAGE_FILE,
    URL,
    WEBPAGE_FILE_NAME,
    SEND_TO_TELEGRAM,
)


class NewReleases:
    def __init__(self) -> None:
        self.albums: List[Album]
        self.history: list
        self.chosen_idx: int
        self.new_releases: list

    def _get_albums_from_metacritic(self):
        if READ_WEBPAGE_FROM_FILE:
            with open(WEBPAGE_FILE_NAME, "rb") as f:
                webpage = f.read()

        else:
            logger.debug("fetching from website")
            req = request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
            webpage = request.urlopen(req).read()

            if SAVE_TO_WEBPAGE_FILE:
                f = open(WEBPAGE_FILE_NAME, "wb")
                f.write(webpage)
                f.close()

        soup = BeautifulSoup(webpage, "html.parser")

        def _parse_text(text: str):
            """for large gaps in elements"""
            return " ".join(text.strip().split())

        def _parse_date(date: str):
            return str(
                datetime.datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
            )

        # main code
        self.albums: List[Album] = []
        for item in soup.select('td[class="clamp-summary-wrap"]'):
            # fetch data
            album_el = item.select('a[class="title"]')
            if not len(album_el):
                continue  # to avoid errors fetching the albums
            album_name = _parse_text(album_el[0].get_text())
            other_info = item.select('div[class="clamp-details"]')[0]
            artist_name = _parse_text(
                other_info.select('div[class="artist"]')[0]
                .get_text()
                .replace("by ", "")
            )
            date = _parse_date(_parse_text(other_info.select("span")[0].get_text()))

            # save to dict
            self.albums.append(Album(album_name, artist_name, date))

        self.albums = self.albums[:40]

        logger.debug("fetched albums from Metacritic")
        return self

    def _get_history(self):
        if not os.path.exists(HISTORY_FILENAME):
            CJSON.dumps([], HISTORY_FILENAME)
        self.history = CJSON.loads(HISTORY_FILENAME)

        logger.debug("fetched history")
        return self

    def _find_new_releases(self):
        # find the chosen_idx (is the last idx + 3 for any misplacement in the website)
        self.chosen_idx = 0
        for idx, album in enumerate(self.albums):
            for added_album in self.history:
                if Album.albums_equal(album, Album.to_album(**added_album)):
                    self.chosen_idx = idx
                    break
            else:
                continue
            break
        self.chosen_idx += 3

        # find out which ones are the new ones
        self.new_releases = []
        for album in self.albums[: self.chosen_idx][::-1]:
            appendable_album = album.to_appendable_dict()
            if appendable_album not in self.history:
                self.new_releases.insert(
                    0, {"album": album, "appendable_album": appendable_album}
                )

        logger.debug("calculated new releases")
        return self

    def save_to_history(self):
        if self.new_releases:
            for new_release in self.new_releases:
                self.history.insert(0, new_release["appendable_album"])

            CJSON.dumps(self.history, HISTORY_FILENAME)
            logger.info("saved new releases to history")
        else:
            logger.info("no new releases to save to history")
        return self

    def get_new_releases(self):
        """returns a list of dicts with keys: `album` and `appendable_album`"""
        self._get_albums_from_metacritic()
        self._get_history()
        self._find_new_releases()
        if not self.new_releases:
            logger.info("no new releases")
        return self.new_releases


if SEND_TO_TELEGRAM:
    from scripts.Telegram_handler import thandler
new_rls_obj = NewReleases()
new_releases = new_rls_obj.get_new_releases()
if new_releases:
    for new_release in new_releases:
        album: Album = new_release["album"]
        if SEND_TO_TELEGRAM:
            logger.debug(f'"{album.NAME}" by "{album.ARTIST}"... ')

            # get the url
            spot_album = shandler.get_album_by_info(album)
            if not spot_album.URL:
                logger.warning(
                    f'couldnt find album in Spotify : "{album.NAME}" by "{album.ARTIST}"'
                )
            logger.debug("got url... ")

            # send the url
            thandler.add_album_to_queue(album=spot_album)
            logger.debug("added message job.")
        else:
            print(f"{album.ARTIST} - {album.NAME}")

    if SEND_TO_TELEGRAM:
        logger.debug("sending messages...")
        thandler.run()

if SEND_TO_TELEGRAM:
    try:
        thandler.run()
    except:
        pass

if new_releases and click.confirm("Save the updates"):
    new_rls_obj.save_to_history()
