"""
Start script to be run when user switches on the application

Will use multi-threading to simultaneously manage different subsystems
"""
import threading
import signal
import sys

from syslogs.logs import print_log

from controller import Controller


def startup_script():
    controller = Controller(student_id=1)
    controller.run()

    """
    try:
        #ui_thread = threading.Thread(target=initialize_user_interface, args=())
        #behaviour_analysis_thread = threading.Thread(target=start_behaviour_analysis, args=())

        #ui_thread.start()
        #behaviour_analysis_thread.start()

        #behaviour_analysis_thread.join()
        #ui_thread.join()

        print_log("Application Run Complete...", "info")
    except Exception as e:
        print_log(str(e), "error")
    """

def handler(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    startup_script()
