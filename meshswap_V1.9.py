import Tkinter
import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import binascii
import sys, os
import re
import string

master = Tkinter.Tk(className=" Storm 4 mesh swapper ")
def open_command():
    file = tkFileDialog.askopenfile(parent=master,mode='rb',title='Select a file')
    if file != None:
        mesh = file.read()
        global meshhex
        meshhex=binascii.hexlify(mesh)
        file.close()

def open_command2():
    file = tkFileDialog.askopenfile(parent=master,mode='rb',title='Select a file')
    if file != None:
        mesh2 = file.read()
        global meshhex2
        meshhex2=binascii.hexlify(mesh2)
        file.close()

def save_command(self):
    file = tkFileDialog.asksaveasfile(mode='wb')
    if file != None:
        data = self
        file.write(data)
        file.close()


menu = Menu(master)
master.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="Open Files", menu=filemenu)

filemenu.add_command(label="Open target charactor", command=open_command)
filemenu.add_command(label="Open target mesh", command=open_command2)
filemenu.add_separator()
#the actual processs\/

mex=Entry(master)
mexl=Label(master, text="insert the body part, example: #XXX00t0 kami")
filly=('times', 9, 'bold')
mexl.config(font=filly)
mexl.grid(row=0, column=1)
mex.grid(row=1, column=1)

mex2=Entry(master)
mex2l=Label(master, text="insert the body part you want, example: #XXX00t0 kami")
filly=('times', 9, 'bold')
mex2l.config(font=filly)
mex2l.grid(row=2, column=1)
mex2.grid(row=3, column=1)

check=IntVar()


radl=Label(master, text="check if you want to change the bytes location")

radl.grid(row=4, column=1)

check = IntVar()
Radiobutton(master, text="none", variable=check, value=1).grid(row=5, column=1)
Radiobutton(master, text="Up", variable=check, value=2).grid(row=6, column=1)
Radiobutton(master, text="Down", variable=check, value=3).grid(row=7, column=1)

chan=Entry(master)
chanl=Label(master, text="if checked, insert the byte change difference")
filly=('times', 9, 'bold')
chan.config(font=filly)
chanl.grid(row=8, column=1)
chan.grid(row=9, column=1)



tex = IntVar()

texcheck = Checkbutton(master, text="fix one texture?", variable=tex)
texcheck.grid(row=10, column=1)


def meshswap():
    
    # takes the input from user and finds the mesh
    mexget=mex.get()
    mex2get=mex2.get()

    # finds the mesh in both files
    
    A=meshhex.find(("00"+binascii.hexlify(mexget)+"00"), 5000)
    B=meshhex2.find(("00"+binascii.hexlify(mex2get)+"00"), 5000)


    #fixes the find size?
    A=A+2
    B=B+2

    #???
    C=A+len(mexget*2)
    C2=B+len(mex2get*2)

    #finds the beggining of the mesh
    D=meshhex.rfind((binascii.hexlify("NDP3")), 0, A)
    E=meshhex2.rfind((binascii.hexlify("NDP3")), 0, B)
    

    # finds the file size
    filealength= meshhex[D-6:D]
    fileblength= meshhex2[E-6:E]



    #turns the hex file length into interger
    filea=int(filealength, 16)
    fileb=int(fileblength, 16)

    #checks and changes the end bytes

    endloc1=D+(filea*2)+2
    endloc2=E+(fileb*2)+2
    loc1=meshhex[endloc1:endloc1+2]
    loc2=meshhex2[endloc2:endloc2+2]
    print int(loc1)
    print int(loc2)
    if int(loc1) > int(loc2):
        loc3= int(loc1) - int(loc2)
        print len(meshhex)
        M=meshhex[0:endloc1+2]
        O=meshhex[endloc1+2+(loc3*8):len(meshhex)]
        XV=M+O
        print len(XV)
        
    elif int(loc2)> int(loc1):
        XV=meshhex
        print "non passable"
        tkMessageBox.showwarning(
            "Open file",
            "Bytes are not compatible")
        return
    else:
        xv=meshhex

    print len(XV)





    #highlights the entire section 
    fullalength= XV[D-54 : D+(filea*2)]
    fullblength= meshhex2[E-54 : E+(fileb*2)]



    # replaces the 2 parts and name
    F=XV.replace(fullalength, fullblength)
    #changes the name
    G=F
  
    #finds the perpertrator
    U=G.rfind("00"+mex2get+"00")
    U=U+2
    L1=len(mexget)
    L2=len(mex2get)
    
    
    if L1==L2:
        G=F.replace("0000"+binascii.hexlify(mex2get)+"00", "0000"+binascii.hexlify(mexget)+"00")
        
    elif L1<L2:
        L3=L2-L1
        p1=G[0:U]
        p2=G[U:U+(L2*2)]
        print len(p2)
        p3=G[U+(L2*2):len(G)]
        p2=binascii.hexlify(mexget)+("00"*L3)
        print len(p2)

        G=p1+p2+p3
    #if the length is larger than the original, check this again
    elif L1>L2:
        L3=L1-L2
        p1=G[0:U]
        p2=G[U:U+(L1*2)]
        print len(p2)
        p3=G[U+(L1*2):len(G)]
        p2=binascii.hexlify(mexget)
        print len(p2)

        G=p1+p2+p3
    
            
   
    # will change the position if the up or down are selected
    #up
    if check.get()==2:

        A=G.find(("00"+binascii.hexlify(mexget)+"00"), 5000)
        A=A+2

        H=G.rfind(("43"), 0, A)

        #get and replace the thing
        jar=int(G[H+2:H+4], 16)
        jar=jar+int(chan.get())
        if jar>255:
            jar=255
        jal=jar
        jar=hex(jar)
        jar=jar[2:len(jar)]
        if jal<=15:
                jar="0"+jar
        
        #splice and dice
        Q=G[0:H+2]
        R=G[H+2:H+4]
        S=G[H+4:len(G)]
        #first replace

        R=R.replace(R, jar)
        G=Q+R+S

        while G[H-128:H-126]=="43":
            H=H-128
            jar=int(G[H+2:H+4], 16)
            jar=jar+int(chan.get())
            if jar>255:
                jar=255
            jal=jar
            jar=hex(jar)
            jar=jar[2:len(jar)]
            if jal<=15:
                jar="0"+jar
            #splice and dice
            Q=G[0:H+2]
            R=G[H+2:H+4]
            S=G[H+4:len(G)]
            #first replace
            R=R.replace(R, (jar))
            G=Q+R+S

        
    # down
    elif check.get()==3:

        A=G.find(("00"+binascii.hexlify(mexget)+"00"), 5000)
        A=A+2

        H=G.rfind(("43"), 0, A)

        #get and replace the thing
        jar=int(G[H+2:H+4], 16)
        jar=jar-int(chan.get())
        if jar<0:
            jar=0
        elif jar>255:
            jar=255
        jal=jar
        jar=hex(jar)
        
        jar=jar[2:len(jar)]
        if jal<=15:
            jar="0"+jar
        #splice and dice
        Q=G[0:H+2]
        R=G[H+2:H+4]
        S=G[H+4:len(G)]
        #first replace
        R=R.replace(R, jar)
        print len(G)

        G=Q+R+S
        while G[H-128:H-126]=="43":
            H=H-128

            jar=int(G[H+2:H+4], 16)
            jar=jar-int(chan.get())
            if jar<0:
                jar=0
            elif jar>255:
                jar=255
            jal=jar
            jar=hex(jar)
            
            jar=jar[2:len(jar)]
            if jal<=15:
                jar="0"+jar
            #splice and dice
            Q=G[0:H+2]
            R=G[H+2:H+4]
            S=G[H+4:len(G)]
            #first replace
            if len(jar)==1:
                print jal
                print jar
                print "NEXT"
            
            R=R.replace(R, jar)
            

            G=Q+R+S
        
        
        print len(G)


    #fixes the textures
    if tex.get()==1:
        print 'hooha'

    #save
    save_command(binascii.unhexlify(G))
def button():
    meshswap()
    
button1 = Button(master, text="start", command=button)
button1.grid(row=12, column=1)

master.mainloop()