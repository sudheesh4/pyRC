import threading
import socket
import os


s=socket.socket()
ad="127.0.0.1"
port=5000
s.bind((ad,port))

s.listen(1)

c,addr=s.accept()
#c.setblocking(False)
def rdr():
    global c
    while True:
        data=c.recv(1024).decode()
        if not data:
            continue
        print("CLIENT-",data)
def sndr():
    global c
    while True:
        data=input("server-")
        c.send(data.encode())

print("connected to ",ad)        
readthread = threading.Thread(target=rdr)
readthread.start()
writethread = threading.Thread(target=sndr)
writethread.start()    
readthread.join()
writethread.join()
c.close()

