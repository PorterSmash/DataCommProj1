# Import socket module 
import socket
import os	

def utf8len(s):
    return bytes(len(s.encode('utf-8')))

def download(s) :
    filename = input("Enter your filename: ")
    s.sendall(bytes(filename, 'utf-8'))

    length_rec = (s.recv(128)).decode('utf-8')
    length_int = int(length_rec)
    n = 0

    file = open(filename, "w")
    while (n < length_int) :
        text = (s.recv(1024)).decode('utf-8')
        file.write(text)
        n += 1024
    file.close()

def upload(s) :
    filename = input("Enter your filename: ")
    s.sendall(bytes(filename, 'utf-8'))

    file = open(filename)
    fsize = os.stat(filename)
    fsize = fsize.st_size
    fsizestr = str(fsize)
    s.sendall(bytes(fsizestr, 'utf-8'))

    fileRam = ""
    for line in file:
      fileRam += line

    s.sendall(bytes(fileRam, 'utf-8'))
    print("Done sending")

    file.close()

# Create a socket object 
s = socket.socket()		 

# Define the port on which you want to connect 
port = 12345				

# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

# receive data from the server 
print( (s.recv(1024).decode('utf-8')))
download(s)
#filename = input("Enter your filename: ")
#s.sendall(bytes(filename, 'utf-8'))

#print(s.send(utf8len(message)))
#length_rec = (s.recv(128)).decode("utf-8")
#length_int = int(length_rec)
#print("Length of file is:" + str(length_int))
#n = 0
#file = open("readfromserver.txt", "w")
#while (n < length_int) :
#    text = (s.recv(1024)).decode('utf-8')
#    file.write(text)
#    n += 1024
#file.close()

#s.sendall(bytes(filename, 'utf-8'))

# close the connection 
s.close()


