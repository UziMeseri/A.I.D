"""This file contains the client GUI"""
import os
import threading
import tkinter
import customtkinter
from PIL import ImageTk, Image
import cv2
from customtkinter import CTkToplevel

from TakeImage import TakePicture
import Functions
import time
from datetime import datetime


class Login(customtkinter.CTk):
    """Class gets the client as a parameter and sets up the login GUI. Example : Login(client) --> Opens a login page"""

    def __init__(self, user):
        super().__init__()

        # Window details
        customtkinter.set_appearance_mode("Dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.geometry("400x550")
        self.title("Login")
        self.user = user
        self.resizable(False, False)

        # Labels
        self.text_var = tkinter.StringVar(value="Welcome to A.I.D - Artificial Intelligence Detection")
        self.Title = customtkinter.CTkLabel(master=self,
                                            textvariable=self.text_var,
                                            width=120,
                                            height=25,
                                            fg_color=("white", "#74747A"),
                                            corner_radius=8, font=("Overpass", 18))
        self.Title.place(relx=0.5, rely=0.035, anchor=tkinter.CENTER)

        self.LoginLabel = customtkinter.CTkLabel(master=self, text="Login : ",
                                                 font=("calibri", 22, 'bold', 'underline'))
        self.LoginLabel.place(relx=0.1, rely=0.5, anchor=tkinter.CENTER)

        self.UserLabel = customtkinter.CTkLabel(master=self, text="Username ", font=("calibri", 18, 'bold'))
        self.UserLabel.place(relx=0.11, rely=0.543, anchor=tkinter.CENTER)

        self.PassLabel = customtkinter.CTkLabel(master=self, text="Password ", font=("calibri", 18, 'bold'))
        self.PassLabel.place(relx=0.11, rely=0.593, anchor=tkinter.CENTER)

        # Logo
        try:
            self.Logo = ImageTk.PhotoImage(Image.open("Logos/Logo1RedSmall.png"))
            self.panel = tkinter.Label(self, image=self.Logo, bd=0)
            self.panel.place(x=100, y=40)
        except:
            'Logo Not Found'

        #  Entries
        self.UserEntry = customtkinter.CTkEntry(master=self, placeholder_text="Enter Username", width=250, height=20)
        self.UserEntry.place(relx=0.55, rely=0.545, anchor=tkinter.CENTER)

        self.PassEntry = customtkinter.CTkEntry(master=self, placeholder_text="Enter Password", width=250, height=20)
        self.PassEntry.place(relx=0.55, rely=0.6, anchor=tkinter.CENTER)

        # Buttons
        self.button = customtkinter.CTkButton(master=self, text="Login", command=self.LoginButton)
        self.button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

    def HashPass(self,Pass):
        """Function receives a string which contains the entered password and hashes it"""
        import hashlib
        hash_md5 = hashlib.md5(Pass.encode())  # make hash MD5 to  string
        return hash_md5.hexdigest()

    def LoginButton(self):
        """Function doesn't get any parameters and is used to send login details over to the server."""
        Username = str(self.UserEntry.get())
        Password = str(self.PassEntry.get())
        Continue = True
        Keywords = ['or','oR','Or','OR','drop','Drop','DRop','DROp','DROP','dRop','dROp','dROP','drOp','drOP','droP']
        for word in Keywords:
            if word in Password or word in Username:
                responseLabel = customtkinter.CTkLabel(master=self, text='Username and password cannot contain the word "or" or "drop" \n in all their variations', font=("calibri", 12))
                responseLabel.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
                Continue = False

        if(Continue):
            Password = self.HashPass(Password) # Hashing password against "Man in the middle"

            self.user.send(Username.encode())
            self.user.send(Password.encode())

            response = self.user.recv(1024).decode()
            if response == "Connected successfully!":
                Login.withdraw(self) # Close login window
                self.toplevel_window = MainWindow(self.user) # Open main window.

            # Server response in case login details are wrong.
            response = response + "                          "
            responseLabel = customtkinter.CTkLabel(master=self, text=response, font=("calibri", 12))
            responseLabel.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


class MainWindow(customtkinter.CTkToplevel):
    """Class gets the client as a parameter and sets up the main window GUI.
    Example : MainWindow(client) --> Opens a the main window"""
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window details
        self.geometry("1500x800")
        self.user = user
        self.title("A.I.D - Artificial Intelligence Detection")
        self.resizable(False, False)

        # Entries
        self.ObjectEntry = customtkinter.CTkEntry(master=self, placeholder_text="Enter Object")
        self.ObjectEntry.place(relx=0.1, rely=0.008)

        # Buttons
        self.button = customtkinter.CTkButton(master=self, text="Capture", command=self.capture)
        self.button.place(relx=0.05, rely=0.025, anchor=tkinter.CENTER)

        self.button = customtkinter.CTkButton(master=self, text="Save", command=self.save)
        self.button.place(relx=0.25, rely=0.025, anchor=tkinter.CENTER)

        self.button = customtkinter.CTkButton(master=self, text="Exit", command=self.exit)
        self.button.place(relx=0.95, rely=0.025, anchor=tkinter.CENTER)

        self.button = customtkinter.CTkButton(master=self, text="Objects", command=self.Objects)
        self.button.place(relx=0.35, rely=0.025, anchor=tkinter.CENTER)

        # Labels
        self.VideoLabel = customtkinter.CTkLabel(master=self, text="Video Display",
                                                 font=("calibri", 22, 'bold', 'underline'))
        self.VideoLabel.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)

        self.ImageDisplay = customtkinter.CTkLabel(master=self, text="Detected Image",
                                                   font=("calibri", 22, 'bold', 'underline'))
        self.ImageDisplay.place(relx=0.75, rely=0.1, anchor=tkinter.CENTER)

        self.Label = customtkinter.CTkLabel(master=self,
                                            text="Please wait patiently for the result, it will come within a couple of seconds. \n Your system may be unresponsive during this time. ",
                                            font=("calibri", 36, 'bold'))
        self.Label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # Video display configuration.
        app = tkinter.Frame(self, bg="white")
        app.grid()
        app.place(relx=0.23, rely=0.43, anchor=tkinter.CENTER)
        # Create a label in the frame
        VideoDisplay = tkinter.Label(app)
        VideoDisplay.grid()

        cap = cv2.VideoCapture(0)

        def video_stream():
            """Function receives no parameters and return a video display if a camera is connected."""
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            VideoDisplay.imgtk = imgtk
            VideoDisplay.configure(image=imgtk)
            VideoDisplay.after(1, video_stream)

        video_stream()

    def save(self):
        """Function receives self and saves the current displayed image in a 'Saves' directory.
        This function is accessed through a button labeled 'Save' on the GUI.
        upon pressing button it saves the currently displayed image to the directory, and rename to the current date."""
        current = datetime.now()
        date = current.strftime("%d/%m/%Y %H:%M:%S")
        date = date.replace('/', '.')
        date = date.replace(':', '.')
        date = date.replace(' ', '-')
        try:
            os.rename('Detected.jpg', f'Saves/{date}.jpg')
        except:
            "Image doesnt exist"

    def exit(self):
        """Function receives self, it disconnects client from the server and closes the GUI.
        This function is accessed through a button labeled 'Exit' on the GUI."""
        self.user.send("Exit".encode())
        self.destroy()

    def Objects(self):
        """Function receives self, it opens a new side window for the client to see what options he has for an object input"""
        ObjectWindow = CTkToplevel(self)
        ObjectWindow.geometry("800x500")
        ObjectWindow.Welcome = customtkinter.CTkLabel(master=ObjectWindow, text="Please choose a category.",font=("calibri", 32, 'bold'))
        ObjectWindow.Welcome.place(relx=0.23, rely=0.12, anchor=tkinter.CENTER)

        def DisplayObjects(Choice):
            '''Function receives the users choice and then displays all items in that category'''
            try: # remove last display if exists
                ObjectWindow.Column1Display.destroy()
                ObjectWindow.Column2Display.destroy()
                ObjectWindow.Column3Display.destroy()
                ObjectWindow.Welcome.destroy()
            except:
                'Doesnt exist'

            Column1=''
            Column2 = ''
            Column3 = ''
            index = 0 # Index of current item.
            for Object in Choice: # Add all items in list to 3 string variables respresenting 3 columns.
                index = index + 1
                if (index % 3 == 0):
                    Column1 = Column1+" - "+Object+"\n"
                if (index % 3 == 1):
                    Column2 = Column2 + " - " + Object + "\n"
                if (index % 3 == 2):
                    Column3 = Column3 + " - " + Object + "\n"

            # Explanation for the user
            ObjectWindow.Welcome = customtkinter.CTkLabel(master=ObjectWindow, text="The system can detect the following objects.",font=("calibri", 32, 'bold'))
            ObjectWindow.Welcome.place(relx=0.38, rely=0.12, anchor=tkinter.CENTER)

            # Display columns
            ObjectWindow.Column1Display = customtkinter.CTkLabel(master=ObjectWindow, text=Column1,font=("calibri", 32, 'bold'))
            ObjectWindow.Column1Display.place(relx=0.15, rely=0.6, anchor=tkinter.CENTER)

            ObjectWindow.Column2Display = customtkinter.CTkLabel(master=ObjectWindow, text=Column2,font=("calibri", 32, 'bold'))
            ObjectWindow.Column2Display.place(relx=0.50, rely=0.6, anchor=tkinter.CENTER)

            ObjectWindow.Column3Display = customtkinter.CTkLabel(master=ObjectWindow, text=Column3,font=("calibri", 32, 'bold'))
            ObjectWindow.Column3Display.place(relx=0.85, rely=0.6, anchor=tkinter.CENTER)

        # Buttons
        ObjectWindow.button = customtkinter.CTkButton(master=ObjectWindow, text="Animals", command= lambda: DisplayObjects(Animals))
        ObjectWindow.button.place(relx=0.10, rely=0.042, anchor=tkinter.CENTER)

        ObjectWindow.button = customtkinter.CTkButton(master=ObjectWindow, text="Transport", command= lambda: DisplayObjects(Transport))
        ObjectWindow.button.place(relx=0.30, rely=0.042, anchor=tkinter.CENTER)

        ObjectWindow.button = customtkinter.CTkButton(master=ObjectWindow, text="Household", command= lambda: DisplayObjects(Household))
        ObjectWindow.button.place(relx=0.50, rely=0.042, anchor=tkinter.CENTER)

        ObjectWindow.button = customtkinter.CTkButton(master=ObjectWindow, text="Food", command= lambda: DisplayObjects(Food))
        ObjectWindow.button.place(relx=0.70, rely=0.042, anchor=tkinter.CENTER)

        ObjectWindow.button = customtkinter.CTkButton(master=ObjectWindow, text="Other", command= lambda: DisplayObjects(Other))
        ObjectWindow.button.place(relx=0.90, rely=0.042, anchor=tkinter.CENTER)

        # Catalogs
        Animals = ['person','bird','cat','dog', 'horse','sheep','cow','elephant','bear','zebra','giraffe',]
        Transport = ['bicycle','car','motorcycle','airplane','bus', 'train','truck','boat','traffic light','fire hydrant','stop sign','parking meter']
        Household = ['wine glass','cup','fork','knife','spoon','bowl','chair','couch','potted plant','bed','dining table','toilet','tv', 'laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster', 'sink','refrigerator','book','clock','vase','hairdryer','toothbrush']
        Food = ['banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut', 'cake',]
        Other = ['bench','backpack','umbrella','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','mask','teddybear','scissors']



    def TakePicture(self):
        """This function receives self, it takes a picture of whatever is currently being displayed."""
        import cv2

        # Create a VideoCapture object
        cap = cv2.VideoCapture(0)

        # Set the video frame width and height
        cap.set(3, 640)
        cap.set(4, 480)

        # Get a single frame from the camera
        ret, frame = cap.read()

        # Show the frame
        cv2.imshow("frame", frame)

        # Save the frame to an image file
        cv2.imwrite("(Client) capture.jpg", frame)

        # Release the VideoCapture object
        cap.release()

    def capture(self):
        """This function receives self, it is accessed through a button labeled 'Capture' pn the GUI.
        The function takes a picture using TakePicture(), and sends the server the image and the object entry.
        After a couple of seconds the functions receives the detected image.
        The function also removes redundant files to save space and keep everything organized."""

        Continue = True
        self.Excepction = customtkinter.CTkLabel(master=self, text="", font=("calibri", 18, 'bold'))
        self.Excepction.place(relx=0.35, rely=0.9)

        try:  # At the beginning of each capture we will remove the last file so that there will be no confusion between the new file and the old file
            os.remove('Detected.jpg')
            os.remove('(Client) capture.jpg')
        except:
            'Something went wrong'

        if self.ObjectEntry.get() == '':  # If not object was entered
            self.Excepction = customtkinter.CTkLabel(master=self, text="Please enter an object to detect!", font=("calibri", 28, 'bold'),fg_color=("#FF0000", "#242424"),text_color="#FF0000")
            self.Excepction.place(relx=0.35, rely=0.9)
            Continue = False

        if Continue:  # If everything is ok and an object was entered
            self.user.send(self.ObjectEntry.get().encode())
            threading.Thread(target=TakePicture).start()
            time.sleep(0.25)
            Functions.Send_Image(self.user, '(Client) capture.jpg')
            Message = self.user.recv(1024).decode()  # Response from server

            if Message == 'Known Object':
                Functions.Recv_Image(self.user) # Receiving detected image
                os.rename('(Server) (Server) DetectedImage.jpg', 'Detected.jpg')

                try:
                    self.result = ImageTk.PhotoImage(Image.open("Detected.jpg"))
                    self.panel = tkinter.Label(self, image=self.result, bd=0)
                    self.panel.place(relx=0.55, rely=0.15)
                except:
                    print("something went wrong")

            else:
                self.Excepction = customtkinter.CTkLabel(master=self, text="'The Object you entered is not a known object. \n 'Please try another object'",
                                                         font=("calibri", 28, 'bold'), fg_color=("#FF0000", "#242424"),
                                                         text_color="#FF0000")
                self.Excepction.place(relx=0.35, rely=0.9)



        # Redisplay the camera
        app = tkinter.Frame(self, bg="white")
        app.grid()
        app.place(relx=0.23, rely=0.43, anchor=tkinter.CENTER)
        # Create a label in the frame
        VideoDisplay = tkinter.Label(app)
        VideoDisplay.grid()

        cap = cv2.VideoCapture(0)

        def video_stream():
            """Function receives no parameters and return a video display if a camera is connected."""
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            VideoDisplay.imgtk = imgtk
            VideoDisplay.configure(image=imgtk)
            VideoDisplay.after(1, video_stream)

        video_stream()
