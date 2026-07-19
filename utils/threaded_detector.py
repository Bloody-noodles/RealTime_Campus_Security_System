import threading
import time


class ThreadedDetector:

    def __init__(self, detector):

        self.detector = detector

        self.frame = None

        self.results = None

        self.running = False

        self.lock = threading.Lock()

        self.thread = None

    def update(self):

        while self.running:

            frame = None

            with self.lock:

                if self.frame is not None:

                    frame = self.frame.copy()

            if frame is not None:

                results = self.detector.detect(frame)

                with self.lock:

                    self.results = results

            else:

                time.sleep(0.005)

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(

            target=self.update,

            daemon=True

        )

        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread is not None:

            self.thread.join(timeout=1)

    def submit(self, frame):

        with self.lock:

            self.frame = frame.copy()

    def get_results(self):

        with self.lock:

            return self.results