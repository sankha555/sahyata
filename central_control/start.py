"""
Start script to be run when user switches on the application

Will use multi-threading to simultaneously manage different subsystems
"""
import signal
import sys

from controller import Controller


def startup_script():
    controller = Controller(student_id=1)
    controller.run()


def handler(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    startup_script()
