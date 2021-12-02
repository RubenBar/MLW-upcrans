#Import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser

#Create an instance of tkinter
win=Tk()

#Set the windows geometry
win.geometry("450x350")
win.title("Ransomware Decryptor")

#Create an object of tkinter image
img = PhotoImage(file = "Interface/alert.png")
img = img.subsample(2, 2)

#Create Canvas
canvas1 = Canvas( win, width = 400, height = 400)
canvas1.pack(fill="both", expand = True)
canvas1.create_image(50, 50, image = img, anchor="nw")

canvas1. create_text(225, 30, text = "Your files have been encrypted!!!", font='bold 18', fill="red")

win.mainloop()
