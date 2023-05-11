"""This file deals with opening a server and calling the DetectOBJ module."""
import os
import socket
import threading
import DetectOBJ.ODM
from DBFunctions import DB
import Functions

# Server details
PORT = 4442
IP = "192.168.1.25"
Client_Connected = False

# Server Setup
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))
server.listen()
print("Server open for clients")
conn,addr = server.accept()

# Checking if username and password are correct.
# Username and password are set to default to prevent system crash in case user didn't enter any login details.
try:
    Username = conn.recv(1024).decode()
    Password = conn.recv(1024).decode()
except:
    Username = 'Default'
    Password = 'Default'

KnownObjects = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
                                 6: 'train',
                                 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign',
                                 12: 'parking meter',
                                 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow',
                                 20: 'elephant',
                                 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag',
                                 27: 'tie',
                                 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball',
                                 33: 'kite',
                                 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard',
                                 38: 'tennis racket',
                                 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon',
                                 45: 'bowl',
                                 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot',
                                 52: 'hot dog',
                                 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant',
                                 59: 'bed',
                                 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
                                 66: 'keyboard',
                                 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
                                 72: 'refrigerator',
                                 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
                                 78: 'hair dryer',
                                 79: 'toothbrush',80:'mask'}  # List of known objects
Database = DB()  # Creates a database to use functions on (CheckLogin, etc..)


while True:  # Receiving username and password to check for login.
    if(DB.CheckLogin(Database,Username,Password)):  # Check login info
        conn.send("Connected successfully!".encode())
        Client_Connected = True
        break

    Keyword = "or"

    conn.send("Username or Password are incorrect, please try again.".encode())
    Username = conn.recv(1024).decode()
    Password = conn.recv(1024).decode()



def SendRecv():  # Function responsible for communication between the 2 ends
    """Function receives no parameters. However, it waits for the client to send an image.
    After receiving the image, it sends it to the ODM module which detects the desired object."""
    while True:
        Object = conn.recv(1024).decode()
        if(Object == "Exit"):  # Exit button was pressed
            conn.close()
            break
        print(Object)

        Functions.Recv_Image(conn) # Receiving image
        if Functions.IsIn(KnownObjects,Object): # Checking if object is known
            Message = 'Known Object'
            print(Message)
            if Object.lower() == 'mask': # Checking if object is a mask
                DetectOBJ.ODM.CustomDetection()
            else:
                DetectOBJ.ODM.DetectOBJ(Object) # ODM module.
        else:
            Message = 'The Object you entered is not a known object. ' \
                      'Please try another object'
            print(Message)
            try:
                os.remove('(Server) DetectedImage.jpg')  # File isn't useful anymore so we delete it
            except:
                'File not found'

        conn.send(Message.encode())
        if Message == 'Known Object': # Send the image back if object is known
            Functions.Send_Image(conn,'(Server) DetectedImage.jpg')
            os.remove('(Server) DetectedImage.jpg')

            # removes the picture, since it has no purpose anymore and solely takes space.
            try:
                os.remove('(Server) (Client) capture.jpg')
            except:
                print("doesnt exists")

threading.Thread(target=SendRecv).start()
