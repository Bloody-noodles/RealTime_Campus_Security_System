from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE


class Detector:

    def __init__(self):

        print("Loading YOLO Model...")

        self.model = YOLO(str(MODEL_PATH))

        print("Model Loaded Successfully!")

    def detect(self, frame):

        results = self.model.track(

            source=frame,

            conf=CONFIDENCE,

            imgsz=640,

            persist=True,

            tracker="bytetrack.yaml",

            verbose=False

        )

        return results