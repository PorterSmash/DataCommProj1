import socket
import os                

def clientDownload(c) :
   filename = (c.recv(1024)).decode('utf-8')

   file = open(filename)
   fsize = os.stat(filename)
   fsize = fsize.st_size
   fsizestr = str(fsize)
   c.sendall(bytes(fsizestr, 'utf-8'))

   fileRam = ""
   for line in file:
      fileRam += line

   c.sendall(bytes(fileRam, 'utf-8'))
   print("Done sending")

   file.close()

def clientUpload(c) :
   filename = (c.recv(1024)).decode('utf-8')

   length_rec = (c.recv(128)).decode('utf-8')
   length_int = int(length_rec)
   n = 0
    
   file = open(filename, "w")
   while (n < length_int) :
      text = (c.recv(1024)).decode('utf-8')
      file.write(text)
      n += 1024
   file.close()
# next create a socket object 
s = socket.socket()          
print ("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345                
  
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
   clientDownload(c)
  
   # Close the connection with the client 
   c.close() 
   exit()