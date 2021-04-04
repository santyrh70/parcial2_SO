import socket
import threading
import sys
import pickle

from tkinter import *
from tkinter import ttk
from datetime import datetime
import random

class Interfaz():
    """docstring for Interfaz""" 
    def __init__(self, host="localhost", port=4000):

        self.cerrar_bool = False

        self.app0 = []
        self.app1 = []
        self.app2 = []
        
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
                            self.app0.append(pid)
                        if num_app == '1':
                            self.app1.append(pid)
                        if num_app == '2':
                            self.app2.append(pid)
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
        app1C = ttk.Button(raiz, text='App1 close', command=lambda:self.cerrar_app("CloseApp1", self.app0, 0))                  
        app1C.place(x=100, y=100)
        app2 = ttk.Button(raiz, text='App2', command=lambda:self.open_app("OpenApp2"))                 
        app2.place(x=25, y=200)
        app2C = ttk.Button(raiz, text='App2 close', command=lambda:self.cerrar_app("CloseApp2", self.app1, 1))                  
        app2C.place(x=100, y=200)
        app3 = ttk.Button(raiz, text='App3', command=lambda:self.open_app("OpenApp3"))                 
        app3.place(x=25, y=300)
        app3C = ttk.Button(raiz, text='App3 close', command=lambda:self.cerrar_app("CloseApp3", self.app2, 2))                  
        app3C.place(x=100, y=300) 

        closeT = ttk.Button(raiz, text='Cerrar', command=lambda:self.cerrarT(raiz))                 
        closeT.place(x=25, y=400)
        
        folder = Entry(raiz)
        folder.place(x=225, y=400) 
        crt = ttk.Button(raiz, text='Crear carpeta',command=lambda:self.createF(folder.get()))
        crt.place(x=150, y=450) 
 
        dlt = ttk.Button(raiz, text='Borrar carpeta',command=lambda:self.deleteF(folder.get()))
        dlt.place(x=350, y=450)  
        raiz.mainloop()
        

    def open_app(self, msg):
        r = self.rand()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=(r+";info;GUI;App;"+msg+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))

    def cerrar_app(self, msg, pid, num):
        for p in pid:
            try:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
                finalstring=(f"OK;send;GUI;App;{msg} {p}->{dt_string}")
                print(f'string que se envia {finalstring}')
                if int(num) == 0:
                    del self.app0[self.app0.index(p)]
                elif int(num) == 1:
                    del self.app1[self.app1.index(p)]
                elif int(num) == 2:
                    del self.app2[self.app2.index(p)]
                self.sock.send(pickle.dumps(finalstring))
            except:
                pass

    def createF(self, name):
        r = self.rand()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=(r+";send;GUI;GestorArch;Create "+name+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))

    def rand(self):
        r = random.randint(1, 10)
        res = ''
        if r<6:
            res = 'OK'
        elif r>=6 and r<9:
            res = 'Ocupado'
        else:
            res = 'Error'
        return res

    def deleteF(self, name):
        r = self.rand()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        finalstring=(r+";send;GUI;GestorArch;Delete "+name+"->"+dt_string)
        print(finalstring)
        self.sock.send(pickle.dumps(finalstring))

    def cerrarT(self, raiz):
        self.cerrar_bool = True
        self.send_msg('salir')
        if self.cerrar_bool:
            raiz.destroy()
            sys.exit()

    def cerrar(self):
        if self.cerrar_bool:
            sys.exit()


c = Interfaz()
    