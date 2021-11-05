import os
from tkinter import *  
from PIL import ImageTk,Image  
from urllib import request
import ssl
import requests
import shutil

global menuState

ssl._create_default_https_context = ssl._create_unverified_context


#request.urlretrieve("https://robbreport.com/wp-content/uploads/2016/09/lamborghini_huracan_slideshow_lead.jpg", "C:/Users/user/Desktop")
# Set up the image URL and filename
image_url = "https://robbreport.com/wp-content/uploads/2016/09/lamborghini_huracan_slideshow_lead.jpg"
filename = image_url.split("/")[-1]
print(filename, "\n", image_url.split("/"))

def Download(url, destination):
    filename = url.split("/")[-1]
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open("C:/Users/user/Desktop/" + filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)


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