############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
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

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%I:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us at : himalpanta@gmail.com or      nijanaryal17@gmail.com ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some files are missing', message='Please contact us for help')
        window.destroy()

###################################################################################

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

###################################################################################

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

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "Register a Student"
    message1.configure(text=res)
    busted_display = Label(window, text="Please Input A Roll Number", font=("Century Gothic ", "16"), bg="#D0D3D4",width=24,height=1)
    busted_display.place(x=800, y=355)
    window.after(2400, busted_display.destroy)

def clear2():
    txt2.delete(0, 'end')
    res = "Register a Student"
    message1.configure(text=res)
    busted_display = Label(window, text="Please Input A Name", font=("Century Gothic ", "16"), bg="#D0D3D4", width=24, height=1)
    busted_display.place(x=800, y=357)
    window.after(2400, busted_display.destroy)

def clear3():
    name.delete(0, 'end')

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
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
    if ((name.isalpha()) or (' ' in name)):
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
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w], [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 50
            elif sampleNum > 50:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

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
    res = "Student Registered Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
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
            if (conf < 70):
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
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))


    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1366x768")
window.resizable(False,False)
window.title("RECOGNITO")
photo = PhotoImage(file = "icon.png")
window.iconphoto(False, photo)

filename = ImageTk.PhotoImage(Image.open('Background.jpg' ))
background_label = tk.Label(window, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame1 = tk.Frame(window, bg="#CACFD2")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#D0D3D4")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text=" RECOGNITO " ,fg="white",bg="#1a1a1a" ,width=45 ,height=1,font=('Quantum', 35))
message3.place(x=0, y=0)
message3 = tk.Label(window, text="📷" ,fg="white",bg="#1a1a1a" ,width=2 ,height=2,font=('Quantum', 30))
message3.place(x=480, y=-34)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text =day+"-"+mont[month]+"-"+year+" | ", fg="white",bg="#262523" ,width=55 ,height=1,font=('Century Gothic', 18))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="white",bg="#262523" ,width=55 ,height=1,font=('Century Gothic', 25))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                     New Students Registration                         ", fg="White",bg="#424949" ,font=('Century Gothic', 17), height=1)
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                        Attendance Section                                 ", fg="White",bg="#424949" ,font=('Century Gothic', 17) )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter Roll number",width=20  ,height=1  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 17) )
lbl.place(x=90, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('Century Gothic', 15))
txt.place(x=70, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 17))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('Century Gothic', 15)  )
txt2.place(x=70, y=173)

message1 = tk.Label(frame2, text="Register a Student" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#D0D3D4" ,fg="black"  ,width=39,height=1, font=('Century Gothic', 16))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#D0D3D4"  ,height=1 ,font=('Century Gothic', 17))
lbl3.place(x=115, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

######################################## SEND EMAILS ###########################################

def email():
    global master1
    master1 = tk.Tk()
    master1.geometry("400x160")
    master1.resizable(False, False)
    master1.title("Send Email")
    master1.configure(background="white")
    master1.eval('tk::PlaceWindow . center')
    lbl4 = tk.Label(master1, text='Enter Email to Send Attendance:', bg='white', font=('Century Gothic', 15))
    lbl4.place(x=15, y=10)

    global old1
    old1 = tk.Entry(master1, width=40, fg="black", relief='solid', font=('Century Gothic', 13), )
    old1.place(x=15, y=45)
    old1.bind('<Return>', sendmail)
    send = tk.Button(master1, text="Send", command=sendmail, fg="White", bg="#614f41", height=1, width=35, activebackground="white", font=('Century Gothic', 13))
    send.place(x=15, y=100)
    clearButton = tk.Button(master1, text="Clear", command=clear3, fg="White", bg="#111211", relief="raised", width=12,activebackground="white", font=('Century Gothic', 10))
    clearButton.place(x=280, y=43)

def sendmail():
    fromaddr = "recognito.attendance@gmail.com"
    toaddr = old1.get()
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    # storing the senders email address
    msg['From'] = fromaddr
    # storing the receivers email address
    msg['To'] = toaddr
    # storing the subject
    msg['Subject'] = "Attendance For the" + date
    # string to store the body of the mail
    body = "The attendance for the date: " + date + " is attached below:"
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent
    filename = "Attendance_" + date + ".csv"
    attachment = open("Attendance\Attendance_" + date + ".csv", "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(fromaddr, "Auth8848")
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    # terminating the session
    s.quit()

##################### MENUBAR #################################
menubar = tk.Menu(window)

menubar.add_cascade(label='Change Password',font=('Century Gothic', 29),command= change_pass)
menubar.add_cascade(label='Contact',font=('Century Gothic', 29),command= contact)
menubar.add_command(label='Exit',font=('Century Gothic', 29), command = window.destroy)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(17,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME' )


###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="White"  ,bg="#111211"  ,width=12 ,activebackground = "white" ,font=('Century Gothic', 10))
clearButton.place(x=335, y=86)

clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="White"  ,bg="#111211"  ,width=12 , activebackground = "white" ,font=('Century Gothic', 10))
clearButton2.place(x=335, y=172)

takeImg = tk.Button(frame2, text="➔ Take Images", command=TakeImages  ,fg="white"  ,bg="#614f41"  ,width=34  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
takeImg.place(x=30, y=300)

trainImg = tk.Button(frame2, text="➔ Register Student", command=TrainImages,fg="white"  ,bg="#614f41"  ,width=34  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
trainImg.place(x=30, y=380)

trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="White"  ,bg="#614f41"  ,width=35  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
trackImg.place(x=47,y=65)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="White"  ,bg="#111211"  ,width=35 ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
quitWindow.place(x=47, y=450)

sendemails = tk.Button(frame2, text="Mail Attendance", command=email ,fg="White"  ,bg="#614f41"  ,width=20 ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
sendemails.place(x=125, y=500)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
