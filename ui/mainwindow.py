import tkinter as tk
from tkinter import *
import imageio
from pygame import mixer
from PIL import Image, ImageTk

window = tk.Tk()

border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

VIDEO_EXTENSIONS = [".mkv", ".mp4", ".flv", ".srt", ".gif"]

frame1 = tk.Frame()
frame2 = tk.Frame()

def stream_video(video, delay, placeholder):
    image = video.get_next_data()
    frame = ImageTk.PhotoImage(Image.fromarray(image))
    placeholder.config(image=frame)
    placeholder.image = frame
    placeholder.after(delay, lambda: stream_video(video, delay, placeholder))


def stream(filepath="1.mkv"):
    root = Tk()
    root.title(filepath)

    frame = Frame()
    placeholder = Label(frame)
    placeholder.pack()
    frame.pack()

    content = imageio.get_reader(filepath)
    delay = int(1000 / content.get_meta_data()['fps'])
    duration = int(content.get_meta_data()['duration']+1)
    stream_video(content, delay, placeholder)
    root.after(duration*1000, lambda: root.destroy())

    root.mainloop()


if __name__ == "__main__":
    file = input("Enter file path: ")
    stream(file)
