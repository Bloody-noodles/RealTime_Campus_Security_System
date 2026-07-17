import sqlite3
from config import DATABASE


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            DATABASE,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS detections(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            object_name TEXT,

            confidence REAL,

            timestamp TEXT

        )

        """)

        self.conn.commit()

    def insert(self, name, confidence, timestamp):

        self.cursor.execute(

            """

            INSERT INTO detections

            (object_name,confidence,timestamp)

            VALUES(?,?,?)

            """,

            (

                name,

                confidence,

                timestamp

            )

        )

        self.conn.commit()

    def close(self):

        self.conn.close()