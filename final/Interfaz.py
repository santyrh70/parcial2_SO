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

        self.cerrar_bool = False

        self.app0 = None
        self.app1 = None
        self.app2 = None
        
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
            '''
            msg = input('->')
            if msg != 'salir':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()
            '''
            self.cerrar()

    def msg_recv(self):
        while True:
            self.cerrar()
            try:
                data = self.sock.recv(1024)
                if data == 'salir':
                    print(pickle.loads(data))
                    self.cerrar_bool = True
                if data:
                    print(pickle.loads(data))
                    msg = pickle.loads(data).split(' ')
                    do = msg[0]
                    num_app = msg[1]
                    pid = msg[2]
                    if do == 'pid':
                        if num_app == '0':
                            self.app0 = pid
                        if num_app == '1':
                            self.app1 = pid
                        if num_app == '2':
                            self.app2 = pid
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    def graficos(self):
        raiz = Tk()
        raiz.geometry('600x600')
        raiz.configure(bg = 'beige')
        raiz.title('Aplicación')
        app1 = ttk.Button(raiz, text='App1', command=lambda:self.open_app("OpenApp1"))                 
        app1.place(x=25, y=100)
        app1C = ttk.Button(raiz, text='App1 close', command=lambda:self.cerrar_app(raiz, "CloseApp1", self.app0))                  
        app1C.place(x=100, y=100)
        app2 = ttk.Button(raiz, text='App2', command=lambda:self.open_app("OpenApp2"))                 
        app2.place(x=25, y=200)
        app2C = ttk.Button(raiz, text='App2 close', command=lambda:self.cerrar_app(raiz, "CloseApp2", self.app1))                  
        app2C.place(x=100, y=200)
        app3 = ttk.Button(raiz, text='App3', command=lambda:self.open_app("OpenApp3"))                 
        app3.place(x=25, y=300)
        app3C = ttk.Button(raiz, text='App3 close', command=lambda:self.cerrar_app(raiz, "CloseApp3", self.app2))                  
        app3C.place(x=100, y=300) 

        folder = Entry(raiz)
        folder.place(x=225, y=400) 
        
        crt = ttk.Button(raiz, text='Crear carpeta',command=lambda:self.createF(folder.get()))
        crt.place(x=150, y=450) 
 
        dlt = ttk.Button(raiz, text='Borrar carpeta',command=lambda:self.deleteF(folder.get()))
        dlt.place(x=350, y=450)  
        raiz.mainloop()
        self.cerrar_bool = True

    def open_app(self, msg):

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("info;GUI;App;"+msg+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))

    def cerrar_app(self, raiz, msg, pid):
        raiz.update()
        try:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
            finalstring=(f"send;GUI;App;{msg} {pid}->{dt_string}")
            self.sock.send(pickle.dumps(finalstring))
        except:
            pass

    def createF(self, name):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("send;GUI;GestorArch;Create "+name+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))



    def deleteF(self, name):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=("send;GUI;GestorArch;Delete "+name+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))

    def cerrar(self):
        if self.cerrar_bool:
            sys.exit()

c = Interfaz()
    