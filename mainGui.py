import _thread as thread
import os
import queue
import subprocess
import sys
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from itertools import count
import myoutput
from myoutput import guiOutput
stdoutQueue = queue.Queue() #queue size is infinite in order to avoid block : )

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):#check if im is string
            im = Image.open(im)# open image
        self.loc = 0
        self.frames = [] #set frame as empty frames

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))#append copy image while keeping original image
                im.seek(i)#seek given frame in the sequnece and it never close the file unlike load
        except EOFError: #catch error and pass
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100 #delay self for 100 sec

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame() #begin next frame class

    def next_frame(self):
        if self.frames:
            self.loc += 1# add one to loc
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame) # after self delay value continue to function self.next_frame


def produce(input):
    while True:
        #reads a line of  jarvis and return it in the form of the string
        line = input.readline()
        stdoutQueue.put(line)  # get line :)
        if not line:
            break


def consume(output, root, term='program terminated thank you for using jarvis'):
    try:
        #main thread check queue and put whatever found it in line
        line = stdoutQueue.get(block=False)   #we do not need to block until another queue is empty so it's set to false
        # pass if empty
    except queue.Empty:
        pass
    else:
        if not line:
            output.writes(term)  # stop loop at the end of the line if there is no line and display program terminated.....
            return
        output.writes(line)  # else display next line that has been inputed from produce
    root.after(200, lambda: consume(output, root, term)) #refresh  window after 200 sec
def redirect_Gui(command, root):
    input = os.popen(command, 'r')  # start jarvis and open it for reading only : ) no input :( although r+ could be used for both
    output = guiOutput(root)
    # start the thread code produce which read line by line from input (jarvis)
    thread.start_new_thread(produce, (input,))  #the function is produce and we throw it input
    #begin class consume throw it ouput and window parameters
    consume(output, root)


if __name__=='__main__':
    window = tk.Tk()
    window.geometry("484x670")
    window.title("Jarvis assistant")
    lbl = ImageLabel(window)
    lbl.pack()
    lbl.load('D:\\university\\cs2\\ja.gif') #change it according to the path u download in project
    # begin re direct class throw it the required parameter which is jarvis py opened by python and window is root
    redirect_Gui('python -u jarvis.py', window) # ps: u parameter to force jarvis not to print anything or take input from terminal
    window.mainloop()
