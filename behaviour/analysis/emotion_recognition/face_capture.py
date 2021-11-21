import cv2 as cv
import time
import os
import pathlib
import signal
import sys
from syslogs.logs import print_log

import imageio as iio
import matplotlib.pyplot as plt


TEMP_DIR = str(pathlib.Path(__file__).parent.resolve()) + '/temp/'


def capture_video(interval=50):
    LAST_SNAPSHOT_TIME = time.time() * 100      # in milliseconds since epoch
    
    try:
        video = cv.VideoCapture(0)
    except:
        print("Program not authorized to open webcam. Please grant appropriate permissions...")

    # Dimensions of the video capturing frame
    video.set(3, 1000)
    video.set(4, 800)

    while True:
        _, frame = video.read()
                
        cv.imshow('SAHyATA', frame)
        
        # Taking a snapshot for analysis
        current_time = time.time() * 100
        if current_time - LAST_SNAPSHOT_TIME >= interval:
            LAST_SNAPSHOT_TIME = current_time
            grayscale_snapshot = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            write_snapshot(grayscale_snapshot, LAST_SNAPSHOT_TIME)
        
        # Close windows if ESC if pressed
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        
    video.release()
    cv.destroyAllWindows()
    
    cleanup()


def take_snapshot():
    camera = iio.get_reader("<video0>")
    screenshot = camera.get_data(0)
    camera.close()

    return screenshot


def write_snapshot(image, timestamp):
    filepath = TEMP_DIR + str(int(timestamp)) + '.jpeg'
    cv.imwrite(filepath, image)


def get_snapshot():
    try:
        files = os.listdir(TEMP_DIR)
        if len(files) == 0:
            return None

        oldest_file = sorted(files)[0]
        filepath = TEMP_DIR + oldest_file
        image = cv.imread(filepath)
        delete_file(filepath)
        return image
    except Exception as e:
        print_log(e, "error")
        return None


def delete_file(filepath):
    try:
        os.remove(filepath)
        return True
    except FileNotFoundError as e:
        print_log(e, "error")
        return False


def cleanup():
    for file in os.listdir(TEMP_DIR):
        filepath = TEMP_DIR + file
        delete_file(filepath)
    print_log("Cleanup complete...", "info")


def handler(signum, frame):
    cleanup()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    capture_video()
