from gui import imageSaver
from tkinter import *

root = Tk()
root.title("4Chan-App")

def Clear():
    for widget in root.winfo_children():
        widget.destroy()

def mainMenu(menuState="start"):
    Clear()
    settings = mainmenuInit(menuState)
    Button(root, text="Start", bg=settings["color"], command=lambda: mainMenu("started"), state=settings["state"]).pack()
    Button(root, text="Here").pack()
    Button(root, text="Here").pack()
    Button(root, text="Here").pack()

def addSearchIndex():
    pass

def imageSaver():
    print("here")

def valueInit():
    global buttonState

def mainmenuInit(menuState):
    if menuState == "start":
        return {"color": "green", "state": "enabled"}
    elif menuState == "started":
        return {"color": "red", "state": "disabled"}

    

mainMenu()

root.mainloop()

