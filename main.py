from urllib import request
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import requests
import threading
import os
import time
import sys
import ast
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

destination = "Desktop"

root = Tk()
root.title("4Chan-App")
root.geometry()
root.configure(bg="#353839")


def Clear():
    for widget in root.winfo_children():
        widget.destroy()

def mainmenuControls(menuState):
    if menuState == "start" and selectionsExist():
        mainMenu("started")
        root.update_idletasks()
        thread = threading.Thread(target=subprocess.run("run.bat", shell=True))
        thread.start()
        mainMenu()
        

    elif menuState == "started":
        imageSaverStop()


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


def mainMenu(menuState="start"):
    Clear()
    settings = mainmenuInit(menuState)
    Button(root, text=settings["text"], bg=settings["color"], command=lambda:mainmenuControls(menuState), state=settings["state"]).pack(fill="x", pady=2)
    Button(root, text="Presets", command=lambda:addQueryMenu(settings["command"])).pack(fill="x", pady=2)
    Button(root, text="Console", command=consoleMenu).pack(fill="x", pady=2)
    Button(root, text="Settings").pack(fill="x", pady=2)
    Button(root, text="Exit", bg="red", command=lambda:root.destroy()).pack(fill="x", pady=2)

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
    mainMenu()


# A window that will display the title of all the different selections previously created by the user
# Hitting the submit button will save and go back a page
# Creates a stringvar and appends that to a list in a loop which will go to addEnabledSelection() 
def checkBoxes():
    Clear()
    global varlist
    root.geometry()
    newFrame = Frame(root)
    count = 0
    varlist = []
    for title in getSelections():
        # Iterates through lists in the Selections.txt
        title = title[0]
        titlevar = title + str(count)
        titlevar = StringVar(value=0)
        Checkbutton(newFrame, text=title,variable=titlevar, onvalue="1", offvalue="0").pack(anchor="w")
        varlist.append(titlevar)
        count += 1
    newFrame.grid(column=0, row=0, sticky="nesw")


def addSearchIndex(title, board, whitelist, blacklist, command="none"):
    if command == "none":
        title = title.get()
        board = board.get()
        whitelist = [s.strip() + ',' for s in whitelist.get().split(',') if s.strip()]
        blacklist = [s.strip() + ',' for s in blacklist.get().split(',') if s.strip()]

        if board == "":
            messagebox.showinfo(title="Bruh", message="Please enter a valid board.")
            addQueryMenu()
            return

    selections = [title, board, [item for item in whitelist], [item for item in blacklist]]
    f = open("Selections.txt", "a+")
    f.write(str(selections) + "\n" )
    f.close
    addQueryMenu()

def addQueryMenu(command="default"):
    Clear()
    if command == "default":
        checkBoxes()
    print(root.grid_size())

    queryFrame = Frame(root)

    title = StringVar()
    board = StringVar()
    whitelist = StringVar()
    blacklist = StringVar()

    Label(queryFrame, text="Title:").grid(column=0, row=0, pady=2)
    Label(queryFrame, text="Board:").grid(column=0, row=1, pady=2)
    Label(queryFrame, text="Whitelist:").grid(column=0, row=2, pady=2)
    Label(queryFrame, text="Blacklist:").grid(column=0, row=3, pady=2)

    e1 = Entry(queryFrame)
    e2 = Entry(queryFrame)
    e3 = Entry(queryFrame)
    e4 = Entry(queryFrame)

    e1.grid(column=1, row=0, pady=2)
    e2.grid(column=1, row=1, pady=2)
    e3.grid(column=1, row=2, pady=2)
    e4.grid(column=1, row=3, pady=2)

    Button(queryFrame, text="Submit", command=lambda:addSearchIndex(e1, e2, e3, e4)).grid(sticky="s", columnspan=queryFrame.grid_size()[0])
    queryFrame.grid(column=1, row=0, sticky="ew")
    Button(root, text="Back", command=lambda:addEnabledSelection(varlist)).grid(sticky="s", columnspan=root.grid_size()[0])
    root.geometry()


def consoleMenu():
    Clear()
    menuFrame = Frame(root)
    Button(menuFrame, text="Back", command=mainMenu).pack()
    menuFrame.pack(fill="x", side="top")

    print(root.winfo_screenwidth(), root.winfo_height())
    a = scrolledtext.ScrolledText(root, height=50, width=160, font="Consolas 15", foreground="#00FF00", background="#353839")
    f = open("console.txt", "r")

    for line in f.readlines():
        a.insert(INSERT, str(line))

    a.pack(side="bottom")
    a.configure(state="disabled")
    f.close()
    print(root.winfo_width(), root.winfo_height())



def imageSaver(selections, destination=destination):
    print("95", selections, len(selections), type(selections))
    count = 0
    json = requests.get("https://a.4cdn.org/" + selections[1] + "/catalog.json").json()

    # Sorts by the threads in each page
    for page in range(len(json) - 1):

        # Sorts through individual threads within a page
        for thread in range(len(json[1]["threads"]) - 1):
            downloading = True

            # Gets the title from the metadata found within the thread's .json
            try:
                title = titleCleanup(str(json[page]["threads"][thread]["com"]).lower() + str(json[page]["threads"][thread]["sub"]).lower())
            except:
                try:
                    title = titleCleanup(str(json[page]["threads"][thread]["com"]).lower())
                except:
                    continue

            # Blacklist filter
            for word in selections[3]:
                if word in title:
                    continue

            # Searches through threads when given the keyword of the preset
            for word in selections[2]:

                # Will go into this block if the comment of a post matches one of the keywords
                if word in title:
                    # Gets the .json of the thread
                    c = requests.get("https://a.4cdn.org/" + selections[1] + "/thread/" + str(json[page]["threads"][thread]["no"]) + ".json").json()

                    # Looks through the .json of the individual comment using the range of however many comments are within the thread
                    for comment in range(len(c["posts"]) - 1):

                        # Sometimes there are no images on a comment hence the try, except
                        try:
                            link = "https://is2.4chan.org/" + selections[1] + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"]
                        except:
                            continue

                        # If there is no path with the same board and preset name it makes one and starts downloading the images there
                        if not os.path.exists(destination + "/" + selections[1] + "/" + selections[0].capitalize()):
                            os.makedirs(destination + "/" + selections[1] + "/" + selections[0].capitalize())

                        # If the same file exists it continues to avoid downloading again
                        if os.path.exists(destination + "/" + selections[1] + "/" + selections[0].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"]):
                            continue

                        request.urlretrieve(link, destination + "/" + selections[1] + "/" + selections[0].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"])
                        count += 1

                        if downloading:
                            print("--------------------------------------------------------------------------------------------")
                            print(datetime.now().strftime(
                                "%H:%M") + " | Link: https://boards.4chan.org/" + selections[1] + "/thread/" + str(
                                json[page]["threads"][thread]["no"]))
                            print(datetime.now().strftime("%H:%M") + " | Thread: " + title + " | /" + selections[1] + "/")
                            print(datetime.now().strftime("%H:%M") + " | Match: " + word)

                        print(datetime.now().strftime("%H:%M") + " | Downloaded: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + selections[1] + "/" + selections[0].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " | " + str(count))
                        downloading = False
                        #sys.stdout.write("\rDownloading: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + board + "/" + preset.capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"])


def imageSaverStop():
    exit()

def titleCleanup(text):
    tag = False
    a = ""
    apostrophe = "&#039;"
    for letter in text:
            if letter == "<":
                tag = True
            elif letter == ">":
                tag = False
            elif tag:
                continue
            else:
                a += letter
    if apostrophe in a:
        a = a.replace(apostrophe, "'")
        return a
    return a

# Simple animation
def animate(seconds):
    for i in range(seconds // 4):
        sys.stdout.write('\rSearching')
        time.sleep(1)
        sys.stdout.write('\rSearching .')
        time.sleep(1)
        sys.stdout.write('\rSearching . .')
        time.sleep(1)
        sys.stdout.write('\rSearching . . .')
        time.sleep(1)
    sys.stdout.write('\r')


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


#imageSaver(custom, "4Chan")

mainMenu()
root.mainloop()

# Image Saver Works
# getSelections needs to get rid of commas - Done
# 