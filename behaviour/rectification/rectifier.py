import pathlib
import os
import threading
import time
import queue

from server.connection import API_BASE_URL
from server import connection
from syslogs import logs
from behaviour.rectification.executer import Executer
from behaviour.analysis.emotion_recognition.observer import CONCERNING_EMOTIONS, SEVERITY

LOCAL_RESOURCES_PATH = str(pathlib.Path(__file__).parent.resolve()) + '/../../content/resources/'


class Rectifier:
    original_emotion = None
    original_criticality = 0
    student_id = None
    is_running = False
    controller = None
    cycle_complete = True

    decisions = []
    bad_decisions = []

    current_decision = None
    current_emotion = None
    current_confidence = None

    current_execution_thread: threading.Thread = None
    clock_thread = None

    def __init__(self, controller, student_id):
        self.controller = controller
        self.student_id = student_id
        self.clock_thread = threading.Thread(target=self.clock, args=())

    def start(self, emotion_detected, confidence):
        logs.print_log("Behaviour rectification started...")
        self.original_emotion = emotion_detected
        self.current_emotion = self.original_emotion
        self.current_confidence = confidence
        print(f"Rectifying {emotion_detected} (confidence: {confidence}%)")
        self.is_running = True
        self.original_criticality = self.criticality(emotion_detected, confidence)

        self.clock_thread.start()

        self.run()

    def run(self):
        if not self.is_running:
            return

        self.decisions = self.get_decisions(self.student_id, self.original_emotion)
        print("Decisions got: ", self.decisions)
        while self.is_running:
            best_decision = self.get_best_decision()
            self.current_decision = best_decision

            result_queue = queue.Queue()
            execution_thread = threading.Thread(target=self.execute_decision, args=(best_decision, result_queue,))
            execution_thread.daemon = True
            self.current_execution_thread = execution_thread
            execution_thread.start()
            response = result_queue.get()

            if response is not None:
                self.follow_up_on_response(response)

    def stop(self):
        self.student_id = None
        self.original_emotion = None
        self.is_running = False
        self.decisions = []
        self.bad_decisions = []
        if self.clock_thread.isAlive():
            self.clock_thread.join()
        self.stop_current_execution()

    @staticmethod
    def get_decisions(student_id, emotion_detected):
        query_params = {
            "student_pk": student_id,
            "emotion": emotion_detected
        }
        query_url = API_BASE_URL + 'decisions'

        decisions = connection.make_get_request(query_url, query_params).json()
        return decisions["soothers"]    # + decisions["resources"]

    def get_best_decision(self):
        best_decision = None
        if len(self.decisions) == 0:
            return best_decision

        best_decision = self.decisions[0]
        self.decisions.pop(0)

        if best_decision in self.bad_decisions:
            best_decision = self.get_best_decision()
        return best_decision

    def execute_decision(self, decision, result_queue):
        try:
            resource_id = decision["resource_pk"]
            if resource_id not in os.listdir(LOCAL_RESOURCES_PATH):
                filepath = self.save_resource_content(resource_id)
            else:
                filepath = LOCAL_RESOURCES_PATH + resource_id

            executer = Executer(filepath, self)
            executer.execute()

            while self.cycle_complete:
                pass
            self.cycle_complete = True

            response = {
                "emotion": self.current_emotion,
                "confidence": self.current_confidence
            }

            result_queue.put(response)
        except:
            self.controller.raise_mega_alarm()

    @staticmethod
    def save_resource_content(resource_id):
        resource_url = API_BASE_URL + 'resource'
        query_params = {
            "resource_pk": resource_id
        }
        resource = connection.make_get_request(resource_url, query_params)
        resource = resource.content

        filepath = str(LOCAL_RESOURCES_PATH) + resource_id
        with open(filepath, mode='wb') as f:
            f.write(resource)

    def follow_up_on_response(self, response):
        emotion = response["emotion"]
        confidence = response["confidence"]

        criticality = self.criticality(emotion, confidence)
        delta = criticality - self.original_criticality
        self.send_feedback(delta)

        if criticality < 0:     # concerning emotion detected
            if delta <= 0:
                # deterioration. Very bad.
                self.bad_decisions.append(self.current_decision)
                self.stop_current_execution()
            else:
                # some improvement at least. fine, try again with the same decision.
                self.decisions = [self.current_decision] + self.decisions
        else:
            logs.print_log("Student behaviour back to normal!", "info")

    @staticmethod
    def criticality(emotion, confidence):
        return SEVERITY[emotion] * abs(SEVERITY[emotion]) * confidence

    def send_feedback(self, delta):
        feedback_url = API_BASE_URL + 'soother'
        payload = {
            "resource_pk": self.current_decision["resource_pk"],
            "student_pk": self.student_id,
            "emotion": self.current_emotion,
            "delta": delta
        }
        print("Sending feedback")
        connection.make_put_request(feedback_url, payload, False)

    def clock(self):
        starting_time = time.time() * 100
        while True and self.is_running:
            current_time = time.time() * 100

            if (current_time - starting_time) % 1500:
                self.cycle_complete = False

    def stop_current_execution(self):
        if self.current_execution_thread and self.current_execution_thread.is_alive():
            del(self.current_execution_thread)
            self.current_execution_thread = None
