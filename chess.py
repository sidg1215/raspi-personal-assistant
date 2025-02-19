import board
import busio
import datetime
from time import sleep

import requests
import adafruit_ssd1306

LOSE_CODES = {"checkmated", "timeout", "resigned", "lose", "abandoned"}
DRAW_CODES = {
    "agreed",
    "repitition",
    "stalemate",
    "insufficient",
    "50move",
    "timevsinsufficient"
}
USERNAME = 'sid1215'
HOST = 'https://api.chess.com/pub'


class ChessScreen:
    def __init__(self, addr=0x3C):
        self.stats = None
        self.display = adafruit_ssd1306.SSD1306_I2C(
            128,
            64,
            busio.I2C(board.SCL, board.SDA),
            addr=addr
        )
        self._init_screen()

    def _init_screen(self):
        self.display.fill(0)
        self.display.text("Chess.com", 0, 0, 1, size=2)
        self.display.show()

    def _get_monthly_stats(self):
        dt = datetime.datetime.now()
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }
        year, month = dt.year, dt.month
        endpoint = f"{HOST}/player/{USERNAME}/games/{year}/{month:02d}"
        res = requests.get(
            endpoint,
            headers=headers
        )
        games = res.json()['games']
        wins = 0
        losses = 0
        draws = 0
        for game in games:
            if game['white']['username'] == 'sid1215':
                result = game['white']['result']
            else:
                result = game['black']['result']
            wins += result == "win"
            losses += result in LOSE_CODES
            draws += result in DRAW_CODES

        return {'wins': wins, 'losses': losses, 'draws': draws}

    def _display_stats(self, stats):
        if stats is None:
            self.display.text("No stats are present currently", 0, 20, 1)
        else:
            self.display.text(f"Wins: {stats['wins']}", 0, 30, 1)
            self.display.text(f"Losses: {stats['losses']}", 0, 40, 1)
            self.display.text(f"Draws: {stats['draws']}", 0, 50, 1)
        self.stats = stats

    def run(self):
        while True:
            stats = self._get_monthly_stats()
            self._display_stats(stats)
            self.display.show()
            sleep(1)


if __name__ == "__main__":
    chess_screen = ChessScreen()
    chess_screen.run()
