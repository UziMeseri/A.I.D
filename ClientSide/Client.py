"""This file deals with connecting a client to the server."""
import socket
import threading
from LoginPage import Login


# Server details and setup
PORT = 4442
IP = "192.168.1.25"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP,PORT))
Connected = False

# GUI
Window = Login(client)
th = threading.Thread(target=Login,args=[client])
th.start()
Window.mainloop()
