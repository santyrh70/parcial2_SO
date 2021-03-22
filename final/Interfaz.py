import socket
import threading
from tkinter import *
from tkinter import ttk
from datetime import datetime




class Aplicacion():

   

    def __init__(self):
        self.conection()
        self.MainApp()
        
    def conection(self):
        self.mi_socket=socket.socket()
        self.mi_socket.connect(('localhost',8000))
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        print(dt_string)
        finalstring=("{cmd:send, src:GUI, dst:GestorArc,msg:log->"+dt_string+"}")
        self.mi_socket.send(finalstring.encode())
        self.respuesta=self.mi_socket.recv(1024)
        print(self.respuesta)
      
    def MainApp(self):

        self.raiz = Tk()
        self.raiz.geometry('700x700')
        self.raiz.configure(bg = 'beige')
        self.raiz.title('Aplicación')
        self.binfo = ttk.Button(self.raiz, text='Info', command=self.app1)                      
        self.binfo.pack(side=LEFT)
        self.bsalir = ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy)                        
        self.bsalir.pack(side=RIGHT)
        self.raiz.mainloop()
    
    def app1(self):
        window = Tk()
        window.title("Application") 
        window.geometry('300x300')
        window.mainloop()



