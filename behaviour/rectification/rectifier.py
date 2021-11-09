from syslogs import logs
from behaviour.rectification.decision_maker import get_decision


class Rectifier:
    emotion_detected = None
    student_id = None
    is_running = False
    controller = None

    def __init__(self, controller, student_id):
        logs.print_log("Behaviour rectification started...")
        self.controller = controller
        self.student_id = student_id

    def start(self, emotion_detected):
        self.emotion_detected = emotion_detected
        self.is_running = True

    def stop(self):
        self.student_id = None
        self.emotion_detected = None
        self.is_running = False

    def make_decision(self):
        if not self.is_running:
            return

        best_decision = get_decision(self.student_id, self.emotion_detected)
        self._execute_decision(best_decision)

    def _execute_decision(self, decision):
        pass
