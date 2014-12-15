import threading
import socket
import os


s=socket.socket()
ad="127.0.0.1"
port=5000
s.connect((ad,port))
#s.setblocking(False)
def rdr():
    global s
    while True:
        data=  s.recv(1024).decode()
        if not data:
            continue
        print("SERVER-",data)
def sndr():
    global s
    while True:
        data=yield from sys.stdin.readline()
        s.send(data.encode())

       
readthread = threading.Thread(target=rdr)
readthread.start()
writethread = threading.Thread(target=sndr)
writethread.start()    
readthread.join()
writethread.join()
s.close()

