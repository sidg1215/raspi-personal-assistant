import board
import busio
from time import sleep

import adafruit_ssd1306
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyScreen:
    def __init__(self, addr=0x3C):
        # Initialize the SpotifyOAuth and the Spotify client
        self.auth = SpotifyOAuth(
            scope="user-read-currently-playing",
            client_id="1582c0b665624392b4921e21bac70b4b",
            client_secret="d2ed49202bb84030872254cb6bef47d5",
            redirect_uri="http://localhost",
        )
        self.sp = spotipy.Spotify(auth_manager=self.auth)
        self.track = None
        self.display = adafruit_ssd1306.SSD1306_I2C(
            128,
            64,
            busio.I2C(board.SCL, board.SDA),
            addr=addr
        )

        self._init_screen()

    def _init_screen(self):
        self.display.fill(0)
        self.display.text("Spotify", 0, 0, 1, size=2)
        self.display.show()

    def _get_current_track(self):
        # Fetch the currently playing track
        track = self.sp.current_user_playing_track()
        if track is None:
            return None
        return {
            'song': track['item']['name'],
            'artists': ', '.join(
                artist['name'] for artist in track['item']['artists']
            )
        }

    def _display_track(self, track):
        if track is None:
            self.display.text("No track is playing", 0, 20, 1)
        else:
            self.display.text("Currently playing...", 0, 20, 1)
            self.display.text(track['song'], 0, 30, 1)
            self.display.text(f"By {track['artists']}", 0, 40, 1)
        self.track = track

    def run(self):
        while True:
            track = self._get_current_track()
            if track != self.track:
                self._init_screen()
                self._display_track(track)
                self.display.show()
            sleep(1)


if __name__ == "__main__":
    spotify_screen = SpotifyScreen()
    spotify_screen.run()
