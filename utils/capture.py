import cv2
from pathlib import Path
from datetime import datetime


class Capture:

    def __init__(self):

        self.folder = Path("captures")
        self.folder.mkdir(exist_ok=True)

    def save(self, frame, object_name):

        filename = datetime.now().strftime(
            f"%Y%m%d_%H%M%S_{object_name}.jpg"
        )

        path = self.folder / filename

        cv2.imwrite(str(path), frame)

        return str(path)