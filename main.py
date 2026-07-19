import cv2
import json
import time

from pathlib import Path

from utils.detector import Detector
from utils.tracker import Tracker
from utils.dashboard import Dashboard
from utils.logger import Logger
from utils.alarm import Alarm
from utils.screenshot import Screenshot

from config import WINDOW_NAME


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

LIVE_FILE = BASE_DIR / "live_data.json"

CAPTURE_FOLDER = BASE_DIR / "captures"


# ==========================================
# LIVE DATA WRITER
# ==========================================

def update_live_data(fps, results, danger):

    classes = {

        "person": 0,
        "phone": 0,
        "laptop": 0,
        "knife": 0,
        "gun": 0,
        "bottle": 0,
        "bag": 0,
        "chair": 0,
        "cup": 0,
        "book": 0

    }

    # --------------------------------------
    # COUNT OBJECTS DIRECTLY FROM YOLO
    # --------------------------------------

    if len(results):

        result = results[0]

        if result.boxes is not None:

            for box in result.boxes:

                cls = int(box.cls[0])

                name = result.names[cls]

                if name in classes:

                    classes[name] += 1

    # --------------------------------------
    # FIND LATEST SCREENSHOT
    # --------------------------------------

    latest_capture = ""

    if CAPTURE_FOLDER.exists():

        images = sorted(

            CAPTURE_FOLDER.glob("*"),

            key=lambda x: x.stat().st_mtime,

            reverse=True

        )

        if images:

            latest_capture = images[0].name

    # --------------------------------------
    # SAVE JSON
    # --------------------------------------

    live = {

        "fps": round(fps, 1),

        "danger": danger,

        "counts": classes,

        "latest_capture": latest_capture

    }

    LIVE_FILE.write_text(

        json.dumps(

            live,

            indent=4

        ),

        encoding="utf-8"

    )
    # ==========================================
# MAIN
# ==========================================

def main():

    detector = Detector()

    tracker = Tracker()

    dashboard = Dashboard()

    logger = Logger()

    alarm = Alarm()

    screenshot = Screenshot()

    # --------------------------------------
    # CAMERA
    # --------------------------------------

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():

        print("Unable to open webcam.")

        return

    prev_time = time.time()

    frame_counter = 0

    print("System Started Successfully!")

    # ======================================
    # LOOP
    # ======================================

    while True:

        success, frame = cap.read()

        if not success:

            break

        frame = cv2.flip(frame, 1)

        frame = cv2.resize(

            frame,

            (1280, 720)

        )

        # ----------------------------------
        # YOLO DETECTION
        # ----------------------------------

        results = detector.detect(frame)

        # ----------------------------------
        # DRAW BOXES
        # ----------------------------------

        frame, detections = tracker.draw(

            frame,

            results

        )

        # ----------------------------------
        # SAVE HISTORY
        # ----------------------------------

        if frame_counter % 5 == 0:

            logger.save(

                detections

            )

        frame_counter += 1

                # ----------------------------------
        # THREAT DETECTION
        # ----------------------------------

        danger = False

        if len(results):

            result = results[0]

            if result.boxes is not None:

                for box in result.boxes:

                    cls = int(box.cls[0])

                    name = result.names[cls]

                    if name in ["knife", "gun"]:

                        danger = True

                        break

        # ----------------------------------
        # ALARM
        # ----------------------------------

        if danger:

            alarm.play()

            if frame_counter % 20 == 0:

                screenshot.save(frame)

        else:

            alarm.stop()

        # ----------------------------------
        # FPS
        # ----------------------------------

        current = time.time()

        fps = 1 / max(

            current - prev_time,

            0.0001

        )

        prev_time = current

        # ----------------------------------
        # UPDATE DASHBOARD
        # ----------------------------------

        update_live_data(

            fps,

            results,

            danger

        )

        # ----------------------------------
        # DRAW DASHBOARD
        # ----------------------------------

        frame = dashboard.draw(

            frame,

            fps,

            detections

        )

        # ----------------------------------
        # SHOW
        # ----------------------------------

        cv2.imshow(

            WINDOW_NAME,

            frame

        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

            # ======================================
    # CLEANUP
    # ======================================

    alarm.stop()

    cap.release()

    cv2.destroyAllWindows()


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    main()