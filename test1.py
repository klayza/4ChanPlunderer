from tkinter import *
import ast
from tkinter import messagebox
root = Tk()
def getSelections():
    try:
        f = open("Selections.txt", "r+")
        ls = []
    except:
        messagebox.showinfo(title="Warning", message="Before proceeding please enter a search query")
        print("Home")
    else:
        for line in f.readlines():
            temp = line.splitlines()
            w = str(temp)[2:-2]
            w = w.replace(",',", "',")
            w = w.replace(",']", "']")
            w = ast.literal_eval(w)
            ls.append(w)
        f.close()
        print("\n\n\n", ls, "\n\n\n")
        return ls

def getSelection(varlist):
    for ivar in varlist:
        print(ivar.get())

def checkBoxes():
    for i in getSelections():
        i = i[0]
        count = 0
        ivar = i
        print(i)
        print(ivar + str(count))
        ivar = StringVar()
        i = Checkbutton(root, text=i,variable=ivar, onvalue=1)
        i.pack()
    Button(root, text="submit", command=lambda:getSelection(ivar)).pack()

checkBoxes()

root.mainloop()