from ast import Return
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import sys
from tk_disparity import compute_disparity

LEFT_PATH = sys.path[0] + "\capture\cleft\{:06d}.jpg"
RIGHT_PATH = sys.path[0] + "\capture\cright\{:06d}.jpg"

left = cv2.VideoCapture(0, cv2.CAP_DSHOW)
right = cv2.VideoCapture(2, cv2.CAP_DSHOW)

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
    compute_disparity(frameId)

def handle_click_right(e):
    print("cam2 clicked")
    print(e.x, e.y)
    compute_disparity(frameId)

def handle_exit(e):
    left.release()
    right.release()
    window.quit()
    exit()

window = tk.Tk()
window.title("Real Time Depth Display")
window.bind('<Escape>', handle_exit)

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

    result_text["text"] = f"your current input is {entry.get()}"

button = tk.Button(master=frame_input, text="Print out input", command=button_callback)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text = tk.Label(master=frame_input, text="", fg="black")
result_text.pack(padx=5, pady=10, side=tk.LEFT)

frame_input.pack(side=tk.LEFT)

frameId = 0
leftFrame = np.zeros(2)
rightFrame = np.zeros(2)

def get_two_frames():
    global frameId, leftFrame, rightFrame
    if not (left.grab() and right.grab()):
        print("No more frames")
        exit()
    
    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

    if not cv2.imwrite(LEFT_PATH.format(frameId), leftFrame):
        raise Exception("Could not write image")
    if not cv2.imwrite(RIGHT_PATH.format(frameId), rightFrame):
        raise Exception("Could not write image")

    frameId += 1

def show_frame_left():
    get_two_frames()
    cv2image = cv2.cvtColor(leftFrame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    caml.imgtk = imgtk
    caml.configure(image=imgtk)
    caml.after(1000, show_frame_left)

def show_frame_right():
    cv2image = cv2.cvtColor(rightFrame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    camr.imgtk = imgtk
    camr.configure(image=imgtk)
    camr.after(1000, show_frame_right)

show_frame_left()
show_frame_right()

window.mainloop()