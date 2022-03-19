from urllib import request
from datetime import datetime
import requests
import shutil
import json
import time
import sys
import ssl
import os

# Console based version; Saves and organizes images from 4chan with filter
# Saves output to .txt and will display in the console section 

WaitTime = 360

# Pass in a board, preset/keyword to search for, and the destination of your downloaded images
def imageSaver(selections, destination):
    ssl._create_default_https_context = ssl._create_unverified_context
    json = requests.get("https://a.4cdn.org/" + selections["Board"] + "/catalog.json").json()
    count = 0


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
            for word in selections["Blacklist"]:
                if word in title:
                    continue

            # Searches through threads when given the keyword of the preset
            for word in selections["Whitelist"]:

                # Will go into this block if the comment of a post matches one of the keywords
                if word in title:
                    # Gets the .json of the thread
                    c = requests.get("https://a.4cdn.org/" + selections["Board"] + "/thread/" + str(json[page]["threads"][thread]["no"]) + ".json").json()

                    # Looks through the .json of the individual comment using the range of however many comments are within the thread
                    for comment in range(len(c["posts"]) - 1):

                        # Sometimes there are no images on a comment hence the try, except
                        try:
                            link = "https://i.4cdn.org/" + selections["Board"] + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"]
                        except:
                            continue

                        # If there is no path with the same board and preset name it makes one and starts downloading the images there
                        if not os.path.exists(destination + "/" + selections["Board"] + "/" + selections["Title"].capitalize()):
                            os.makedirs(destination + "/" + selections["Board"] + "/" + selections["Title"].capitalize())

                        # If the same file exists it continues to avoid downloading again
                        if os.path.exists(destination + "/" + selections["Board"] + "/" + selections["Title"].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"]):
                            continue
                        
                        Download(link, destination + "/" + selections["Board"] + "/" + selections["Title"].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"])
                        count += 1
                        f = open("console.txt", "a+")
                        if downloading:
                            
                            print("--------------------------------------------------------------------------------------------")
                            f.write("\n--------------------------------------------------------------------------------------------")

                            print(datetime.now().strftime("%H:%M") + " | Link: https://boards.4chan.org/" + selections["Board"] + "/thread/" + str(json[page]["threads"][thread]["no"]))
                            f.write("\n" + datetime.now().strftime("%H:%M") + " | Link: https://boards.4chan.org/" + selections["Board"] + "/thread/" + str(json[page]["threads"][thread]["no"]))

                            print(datetime.now().strftime("%H:%M") + " | Thread: " + title + " | /" + selections["Board"] + "/")
                            f.write("\n" + datetime.now().strftime("%H:%M") + " | Thread: " + title + " | /" + selections["Board"] + "/")

                            print(datetime.now().strftime("%H:%M") + " | Match: " + word)
                            f.write("\n" + datetime.now().strftime("%H:%M") + " | Match: " + word)

                        print(datetime.now().strftime("%H:%M") + " | Downloaded: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + selections["Board"] + "/" + selections["Title"].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " | " + str(count))
                        f.write("\n" + (datetime.now().strftime("%H:%M") + " | Downloaded: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + selections["Board"] + "/" + selections["Title"].capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " | " + str(count)))
                        f.close()
                        downloading = False
                        #sys.stdout.write("\rDownloading: " + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"] + " to " + destination + "/" + board + "/" + preset.capitalize() + "/" + str(c["posts"][comment]["tim"]) + c["posts"][comment]["ext"])
    

def Download(url, destination):
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(destination,'wb') as f:
            shutil.copyfileobj(r.raw, f)


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
    try:
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
    except KeyboardInterrupt:
        print("\nStopped")
        main()
        


# Will save a txt file with search paramaters
def CreateSelections(mode): # REQ: Add ability to check if board entered is valid
    W_terms = []
    B_terms = []
    count = 0
    board = input("Enter board name: ")

    print("Press enter when done")

    # Adds search terms to W_terms until user enters a blank key
    # Count will determine if the user entered a blank key or not
    while True:
        term = input("Enter a search term: ")
        if term == "" and count > 0:
            break
        W_terms.append(term)
        count += 1
    count = 0

    # Adds blacklist terms to B_terms
    print("If blacklist not needed just press enter")
    while True:
        term = input("Enter a word to blacklist: ")
        if term == "" and count == 0:
            B_terms.append("")
            break
        if term == "" and count > 0:
            break
        B_terms.append(term)
        count += 1
    title = input("Enter the title for this config: ")
        
    config = [{
        "Title": title,
        "Board": board,
        "Whitelist": W_terms,
        "Blacklist": B_terms
             }]

    # Will run if the config file already exists
    if os.path.exists("Config.json"):
        config = {
            "Title": title,
            "Board": board,
            "Whitelist": W_terms,
            "Blacklist": B_terms
                }
        previous = GetSelections()
        previous.append(config)
        config = previous
        mode = "w+"

    config_json = json.dumps(config)

    with open("Config.json", mode) as f:
        f.write(config_json)


def GetSelections():
    with open("Config.json", "r+") as f:
        return json.load(f)

def main():
    print("Use commands '(C)reate' or '(S)tart'")   # Add feature to ask user if they want to autoatically start when running program when 'Start' is entered for the first time. Also ask for a default directory
    while True:
        command = input("> ").upper()
        if "C" in command:
            CreateSelections("a+")
            continue
        if "S" in command:
            if not os.path.exists("Config.json"):
                print("Search paramaters were not found, let's make one")
                CreateSelections("w+")
        # Makes a file to store destination
        if not os.path.exists("Destination.txt"):
            with open("Destination.txt", "w") as f:
                f.write("")
            print("Destination.txt was created, enter a path")
            continue

        # When specifying the path, note that this program will add folders based on the board name
        with open("Destination.txt", "r+") as f:
            global destination 
            destination = f.read()
            if not os.path.isdir(destination):
                print("Path is invalid in Destinations.txt")
                continue

        if not os.path.exists(destination):
            res = input("This path doesn't already exist, create one? ").upper()
            if "Y" in res:
                os.mkdir(destination)
                break
            continue
        if not os.path.exists("Config.json"):
            print("Search paramaters were not found, let's make one")
            CreateSelections("w+")
        break

main()
print("Starting search, use Ctrl + C to stop")
while True:
    for selection in GetSelections():
        try:
            imageSaver(selection, destination)
        except requests.exceptions.SSLError:
            res = input("There was a problem connecting, try again? ").upper()
            if "N" in res:
                exit()
            else:
                continue
            
    with open("console.txt", "a+") as f:
            f.write("\n" + (datetime.now().strftime("%H:%M") + " | Waiting " + str(WaitTime)))   
            f.close() 
    animate(WaitTime)