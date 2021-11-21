"""
Sends a file to be displayed on the screen in response to an execution request
made by the behaviour rectifier.
"""

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

    def relay_content_to_screen(self):
        os.system("python "+FILE_LOC+" "+self.filepath)
