import threading
import winsound

from config import ALARM_SOUND


class Alarm:

    def __init__(self):

        self.playing = False

        self.thread = None

    def _loop(self):

        while self.playing:

            winsound.PlaySound(

                str(ALARM_SOUND),

                winsound.SND_FILENAME

            )

    def play(self):

        if self.playing:

            return

        self.playing = True

        self.thread = threading.Thread(

            target=self._loop,

            daemon=True

        )

        self.thread.start()

    def stop(self):

        self.playing = False

        winsound.PlaySound(

            None,

            winsound.SND_PURGE

        )