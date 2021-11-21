import tkinter as tk
import imageio
from pygame import mixer
from PIL import Image, ImageTk

file = input("Enter file path: ")     

window = tk.Tk()

def stream_video(video, delay, placeholder):
    image = video.get_next_data()
    videoframe = ImageTk.PhotoImage(Image.fromarray(image))
    placeholder.config(image=videoFrame)
    placeholder.image = videoFrame
    placeholder.after(delay, lambda: stream_video(video, delay, placeholder))

def initialised():
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

quesFrame = tk.Frame(borderwidth = 10, master = window)
videoFrame = tk.Frame(borderwidth = 10, master = window)
inputFrame = tk.Frame(borderwidth = 10, master = window)

welcomeFrame = tk.Frame(borderwidth = 10, master = window)
welcomeScreen = tk.Label(master = welcomeFrame, text = "Welcome to SAHyATA \n Please enter your details and click Submit", fg = "black", bg = "white", width = 120, height = 10, font = 100)
nameLabel = tk.Label(master = welcomeFrame, text = "Name: ", fg = "black", bg = "white", width = 60, height = 2, font = 30)
nameEntry = tk.Entry(master = welcomeFrame, fg = "black", bg = "white", width = 60, font = 30)
IDLabel = tk.Label(master = welcomeFrame, text = "ID: ", fg = "black", bg = "white", width = 60, height = 2, font = 30)
IDEntry = tk.Entry(master = welcomeFrame, fg = "black", bg = "white", width = 60, font = 30)
ColorLabel = tk.Label(master = welcomeFrame, text = "Color preferences: ", fg = "black", bg = "white", width = 60, height = 2, font = 30)
ColorEntry = tk.Entry(master = welcomeFrame, fg = "black", bg = "white", width = 60, font = 30)
submitButton = tk.Button(master = welcomeFrame, text = "Submit", height = 4, width = 14, command = initialised)

quesBox = tk.Label(master = quesFrame, text = "QUESTION WILL BE DISPLAYED HERE", fg="white", bg="black", width=90, height=25, font=100)
textBox = tk.Text(master = inputFrame, width = 45, height = 23)
prevButton = tk.Button(master = inputFrame, text = "Previous", height = 2, width = 7)
nextButton = tk.Button(master = inputFrame, text = "Next", height = 2, width = 7)

welcomeFrame.pack()
welcomeScreen.pack()
# nameLabel.pack(side = tk.LEFT)
nameLabel.pack()
nameEntry.pack()
# IDLabel.pack(side = tk.LEFT)
IDLabel.pack()
IDEntry.pack()
ColorLabel.pack()
ColorEntry.pack()
submitButton.pack()

window.mainloop()
