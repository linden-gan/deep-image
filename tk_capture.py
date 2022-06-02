from ast import Return
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import sys
from threading import Thread

LEFT_PATH = sys.path[0] + "\capture\cleft\{:06d}.jpg"
RIGHT_PATH = sys.path[0] + "\capture\cright\{:06d}.jpg"

left = cv2.VideoCapture(0, cv2.CAP_DSHOW)
right = cv2.VideoCapture(1)

CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

def handle_click_left(e):
    print("cam1 clicked")
    print(e.x, e.y)
    # global entry
    # print(entry.get())

def handle_click_right(e):
    print("cam2 clicked")
    print(e.x, e.y)

window = tk.Tk()
window.title("Real Time Depth Display")
window.bind('<Escape>', lambda e: window.quit())

frame_big = tk.Frame(master=window, width=1300, height=500)
caml = tk.Label(master=frame_big, width=640, height=480)
caml.pack(padx=5, pady=10, side=tk.LEFT)
caml.bind("<Button-1>", handle_click_left)

camr = tk.Label(master=frame_big, width=640, height=480)
camr.pack(padx=5, pady=10, side=tk.LEFT)
camr.bind("<Button-1>", handle_click_right)

frame_big.pack()

frame_input = tk.Frame(master=window)
text = tk.Label(master=frame_input, text="Please input your camera's field of view (FOV):", fg="black")
text.pack(padx=5, pady=10, side=tk.LEFT)

entry = tk.Entry(master=frame_input)
entry.pack(padx=5, pady=10, side=tk.LEFT)

def button_callback():
    global entry, result_text
    print(f"your current input is {entry.get()}")
    # _, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    # cv2.imwrite('webcamcap.png', frame)
    # print('img saved')

    result_text["text"] = f"your current input is {entry.get()}"

button = tk.Button(master=frame_input, text="Print out input and save webcam capture img", command=button_callback)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text = tk.Label(master=frame_input, text="", fg="black")
result_text.pack(padx=5, pady=10, side=tk.LEFT)

frame_input.pack(side=tk.LEFT)

frameId = 0

def show_two_frames():
    global frameId
    if not (left.grab() and right.grab()):
        print("No more frames")
        exit()
    
    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

    # if not cv2.imwrite(LEFT_PATH.format(frameId), leftFrame):
    #     raise Exception("Could not write image")
    # if not cv2.imwrite(RIGHT_PATH.format(frameId), rightFrame):
    #     raise Exception("Could not write image")
    
    t1 = Thread(target=show_frame_left, args=(leftFrame,))
    t2 = Thread(target=show_frame_right, args=(rightFrame,))

    t1.start()
    t1.setDaemon(True)
    t2.start()
    t2.setDaemon(True)

    t1.join()
    t2.join()

    frameId += 1
    show_two_frames()

def show_frame_left(frame):
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    caml.imgtk = imgtk
    caml.configure(image=imgtk)
    caml.after(50)

def show_frame_right(frame):
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    camr.imgtk = imgtk
    camr.configure(image=imgtk)
    camr.after(50)

show_two_frames()

window.mainloop()