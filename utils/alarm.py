import pygame
from config import ALARM_SOUND


class Alarm:

    def __init__(self):

        pygame.mixer.init()

        self.playing = False

        try:
            pygame.mixer.music.load(str(ALARM_SOUND))
        except Exception:
            print("Alarm sound not found.")

    def play(self):

        if not self.playing:

            try:
                pygame.mixer.music.play(-1)
                self.playing = True
            except Exception:
                pass

    def stop(self):

        if self.playing:

            pygame.mixer.music.stop()
            self.playing = False