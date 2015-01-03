import threading
import socket
import os
import time
import sys

log=''
users={}
names={'server':'god'}#both dicctionary have address as key,as each will have different address
class nclient:
    def __init__(self,csock,cad,cname):
        self.sock=csock
        self.ad=cad
        self.name=cname
        global users,names
        users[cad]=csock
        names[cad]=cname
        data=cname+":Connected!"
        print(data)
        self.sendll(data)
        data=cad[0]
        csock.send(data.encode())
        data=str(names)
        csock.send(data.encode())

        self.sendll(data)

        self.rthread=threading.Thread(target=self.recieve)
        self.rthread.start()
    def recieve(self):
        global users,log
        while True:
            try:
                data=self.sock.recv(1024).decode()

            except:
                data=self.name+":Disconnected!"
                self.sock.close()
                print(data)
                self.sendll(data)  
                del users[self.ad]
                del names[self.ad]
                break
            index=0
            if data=='123abc':
                self.sendll(data) 
                data=self.sock.recv(512).decode()
            for d in data:
                if d=='>':
                    break
                index=index+1
                
            try:
                tempdata=data[index+1:]
                if tempdata[:13]=='changed name:':
                    #data=self.name+" changed name to:"+tempdata[13:]
                    self.name=tempdata[13:]
                    names[self.ad]=self.name
               
                   
            except:
                
                pass
            data=data
            print(data)
            self.sendll(data)   


    def sendll(self,data):
        global users,log
        for nad,cs in users.items():
            if nad==self.ad:
                continue
            log=log+'\n'+data
            cs.send(data.encode())
        open('server_log.dat','w').write(log)
def createconn(c,addr,nam):
    clt=nclient(c,addr,nam)

def nserver():
    s=socket.socket()

    k=input("Listen on ip?\n1.localhost\n2."+socket.gethostname()+"\n")
    if k=='1':

        adr='127.0.0.1'
        print("Listening on ",adr)
    else:
        if k=='2':
            adr=socket.gethostname()
            print("Listening on ",adr)
        else :
            print("Invalid Choice! Listening on localhost!")
            adr='127.0.0.1'
    port=5000
    s.bind((adr,port))
    s.listen(5)
   
    while True:

        c,addr=s.accept()
        na=c.recv(512).decode()
        print("connected to",addr)
        createconn(c,addr,na)
        

    
sevrth=threading.Thread(target=nserver)
sevrth.start()
sevrth.join()


            
        
