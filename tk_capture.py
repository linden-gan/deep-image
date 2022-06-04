from ast import Return
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import sys
from tk_disparity import compute_disparity
from traditional.cutil import compute_depth

REMAP_INTERPOLATION = cv2.INTER_LINEAR

calibration = np.load(sys.path[0] + "\cam\calib.npz", allow_pickle=False)
imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

LAST_CLICK_POS = None

left = cv2.VideoCapture(0, cv2.CAP_DSHOW)
right = cv2.VideoCapture(2, cv2.CAP_DSHOW)

CAMERA_WIDTH, CAMERA_HEIGHT = 1024, 576
left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

LAST_CLICK_POS = None
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

def handle_click_left(e):
    global LAST_CLICK_POS
    print("left cam clicked")
    x = e.x * CROP_WIDTH / DISPLAY_WIDTH
    y = e.y * CAMERA_HEIGHT / DISPLAY_HEIGHT
    x = DISPLAY_WIDTH - 1 if e.x >= DISPLAY_WIDTH else e.x
    y = DISPLAY_HEIGHT - 1 if e.y >= DISPLAY_HEIGHT else e.y
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
caml = tk.Label(master=frame_big, width=640, height=480)
caml.pack(padx=5, pady=10, side=tk.LEFT)
caml.bind("<Button-1>", handle_click_left)

camr = tk.Label(master=frame_big, width=640, height=480)
camr.pack(padx=5, pady=10, side=tk.LEFT)
camr.bind("<Button-1>", handle_click_right)

frame_big.pack()

frame_input_parent = tk.Frame(master=window)

frame_input_fov = tk.Frame(master=frame_input_parent)
text = tk.Label(master=frame_input_fov, text="Please input your camera's field of view (FOV) in degree, default = 90:", fg="black")
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

button = tk.Button(master=frame_input_fov, text="Confirm FOV", command=button_callback_fov)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text_fov = tk.Label(master=frame_input_fov, text="", fg="black")
result_text_fov.pack(padx=5, pady=10, side=tk.LEFT)

# frame_input_fov.pack(side=tk.LEFT)
frame_input_fov.grid(row=0, column=0, sticky='w')

frame_input_baseline = tk.Frame(master=frame_input_parent)
text = tk.Label(master=frame_input_baseline, text="Please input the baseline (distance) between your cameras in meter, default = 0.155:", fg="black")
text.pack(padx=5, pady=10, side=tk.LEFT)

entry_baseline = tk.Entry(master=frame_input_baseline)
entry_baseline.pack(padx=5, pady=10, side=tk.LEFT)

button = tk.Button(master=frame_input_baseline, text="Confirm Baseline", command=button_callback_baseline)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text_baseline = tk.Label(master=frame_input_baseline, text="", fg="black")
result_text_baseline.pack(padx=5, pady=10, side=tk.LEFT)

# frame_input_baseline.pack(side=tk.LEFT)
frame_input_baseline.grid(row=1, column=0, sticky='w')

frame_input_parent.pack(side=tk.LEFT)

leftFrame = np.zeros(2)
rightFrame = np.zeros(2)
fixedLeft = np.zeros(2)
fixedRight = np.zeros(2)

def get_two_frames():
    global leftFrame, rightFrame, fixedLeft, fixedRight
    if not (left.grab() and right.grab()):
        print("No more frames")
        exit()
    
    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()
    leftFrame = cropHorizontal(leftFrame)
    leftHeight, leftWidth = leftFrame.shape[:2]
    rightFrame = cropHorizontal(rightFrame)
    rightHeight, rightWidth = rightFrame.shape[:2]

    if (leftWidth, leftHeight) != imageSize:
        print("Left camera has different size than the calibration data")
        return

    if (rightWidth, rightHeight) != imageSize:
        print("Right camera has different size than the calibration data")
        return

    

    fixedLeft = cv2.remap(leftFrame, leftMapX, leftMapY, REMAP_INTERPOLATION)
    fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)


CROP_WIDTH = 980
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

def show_frame_left():
    get_two_frames()
    # add ciricle if some cordinate is clicked
    leftFrame_dotted = leftFrame.copy()
    resizedLeft = cv2.resize(leftFrame_dotted, (640, 480), interpolation = REMAP_INTERPOLATION)
    if LAST_CLICK_POS is not None:
        # note that color is BGR
        resizedLeft = cv2.circle(resizedLeft, LAST_CLICK_POS, radius=3, color=(0, 0, 255), thickness=-1)

    cv2image = cv2.cvtColor(resizedLeft, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    caml.imgtk = imgtk
    caml.configure(image=imgtk)
    caml.after(50, show_frame_left)

def show_frame_right():
    resizedRight = cv2.resize(rightFrame, (640, 480), interpolation = REMAP_INTERPOLATION)
    cv2image = cv2.cvtColor(resizedRight, cv2.COLOR_BGR2RGBA)
    
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    camr.imgtk = imgtk
    camr.configure(image=imgtk)
    camr.after(50, show_frame_right)

label = tk.Label(window, text="", fg="red", font="12px")
label.pack(padx=5, pady=10, side=tk.LEFT)

def show_depth():
    global LAST_CLICK_POS, label
    if LAST_CLICK_POS is not None:
        disparity = compute_disparity(fixedLeft, fixedRight)
        curr_depth = compute_depth(disparity, fov, baseline, LAST_CLICK_POS[0], LAST_CLICK_POS[1])
        label["text"] = f"depth at the red dot: {str(round(curr_depth, 3))}"
        # print(round(curr_depth, 3))
    label.after(1000, show_depth)

show_frame_left()
show_frame_right()
show_depth()

window.mainloop()