from tkinter import *
from PIL import ImageTk, Image, ImageFilter

root = Tk()

def main():
    # Define image
    image = Image.open("hopper.jpg")
    bg = ImageTk.PhotoImage(image.resize((400, 250), Image.ANTIALIAS).filter(filter=ImageFilter.GaussianBlur(8)))

    # Create a canvas
    my_canvas = Canvas(root, width=400, height=250, borderwidth=0, highlightthickness=0)
    my_canvas.pack(fill="both", expand=True)

    # Set image in canvas
    my_canvas.create_image(0,0, image=bg, anchor="nw")
    # Add a label

    # add some buttons
    button1 = Button(root, text="Start")
    button2 = Button(root, text="Reset Scores")
    button3 = Button(root, text="Exit")

    button1_window = my_canvas.create_window(10, 10, anchor="nw", window=button1)
    button2_window = my_canvas.create_window(100, 10, anchor="nw", window=button2)
    button3_window = my_canvas.create_window(230, 10, anchor="nw", window=button3)

    def resizer(e):
    	global bg1, resized_bg, new_bg
    	# Open our image
    	bg1 = Image.open("hopper.jpg")
    	# Resize the image
    	print(str(e.width), str(e.height))
    	resized_bg = bg1.resize((e.width, e.height), Image.ANTIALIAS).filter(filter=ImageFilter.GaussianBlur(8))
    	# Define our image again
    	new_bg = ImageTk.PhotoImage(resized_bg)
    	# Add it back to the canvas
    	my_canvas.create_image(0,0, image=new_bg, anchor="nw")

    root.bind('<Configure>', resizer)


main()
root.mainloop()