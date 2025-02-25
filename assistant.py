import board
import busio
import adafruit_ssd1306
from pywhispercpp.examples.assistant import Assistant


class AssistantScreen():
    def __init__(self, addr=0x3c):
        self.display = adafruit_ssd1306.SSD1306_I2C(
            128,
            64,
            busio.I2C(board.SCL, board.SDA),
            addr=addr
        )

        self._init_screen()

    def _init_screen(self):
        self.display.fill(0)
        self.display.text("Sushi", 0, 0, 1, size=2)
        self.display.show()

    def _display_text(self, text):
        if not text.startswith("["):
            self._init_screen()
            self.display.text(text, 0, 20, 1)
            self.display.show()

    def run(self):
        assistant = Assistant(
            commands_callback=lambda text: self._display_text(text),
            n_threads=8
        )
        assistant.start()


if __name__ == "__main__":
    spotify_screen = AssistantScreen()
    spotify_screen.run()
