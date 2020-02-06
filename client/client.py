# Import socket module 
import socket
#Ability to look at files in directory
import os	

#Returns length of file in bytes when encoded in utf-8 (Default for VSCode which I use)
#S param is socket in use
def utf8len(s):
    return bytes(len(s.encode('utf-8')))

#Used to download files from the server
def download(s) :
    #This must be a file in the server directory
    filename = input("Enter your filename: ")
    #Send the filename in UTF-8 format to the server
    s.sendall(bytes(filename, 'utf-8'))

    #The server sent the length of the file in bytes, let's receive that
    length_rec = (s.recv(128)).decode('utf-8')
    #Converts the string received to int
    length_int = int(length_rec)
    #Set up iterator
    n = 0
    #Open the file for writing
    file = open(filename, "w")

    #We download the file in 1024 byte chunks. Because it's TCP, we'll never lose a chunk.
    #If the file is larger than 1024, we need multiple chunks. N checks if the total size
    #of chunks downloaded is larger than the file size. Once it is, we know we got all the
    #chunks downloaded. After each chunk is downloaded, increment N by 1024 to keep track of
    #what portion of the file has been downloaded.
    while (n < length_int) :
        text = (s.recv(1024)).decode('utf-8')
        #Write the chunk to the file as we go.
        file.write(text)
        n += 1024
    #Close the file when finished.
    file.close()

#This time we send a file to the server in chunks.
#this is the opposite of what was occuring in the download
#method. 
def upload(s) :
    #Send file name
    filename = input("Enter your filename: ")
    s.sendall(bytes(filename, 'utf-8'))

    #Open file
    file = open(filename)
    
    #these 3 lines use the os lib to get the size of the file
    #in bytes and  convert it as a string
    fsize = os.stat(filename)
    fsize = fsize.st_size
    fsizestr = str(fsize)

    #Send the file size to the server
    s.sendall(bytes(fsizestr, 'utf-8'))

    #for each line in the file, write to this string.
    #This is super dirty and probably not allowed.
    fileRam = ""
    for line in file:
      fileRam += line

    #Send that file to the server
    s.sendall(bytes(fileRam, 'utf-8'))
    print("Done sending")

    #Close the file
    file.close()

# Create a socket object 
s = socket.socket()		 

#Get initial connect command
print("Use 'CONNECT <server name/IP address> <server port>' to connect")
init_connection = input("Command: ")

#split the command into a list of words delineated by spaces
command_parse = init_connection.split()

#Port and host are 3rd and 2nd in the command line
port = int(command_parse[2])
host = command_parse[1]

# Define the port on which you want to connect 
#port = 12345				

# connect to the server on local computer 
s.connect((host, port)) 

# receive data from the server
# Get "Connection Established" 
print( (s.recv(1024).decode('utf-8')))
print("")

#Next three lines set up initial interface
internal_command = input("What do you want to do? ")
internal_command_parse = internal_command.split()
first_arg = internal_command_parse[0]

if(first_arg == "Download") :
    #Notify server that I want to download
    s.sendall(bytes("d", "utf-8"))
    #Call download
    download(s)

# close the connection 
s.close()


