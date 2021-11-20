from behaviour.analysis.emotion_recognition import face_capture, emotion_classifier
from syslogs import logs

import sys
import time
import threading
import cv2 as cv

CONCERNING_EMOTIONS = ["sad", "fear", "angry"]
SEVERITY = {
    "happy": 3,
    "surprise": 2,
    "neutral": 1,
    "sad": -1,
    "fear": -2,
    "angry": -3
}


def handler(signum, frame):
    sys.exit(0)


class Observer:
    controller = None
    current_behaviour = None
    confidence = 0
    is_running = True

    def __init__(self, controller):
        self.controller = controller
        logs.print_log("Observer created...")

    def start(self):
        logs.print_log("Observer started...", "info")

        # video_capture_thread = threading.Thread(target=face_capture.capture_video, args=())
        # video_capture_thread.start()

        observation_thread = threading.Thread(target=self.observe_behaviour, args=())
        observation_thread.start()

        #video_capture_thread.join()
        observation_thread.join()

    def pause(self):
        self.is_running = False

    def resume(self):
        self.is_running = True

    def __del__(self):
        print("Over")
        face_capture.cleanup()

    def observe_behaviour(self, interval=50):
        """
        Regularly observes the main of the student. Raises an alarm is main is concerning.
        :param interval: time interval in milliseconds at which to check main (default is 500 ms)
        :return:
        """

        start_time = time.time() * 100

        while self.is_running:
            current_time = time.time() * 100

            if (current_time - start_time) % interval == 0:
                # latest_image = face_capture.get_snapshot()
                # if latest_image is None:
                #     continue

                latest_image = face_capture.take_snapshot()
                if latest_image is None:
                    print("No image captured")
                #print(latest_image)
                cv.namedWindow("test")
                cv.imshow("test", latest_image)

                self.current_behaviour, self.confidence = emotion_classifier.classify_face_emotion(latest_image)

                print(self.current_behaviour)
                if self.current_behaviour in CONCERNING_EMOTIONS:
                    self.raise_alarm()
                else:
                    if self.controller.is_rectification_on:
                        self.controller.interrupt("is_behaviour_ok", True)
                    logs.print_log("All OK", "info")

    def raise_alarm(self):
        """
        Basically sends an interrupt signal to the central controller
        :return:
        """
        emotion = self.current_behaviour
        logs.print_log(f"Student is showing {emotion} emotion. Something's wrong!", "critical")
        self.controller.rectifier.current_emotion = emotion
        self.controller.rectifier.current_confidence = self.confidence
        self.controller.interrupt("is_behaviour_ok", False, {
            "emotion_detected": emotion,
            "confidence": self.confidence,
        })
