from urllib import request
from datetime import datetime
from tkinter import *
import requests
import os
import time
import sys
import animation

root = Tk()
root.title("4Chan-App")

def Clear():
    for widget in root.winfo_children():
        widget.destroy()

def mainMenu():
    Clear()
    Button(root, text="Here").pack()



mainMenu()
root.mainloop()
