from urllib import request
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import requests
import os
import time
import sys
import ast
import ssl

root = Tk()

a = scrolledtext.ScrolledText(root, height=30, width=110)
f = open("console.txt", "r")
print(str(f.readline()))
for line in f.readlines():
    a.insert(INSERT, str(line))
a.pack()
a.configure(state="disabled")
f.close()



root.mainloop()
