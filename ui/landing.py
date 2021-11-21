import tkinter as tk
import imageio
from pygame import mixer
from PIL import Image, ImageTk

file = input("Enter file path: ")	

window = tk.Tk()

quesFrame = tk.Frame(borderwidth = 10, master = window)
videoFrame = tk.Frame(borderwidth = 10, master = window)
inputFrame = tk.Frame(borderwidth = 10, master = window)

quesBox = tk.Label(master = quesFrame, text = "QUESTION WILL BE DISPLAYED HERE", fg="white", bg="black", width=90, height=25, font=100)
textBox = tk.Text(master = inputFrame, width = 45, height = 23)
prevButton = tk.Button(master = inputFrame, text = "Previous", height = 2, width = 7)
nextButton = tk.Button(master = inputFrame, text = "Next", height = 2, width = 7)

def stream_video(video, delay, placeholder):
    image = video.get_next_data()
    videoframe = ImageTk.PhotoImage(Image.fromarray(image))
    placeholder.config(image=videoFrame)
    placeholder.image = videoFrame
    placeholder.after(delay, lambda: stream_video(video, delay, placeholder))

placeholder = tk.Label(videoFrame)
placeholder.pack()
videoFrame.pack(side = tk.RIGHT)

content = imageio.get_reader(file)
delay = int(1000 / content.get_meta_data()['fps'])
duration = int(content.get_meta_data()['duration']+1)
stream_video(content, delay, placeholder)

quesFrame.pack(side = tk.LEFT)
videoFrame.pack(side = tk.RIGHT)
inputFrame.pack(side = tk.RIGHT)

quesBox.pack()
textBox.pack()
prevButton.pack(side = tk.LEFT)
nextButton.pack(side = tk.RIGHT)

window.mainloop()
