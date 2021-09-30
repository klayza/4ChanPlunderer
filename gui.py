from urllib import request
from datetime import datetime
from tkinter import *
import requests
import os
import time
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
destination = "C:/Users/Administrator/Desktop/4Chan"

root = Tk()

def Clear():
    for widget in root.winfo_children():
        widget.destroy()

def mainMenu():
    Clear()
    Button(root, text="Here").pack()

def addSearchIndex():
    pass



root.title("4Chan-App")


# For presets provide the name of the preset and then add keywords to it
presets = {"lanscape": ["woods", "forest", "mountain", "landscape", "nature"]}



# Pass in a board, preset/keyword to search for, and the destination of your downloaded images
def imageSaver(board, preset, blacklist="example", destination=destination):
    count = 0
    try:
        json = requests.get("https://a.4cdn.org/" + board + "/catalog.json").json()
    except:
        print("Had trouble connecting, please check connection")
        exit()
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

            if blacklist in title:
                continue

            # Adds keyword to the dictionary if not already in it
            if preset not in presets:
                presets[preset] = [preset]

            # Searches through threads when given the keyword of the preset
            for phrase in presets[preset]:

                # Will go into this block if the comment of a post matches one of the keywords
                if phrase in title:
                    # Gets the .json of the thread
                    c = requests.get("https://a.4cdn.org/" + board + "/thread/" + str(json[page]["threads"][thread]["no"]) + ".json").json()

                    # Looks through the .json of the individual comment using the range of however many comments are within the thread
                    for comment in range(len(c["posts"]) - 1):

                        # Sometimes there are no images on a comment hence the try, except
                        try:
                            link = "https://is2.4chan.org/" + board + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"]
                        except:
                            continue

                        # If there is no path with the same board and preset name it makes one and starts downloading the images there
                        if not os.path.exists(destination + "/" + board + "/" + preset.capitalize()):
                            os.makedirs(destination + "/" + board + "/" + preset.capitalize())

                        # If the same file exists it continues to avoid downloading again
                        if os.path.exists(destination + "/" + board + "/" + preset.capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"]):
                            continue

                        request.urlretrieve(link, destination + "/" + board + "/" + preset.capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"])
                        count += 1

                        if downloading:
                            print("--------------------------------------------------------------------------------------------")
                            print(datetime.now().strftime(
                                "%H:%M") + " | Link: https://boards.4chan.org/" + board + "/thread/" + str(
                                json[page]["threads"][thread]["no"]))
                            print(datetime.now().strftime("%H:%M") + " | Thread: " + title + " | /" + board + "/")
                            print(datetime.now().strftime("%H:%M") + " | Match: " + phrase)

                        print(datetime.now().strftime("%H:%M") + " | Downloaded: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + board + "/" + preset.capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " | " + str(count))
                        downloading = False
                        #sys.stdout.write("\rDownloading: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + board + "/" + preset.capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"])


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


if __name__ == "__main__":
    mainMenu()
    print("---------[Starting Search]---------")
    while True:
        imageSaver("gif", "")
        imageSaver("wg", "landscape")
        imageSaver("wg", "battlestation")
        imageSaver("wg", "comfy", "map")
        imageSaver("w", "evangelion")
        animate(360)


root.mainloop()
