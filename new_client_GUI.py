import threading
import socket
import os
import time
from tkinter import *
import sys

root=Tk()
myname="EFGH"
root.minsize(width=666, height=666)
root.maxsize(width=666, height=666)
chat=Frame(root,width=660,height=450)
text=Frame(root)
chat.pack()
cht=Text(chat,height=30,width=70,state=DISABLED)
cht.pack(fill=Y)
scrollb=Scrollbar(chat)
scrollb.pack(side=RIGHT,fill=Y)
scrollb.config(command=cht.yview)
cht.config(yscrollcommand=scrollb.set)
text.pack()
c=socket.socket()
adr='127.0.0.1'
myname=input("Enter username\n")
adr=input("Enter IP\n")
port=5000

try:
    c.connect((adr,port))
except:
    print("unable to connect!")
    time.sleep(1)
    os._exit(1)
c.send(myname.encode())
name=c.recv(512).decode()        


data="Connected to " +name
cht["state"] = NORMAL
cht.insert(END,data)
cht["state"] = DISABLED
cht.yview_pickplace("end")
entry=Entry(text)
entry.pack(side=LEFT,fill=X)
def reciv():
    while True:
        global cht,name
        try:
            global c
            data=c.recv(1024).decode()
        except:
            
            data="\n"+name+" Disconnected"
            cht["state"] = NORMAL
            cht.insert(END,data)
            cht["state"] = DISABLED
            cht.yview_pickplace("end")
            time.sleep(1)
            os._exit(1)
        
       
        data="\n"+name+">"+data
        cht["state"] = NORMAL
        cht.insert(END,data)
        cht["state"] = DISABLED
        cht.yview_pickplace("end")
        
        
def sndmsg(*args):
    global entry
    strng=entry.get()
    if strng :
        entry.delete(0, END)
        entry.insert(0, "")
        global c,myname
        c.send(strng.encode())
        strng="\n"+myname+">"+strng
        global cht
        cht["state"] = NORMAL
        cht.insert(END,strng)
        cht["state"] = DISABLED
        cht.yview_pickplace("end")
root.bind("<Return>",sndmsg)      
readthread = threading.Thread(target=reciv)
readthread.start()
button=Button(text,text="SEND",command=sndmsg)
button.pack(side=LEFT)
root.mainloop()
c.close()

