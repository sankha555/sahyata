"""
Sends a file to be displayed on the screen in response to an execution request
made by the behaviour rectifier.
"""

from content import streamers
from content.streamers import FILE_LOC
import os


class Executer:
    filepath = None     # path to resource object
    rectifier = None

    def __init__(self, filepath, rectifier):
        self.filepath = filepath
        self.rectifier = rectifier
        print("Executer initiated")

    def execute(self):
        print("Executing "+self.filepath)
        self.relay_content_to_screen()
        #self.rectifier.stop_current_execution()

    def relay_content_to_screen(self):
        print("In relaying")
        #streamers.stream(filepath=self.filepath)
        #streamers.main()
        os.system("python "+FILE_LOC+" "+self.filepath)


if __name__ == "__main__":
    executer = Executer("/Users/maniklaldas/Desktop/Misc/index/media/bits.png", None)
    executer.execute()
