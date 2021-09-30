from urllib import request
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import threading
import requests
import os
import time
import sys
import ast
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
destination = "Desktop"

root = Tk()
root.title("4Chan-App")
root.geometry("400x400")


def Clear():
    for widget in root.winfo_children():
        widget.destroy()

def mainmenuControls(menuState):
    if menuState == "start" and selectionsExist():
        mainMenu("started")
        print("Starting Search")
        print(getSelections(), "here")
        for selections in getSelections():
            thread = threading.Thread(target=imageSaver, args=(selections, ))
            thread.start()
            thread.join()
        mainMenu("started")

    elif menuState == "started":
        imageSaverStop()


# Will determine what the main menu is supposed to look like
def mainmenuInit(menuState):
    if menuState == "start":
        return {"color": "green", "state": "normal", "text": "Start", "menuState": "started"}
    elif menuState == "started":
        return {"color": "red", "state": "disabled", "text": "Stop", "menuState": "start"}


def mainMenu(menuState="start"):
    Clear()
    settings = mainmenuInit(menuState)
    Button(root, text=settings["text"], bg=settings["color"],command=lambda:mainmenuControls(menuState)).pack(fill="x", pady=2)
    Button(root, text="Presets", command=lambda:addQueryMenu()).pack(fill="x", pady=2)
    Button(root, text="Console").pack(fill="x", pady=2)
    Button(root, text="Settings").pack(fill="x", pady=2)
    Button(root, text="Exit", bg="red", command=lambda:root.destroy()).pack(fill="x", pady=2)



def addSearchIndex(title, board, whitelist, blacklist, command="none"):
    if command == "none":
        title = title.get()
        board = board.get()
        whitelist = [s.strip() + ',' for s in whitelist.get().split(',') if s.strip()]
        blacklist = [s.strip() + ',' for s in blacklist.get().split(',') if s.strip()]


    selections = [title, board, [item for item in whitelist], [item for item in blacklist]]
    f = open("Selections.txt", "a+")
    f.write(str(selections) + "\n" )
    f.close
    addQueryMenu()

def addQueryMenu():
    Clear()

    title = StringVar()
    board = StringVar()
    whitelist = StringVar()
    blacklist = StringVar()

    Label(root, text="Title").pack(fill="x", pady=2)
    Label(root, text="Board").pack(fill="x", pady=2)
    Label(root, text="Whitelist").pack(fill="x", pady=2)
    Label(root, text="Blacklist").pack(fill="x", pady=2)

    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)
    e4 = Entry(root)

    e1.pack(fill="x", pady=2)
    e2.pack(fill="x", pady=2)
    e3.pack(fill="x", pady=2)
    e4.pack(fill="x", pady=2)

    Button(root, text="Submit", command=lambda:addSearchIndex(e1, e2, e3, e4)).pack(anchor="s")
    Button(root, text="Back", command=lambda:mainMenu()).pack(anchor="s")



def imageSaver(selections, destination=destination):
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
    return None
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
def getSelections():
    try:
        f = open("Selections.txt", "r+")
        ls = []
    except:
        messagebox.showinfo(title="Warning", message="Before proceeding please enter a search query")
        mainMenu("start")
    else:
        for line in f.readlines():
            temp = line.splitlines()
            w = str(temp)[2:-2]
            w = w.replace(",',", "',")
            w = w.replace(",']", "']")
            w = ast.literal_eval(w)
            ls.append(w)
        f.close()
        print(ls)
        return ls


#addSearchIndex("Wallpaper", "wg", ["comfy", "nature", "another-one"], ["uncomfortable", "inside"], command="manual")
#imageSaver(custom, "4Chan")

mainMenu()
root.mainloop()

# Image Saver Works
# getSelections needs to get rid of commas - Done
# 