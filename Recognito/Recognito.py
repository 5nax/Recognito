############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mess
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
import tkinter.simpledialog as tsd
from tkvideo import tkvideo
import cv2 , os
import csv
import numpy as np
from PIL import Image
from PIL import ImageTk
import pandas as pd
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

###########################################################################################
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
###########################################################################################
def tick():
    time_string = time.strftime('%I:%M:%S %p')
    clock.config(text=time_string)
    clock.after(200,tick)

###########################################################################################
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some files are missing', message='Please contact us for help')
        window.destroy()

###########################################################################################
def func(event):
    psw()

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    password = PSW_INP.get()
    if (password == key):
        show_frame(MainPage)
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
        clear()
###########################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()
    ###########################################################################################
def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='Enter Old Password',bg='white',font=('Century Gothic', 10 ))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('Century Gothic', 11),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='Enter New Password', bg='white', font=('Century Gothic', 10))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('Century Gothic', 11),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('Century Gothic', 10))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('Century Gothic', 11),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="White"  ,bg="#111211" ,height=1,width=20 , activebackground = "white" ,font=('Century Gothic', 10))
    cancel.place(x=205, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="White", bg="#614f41", height = 1,width=20, activebackground="white", font=('Century Gothic', 10))
    save1.place(x=20, y=120)
    master.mainloop()

    ###########################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.','','CLASS', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    Class = (txt5.get())
    if ((name.isalpha()) or (' ' in name)):
        if ((Id.isnumeric()) or (' ' in Id)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w], [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                    cv2.imshow('Taking Images', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 50:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [serial,'',Class,'', Id, '', name]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()

        else:
            if (name.isalpha() == False):
                Popup = Label(Registerpage, text="Enter Correct Name", font=("Century Gothic", 18), bg="#d0d3d4",
                              width=21, height=1)
                Popup.place(x=167, y=490)
                Popup.after(2400, Popup.destroy)
            elif (Id.isalpha() == True):
                Popup = Label(Registerpage, text="Enter Correct Roll Number", font=("Century Gothic", 18), bg="#d0d3d4",
                              width=21, height=1)
                Popup.place(x=167, y=500)
                Popup.after(2400, Popup.destroy)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    mess._show(title='Registration',
               message="Student Registered Sucessfully")


############################################################################################3

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 225, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf > 30):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
            else:
                Id = 'Not Registered'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font , 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()


    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }


def clear():
    txt.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    busted_display = Label(Registerpage, text="Please Input A Roll Number", font=("Century Gothic ", 13), bg="#fff",width=22,height=1)
    busted_display.place(x=140, y=235)
    window.after(2400, busted_display.destroy)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    busted_display = Label(Registerpage, text="Please Input A Name", font=("Century Gothic",13), bg="#fff", width=21, height=1)
    busted_display.place(x=140, y=334)
    window.after(2400, busted_display.destroy)

def clear3():
    old1.delete(0, 'end')

def clear4():
    PSW_INP.delete(0, 'end')

def clear5():
    txt5.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    busted_display = Label(Registerpage, text="Please Input A Faculty", font=("Century Gothic", 13), bg="#fff", width=21,
                           height=1)
    busted_display.place(x=140, y=425)
    window.after(2400, busted_display.destroy)
###########################################################################################
def contact():
    mess._show(title='Contact us', message="Please contact us at : himalpanta@gmail.com or      nijanaryal17@gmail.com ")

def confirm1():
    answer = askyesno(title='Logout', message='Are you sure that you want to logout?')
    if answer:
        show_frame(Startup)
    PSW_INP.delete(0, 'end')
def confirm2():
    answer = askyesno(title='Quit', message='Are you sure that you want to Quit?')
    if answer:
        window.destroy()
def show_frame(frame):
    frame.tkraise()
###########################################################################################

################################ TEXBOX & LABELS ##################################

window = tk.Tk()
window.geometry("1366x768")
window.resizable(False,False)
window.title("RECOGNITO")
window.rowconfigure(0,weight=1)
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='icon.png'))

filename = ImageTk.PhotoImage(Image.open('Background.jpg' ))
###################################################--------------------STARTUP PAGE----------############################################################
Startup = tk.Frame(window)
Startup.grid(row=0,column=0,stick='nsew')

background_label = tk.Label(Startup)
background_label.place(x=-2, y=0, relwidth=1, relheight=1)

player = tkvideo("RECOGNITO.mp4", background_label,
                 loop = 1, size = (1366, 768))
player.play()


login = tk.Button(Startup, text="LOGIN", command=psw,fg="BLACK"  ,bg="WHITE"  ,width=20 ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
login.place(x=430, y=500)

Forget = tk.Button(Startup, text="Forgot Password", command=contact  ,fg="BLACK"  ,bg="WHITE"  ,width=20 , activebackground = "white" ,font=('Century Gothic', 15))
Forget.place(x=740, y=500)

Enter_PSW = tk.Label(Startup, text="Enter Your Password " ,bg="WHITE" ,fg="BLACK"  ,width=20 ,height=1,font=('Century Gothic', 17, ))
Enter_PSW.place(x=565, y=390)

global PSW_INP
PSW_INP = tk.Entry(Startup, width=25, fg="black", relief='solid', font=('Century Gothic', 28), show='*')
PSW_INP.place(x=430, y=430)
PSW_INP.bind('<Return>', func)

clearButton = tk.Button(Startup, text="Clear", command=clear4  ,fg="White"  ,bg="#111211"  ,width=8 ,activebackground = "white" ,font=('Century Gothic', 18))
clearButton.place(x=860, y=427)


########################################################--------MAIN MENU PAGE############################################################################

MainPage = tk.Frame(window, width= 1366 , height= 768)
MainPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(MainPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


button1 = Button(MainPage, text="R e g i s t e r   a   N e w    S t u d e n t",font=('Quantum Mechanics', 12 ,'bold'), command=lambda : show_frame(Registerpage),relief=RAISED, bg="#85a8b5", fg="#fff", activebackground="#000", activeforeground="#fff", width= 35, height=2)
button1.pack()
button1.place(x=150,y=230)

button2 = Button(MainPage, text="T a k e   A t t e n d a n c e",font=('Quantum Mechanics', 12 ,'bold'),command=lambda : show_frame(TakeattdPage),relief=RAISED, bg="#85a8b5", fg="#fff", activebackground="#000", activeforeground="#fff", width= 35, height=2)
button2.pack()
button2.place(x=150,y=320)

button3= Button(MainPage, text="V i e w   A t t e n d a n c e",font=('Quantum Mechanics', 12,'bold'),command=lambda : [show_frame(ViewPage),viewtablee()],relief=RAISED, bg="#85a8b5", fg="#fff", activebackground="#000", activeforeground="#fff", width= 35, height=2)
button3.pack()
button3.place(x=150,y=410)

button4= Button(MainPage, text="M a i l   A t t e n d a n c e",font=('Quantum Mechanics', 12,'bold'),command=lambda : show_frame(sendPage),relief=RAISED, bg="#85a8b5", fg="#fff", activebackground="#000", activeforeground="#fff", width= 35, height=2)
button4.pack()
button4.place(x=150,y=500)

button5= Button(MainPage, text="L o g  O u t",font=('Quantum Mechanics', 12, 'bold' ),command=lambda : confirm1(),bg="#404040", fg="#fff", activebackground="#000", activeforeground="#fff", width= 20, height=2)
button5.pack()
button5.place(x=1150,y=610)

button6= Button(MainPage, text=" Q u i t ",font=('Quantum Mechanics', 12, 'bold' ),command=lambda : confirm2(), bg="#404040", fg="#fff", activebackground="#000", activeforeground="#fff", width= 20, height=2)
button6.pack()
button6.place(x=1150,y=680)

button8= Button(MainPage, text="C h a n g e  P a s s w o r d",font=('Quantum Mechanics', 12, 'bold' ),command=lambda : change_pass(),bg="#404040", fg="#fff", activebackground="#000", activeforeground="#fff", width= 20, height=2)
button8.pack()
button8.place(x=1150,y=530)

button9 = Button(MainPage, text="V i e w  R e g i s t e r e d  S t u d e n t s",font=('Quantum Mechanics', 12 ,'bold'), command=lambda : [show_frame(StudPage),viewtable1()],relief=RAISED, bg="#85a8b5", fg="#fff", activebackground="#000", activeforeground="#fff", width= 35, height=2)
button9.pack()
button9.place(x=150,y=150)

datef = tk.Label(MainPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

clock = tk.Label(MainPage,fg="white",bg="#262523" ,height=1,font=('Century Gothic', 25))
clock.pack()
clock.place(x=600,y=973333)
tick()

#################################--------------REGISTER PAGE------------------############################################################
Registerpage = tk.Frame(window, width= 1366 , height= 768)
Registerpage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(Registerpage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Regframe = tk.Frame(Registerpage, bg="#D0D3D4")
Regframe.place(relx=0.05, rely=0.17, relwidth=0.38, relheight=0.80)

head2 = tk.Label(Regframe, text="                     New Students Registration                         ", fg="White",bg="#424949" ,font=('Century Gothic', 17), height=1)
head2.place(x=0,y=0)

lbl = tk.Label(Regframe, text="Enter Roll number:",width=20  ,height=1  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 18) )
lbl.place(x=-10, y=55)

txt = tk.Entry(Regframe,width=32 ,fg="black",font=('Century Gothic', 19))
txt.place(x=37, y=100)

lbl3 = tk.Label(Regframe, text="Enter Faculty:",width=20  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 18))
lbl3.place(x=-42, y=255)

txt5 = tk.Entry(Regframe,width=32 ,fg="black",font=('Century Gothic', 19))
txt5.place(x=37, y=288)

lbl2 = tk.Label(Regframe, text="Enter Name:",width=20  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 18))
lbl2.place(x=-42, y=165)

txt2 = tk.Entry(Regframe,width=32 ,fg="black",font=('Century Gothic', 19)  )
txt2.place(x=37, y=200)

takeImg = tk.Button(Regframe, text="➔ Take Images", command=TakeImages  ,fg="white"  ,bg="#614f41"  ,width=34  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
takeImg.place(x=45, y=355)

trainImg = tk.Button(Regframe, text="➔ Register Student", command=TrainImages,fg="white"  ,bg="#614f41"  ,width=34  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
trainImg.place(x=45, y=430)

datef = tk.Label(Registerpage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(Registerpage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

clearButton = tk.Button(Regframe, text="Clear", command=clear  ,fg="White"  ,bg="#111211"  ,width=12 ,activebackground = "white" ,font=('Century Gothic', 14))
clearButton.place(x=350, y=97)
clearButton2 = tk.Button(Regframe, text="Clear", command=clear2  ,fg="White"  ,bg="#111211"  ,width=12 , activebackground = "white" ,font=('Century Gothic', 14))
clearButton2.place(x=350, y=195)
clearButton3 = tk.Button(Regframe, text="Clear", command=clear5  ,fg="White"  ,bg="#111211"  ,width=12 , activebackground = "white" ,font=('Century Gothic', 14))
clearButton3.place(x=350, y=289)
###############################------------------TAKE ATTENDANCE PACE--------------------###################################################
TakeattdPage = tk.Frame(window, width= 1366 , height= 768)
TakeattdPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(TakeattdPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Takeattd = tk.Frame(TakeattdPage, bg="#D0D3D4")
Takeattd.place(relx=0.05, rely=0.25, relwidth=0.38, relheight=0.50)

message1 = tk.Label(Takeattd, text="Steps to Take Attendance:" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message1.place(x=0, y=0)

message2 = tk.Label(Takeattd, text="➜ Click on Take Attendance after each" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message2.place(x=0, y=40)

message3 = tk.Label(Takeattd, text="individual attendance is registered" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message3.place(x=0, y=65)

trackImg = tk.Button(TakeattdPage, text="Take Attendance", command=TrackImages  ,fg="White"  ,bg="#614f41"  ,width=30  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
trackImg.place(x=145,y=480)

back = tk.Button(TakeattdPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

datef = tk.Label(TakeattdPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

##################################------------------VIEW ATTENDANCE PAGE ----------------########################################################
ViewPage = tk.Frame(window, width= 1366 , height= 768)
ViewPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(ViewPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Viewframe = tk.Frame(ViewPage, bg="#D0D3D4")
Viewframe.place(relx=0.05, rely=0.20, relwidth=0.38, relheight=0.60)

def viewtablee():
    tv= ttk.Treeview(Viewframe,height =13,columns = ('name','date','time'))
    tv.column('#0',width=82)
    tv.column('name',width=130)
    tv.column('date',width=133)
    tv.column('time',width=133)
    tv.grid(row=2,column=0,padx=(17,0),pady=(150,0),columnspan=4)
    tv.heading('#0',text ='ID')
    tv.heading('name',text ='NAME')
    tv.heading('date',text ='DATE')
    tv.heading('time',text ='TIME' )
    scroll = ttk.Scrollbar(Viewframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
            i = 0
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if (i > 1):
                    if (i % 2 != 0):
                        iidd = str(lines[0]) + '   '
                        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
        csvFile1.close()

message = tk.Label(Viewframe, text="Attendance For the Date: " + date  ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message.place(x=20, y=40)

datef = tk.Label(ViewPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(ViewPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

#####################################-----------VIEW STUDENTS PAGE----------------##############################################################
StudPage = tk.Frame(window, width= 1366 , height= 768)
StudPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(StudPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Studframe = tk.Frame(StudPage, bg="#D0D3D4")
Studframe.place(relx=0.05, rely=0.20, relwidth=0.38, relheight=0.60)

def viewtable1():
    tv = ttk.Treeview(Studframe, height=13, columns=('class', 'roll', 'name'))
    tv.column('#0', anchor=CENTER, width=82)
    tv.column('class', anchor=CENTER, width=130)
    tv.column('roll', anchor=CENTER, width=133)
    tv.column('name', anchor=CENTER, width=133)
    tv.grid(row=2, column=0, padx=(17, 0), pady=(150, 0), columnspan=4)
    tv.heading('#0', text='ID')
    tv.heading('name', text='NAME')
    tv.heading('roll', text='ROLL NUMBER')
    tv.heading('class', text='Faculty')
    scroll = ttk.Scrollbar(Studframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            i = 0
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if (i > 1):
                    if (i % 2 != 0):
                        iidd = str(lines[0]) + '   '
                        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))

    csvFile1.close()
message = tk.Label(Studframe, text=" Registered Students Information" , bg="#D0D3D4", fg="black", width=39, height=1,
                       font=('Century Gothic', 15,))
message.place(x=20, y=40)

datef = tk.Label(StudPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.place(x=760,y=390)

back = tk.Button(StudPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)
###################################################################################################

message = tk.Label(Viewframe, text="Attendance For the Date: " + date  ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message.place(x=20, y=40)

datef = tk.Label(ViewPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(ViewPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

def openattendancefile():
    tv= ttk.Treeview(Viewframe,height =13,columns = ('name','date','time'))
    tv.column('#0',width=82)
    tv.column('name',width=130)
    tv.column('date',width=133)
    tv.column('time',width=133)
    tv.grid(row=2,column=0,padx=(17,0),pady=(150,0),columnspan=4)
    tv.heading('#0',text ='ID')
    tv.heading('name',text ='NAME')
    tv.heading('date',text ='DATE')
    tv.heading('time',text ='TIME' )
    scroll = ttk.Scrollbar(Viewframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    with open(askopenfilename()) as csvFile1:
        i = 0
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    message = tk.Label(Viewframe, text=csvFile1.name.split("/")[-1], bg="#D0D3D4", fg="black", width=39, height=1,
                       font=('Century Gothic', 15,))
    message.place(x=20, y=40)

open1 = tk.Button(ViewPage, text="View Attendance", command=lambda: openattendancefile(), fg="white", bg="#404040",
                         width=20, height=1, activebackground="white", font=('Century Gothic', 15))
open1.place(x=180, y=240)

################################################ SEND EMAIL PAGE ########################################################################

sendPage = tk.Frame(window, width= 1366 , height= 768)
sendPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(sendPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Sendmailframe = tk.Frame(sendPage, bg="#D0D3D4")
Sendmailframe.place(relx=0.05, rely=0.20, relwidth=0.38, relheight=0.30)

lbl4 = tk.Label(Sendmailframe, text='Enter Email to Send Attendance:', bg='#d0d3d4', font=('Century Gothic', 15))
lbl4.place(x=85, y=10)
datef = tk.Label(sendPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#90acbc" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(sendPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

def sendmail():
    fromaddr = "recognito.attendance@gmail.com"
    toaddr = old1.get()
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Attendance For the date: " + date
    body = "The attendance for the date: " + date + " is attached below:"
    msg.attach(MIMEText(body, 'plain'))
    filename = "Attendance_" + date + ".csv"
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        attachment = open("Attendance\Attendance_" + date + ".csv", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(fromaddr, "tcygtpwzkjbwpyhu")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        mess._show(title='Sucessfull',
                   message="Attendance for the Date: " + date + " is sent to " +toaddr)
    else :
        mess._show(title='Error',
                   message="Attendance for the Date: "+date+" is not taken")

global old1
old1 = tk.Entry(Sendmailframe, width=35, fg="black", relief='solid', font=('Century Gothic', 17), )
old1.place(x=15, y=80)
old1.bind('<Return>', sendmail)

send = tk.Button(sendPage, text="Send", command=sendmail, fg="White", bg="#614f41", height=1, width=35, activebackground="white", font=('Century Gothic', 13))
send.place(x=130, y=300)

clearButton = tk.Button(sendPage, text="Clear", command=clear3, fg="White", bg="#111211", relief="raised", width=12,
                        activebackground="white", font=('Century Gothic', 12))
clearButton.place(x=445, y=231)

show_frame(Startup)
########################################################################################################################
window.mainloop()