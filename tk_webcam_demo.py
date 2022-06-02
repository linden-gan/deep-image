import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np

width, height = 640, 380
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def handle_click1(e):
    print("cam1 clicked")
    print(e.x, e.y)
    global entry
    print(entry.get())

def handle_click2(e):
    print("cam2 clicked")
    print(e.x, e.y)


window = tk.Tk()
window.title("Webcam demo")
window.bind('<Escape>', lambda e: window.quit())

frame1 = tk.Frame(master=window, width=1300, height=600)
lcam1 = tk.Label(master=frame1, width=640, height=380)
lcam1.pack(padx=5, pady=10, side=tk.LEFT)
lcam1.bind("<Button-1>", handle_click1)

lcam2 = tk.Label(master=frame1, width=640, height=380)
lcam2.pack(padx=5, pady=10, side=tk.LEFT)
lcam2.bind("<Button-1>", handle_click2)

frame1.pack()

frame2 = tk.Frame(master=window)
text = tk.Label(master=frame2, text="Please input blabla:", fg="black")
text.pack(padx=5, pady=10, side=tk.LEFT)

entry = tk.Entry(master=frame2)
entry.pack(padx=5, pady=10, side=tk.LEFT)

def button_callback():
    global entry,cap,result_text
    print(f"your current input is {entry.get()}")
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite('webcamcap.png', frame)
    print('img saved')

    result_text["text"] = f"your current input is {entry.get()}"

button = tk.Button(master=frame2, text="Print out input and save webcam capture img", command=button_callback)
button.pack(padx=5, pady=10, side=tk.LEFT)

result_text = tk.Label(master=frame2, text="", fg="black")
result_text.pack(padx=5, pady=10, side=tk.LEFT)

frame2.pack(side=tk.LEFT)


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lcam1.imgtk = imgtk
    lcam1.configure(image=imgtk)
    lcam1.after(50, show_frame)
    

def show_frame2():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lcam2.imgtk = imgtk
    lcam2.configure(image=imgtk)
    lcam2.after(50, show_frame2)

show_frame()
show_frame2()
window.mainloop()