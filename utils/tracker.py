import cv2


class Tracker:

    def draw(self, frame, results):

        detections = []

        if len(results) == 0:
            return frame, detections

        result = results[0]

        if result.boxes is None:
            return frame, detections

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            conf = float(box.conf[0])

            cls = int(box.cls[0])

            name = result.names[cls]

            ID = -1

            if box.id is not None:

                ID = int(box.id.item())

            detections.append({

                "id": ID,

                "name": name,

                "conf": conf,

                "box": [x1, y1, x2, y2]

            })

            if name in ["knife", "gun"]:

                color = (0, 0, 255)

            else:

                color = (0, 255, 0)

            # Bounding Box

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                color,

                2

            )

            label = f"{name.upper()}  #{ID}"

            confidence = f"{int(conf*100)}%"

            (tw, th), _ = cv2.getTextSize(

                label,

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                2

            )

            cv2.rectangle(

                frame,

                (x1, y1-35),

                (x1+tw+95, y1),

                color,

                -1

            )

            cv2.putText(

                frame,

                label,

                (x1+6, y1-12),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                (255,255,255),

                2

            )

            cv2.putText(

                frame,

                confidence,

                (x1+tw+15, y1-12),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                (255,255,0),

                2

            )

        return frame, detections