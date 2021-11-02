import cv2 as cv
import time
import os
import signal
import sys
from syslogs.logs import print_log

TEMP_DIR = '/Users/maniklaldas/Desktop/Sem 3-1/AI/Assignmnt/sahyata/emotion_recognition/temp/'


def capture_video():
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
        if current_time - LAST_SNAPSHOT_TIME >= 50:
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


def write_snapshot(image, timestamp):
    filepath = TEMP_DIR + str(int(timestamp)) + '.jpeg'
    cv.imwrite(filepath, image)


def get_snapshot():
    try:
        oldest_file = sorted(os.listdir(TEMP_DIR))[0] 
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
