import threading
import socket
import os
import time
import sys
import colorama
from colorama import Fore, Back, Style
k=""
myname="jointedace"
def snd():
    s=socket.socket()
    ad="127.0.0.1"
    global k
    
    ad=k
    port=5500
    time.sleep(1)
    s.connect((ad,port))
    s.send(myname.encode())
    while True:
        data=sys.stdin.readline()
        s.send(data.encode())

writethread = threading.Thread(target=snd)
  
def reci():

    s=socket.socket()
    ad="127.0.0.1"
    ad="jointedace"
    port=5000
    try:
       s.bind((ad,port))
    except:
        print("Port already in use! ")
        time.sleep(1)
        os._exit(1)
    s.listen(1)
    print("Waiting for connection")
    c,addr=s.accept()
    global k
    k=c.recv(1024).decode()
   # name=c.recv(512).decode() doesnt work!
    #name="k"
##    print(addr)
    print( "connected to " ,k)
    name=c.recv(1024).decode()
    
    #k=addr[0]
    writethread.start()  
    while True:
        try:
           data=c.recv(1024).decode()
        except:
            print("User Disconnected!")
            time.sleep(1)
            os._exit(1)
            
        data="\n " + name + "> "+data
        print(data)
##        print(Fore.GREEN +data)
##        print(Fore.WHITE )

myname=input("Enter your name-\n")

readthread = threading.Thread(target=reci)
readthread.start()

readthread.join()
writethread.join()    
