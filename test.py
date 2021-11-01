import os
from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  

imagecanvas = Canvas(root, bg="#353839", borderwidth=0, highlightthickness=0)
imagecanvas.pack(fill="both", expand=True, anchor="n")

canvas = Canvas(root, bg="#353839", borderwidth=0, highlightthickness=0)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("hopper.jpg"))  
canvas.create_image(20, 20, anchor=NW, image=img) 
root.mainloop() 

def GetBoardPresets(board='b'):
    for root, dirs, files in os.walk("E:/Media/4Chan/" + board):
        if len(dirs) == 0:
            continue
        return dirs

def getBoards():
    a = os.walk("E:/Media/4Chan")
    for i in a:
    	return i[1]

lista = ['34534.webm', 'dawd.mp3,', '8923.webm', '5325.jpg', 't3434.png', '345345.gif']
listb = []

for file in lista:
    if '.jpg' in file or '.png' in file:
        listb.append(file)

print(listb)

#print(getBoards())