import socket
import threading
import Interfaz as In

class Kernel:
    def __init__(self):
        self.mi_socket = None
        main = threading.Thread(target=self.StartKernel) 
        componets = threading.Thread(target=self.Components)
        main.start()
        componets.start()


    def StartKernel(self):
        self.mi_socket=socket.socket()
        self.mi_socket.bind(('localhost',8000))
        self.mi_socket.listen(5)
        while True:
            conexion,addr=self.mi_socket.accept()
            print("Nueva conexion establecida!")
            print(addr)
            peticion=conexion.recv(1024)
            print(peticion)
            conexion.send("1".encode())
            conexion.close()

    def Components(self):
        interfaz=threading.Thread(target=In.Aplicacion)
        interfaz.start()