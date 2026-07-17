from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "best.pt"

CONFIDENCE = 0.45

WINDOW_NAME = "Real-Time Campus Security System"

LOGO_PATH = BASE_DIR / "fuoye.jpg"

DATABASE = BASE_DIR / "detections.db"

ALARM_SOUND = BASE_DIR / "sounds" / "alarm.wav"

SCREENSHOT_FOLDER = BASE_DIR / "captures"

SCREENSHOT_FOLDER.mkdir(exist_ok=True)