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
    for titlevar in varlist:
        print(titlevar)

def checkBoxes():
    count = 0
    for title in getSelections():
        varlist = []
        title = title[0]

        titlevar = title + str(count)
        print("Label: " + title)
        print("Tvar: " + titlevar)
        titlevar = StringVar()
        tilevar = Checkbutton(root, text=title,variable=titlevar,onvalue=1)
        tilevar.pack()
        varlist.append(tilevar)
        count += 1
    Button(root, text="submit", command=lambda:getSelection(varlist)).pack()

checkBoxes()

root.mainloop()
