import os
def Recv_Image(user):
    '''Function receives a user and that user receives an image'''
    FILE_NAME = user.recv(1024).decode()
    user.send(f"File name {FILE_NAME} received ".encode())
    file = FILE_NAME.split(".")[0]
    print(FILE_NAME)
    file_size = int(user.recv(1024).decode())
    user.send(f"File size {FILE_NAME} received ".encode())
    file = open('(Server) ' + file + '.jpg', "ab")
    data = user.recv(file_size)
    file.write(data)
    file.close()



def Send_Image(user,name):
    '''Function receives a user and file name and that user sends an image'''
    file = open(name, "rb")
    file_content = file.read()
    user.send(name.encode())
    print(user.recv(1024).decode())
    file_size = os.path.getsize(f'{name}')
    user.send(str(file_size).encode())
    print(user.recv(1024).decode())
    user.send(file_content)
    file.close()

def IsIn(Dict,Obj):
    '''Function receives a dictionary and a string containing the object the user wants to detect, this function
    returns True if object exists in the dictionary (i.e a known object), and False otherwise (i.e not a known
    object) '''
    Obj = Obj.lower()
    for Key in Dict:
        if(Obj == Dict[Key]):
            return True
    return False




