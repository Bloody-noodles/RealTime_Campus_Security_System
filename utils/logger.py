from datetime import datetime

from utils.database import Database


class Logger:

    def __init__(self):

        self.db = Database()

        self.last_log = {}

    def save(self, detections):

        now = datetime.now()

        current = now.timestamp()

        for obj in detections:

            name = obj["name"]

            confidence = obj["conf"]

            if name in self.last_log:

                if current - self.last_log[name] < 2:

                    continue

            self.db.insert(

                name,

                confidence,

                now.strftime("%Y-%m-%d %H:%M:%S")

            )

            self.last_log[name] = current