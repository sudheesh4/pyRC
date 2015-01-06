import threading
import socket
import os
import time
from tkinter import *
from tkinter import ttk
from mssgboxes import *
import time
import sys
import winsound

def dosomething():
     print("YO")
myname=""
adr='127.0.0.1'
tempn=[]
names={}
links={}
nooflinks=0
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
        port=13204
        print('a')
        sendsock=socket.socket()
        print('b')
        sendsock.bind((sadr,port))
        print('c')
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

    
chat=Frame(root)
text=Frame(root)
##chat.pack()
##text.pack()

chat.grid(row=0,column=0,padx=(0,0))
text.grid(row=1,column=0)
cht=Text(chat,height=15,width=30,state=DISABLED)
#cht.pack(fill=Y)
cht.grid(row=0,column=0,padx=(0,0))
scrollb=ttk.Scrollbar(chat)
#scrollb.pack(side=RIGHT,fill=Y)
scrollb.grid(row=0,column=1,sticky='ns')
scrollb.config(command=cht.yview)
cht.config(yscrollcommand=scrollb.set)
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
#entry.grid(row=0,column=0,columnspan=3)
def reciv():
    global log,links
    while True:
        global cht,name
        try:
             global c
             data=c.recv(256).decode()
                    #data="\n"+data
             global names,nooflinks
             if data[0:5]=='Link:':
                  links[nooflinks]=data[5:]
                  nooflinks=nooflinks+1
                  cht["state"] = NORMAL
                  cht.insert(END,"\n Link "+str(nooflinks)+" added!")
                  cht["state"] = DISABLED
                  log=log+'\n Link '+str(nooflinks)+" added!"
                  cht.yview_pickplace("end")
                  winsound.Beep(310,800)             
                  continue
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
        except:
            
            data="\nServer Down!"
            cht["state"] = NORMAL
            cht.insert(END,data)
            log=log+'nServer Down!'
            cht["state"] = DISABLED
            cht.yview_pickplace("end")
            time.sleep(1)
            os._exit(1)
        
       

            
        
        

        
def sndmsg(*args):
    global entry
    strng=entry.get()
    time.sleep(.01)
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
def sendlink():

     temp=[]
     d = SOMEMSG(root,"URL",temp)
     root.wait_window(d.top)
     link="Link:"+temp[0]
     
     try:
        c.send(link.encode())

     except:
        d=MSSG(root,"COULDNT SEND :/")
def downlink(i):
     import download3
     t=threading.Thread(target=download3.interact,args=(links[i],"LINK "+str(i+1)))
     t.start()
def showlink():
     global links,nooflinks
     top=Toplevel(root)
     i=0
     for i in range(0,nooflinks):
          Button(top,text=str(i+1),command=lambda:downlink(i)).grid(row=i,column=0)
          Label(top,text=links[i][0:15]).grid(row=i,column=2)
     if nooflinks==0:
          Label(top,text="No one has shared  any link with you, yet! :/").grid(row=0,column=0,columnspan=3)
     Button(top,text="OK",command=top.destroy).grid(row=nooflinks+1,column=2)
     
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
def clearchat():
     global log
     
     log=''

     cht['state']=NORMAL
     cht.delete(1.0, END)
     cht['state']=DISABLED
root.bind("<Return>",sndmsg)      
readthread = threading.Thread(target=reciv)
readthread.start()
button=ttk.Button(text,text="SEND",command=sndmsg)
button.pack(side=LEFT)

menu=Menu(root)
root.config(menu=menu)
submenu=Menu(menu)
submenu2=Menu(menu)
menu.add_cascade(label="Actions",menu=submenu)
menu.add_cascade(label="File Options",menu=submenu2)
submenu.add_command(label="Change Name",command=changename)
submenu.add_command(label="Save Log",command=savelog)
submenu.add_command(label="Send Download Link",command=sendlink)
submenu.add_command(label="Down. Link",command=showlink)
submenu.add_command(label="Clear",command=clearchat)
submenu.add_command(label="Whois",command=dosomething)
submenu2.add_command(label="Send File",command=sendfilt)
submenu2.add_command(label="Recieve File",command=recvfilet)
root.mainloop()
try:
   c.close()
except:
    print("")
finally:
    #open('log.dat','w').write(log)
    pass
