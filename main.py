from tkinter import messagebox, scrolledtext
from PIL import ImageTk, Image as Img1, ImageFilter
from tkinter import *
import subprocess
import ctypes
import psutil
import ast
import ssl
import os

global menuState

ssl._create_default_https_context = ssl._create_unverified_context

destination = "Desktop"
w, h = 400, 600

root = Tk()

config = {"width":53, "height":2, "font":"Consolas 21 bold"}
root.title("4Chan-App")
#root.geometry(f"{str(w)}x{str(h)}")
root.configure(bg="#353839")
root.state('zoomed')

class windowStats:
    def __init__(self):
        self.isrunning = False

        if os.path.exists("Selections.txt"):
            self.issetup = False 
        else:
            self.issetup = True

        if os.path.exists("EnabledSelections.txt"):
            with open("EnabledSelections.txt", "r+") as f:
                if str(f.readline()) == "":
                    self.missingenabledselections = True
                else:
                    self.missingenabledselections = False
        else:
            self.missingenabledselections = True
            

        

# Clears the window
def Clear():
    for widget in root.winfo_children():
        widget.destroy()
     
    
# Once the Start/Stop button is pushed it will either start or stop downloading depending on if the process is running or not
def mainmenuControls():
    if window.isrunning == False and window.issetup == False:
        f = open("EnabledSelections.txt", "r+")
        if f.readline == "":
            messagebox.showinfo(title="Bruh", message="Please check off a filter you want to apply before continuing.")
            addQueryMenu()
        startorstopDownload("start")
        window.isrunning = True
        mainMenu()

    elif window.isrunning:
        startorstopDownload("stop")
        window.isrunning = False
        mainMenu()

    else:
        print(window.isrunning, window.issetup)


# Will determine what the main menu is supposed to look like
def mainmenuInit():
    if window.issetup or window.missingenabledselections:
        return  {"color": "light gray", "state": "disabled", "text": "Start", "menuState": "started", "command":"setup"}
    elif not window.isrunning:
        return {"color": "green", "state": "normal", "text": "Start", "menuState": "started", "command":"default"}
    elif window.isrunning:
        return {"color": "red", "state": "normal", "text": "Stop", "menuState": "start", "command":"default"}
    else:
        return {"color": "red", "state": "normal", "text": "Stop", "menuState": "start", "command":"default"}


# Makes sure the download process has stopped and closes the program
def Exit():
    if window.isrunning:
        startorstopDownload("stop")
    root.destroy()


# Adds a canvas image to main menu screen
def DisplayImage(image="default", resize="default"):
    global bg, my_canvas

    # Create a canvas
    my_canvas = Canvas(root, bg="#353839", borderwidth=0, highlightthickness=0)
    my_canvas.pack(fill="both", expand=True, anchor="n")

    # Define image
    if image == "default" and resize == "default":
        image = Img1.open("hopper.jpg")
    else:
        image = Img1.open(image)
    root.update()
    #print(my_canvas.winfo_width(), my_canvas.winfo_height())
    bg = ImageTk.PhotoImage(image.resize((my_canvas.winfo_width(), my_canvas.winfo_height()), Img1.ANTIALIAS).filter(filter=ImageFilter.GaussianBlur(0)))

    # Set image in canvas
    my_canvas.create_image(0,0, image=bg, anchor="nw")
    

    def resizer(e):
    	global bg1, resized_bg, new_bg
    	# Open image
    	bg1 = Img1.open("hopper.jpg")
    	# Resize the image
    	#print(str(e.width), str(e.height))
    	resized_bg = bg1.resize((e.width, e.height), Img1.ANTIALIAS).filter(filter=ImageFilter.GaussianBlur(50))
    	# Define image again
    	new_bg = ImageTk.PhotoImage(resized_bg)
    	# Add it back to the canvas
    	my_canvas.create_image(0,0, image=new_bg, anchor="nw")

    #root.bind('<Configure>', resizer)


# Shown after clicking a board and will display images within a folder the preset name clicked
def PresetSelect(board):
    Clear()
    presets = GetBoardPresets(board)
    for preset in presets:
        Button(root, **config, bg="dark gray", text=preset, command=lambda b = board, p = preset:ImageViewer(b + "/" + p)).pack(fill="x", pady=2)
    Button(root, **config, bg="red", text="All", command=lambda:ImageViewer(board, True)).pack(fill="x", pady=2)
    Button(root, **config, bg="red", text="Back", command=lambda:BoardSelect()).pack(fill="x", pady=2)


    
# Presents user with board and when clicked will show all selections within that specified board
# Will have the 'show all' in the board and preset menus
def BoardSelect():
    Clear()
    boards = getBoards()
    for board in boards:
        Button(root, **config, bg="dark gray", text=board, command=lambda b = board:PresetSelect(b)).pack(fill="x", pady=2)
    Button(root, **config, bg="dark gray", text="All", command=lambda:ImageViewer("all", True)).pack(fill="x", pady=2)
    Button(root, **config, bg="red", text="Back", command=lambda:mainMenu()).pack(fill="x", pady=2)


def ImageViewer(location, all=False, i=0):
    Clear()
    global image                                    # Potentially dangerous
    folder = "E:/Media/4Chan"
    files = []
    images = []

    # Runs if user selected all files
    if all and location == "all":
        for r, d, f in os.walk(folder):
            for file in f:
                files.append(os.path.join(r, file))
    
    # Runs if user selected all within a board
    elif all:
        for r, d, f in os.walk(folder + "/" + location):
            for file in f:
                files.append(os.path.join(r, file))

    # Runs if user selected a particular preset within a board
    else:  
        for r, d, f in os.walk(folder + "/" + location):
            for file in f:
                files.append(os.path.join(r, file))
    
    # Appends files to new list with the file extension of .jpg or .png and removes the rest (.gif coming later)
    for file in files:
        if '.jpg' in file or '.png' in file:
            images.append(file)
            images.reverse()

    # Will check if there are any images, and if not will go back a page
    if len(images) == 0:
        messagebox.showinfo(title="Bruh", message="No images found")
        BoardSelect()
    
    def Forward(i):
        if i < len(images):
            ImageViewer(location, all, i)
        

    def Backward(i):
        if i >= 0:
            ImageViewer(location, all, i)
    
    def Wallpaper():
        ctypes.windll.user32.SystemParametersInfoW(20, 0, images[i] , 0)


    navigation = Frame(root, height=30, bg="tan")
    navigation.pack(fill="x")
    Button(navigation, text="-->", command=lambda:Forward(i + 1)).grid(padx="2", row=0, column=2, sticky="W")
    Button(navigation, text="Exit", command=lambda:BoardSelect()).grid(padx="2", row=0, column=1)
    Button(navigation, text="<--", command=lambda:Backward(i - 1)).grid(padx="2", row=0, column=0, sticky="E")
    Button(navigation, text="Set Wallpaper", command=lambda:Wallpaper()).grid(padx="2", row=0, column=4, sticky="E")
    Button(navigation, text="Open Image", command=lambda i = images[i]:Img1.open(i).show()).grid(padx="2", row=0, column=5, sticky="E")
    DisplayImage(images[i])
    
'''
The main menu. Will configure it's button's settings with the function mainmenuInit which returns a dictionary of settings
First button will change to either start or stop depending on if the download process is running or not
Second will take the user to the adding selection menu
Third will open the console that the download process produced for the user to read
Fourth will open settings
Fifth will close the app and stop the download process
'''

def mainMenu():
    Clear()
    settings = mainmenuInit()
    DisplayImage()
    Button(root, **config, text=settings["text"], bg=settings["color"], command=lambda:mainmenuControls(), state=settings["state"]).pack(fill="x", pady=2)
    Button(root, **config, text="Library", bg="dark gray", command=lambda:BoardSelect()).pack(fill="x", pady=2)
    Button(root, **config, text="Presets", bg="dark gray", command=lambda:addQueryMenu()).pack(fill="x", pady=2)
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
    mainMenu()


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

        c = Checkbutton(newFrame, **config, text=title, variable=titlevar, onvalue="1", offvalue="0", bg="dark gray", compound="top", relief="raised")

        # Checks box off if it is already selected
        if title in str(getSelections("EnabledSelections.txt")):
            c.select()
        c.pack(anchor="w", pady=2, padx=2)

        varlist.append(titlevar)
        count += 1
    newFrame.grid(row=2, column=0)


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
            if window.issetup:
                addQueryMenu(command="setup")
            else:
                addQueryMenu()
            return

    window.issetup = False
    selections = [title, board, [item for item in whitelist], [item for item in blacklist]]
    f = open("Selections.txt", "a+")
    f.write(str(selections) + "\n" )
    f.close
    addQueryMenu()


# The menu that contains the checkbox and query frame.
def addQueryMenu():
    Clear()
    if not window.issetup:
        checkBoxes()

    queryFrame = Frame(root, bg="dark gray")

    title = StringVar()
    board = StringVar()
    whitelist = StringVar()
    blacklist = StringVar()

    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Title:").grid(column=0, row=0, pady=2, padx=2, sticky="w")
    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Board:").grid(column=0, row=1, pady=2, padx=2, sticky="w")
    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Whitelist:").grid(column=0, row=2, pady=2, padx=2, sticky="w")
    Label(queryFrame, bg="dark gray", font="Consolas 21 bold", text="Blacklist:").grid(column=0, row=3, pady=2, padx=2, sticky="w")

    e1 = Entry(queryFrame, bg="lightgray", font="Consolas 21 bold",)
    e2 = Entry(queryFrame, bg="lightgray", font="Consolas 21 bold",)
    e3 = Entry(queryFrame, bg="lightgray", font="Consolas 21 bold",)
    e4 = Entry(queryFrame, bg="lightgray", font="Consolas 21 bold",)

    e1.grid(column=1, row=0, pady=2)
    e2.grid(column=1, row=1, pady=2)
    e3.grid(column=1, row=2, pady=2)
    e4.grid(column=1, row=3, pady=2)

    Button(root, **config, bg="green", text="Save", command=lambda:addSearchIndex(e1, e2, e3, e4)).grid(row=1, column=0)
    queryFrame.grid(column=0, row=0, sticky="n")

    # Will go to back to main menu if the user hasn't made a filter yet
    if window.issetup:
        Button(root, **config, bg="red", text="Back", command=lambda:mainMenu()).grid(row=3, column=0)
        root.geometry()
    # Otherwise this will create a back button that will save the input to Selections.txt and return to main menu
    else:
        if varlist == None:
            mainMenu()
        else:
            Button(root, **config, bg="red", text="Back", command=lambda:addEnabledSelection(varlist)).grid(row=3, column=0)
            root.geometry()
    


# A menu that will display what the console has been outputting, time, file, match, board, etc.
def consoleMenu():
    Clear()
    menuFrame = Frame(root, bg="#353839")
    Button(menuFrame, **config, text="Back", bg="red", command=lambda:mainMenu()).pack()
    menuFrame.pack(fill="x", side="top")

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
        proc = subprocess.Popen("console.py", shell=True)
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
    return False


# Returns true if there are selection within the file Selections.txt and false if none are found
def selectionsExist():
    selections = getSelections()
    if selections != None:
        return True
    elif selections == None:
        return False


# Will return true if the download process is running and false if not
def getMenuState():
    if checkIfProcessRunning("pythonw.exe"):
        return "started"
    else:
        return "start"


# Scans the folder of a board passed in and returns a list of presets in that folder
def GetBoardPresets(board='b'):
    for root, dirs, files in os.walk("E:/Media/4Chan/" + board):
        if len(dirs) == 0:
            continue
        return dirs


# Scans the folders in the save location and returns a list of boards that have been created
def getBoards():
    a = os.walk("E:/Media/4Chan")
    for i in a:
    	return i[1]


# Returns a list of all lines in Selections.txt
def getSelections(search="Selections.txt"):
    try:
        f = open(search, "r+")
        ls = []
    except:
        messagebox.showinfo(title="Warning", message="Before proceeding please enter a search query")
        mainMenu()
    else:
        for line in f.readlines():
            temp = line.splitlines()
            w = str(temp)[2:-2]
            w = w.replace(",',", "',")
            w = w.replace(",']", "']")
            w = ast.literal_eval(w)
            ls.append(w)
        f.close()
        return ls

window = windowStats()
window.__init__()
mainMenu()
root.mainloop()
