import socket
import threading
import sys
import pickle

from tkinter import *
from tkinter import ttk
from datetime import datetime

class Interfaz():
    """docstring for Interfaz""" 
    def __init__(self, host="localhost", port=4000):

        self.close_all = False
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.send_msg('GUI')

        msg_recv = threading.Thread(target=self.msg_recv)

        graficos = threading.Thread(target=self.graficos)

        msg_recv.daemon = True
        msg_recv.start()
        graficos.daemon = True
        graficos.start()

        while True:
            msg = input('->')
            if msg != 'salir':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(pickle.loads(data))
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    def graficos(self):
        raiz = Tk()
        raiz.geometry('600x600')
        raiz.configure(bg = 'beige')
        raiz.title('Aplicación')
        app1 = ttk.Button(raiz, text='App1', command=lambda:self.open("OpenApp1"))                 
        app1.place(x=25, y=100)
        app1C = ttk.Button(raiz, text='App1 close', command=lambda:self.open("CloseApp2"))                  
        app1C.place(x=100, y=100)
        app2 = ttk.Button(raiz, text='App2', command=lambda:self.open("OpenApp2"))                 
        app2.place(x=25, y=200)
        app2C = ttk.Button(raiz, text='App2 close', command=lambda:self.open("CloseApp2"))                  
        app2C.place(x=100, y=200)
        app3 = ttk.Button(raiz, text='App3', command=lambda:self.open("OpenApp3"))                 
        app3.place(x=25, y=300)
        app3C = ttk.Button(raiz, text='App3 close', command=lambda:self.open("CloseApp3"))                  
        app3C.place(x=100, y=300) 

        folder = Entry(raiz)
        folder.place(x=225, y=400) 
        
        crt = ttk.Button(raiz, text='Crear carpeta',command=lambda:self.createF(folder.get()))
        crt.place(x=150, y=450) 
 
        dlt = ttk.Button(raiz, text='Borrar carpeta',command=lambda:self.deleteF(folder.get()))
        dlt.place(x=350, y=450)  
        raiz.mainloop()

    def open(self, msg):

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("send;GUI;App;"+msg+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))


    def createF(self, name):

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("send;GUI;GestorArch;Create "+name+"->"+dt_string)
        self.sock.send(pickle.dumps(finalstring))



    def deleteF(self, name):

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("send;GUI;GestorArch;Delete "+name+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))

c = Interfaz()
    