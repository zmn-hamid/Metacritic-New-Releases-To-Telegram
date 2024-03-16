from Telegram_handler import thandler
from Spotify_handler import shandler
from new_releases import new_rls_obj
from AlbumOBJ import Album
from Log import logger


new_releases = new_rls_obj.get_new_releases()
for new_release in new_releases:
    album: Album = new_release["album"]
    logger.debug(f'"{album.NAME}" by "{album.ARTIST}"... ')

    # get the url
    spot_album = shandler.get_album_by_info(album)
    if not spot_album.URL:
        logger.warning(
            f'couldnt find album in Spotify : "{album.NAME}" by "{album.ARTIST}"'
        )
    logger.debug("got url... ")

    # send the url
    thandler.send_album(album=spot_album)
    logger.debug("added message job.")


logger.debug("sending messages...")
thandler.run()
