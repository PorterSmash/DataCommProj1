#Read the comments on client.py first, they are more descriptive

import socket
import os                

#Sending a file to the client
#C param is client socket connection
def clientDownload(c) :
   #Get filename from client
   filename = (c.recv(1024)).decode('utf-8')

   #Get file size
   file = open(filename)
   fsize = os.stat(filename)
   fsize = fsize.st_size
   fsizestr = str(fsize)

   #Send size
   c.sendall(bytes(fsizestr, 'utf-8'))

   #convert file to string
   fileRam = ""
   for line in file:
      fileRam += line

   #send it bro
   c.sendall(bytes(fileRam, 'utf-8'))
   print("Done sending")

   file.close()

#Now we're getting a file from the client
def clientUpload(c) :
   #Get name and length
   filename = (c.recv(1024)).decode('utf-8')

   length_rec = (c.recv(128)).decode('utf-8')
   length_int = int(length_rec)
   n = 0

   #Open file with write permissions 
   file = open(filename, "w")
   #take it all in
   while (n < length_int) :
      text = (c.recv(1024)).decode('utf-8')
      file.write(text)
      n += 1024
   file.close()
# next create a socket object 
s = socket.socket()          
print ("Socket successfully created")
port_parse = input("Enter port number: ")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = int(port_parse)                
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print ("socket binded to " + str(port)) 
  
# put the socket into listening mode 
s.listen(5)      
print ("socket is listening")            
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print ('Got connection from', addr) 
  
   # send a thank you message to the client.  
   c.sendall(bytes('Connection established.', 'utf-8'))
   #Receive command type from client, tells us what method to run
   command = (c.recv(1024)).decode('utf-8')
   #Assume it's d
   if(command == "d") :
      clientDownload(c)
  
   # Close the connection with the client 
   c.close() 
   exit()