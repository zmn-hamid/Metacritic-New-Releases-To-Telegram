import datetime
from difflib import SequenceMatcher
from typing import *

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from AlbumOBJ import Album
from config import CLIENT_ID, CLIENT_SECRET, NUMBER_OF_FETCHED_ALBUMS

spot: spotipy.Spotify
sp: spotipy.Spotify


class SpotifyHandler:
    def __init__(self) -> None:
        self.spot: spotipy.Spotify = None
        self.sp: spotipy.Spotify = None

    def prepare_spot(self):
        if not self.spot:
            self.spot = spotipy.Spotify(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                )
            )

    @staticmethod
    def parse_album(album_dict: dict) -> Album:
        date = album_dict["release_date"]
        if len(date.split("-")) == 3:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        return Album(
            album_dict["name"],
            album_dict["artists"][0]["name"],
            date,
            album_dict["external_urls"]["spotify"],
        )

    @staticmethod
    def similarity(a: str, b: str) -> float:
        """the percentage of similarity between a and b"""
        return SequenceMatcher(None, a, b).ratio() * 100

    def get_album_by_info(self, album: Album) -> Album:
        name, artist = album.NAME, album.ARTIST
        self.prepare_spot()
        res = self.spot.search(
            f"album:{name} - artist:{artist}",
            limit=NUMBER_OF_FETCHED_ALBUMS,
            type="album",
            market="AU",  # Australia
        )
        fetched_albums = res["albums"]["items"]
        if not len(fetched_albums):
            return album
        else:
            album_idx_similary = []
            for idx, fetched_album in enumerate(fetched_albums):
                parsed_fetched_album = SpotifyHandler.parse_album(fetched_album)
                if (
                    parsed_fetched_album.NAME.upper() == name.upper()
                    and parsed_fetched_album.ARTIST.upper() == artist.upper()
                ):
                    return parsed_fetched_album
                album_idx_similary.append(
                    [
                        idx,
                        (
                            SpotifyHandler.similarity(
                                parsed_fetched_album.ARTIST, artist
                            )
                            * 10
                            + SpotifyHandler.similarity(parsed_fetched_album.NAME, name)
                            * 5
                        )
                        / 15,
                    ]
                )
            else:
                # none of them were similar enough
                # if the most similar one had the similarity of > 90, return that
                # else return original album
                album_idx_similary.sort(key=lambda item: item[1], reverse=True)
                if album_idx_similary[0][1] > 90:
                    return SpotifyHandler.parse_album(
                        fetched_albums[album_idx_similary[0][0]]
                    )
                else:
                    return album


shandler = SpotifyHandler()
if __name__ == "__main__":
    x = shandler.get_album_by_info(
        Album(
            "WORLD WIDE WHACK",
            "Tierra Whack",
            "2024-03-15",
        )
    )
    print(x.NAME, x.ARTIST, x.URL)
