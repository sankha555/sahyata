from tkinter import *

from pygame import mixer
from PIL import Image, ImageTk
from matplotlib import pyplot
import pathlib

from syslogs import logs

VIDEO_EXTENSIONS = [".mkv", ".mp4", ".flv", ".srt", ".gif"]
AUDIO_EXTENSIONS = [".mp3"]
IMAGE_EXTENSIONS = [".jpeg", ".jpg", ".png", ".tiff", ".gif"]

FILE_LOC = str(pathlib.Path(__file__).parent.resolve()) + '/streamers.py'

mixer.init()

root = Tk()

def get_file_type(filepath):
    extension = "." + filepath.split('.')[-1]
    if extension in VIDEO_EXTENSIONS:
        return "video"
    if extension in AUDIO_EXTENSIONS:
        return "audio"
    if extension in IMAGE_EXTENSIONS:
        return "image"


def stream_video(video, delay, placeholder):
    try:
        image = video.get_next_data()
        frame = ImageTk.PhotoImage(Image.fromarray(image))
        placeholder.config(image=frame)
        placeholder.image = frame
        placeholder.after(delay, lambda: stream_video(video, delay, placeholder))
    except Exception as e:
        logs.print_log(e, "error")
        video.close()


def stream_audio(filepath):
    mixer.music.load(filepath)
    mixer.music.play()


def stream_image(filepath):
    frame = Frame()
    placeholder = Label(frame)
    placeholder.pack()
    frame.pack()

    image = ImageTk.PhotoImage(Image.open(filepath))
    placeholder.config(image=image)
    placeholder.image = image


def stream(filepath="1.mkv"):
    pyplot.switch_backend('Agg')
    print("Streaming "+filepath)

    #root.title(filepath)

    file_type = get_file_type(filepath)
    if file_type == "video":
        frame = Frame()
        placeholder = Label(frame)
        placeholder.pack()
        frame.pack()

        content = imageio.get_reader(filepath)
        delay = int(1000 / content.get_meta_data()['fps'])
        duration = int(content.get_meta_data()['duration']+1)
        stream_video(content, delay, placeholder)
        root.after(duration*1000, lambda: root.destroy())

    elif file_type == "audio":
        duration = int(mixer.Sound(filepath).get_length()+1)
        stream_audio(filepath)
        root.after(duration*1000, lambda: root.destroy())

    elif file_type == "image":
        stream_image(filepath)

    root.mainloop()

def main():
    print("In main of streamers.py")
    file = '/Users/maniklaldas/Desktop/Sem 3-1/AI/Assignmnt/sahyata/behaviour/rectification/../../content/resources/dog_JaV8fNT.mp4'
    stream(file)

if __name__ == "__main__":
    # file = '/Users/maniklaldas/Desktop/Sem 3-1/AI/Assignmnt/sahyata/behaviour/rectification/../../content/resources/dog_JaV8fNT.mp4'
    # stream(file)
    main()
