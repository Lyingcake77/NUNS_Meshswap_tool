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

filemenu.add_command(label="Open target charector", command=open_command)
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


def meshswap():
    # takes the input from user and finds the mesh
    mexget=mex.get()
    mex2get=mex2.get()

    # finds the mesh in both files
    
    A=meshhex.find(("00"+binascii.hexlify(mexget)+"00"), 5000)
    B=meshhex2.find(("00"+binascii.hexlify(mex2get)+"00"), 5000)


    #fixes the file size?
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

    
    #highlights the entire section 
    fullalength= meshhex[D-54 : D+(filea*2)]
    fullblength= meshhex2[E-54 : E+(fileb*2)]



    # replaces the 2 parts and name
    
    #meshhex.replace(mex2get, mexget)
    F=meshhex.replace(fullalength, fullblength)
    G=F.replace("0000"+binascii.hexlify(mex2get)+"00", "0000"+binascii.hexlify(mexget)+"00")

    save_command(binascii.unhexlify(G))

def button():
    meshswap()
    
button1 = Button(master, text="start", command=button)
button1.grid(row=4, column=1)

master.mainloop()