import threading
import socket
import os
import time

import sys
myname="jointedace"

def reci():
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    s=socket.socket()
    ad="127.0.0.1"
    ad=socket.gethostname()
    port=5500
    try:
       s.bind((ad,port))
    except:
        print("Port already in use! ")
        time.sleep(1)
        os._exit(1)
    s.listen(1)

    c,addr=s.accept()
    name=c.recv(1024).decode()
#    print( "connected to " , name)
    while True:
        try:
           data=c.recv(1024).decode()
        except:
            print("User Disconnected!")
            time.sleep(1)
            os._exit(1)
            exit()
        data="\n " + name + "> "+data
        print(Fore.GREEN +data)
        print(Fore.WHITE +"")
def snd():
    s=socket.socket()
    ad="127.0.0.1"
    ad=input("Enter ip/hostname \n")
    port=5000
    time.sleep(1)
    s.connect((ad,port))
    print("Connected to ",ad)
    s.send(socket.gethostname().encode())
    time.sleep(1)
    s.send(myname.encode())
    while True:
        data=sys.stdin.readline()
        s.send(data.encode())

myname=input("Enter your name-\n")

readthread = threading.Thread(target=reci)
readthread.start()
writethread = threading.Thread(target=snd)
writethread.start()    
readthread.join()
writethread.join()    
