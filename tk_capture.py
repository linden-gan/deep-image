from ast import Return
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import sys
from tk_disparity import compute_disparity
from traditional.cutil import compute_depth

LAST_CLICK_POS = None

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

LAST_CLICK_POS = None

def handle_click_left(e):
    global LAST_CLICK_POS
    print("left cam clicked")
    x = CAMERA_WIDTH - 1 if e.x >= CAMERA_WIDTH - 20 else e.x
    y = CAMERA_HEIGHT - 1 if e.y >= CAMERA_HEIGHT else e.y
    LAST_CLICK_POS = (x, y)
    print(x)
    print(y)
    

def handle_click_right(e):
    print("right cam clicked")

def handle_exit(e):
    left.release()
    right.release()
    window.quit()
    exit()

window = tk.Tk()
window.title("Real Time Depth Display")
window.bind('<Escape>', handle_exit)

frame_big = tk.Frame(master=window, width=1300, height=500)
caml = tk.Label(master=frame_big, width=620, height=480)
caml.pack(padx=5, pady=10, side=tk.LEFT)
caml.bind("<Button-1>", handle_click_left)

camr = tk.Label(master=frame_big, width=620, height=480)
camr.pack(padx=5, pady=10, side=tk.LEFT)
camr.bind("<Button-1>", handle_click_right)

frame_big.pack()

frame_input_fov = tk.Frame(master=window)
text = tk.Label(master=frame_input_fov, text="Please input your camera's field of view (FOV):", fg="black")
text.pack(padx=5, pady=10, side=tk.LEFT)

entry_fov = tk.Entry(master=frame_input_fov)
entry_fov.pack(padx=5, pady=10, side=tk.LEFT)

fov = 150.0
baseline = 0.155

def button_callback_fov():
    global entry_fov, result_text_fov, fov
    print(f"your current input FOV is {entry_fov.get()}")

    fov = float(entry_fov.get())
    result_text_fov["text"] = f"\nyour current input FOV is {entry_fov.get()}"

def button_callback_baseline():
    global entry_baseline, result_text_baseline, baseline
    print(f"your current input baseline is {entry_baseline.get()}")

    baseline = float(entry_baseline.get())
    result_text_baseline["text"] = f"\nyour current input baseline is {entry_baseline.get()}"

button = tk.Button(master=frame_input_fov, text="Print out input FOV", command=button_callback_fov)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text_fov = tk.Label(master=frame_input_fov, text="", fg="black")
result_text_fov.pack(padx=5, pady=10, side=tk.LEFT)

frame_input_fov.pack(side=tk.LEFT)

frame_input_baseline = tk.Frame(master=window)
text = tk.Label(master=frame_input_baseline, text="Please input the baseline (distance) between your cameras:", fg="black")
text.pack(padx=5, pady=10, side=tk.LEFT)

entry_baseline = tk.Entry(master=frame_input_fov)
entry_baseline.pack(padx=5, pady=10, side=tk.LEFT)

button = tk.Button(master=frame_input_baseline, text="Print out input baseline", command=button_callback_baseline)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text_baseline = tk.Label(master=frame_input_baseline, text="", fg="black")
result_text_baseline.pack(padx=5, pady=10, side=tk.LEFT)

frame_input_baseline.pack(side=tk.LEFT)

leftFrame = np.zeros(2)
rightFrame = np.zeros(2)

def get_two_frames():
    global leftFrame, rightFrame
    if not (left.grab() and right.grab()):
        print("No more frames")
        exit()
    
    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
CROP_WIDTH = 620
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

def show_frame_left():
    get_two_frames()
    # add ciricle if some cordinate is clicked
    leftFrame_dotted = cropHorizontal(leftFrame)
    if LAST_CLICK_POS is not None:
        # note that color is BGR
        leftFrame_dotted = cv2.circle(leftFrame_dotted, LAST_CLICK_POS, radius=3, color=(0, 0, 255), thickness=-1)

    cv2image = cv2.cvtColor(leftFrame_dotted, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    caml.imgtk = imgtk
    caml.configure(image=imgtk)
    caml.after(50, show_frame_left)

def show_frame_right():
    rightFrameCrop = cropHorizontal(rightFrame)
    cv2image = cv2.cvtColor(rightFrameCrop, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    camr.imgtk = imgtk
    camr.configure(image=imgtk)
    camr.after(50, show_frame_right)

label = tk.Label(window, text="", fg="red")
label.pack(padx=5, pady=10, side=tk.LEFT)

def show_depth():
    global LAST_CLICK_POS, label
    if LAST_CLICK_POS is not None:
        disparity = compute_disparity(leftFrame, rightFrame)
        curr_depth = compute_depth(disparity, fov, baseline, LAST_CLICK_POS[0], LAST_CLICK_POS[1])
        label["text"] = str(round(curr_depth, 3))
        print(round(curr_depth, 3))
    label.after(1000, show_depth)

show_frame_left()
show_frame_right()
show_depth()

window.mainloop()