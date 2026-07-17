import cv2
from datetime import datetime
from config import LOGO_PATH


class Dashboard:

    def __init__(self):

        self.logo = cv2.imread(str(LOGO_PATH))

        if self.logo is not None:
            self.logo = cv2.resize(self.logo, (70, 70))

    def draw(self, frame, fps, detections):

        h, w = frame.shape[:2]

        panel_height = 110

        cv2.rectangle(frame, (0, 0), (w, panel_height), (35, 35, 35), -1)

        # ----------------------------------
        # School Logo
        # ----------------------------------

        if self.logo is not None:

            frame[20:90, 20:90] = self.logo

        # ----------------------------------
        # Title
        # ----------------------------------

        cv2.putText(

            frame,

            "REAL-TIME CAMPUS SECURITY SYSTEM",

            (110, 35),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.9,

            (0, 255, 255),

            2

        )

        cv2.putText(

            frame,

            "Federal University Oye-Ekiti",

            (110, 65),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (230, 230, 230),

            1

        )

        # ----------------------------------
        # Counts
        # ----------------------------------

        counts = {}

        for obj in detections:

            name = obj["name"]

            counts[name] = counts.get(name, 0) + 1

        x = 420

        for name in sorted(counts):

            cv2.putText(

                frame,

                f"{name.capitalize()}: {counts[name]}",

                (x, 35),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (255, 255, 255),

                2

            )

            x += 170

        # ----------------------------------
        # Bottom info
        # ----------------------------------

        cv2.putText(

            frame,

            f"FPS : {fps:.1f}",

            (20, 100),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        cv2.putText(

            frame,

            f"Objects : {len(detections)}",

            (170, 100),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        # ----------------------------------
        # Threat
        # ----------------------------------

        danger = any(

            obj["name"] in ["knife", "gun"]

            for obj in detections

        )

        if danger:

            text = "THREAT DETECTED"

            color = (0, 0, 255)

        else:

            text = "SYSTEM SAFE"

            color = (0, 140, 0)

        cv2.rectangle(frame, (w-300, 20), (w-20, 90), color, -1)

        cv2.putText(

            frame,

            text,

            (w-280, 65),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.9,

            (255,255,255),

            2

        )

        # ----------------------------------
        # Time
        # ----------------------------------

        cv2.putText(

            frame,

            datetime.now().strftime("%d/%m/%Y  %H:%M:%S"),

            (w-330, 105),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (255,255,255),

            2

        )

        return frame