from urllib import request
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import requests
import threading
import psutil
import os
import time
import sys
import ast
import ssl

global menuState

ssl._create_default_https_context = ssl._create_unverified_context

destination = "Desktop"

root = Tk()
config = {"width":53, "height":4, "font":"Consolas 21 bold"}
root.title("4Chan-App")
root.geometry()
root.configure(bg="#353839")


# Clears the window
def Clear():
    for widget in root.winfo_children():
        widget.destroy()


# Once the Start/Stop button is pushed it will either start or stop downloading depending on if the process is running or not
def mainmenuControls(menuState):
    if menuState == "start" and selectionsExist():
        f = open("EnabledSelections.txt", "r+")
        if f.readline == "":
            messagebox.showinfo(title="Bruh", message="Please check off a filter you want to apply before continuing.")
            addQueryMenu()
        startorstopDownload("start")
        mainMenu("started")

    elif menuState == "started":
        startorstopDownload("stop")
        mainMenu("start")


# Will determine what the main menu is supposed to look like
def mainmenuInit(menuState):
    if not os.path.exists("Selections.txt"):
        return  {"color": "light gray", "state": "disabled", "text": "Start", "menuState": "started", "command":"setup"}
    elif menuState == "start":
        return {"color": "green", "state": "normal", "text": "Start", "menuState": "started", "command":"default"}
    elif menuState == "started":
        return {"color": "red", "state": "normal", "text": "Stop", "menuState": "start", "command":"default"}
    else:
        return {"color": "red", "state": "normal", "text": "Stop", "menuState": "start", "command":"default"}


# Makes sure the download process has stopped and closes the program
def Exit():
    if getMenuState() == "started":
        startorstopDownload("stop")
    root.destroy()
    

# The main menu. Will configure it's button's settings with the function mainmenuInit which returns a dictionary of settings
# First button will change to either start or stop depending on if the download process is running or not
# Second will take the user to the adding selection menu
# Third will open the console that the download process produced for the user to read
# Fourth will open settings
# Fifth will close the app and stop the download process
def mainMenu(menuState="start"):
    Clear()
    settings = mainmenuInit(menuState)
    Button(root, **config, text=settings["text"], bg=settings["color"], command=lambda:mainmenuControls(menuState), state=settings["state"]).pack(fill="x", pady=2)
    Button(root, **config, text="Presets", bg="dark gray", command=lambda:addQueryMenu(settings["command"])).pack(fill="x", pady=2)
    Button(root, **config, text="Console", bg="dark gray", command=consoleMenu).pack(fill="x", pady=2)
    Button(root, **config, text="Settings", bg="dark gray").pack(fill="x", pady=2)
    Button(root, **config, text="Exit", bg="red", command=lambda:Exit()).pack(fill="x", pady=2)
    root.geometry()

# When a list of stringvars is passed in it will get the correlating values using .get()
# If a checkmark is detected it will write it to a file called EnabledSelections.txt
def addEnabledSelection(varlist):  
    count = 0
    f_list = getSelections()
    text = ""

    for titlevar in varlist:
        if titlevar.get() == "0":
            count += 1
            continue

        elif titlevar.get() == "1":
            text += str(f_list[count]) + "\n"
            count += 1

    f = open("EnabledSelections.txt", "w+")
    f.write(text)
    f.close
    mainMenu(getMenuState())


# A window that will display the title of all the different selections previously created by the user
# Pressing the back button will save and go back a page
# Creates a stringvar and appends that to a list in a loop which will go to addEnabledSelection() 
def checkBoxes():
    Clear()
    global varlist
    root.geometry()
    newFrame = Frame(root, bg="#353839")
    count = 0
    varlist = []
    for title in getSelections():
        # Iterates through lists in the Selections.txt
        title = title[0]
        titlevar = title + str(count)
        titlevar = StringVar(value=0)
        Checkbutton(newFrame, **config, text=title, variable=titlevar, onvalue="1", offvalue="0", bg="dark gray", compound="top", relief="raised").pack(anchor="w", pady=2, padx=2)
        varlist.append(titlevar)
        count += 1
    newFrame.grid(column=0, row=0, sticky="nesw")


# Retrieves the fields information and converts it into a list, then it's saved to Selections.txt
def addSearchIndex(title, board, whitelist, blacklist, command="none"):
    if command == "none":
        title = title.get()
        board = board.get()
        whitelist = [s.strip() + ',' for s in whitelist.get().split(',') if s.strip()]
        blacklist = [s.strip() + ',' for s in blacklist.get().split(',') if s.strip()]

        # Doesn't let you proceed if you forgot to add a board
        if board == "":
            messagebox.showinfo(title="Bruh", message="Please enter a valid board.")
            addQueryMenu(command="setup")
            return

    selections = [title, board, [item for item in whitelist], [item for item in blacklist]]
    f = open("Selections.txt", "a+")
    f.write(str(selections) + "\n" )
    f.close
    addQueryMenu()


# The menu that contains the checkbox and query frame.
def addQueryMenu(command="default"):
    Clear()
    menuState = getMenuState()
    if command == "default":
        checkBoxes()
    print(root.grid_size())

    queryFrame = Frame(root, bg="dark gray")

    title = StringVar()
    board = StringVar()
    whitelist = StringVar()
    blacklist = StringVar()

    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Title:").grid(column=0, row=0, pady=2)
    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Board:").grid(column=0, row=1, pady=2)
    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Whitelist:").grid(column=0, row=2, pady=2)
    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Blacklist:").grid(column=0, row=3, pady=2)

    e1 = Entry(queryFrame, font="Consolas 21 bold",)
    e2 = Entry(queryFrame, font="Consolas 21 bold",)
    e3 = Entry(queryFrame, font="Consolas 21 bold",)
    e4 = Entry(queryFrame, font="Consolas 21 bold",)

    e1.grid(column=1, row=0, pady=2)
    e2.grid(column=1, row=1, pady=2)
    e3.grid(column=1, row=2, pady=2)
    e4.grid(column=1, row=3, pady=2)

    Button(root, **config, bg="green", text="Save", command=lambda:addSearchIndex(e1, e2, e3, e4)).grid(sticky="e", row=1, column=1)
    queryFrame.grid(column=1, row=0, sticky="ew")

    # Will go to back to main menu if the user hasn't made a filter yet
    if command == "setup":
        Button(root, **config, bg="red", text="Back", command=lambda:mainMenu(menuState)).grid(sticky="w", row=1, column=0)
    # Otherwise this will create a back button that will save the input to Selections.txt and return to main menu
    else:
        Button(root, **config, bg="red", text="Back", command=lambda:addEnabledSelection(varlist)).grid(sticky="w", row=1, column=0)
    root.geometry()


# A menu that will display what the console has been outputting, time, file, match, board, etc.
def consoleMenu():
    Clear()
    menuFrame = Frame(root, bg="#353839")
    Button(menuFrame, **config, text="Back", bg="red", command=mainMenu).pack()
    menuFrame.pack(fill="x", side="top")

    print(root.winfo_screenwidth(), root.winfo_height())
    a = scrolledtext.ScrolledText(root, height=50, width=160, font="Consolas 15", background="dark gray")
    try:
        f = open("console.txt", "r")
    except :
        f = open("console.txt", "w+")

    for line in f.readlines():
        a.insert(INSERT, str(line))

    a.pack(side="bottom")
    a.configure(state="disabled")
    f.close()
    root.geometry()


# Opens an external .pyw file that downloads images to a directory and saves the output to a file
# Provide a command and the function will carry that out. But if in the wrong order will fail
def startorstopDownload(command):
    global proc
    if command == "start":
        proc = subprocess.Popen("console.pyw", shell=True)
    if command == "stop":
        process = psutil.Process(proc.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()


# Will check if the downloading process is running
def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


# Will return true if the download process is running and false if not
def getMenuState():
    if checkIfProcessRunning("pythonw.exe"):
        return "started"
    else:
        return "start"


# Returns true if there are selection within the file Selections.txt and false if none are found
def selectionsExist():
    selections = getSelections()
    if selections != None:
        return True
    elif selections == None:
        return False


# Returns a list of all lines in Selections.txt
def getSelections(command="default"):
    try:
        f = open("Selections.txt", "r+")
        ls = []
    except:
        messagebox.showinfo(title="Warning", message="Before proceeding please enter a search query")
        mainMenu("start")
    else:
        for line in f.readlines():
            temp = line.splitlines()
            print("Temp:", temp)
            w = str(temp)[2:-2]
            print("1", w)
            w = w.replace(",',", "',")
            w = w.replace(",']", "']")
            print("2", w)
            w = ast.literal_eval(w)
            ls.append(w)
            print("3", w)
            print("222", w, type(w))
        f.close()
        print("\n\n\n", ls, "\n\n\n")
        return ls


mainMenu()
root.mainloop()