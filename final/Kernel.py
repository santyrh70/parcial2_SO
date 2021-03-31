import socket
import threading
import Interfaz



def main():
    main = threading.Thread(target=StartKernel) 
    componets = threading.Thread(target=Components)
    main.start()
    componets.start()


def StartKernel():
    mi_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mi_socket.bind(('localhost',8001))
    mi_socket.listen(5)
    while 0==0:
        conexion,addr=mi_socket.accept()
        print("Nueva conexion establecida!")
        print(addr)
        peticion=conexion.recv(1024)
        print(peticion)
        conexion.send("se abre la GUI".encode())
        conexion.close()
       

def Components():
    interfaz=threading.Thread(target=Interfaz.main)
    interfaz.start()
