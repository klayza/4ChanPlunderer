from tkinter import *
import ast
from tkinter import messagebox

root = Tk()

def Clear():
    for widget in root.winfo_children():
        widget.destroy()


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
        return ls


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


# A window that will display the title of all the different selections previously created by the user
# Hitting the submit button will save and go back a page
# Creates a stringvar and appends that to a list in a loop which will go to addEnabledSelection() 
def checkBoxes():
    Clear()
    root.geometry("300x500")
    count = 0
    varlist = []
    for title in getSelections():
        # Iterates through lists in the Selections.txt
        title = title[0]
        titlevar = title + str(count)
        titlevar = StringVar(value=0)
        Checkbutton(root, text=title,variable=titlevar, onvalue="1", offvalue="0").pack(fill="x")
        varlist.append(titlevar)
        count += 1
    Button(root, text="submit", command=lambda:addEnabledSelection(varlist)).pack()

checkBoxes()

root.mainloop()
