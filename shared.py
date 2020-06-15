#Main gui is the main gui which will run them please run from there and maximize the window
import tkinter as Tk
from tkinter import *
import sys

def on_click():
    said = textbox.get()
    print(said)
    window.destroy()
    return said


window =Tk()
textbox = Entry(window, width=60)
textbox.pack(side=TOP)
Button(window, text="Send", width=8, command=lambda: on_click()).pack(side=BOTTOM)
window.mainloop()
