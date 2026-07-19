import cv2

from datetime import datetime


class Dashboard:

    def draw(self, frame, fps, detections):

        h, w = frame.shape[:2]

        overlay = frame.copy()

        cv2.rectangle(

            overlay,

            (0, 0),

            (w, 110),

            (25, 25, 25),

            -1

        )

        cv2.addWeighted(

            overlay,

            0.85,

            frame,

            0.15,

            0,

            frame

        )

        cv2.putText(

            frame,

            "REAL-TIME CAMPUS SECURITY SYSTEM",

            (20, 32),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.85,

            (0, 255, 255),

            2

        )

        cv2.putText(

            frame,

            f"FPS : {fps:.1f}",

            (20, 70),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (255, 255, 255),

            2

        )

        cv2.putText(

            frame,

            f"Objects : {len(detections)}",

            (170, 70),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (255, 255, 255),

            2

        )

        threat = any(

            d["name"] in ["knife", "gun"]

            for d in detections

        )

        if threat:

            status = "THREAT DETECTED"

            color = (0, 0, 255)

        else:

            status = "SAFE"

            color = (0, 255, 0)

        cv2.putText(

            frame,

            status,

            (390, 70),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.70,

            color,

            2

        )

        cv2.putText(

            frame,

            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),

            (860, 70),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (255, 255, 255),

            2

        )

        return frame