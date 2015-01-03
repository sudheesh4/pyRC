import threading
import socket
import os
import time
from tkinter import *
from mssgboxes import *
import sys
import winsound
def dosomething():
     print("YO")
myname=""
adr='127.0.0.1'
tempn=[]
names={}
root=Tk()
d = SOMEMSG(root,"Enter Username",tempn)
root.withdraw()
root.wait_window(d.top)
myname=tempn[0]
tempn=[]
iprandom = SOMEMSG(root,"Enter Address to connect to",tempn)
root.wait_window(iprandom.top)
adr=tempn[0]
root.update()
root.deiconify()
myadr=""
log=''

##root.minsize(width=666, height=550)
##root.maxsize(width=666, height=550)
root.title('pyirc')
def clntcnntd(want):
    global names
    for ade,na in names.items():
        if want==na:

            return ade
    return "Not Found!"
def sendfil():
    try:
        global myadr,log
        sadr=myadr
        port=6100
        sendsock=socket.socket()
        sendsock.bind((sadr,port))
        temp=[]
        fi=SOMEMSG(root,"Enter Name file to send ",temp)
        root.wait_window(fi.top)
        
        filna=temp[0]
        img=open(filna,'rb')
        
        
        sendsock.listen(1)
        c,st=sendsock.accept()
        
        ms=MSSG(root,"CONNECTED TO "+str(st))

        c.send(filna.encode())
        log=log+'\n Sending file to '+str(st)+';file:'+filna
        
        
        while True:
            imdata=img.read(512)
            if not imdata:
                break
            c.send(imdata)
        ms=MSSG(root,"Sent successully! ")
        log=log+'\nSent successully!'
        c.close()
        sendsock.close()
    except:
        ms=MSSG(root,"Unable to process your request! ")
        
def sendfilt():
    rvt = threading.Thread(target=sendfil)
    rvt.start()




def recvfile():
    try:
       # sern=input("Enter name of user\n")
        sern=[]
        fi=SOMEMSG(root,"Enter Name of user to recieve file from ",sern)
        root.wait_window(fi.top)
        
        
        adrr=clntcnntd(sern[0])
        so=socket.socket()
        po=6100
        
        #adrr="jointedace"
        
        so.connect((adrr[0],po))
        ms=MSSG(root,"Connected! ")
        
        ext=so.recv(512).decode()
        
        
        
        i=0

        ext='(Recieved)'+ext
        file=open(ext,'wb')
        global log
        log=log+'\n Recieving file ;file-'+ext
        
        ms=MSSG(root,"Recieving Please wait!")
        while True:
            data=so.recv(512)
            if not data:
                break
            file.write(data)
        file.close()
        ms=MSSG(root,"Recieved successfully! ")
        log=log+'\n Recieved file successfully!'
        so.close()
    except:
        ms=MSSG(root,"Unable to process your request! ")
def recvfilet():
    rvt = threading.Thread(target=recvfile)
    rvt.start()

    
chat=Frame(root,width=250,height=100)
text=Frame(root)
chat.pack()
text.pack()
cht=Text(chat,height=15,width=30,state=DISABLED)
cht.pack(fill=Y)
scrollb=Scrollbar(chat)
scrollb.pack(side=RIGHT,fill=Y)
scrollb.config(command=cht.yview)
cht.config(yscrollcommand=scrollb.set)

filsnd=Button(chat,text="Send File",command=sendfilt)
filsnd.pack(side=LEFT)
filrev=Button(chat,text="Recieve File",command=recvfilet)
filrev.pack(side=LEFT)
c=socket.socket()

#myname=input("Enter username\n")
root.title('pyRC- '+myname)

port=5000

try:
    c.connect((adr,port))
except:
    ms=MSSG(root,"Unable to connect! :/")
    time.sleep(1)
    os._exit(1)

c.send(myname.encode())
myadr=c.recv(1024).decode()

temp=c.recv(1024).decode()
names=eval(temp)
#name=c.recv(512).decode()        
data="Connected ! "

cht["state"] = NORMAL
cht.insert(END,data)
cht["state"] = DISABLED
cht.yview_pickplace("end")
entry=Entry(text,width=50)
entry.pack(side=LEFT,fill=X)
def reciv():
    global log
    while True:
        global cht,name
        try:
            global c
            data=c.recv(1024).decode()
        except:
            
            data="\nServer Down!"
            cht["state"] = NORMAL
            cht.insert(END,data)
            log=log+'nServer Down!'
            cht["state"] = DISABLED
            cht.yview_pickplace("end")
            time.sleep(1)
            os._exit(1)
        
       
        #data="\n"+data
        global names    
        if data=='123abc':
            data=c.recv(512).decode()
            index=0
            for d in data:
            
                if d=='>':
                    
                    break
                index=index+1
            try:
                tempdata=data[index+1:]
                
                if tempdata[:13]=='changed name:':
                    cad=clntcnntd(data[0:index])
                    
                    names[cad]=tempdata[13:]
                    
            except:
                pint('fer')
                pass
        randvar=data.split(':')
        
        cht["state"] = NORMAL
        cht.insert(END,"\n"+data)
        cht["state"] = DISABLED
        log=log+'\n'+data
        cht.yview_pickplace("end")
        winsound.Beep(310,800)
        
        if len(randvar)>=2:
            if randvar[1] == "Connected!":
                 data=c.recv(1024).decode()
                 names=eval(data)
            
        
        

        
def sndmsg(*args):
    global entry
    strng=entry.get()
    if strng :
        entry.delete(0, END)
        entry.insert(0, "")
        global c,myname
        strng=myname+">"+strng
        c.send(strng.encode())
        strng="\n"+strng
        global cht,log
        cht["state"] = NORMAL
        cht.insert(END,strng)
        cht["state"] = DISABLED
        log=log+strng
        cht.yview_pickplace("end")
def changename():
    
    global c,myname,names,tempn
    tempname=myname
    tempn=[]
    d = SOMEMSG(root,"Enter Username",tempn)
    root.withdraw()
    root.wait_window(d.top)
    myname=tempn[0]
    tempn=[]
    root.update()
    root.deiconify()
    clntc=clntcnntd(tempname)
    names[clntc]=myname
    k='123abc'
    c.send(k.encode())
    informothers=tempname+">changed name:"+myname
    c.send(informothers.encode())
    strng='\n'+tempname+" changed name to:"+myname
    
    global cht,log
    cht["state"] = NORMAL
    cht.insert(END,strng)
    cht["state"] = DISABLED
    log=log+strng
    cht.yview_pickplace("end")
    root.title('pyRC- '+myname)
def savelog():
    try:
        open('log.dat','w').write(log)
    except:
        print('couldnt save log ! :/')
        return
    ms=MSSG(root,"Log saved! ")
root.bind("<Return>",sndmsg)      
readthread = threading.Thread(target=reciv)
readthread.start()
button=Button(text,text="SEND",command=sndmsg)
button.pack(side=LEFT)
menu=Menu(root)
root.config(menu=menu)
submenu=Menu(menu)
menu.add_cascade(label="Options",menu=submenu)
submenu.add_command(label="Change Name",command=changename)
submenu.add_command(label="Save Log",command=savelog)
submenu.add_command(label="Whois",command=dosomething)
root.mainloop()
try:
   c.close()
except:
    print("")
finally:
    #open('log.dat','w').write(log)
    pass
