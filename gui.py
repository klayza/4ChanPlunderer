#!/usr/bin/env python      1
from tkinter import *      

def createWidgets(self):
        top=self.winfo_toplevel()                
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)         
        self.rowconfigure(0, weight=1)           
        self.columnconfigure(0, weight=1)        
        self.quit = Button(self, text='Quit', command=self.quit)
        self.quit.grid(row=0, column=0,          
            sticky=NSEW)

app = Tk()                       
app.title('Sample application')   
createWidgets(app) 
app.mainloop()                            