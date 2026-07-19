from threading import Lock

_lock = Lock()

state = {
    "fps": 0,
    "danger": False,
    "objects": [],
    "counts": {
        "person": 0,
        "phone": 0,
        "bottle": 0,
        "laptop": 0,
        "knife": 0,
        "gun": 0
    }
}


def update(fps, detections):

    counts = {
        "person": 0,
        "phone": 0,
        "bottle": 0,
        "laptop": 0,
        "knife": 0,
        "gun": 0
    }

    danger = False

    for obj in detections:

        name = obj["name"]

        if name in counts:
            counts[name] += 1

        if name in ["knife", "gun"]:
            danger = True

    with _lock:

        state["fps"] = round(fps, 1)
        state["danger"] = danger
        state["objects"] = detections
        state["counts"] = counts


def get():

    with _lock:

        return state.copy()