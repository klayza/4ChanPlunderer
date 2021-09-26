from urllib import request
from datetime import datetime
from tkinter import *
import requests
import os
import time
import sys
import animation

# Console based version

destination = "E:/Media/4Chan"

# Pass in a board, preset/keyword to search for, and the destination of your downloaded images
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

# Simple animation to
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
    print("---------[Starting Search]---------")
    while True:
        # [Title, Board, [Whitelists], [Blacklists]]
        imageSaver(["My Filter", "wg", ["nature", "forest"], ["industrial", "city"]])
        animate(360)


