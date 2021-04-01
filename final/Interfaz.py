import socket
import threading
import sys
from tkinter import *
from tkinter import ttk
from datetime import datetime

mi_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.connect(('localhost',8001))



  
def MainApp():
    try:
       
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("{cmd:send, src:GUI, dst:GestorArc,msg:log->"+dt_string+"}")
        mi_socket.send("GUI".encode())
        respuesta=mi_socket.recv(1024)
        print(respuesta)      
        raiz = Tk()
        raiz.geometry('600x600')
        raiz.configure(bg = 'beige')
        raiz.title('Aplicación')
        app1 = ttk.Button(raiz, text='App1', command=lambda:open("OpenApp1"))                 
        app1.place(x=25, y=100)
        app1C = ttk.Button(raiz, text='App1 close', command=lambda:open("CloseApp2"))                  
        app1C.place(x=100, y=100)
        app2 = ttk.Button(raiz, text='App2', command=lambda:open("OpenApp2"))                 
        app2.place(x=25, y=200)
        app2C = ttk.Button(raiz, text='App2 close', command=lambda:open("CloseApp2"))                  
        app2C.place(x=100, y=200)
        app3 = ttk.Button(raiz, text='App3', command=lambda:open("OpenApp3"))                 
        app3.place(x=25, y=300)
        app3C = ttk.Button(raiz, text='App3 close', command=lambda:open("CloseApp3"))                  
        app3C.place(x=100, y=300) 

        folder = Entry(raiz)
        folder.place(x=225, y=400) 
        
        crt = ttk.Button(raiz, text='Crear carpeta',command=lambda:createF(folder.get()))
        crt.place(x=150, y=450) 
 
        dlt = ttk.Button(raiz, text='Borrar carpeta',command=lambda:deleteF(folder.get()))
        dlt.place(x=350, y=450)  
        raiz.mainloop()

        mi_socket.close()
    except:
        print("stop")
        sys.exit(1)


def open(msg):

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
    finalstring=("cmd:send, src:GUI, dst:App, msg:"+msg+"->"+dt_string)
    print(finalstring)
    mi_socket.send(finalstring.encode())


def createF(name):

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
    finalstring=("cmd:send, src:GUI, dst:FileManagement, msg:create "+name+"->"+dt_string)
    mi_socket.send(finalstring.encode())



def deleteF(name):

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
    finalstring=("cmd:send, src:GUI, dst:FileManagement, msg:Delete "+name+"->"+dt_string)
    print(finalstring)
    mi_socket.send(finalstring.encode())



   





MainApp()