from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "detections.db"


def get_recent_events(limit=15):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    try:

        cursor.execute("""

        SELECT object_name, confidence, timestamp

        FROM detections

        ORDER BY id DESC

        LIMIT ?

        """, (limit,))

        rows = cursor.fetchall()

    except:

        rows = []

    conn.close()

    return rows


@app.route("/")
def home():

    events = get_recent_events()

    return render_template(

        "index.html",

        events=events

    )


if __name__ == "__main__":

    app.run(debug=True)