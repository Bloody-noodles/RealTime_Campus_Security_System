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

            object_id = -1

            if box.id is not None:

                object_id = int(box.id.item())

            color = (0, 255, 0)

            if name == "knife":

                color = (0, 0, 255)

            elif name == "gun":

                color = (0, 0, 255)

            elif name == "fire extinguisher":

                color = (0, 165, 255)

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                color,

                2

            )

            label = f"{name.upper()}  {conf:.2f}"

            if object_id != -1:

                label = f"{name.upper()} #{object_id} {conf:.2f}"

            cv2.putText(

                frame,

                label,

                (x1, y1 - 8),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                color,

                2

            )

            detections.append(

                {

                    "id": object_id,

                    "name": name,

                    "conf": conf,

                    "box": [x1, y1, x2, y2]

                }

            )

        return frame, detections