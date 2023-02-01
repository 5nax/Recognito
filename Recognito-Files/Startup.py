############################################# IMPORTING ################################################

import tkinter as tk
from tkinter import *
from tkinter import messagebox as mess
import os
from PIL import Image
from PIL import ImageTk

################################## FUNCTIONS ######################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def nextPage():
    ws.destroy()
    import main

def clear():
    old.delete(0, 'end')

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    password = old.get()
    if (password == key):
        nextPage()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
        clear()

def func(event):
    psw()

def contact():
    mess._show(title='Contact us', message="Please contact us at : himalpanta@gmail.com or      nijanaryal17@gmail.com ")

################################# GUI BACK END ####################################

ws = Tk()
ws.geometry('1366x768')
ws.title("RECOGNITO")
ws.resizable(False,False)
photo = PhotoImage(file = "icon.png")
ws.iconphoto(False, photo)


filename = ImageTk.PhotoImage(Image.open('Background.jpg' ))
background_label = tk.Label(ws, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
################################ TEXBOX & LABELS ##################################

message3 = tk.Label(ws, text=" RECOGNITO " ,fg="white",bg="#1a1a1a" ,width=45 ,height=1,font=('Quantum', 35))
message3.place(x=0, y=0)

message3 = tk.Label(ws, text="📷" ,fg="white",bg="#1a1a1a" ,width=2 ,height=2,font=('Quantum', 30))
message3.place(x=480, y=-34)

message1 = tk.Label(ws, text="Enter Your Password " ,bg="#a77c5a" ,fg="White"  ,width=20 ,height=1,font=('Century Gothic', 17, ))
message1.place(x=585, y=390)

global old
old = tk.Entry(ws, width=25, fg="black", relief='solid', font=('Century Gothic', 28), show='*')
old.place(x=450, y=430)
old.bind('<Return>', func)

################################# BUTTONS ########################################

clearButton = tk.Button(ws, text="Clear", command=clear  ,fg="White"  ,bg="#111211"  ,width=8 ,activebackground = "white" ,font=('Century Gothic', 18))
clearButton.place(x=880, y=427)

login = tk.Button(ws, text="LOGIN", command=psw,fg="White"  ,bg="#614f41"  ,width=20 ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
login.place(x=450, y=500)

Forget = tk.Button(ws, text="Forgot Password", command=contact  ,fg="White"  ,bg="#614f41"  ,width=20 , activebackground = "white" ,font=('Century Gothic', 15))
Forget.place(x=760, y=500)

#################################### END #########################################

ws.mainloop()

##################################################################################