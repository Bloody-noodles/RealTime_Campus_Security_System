from flask import (

    Flask,
    render_template,
    jsonify,
    send_from_directory,
    Response

)

import json
import sqlite3
import os
import atexit

from pathlib import Path

from webcamera import WebCamera

from utils.timeline import EVENTS

from flask import (
    Flask,
    render_template,
    jsonify,
    send_from_directory,
    Response,
    request,
    redirect,
    url_for,
    session
)


# ==========================================
# APP
# ==========================================

app = Flask(__name__)
app.secret_key = "fuoye_security_2026"

# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE = BASE_DIR / "detections.db"

CAPTURES = BASE_DIR / "captures"

LIVE_DATA = BASE_DIR / "live_data.json"


# ==========================================
# CAMERA
# ==========================================

camera = WebCamera()


# ==========================================
# DATABASE
# ==========================================

def get_db():

    conn = sqlite3.connect(

        DATABASE

    )

    conn.row_factory = sqlite3.Row

    return conn

    # ==========================================
# PAGES
# ==========================================

@app.route("/")
def home():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template("index.html")

    # ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        if username == "admin" and password == "admin123":

            session["user"] = username

            return redirect(url_for("home"))

        return render_template(

            "login.html",

            error="Invalid Username or Password"

        )

    return render_template("login.html")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.route("/analytics")
def analytics():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template("analytics.html")


# ==========================================
# SCREENSHOTS
# ==========================================

@app.route("/captures/<filename>")
def captures(filename):

    return send_from_directory(

        CAPTURES,

        filename

    )


# ==========================================
# LIVE VIDEO
# ==========================================

@app.route("/video_feed")
def video_feed():

    return Response(

        camera.generate_frames(),

        mimetype="multipart/x-mixed-replace; boundary=frame"

    )

# ==========================================
# DASHBOARD API
# ==========================================

@app.route("/api/dashboard")
def dashboard():

    if "user" not in session:

        return jsonify({"error":"Unauthorized"}),401
    timeline = EVENTS

    # --------------------------------------
    # LIVE DATA
    # --------------------------------------

    live = {

        "fps": 0,

        "danger": False,

        "counts": {

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

        },

        "latest_capture": ""

    }

    if LIVE_DATA.exists():

        try:

            with open(

                LIVE_DATA,

                "r",

                encoding="utf-8"

            ) as f:

                live = json.load(f)

        except Exception as e:

            print("LIVE DATA ERROR:", e)

            

    # --------------------------------------
    # DATABASE LOGS
    # --------------------------------------

    logs = []

    try:

        conn = get_db()

        cur = conn.cursor()

        cur.execute("""

            SELECT object_name,
                   confidence,
                   timestamp

            FROM detections

            ORDER BY id DESC

            LIMIT 20

        """)

        logs = [dict(row) for row in cur.fetchall()]

        conn.close()

    except Exception as e:

        print("DATABASE ERROR:", e)

    # --------------------------------------
    # RESPONSE
    # --------------------------------------

    return jsonify({

        "counts": live.get("counts", {}),

        "danger": live.get("danger", False),

        "fps": live.get("fps", 0),

        "latest_capture": live.get(

            "latest_capture",

            ""

        ),

        "logs": logs

    })

    # ==========================================
# CLEANUP
# ==========================================

@atexit.register
def shutdown():

    try:

        camera.release()

    except Exception:
        pass


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True,

        threaded=True,

        use_reloader=False

    )