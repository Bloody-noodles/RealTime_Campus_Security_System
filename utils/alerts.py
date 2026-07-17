import cv2
import os
from datetime import datetime
from playsound import playsound
import threading

alarm_running = False


def play_alarm():

    global alarm_running

    if alarm_running:
        return

    alarm_running = True

    def worker():

        global alarm_running

        try:
            playsound("sounds/mixkit-police-siren-us-1643.wav")
        except:
            pass

        alarm_running = False

    threading.Thread(target=worker, daemon=True).start()


def save_screenshot(frame):

    os.makedirs("captures", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")

    path = os.path.join("captures", filename)

    cv2.imwrite(path, frame)

    print(f"[INFO] Screenshot saved -> {path}")