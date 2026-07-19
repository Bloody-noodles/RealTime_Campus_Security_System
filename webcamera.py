import cv2
import time
import json
from pathlib import Path

from utils.detector import Detector
from utils.tracker import Tracker
from utils.dashboard import Dashboard
from utils.logger import Logger
from utils.alarm import Alarm
from utils.screenshot import Screenshot
from utils.timeline import Timeline


LIVE_FILE = Path("live_data.json")


class WebCamera:

    def __init__(self):

        self.detector = Detector()

        self.tracker = Tracker()

        self.dashboard = Dashboard()

        self.logger = Logger()

        self.alarm = Alarm()

        self.screenshot = Screenshot()

        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.prev_time = time.time()

        self.fps = 0

        self.frame_counter = 0

        self.last_dashboard_update = time.time()

        self.last_screenshot = 0
        self.timeline = Timeline()

        self.timeline.add(

            "🟢",

            "SYSTEM STARTED",

            "Monitoring initialized."

        )

    def update_live_data(self, fps, detections, danger):

        classes = [

            "person",

            "phone",

            "laptop",

            "knife",

            "gun",

            "bottle",

            "bag",

            "chair",

            "cup",

            "book"

        ]

        counts = {

            item: 0

            for item in classes

        }

        for obj in detections:

            name = obj["name"]

            if name in counts:

                counts[name] += 1

        latest_capture = ""

        capture_folder = Path("captures")

        if capture_folder.exists():

            images = sorted(

                capture_folder.glob("*"),

                key=lambda x: x.stat().st_mtime,

                reverse=True

            )

            if images:

                latest_capture = images[0].name

        data = {

            "fps": round(fps, 1),

            "danger": danger,

            "counts": counts,

            "latest_capture": latest_capture

        }

        with open(LIVE_FILE, "w") as f:

            json.dump(data, f)
    def generate_frames(self):

        while True:

            success, frame = self.cap.read()

            if not success:

                break

            frame = cv2.flip(frame, 1)

            # ----------------------------
            # YOLO Detection
            # ----------------------------

            results = self.detector.detect(frame)

            frame, detections = self.tracker.draw(

                frame,

                results

            )

            # ----------------------------
            # Database Logging
            # ----------------------------

            if self.frame_counter % 15 == 0:

                self.logger.save(detections)

            self.frame_counter += 1

            # ----------------------------
            # Threat Detection
            # ----------------------------

            danger = any(

                obj["name"] in ["knife", "gun"]

                for obj in detections

            )

            if danger:

                self.alarm.play()

                if time.time() - self.last_screenshot > 5:

                    self.screenshot.save(frame)

                    self.last_screenshot = time.time()

            else:

                self.alarm.stop()

            # ----------------------------
            # FPS
            # ----------------------------

            current = time.time()

            instant_fps = 1 / (current - self.prev_time)

            self.fps = self.fps * 0.9 + instant_fps * 0.1

            self.prev_time = current

            # ----------------------------
            # Dashboard JSON
            # ----------------------------

            if current - self.last_dashboard_update > 0.5:

                self.update_live_data(

                    self.fps,

                    detections,

                    danger

                )

                self.last_dashboard_update = current

            # ----------------------------
            # Draw Dashboard Overlay
            # ----------------------------

            frame = self.dashboard.draw(

                frame,

                self.fps,

                detections

            )

            # ----------------------------
            # Encode JPEG
            # ----------------------------

            ok, buffer = cv2.imencode(

                ".jpg",

                frame,

                [

                    int(cv2.IMWRITE_JPEG_QUALITY),

                    80

                ]

            )

            if not ok:

                continue

            frame_bytes = buffer.tobytes()

            yield (

                b'--frame\r\n'

                b'Content-Type: image/jpeg\r\n\r\n'

                + frame_bytes +

                b'\r\n'

            )

    def release(self):

        self.alarm.stop()

        if self.cap.isOpened():

            self.cap.release()