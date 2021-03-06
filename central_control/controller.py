from syslogs import logs
from behaviour.analysis.emotion_recognition.observer import Observer
from behaviour.rectification.rectifier import Rectifier

import time
import sys
import threading


class Controller:
    is_behaviour_ok = False
    is_assignment_on = False
    is_rectification_on = False

    observer = None
    rectifier = None
    #assignment_manager = None

    student_id = None

    def __init__(self, student_id):
        logs.print_log("Application Run Started...")

        self.observer = Observer(controller=self)
        self.rectifier = Rectifier(controller=self, student_id=student_id)

    def run(self):
        behaviour_thread = threading.Thread(target=self.start_behaviour_analysis, args=())
        behaviour_thread.start()

    def interrupt(self, field, value, data={}):
        setattr(self, field, value)
        logs.print_log(f"{field} value changed to {value}")
        self.follow_up(field, value, data)

    def follow_up(self, field, value, data):
        if field == "is_behaviour_ok":
            if not value:
                self.interrupt("is_assignment_on", False)
                self.interrupt("is_rectification_on", True, data)
            else:
                self.interrupt("is_assignment_on", True)
                self.interrupt("is_rectification_on", False)

        if field == "is_rectification_on":
            if value:
                if self.rectifier.is_running and (data["emotion_detected"] != self.rectifier.original_emotion):
                    self.rectifier.stop()
                self.rectifier.start(data["emotion_detected"], data["confidence"])
            else:
                # stop the rectifier
                self.rectifier.stop()

        if field == "is_assignment_on":
            if value:
                self.start_assignment_management()
            else:
                # pause the assignment manager
                pass

    def start_behaviour_analysis(self):
        self.observer.start()

        time.sleep(5)

    def start_assignment_management(self):
        pass

    def raise_mega_alarm(self):
        self.rectifier.stop()
        print("Sorry, please call the teacher!")
        sys.exit(0)
