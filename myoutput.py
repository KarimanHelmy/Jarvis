from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText
# This code was a snippet from a book but I edited it for my convenience
class guiOutput:
    font = ('courier', 10, 'normal') # font type courier, size 9, normal # in class for all, self for one

    def __init__(self, parent=None):#parent is set to none so it can accept mainGui as a parent
        self.text = None
        if parent:
            self.show(parent)         # pop up now or on first write  if there is a parent

    def show(self, parent=None):             # in parent now,
        if self.text:# if there is no text return nothing : )
            return
        self.text = ScrolledText(parent)
        self.text.config(font=self.font)
        self.text.pack() #organize child widget into a block before putting it in parent widget which in this case is mainGui

    def writes(self, text):
        self.show()
        self.text.insert(END, text) #show text after last character stored in data, text in jarvis is already str no need to str anything :)
        self.text.see(END)# given position in the end is visible
        self.text.update()   # update guiOutput with text

    def writeLine(self, lines):
        for line in lines:
            self.writes(line)

