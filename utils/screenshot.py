import cv2
from datetime import datetime
from config import SCREENSHOT_FOLDER


class Screenshot:

    def __init__(self):

        self.last_saved = None

    def save(self, frame):

        now = datetime.now()

        if self.last_saved:

            elapsed = (now - self.last_saved).total_seconds()

            if elapsed < 3:
                return

        filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"

        cv2.imwrite(
            str(SCREENSHOT_FOLDER / filename),
            frame
        )

        self.last_saved = now