import cv2
import time

from utils.detector import Detector
from utils.tracker import Tracker
from utils.dashboard import Dashboard
from utils.logger import Logger
from utils.alarm import Alarm
from utils.screenshot import Screenshot

from config import WINDOW_NAME


def main():

    detector = Detector()
    tracker = Tracker()
    dashboard = Dashboard()

    logger = Logger()
    alarm = Alarm()
    screenshot = Screenshot()

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():

        print("Unable to open webcam.")
        return

    prev_time = time.time()

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        frame = cv2.resize(frame, (1280, 720))

        results = detector.detect(frame)

        frame, detections = tracker.draw(frame, results)

        # -----------------------------
        # LOG DETECTIONS
        # -----------------------------
        logger.save(detections)

        # -----------------------------
        # THREAT DETECTION
        # -----------------------------
        danger = False

        for obj in detections:

            if obj["name"] in ["knife", "gun"]:

                danger = True
                break

        if danger:

            alarm.play()

            screenshot.save(frame)

        else:

            alarm.stop()

        current = time.time()

        fps = 1 / (current - prev_time)

        prev_time = current

        frame = dashboard.draw(
            frame,
            fps,
            detections
        )

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()