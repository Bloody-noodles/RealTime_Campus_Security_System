from ultralytics import YOLO

from config import MODEL_PATH
from config import CONFIDENCE


class Detector:

    def __init__(self):

        print("Loading YOLO Model...")

        self.model = YOLO(str(MODEL_PATH))

        print("Model Loaded Successfully!")

    def detect(self, frame):

        results = self.model.track(

            source=frame,

            persist=True,

            tracker="bytetrack.yaml",

            imgsz=512,

            conf=CONFIDENCE,

            verbose=False

        )

        return results