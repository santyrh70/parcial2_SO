import os
from os import sys
import socket 
import threading 
import os
import os.path
import subprocess

direcciones={}
mi_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.bind(('localhost',8001))


def main():
    Components()


def StartKernel(conexion,addr):

    
    while True:
        
        peticion=conexion.recv(1024)
        decode=str(peticion.decode('utf-8'))
        print(decode)
        if len(direcciones)<1:
            if decode.startswith("App"):
                direcciones["App"]=conexion
                
            elif decode.startswith("GestorArc"):
                direcciones["GestorArc"]=conexion
            elif decode.startswith("GUI"):
                direcciones["GUI"]=conexion
                conexion.send("ready".encode())

        else:
            aux=decode.split(", ")
            if "send" in aux[0]:
                if "App" in aux[2]:
                    target=direcciones["App"]
                    target.send(decode.encode())
                elif "GestorArc" in aux[2]:
                    target=direcciones["GestorArc"]
                    target.send(decode.encode())
            elif "stop" in aux[0]:
                system.exit(1)
            elif "info" in aux[0]:
                if "App" in aux[2]:
                    target=direcciones["App"]
                    target.send(decode.encode())
                elif "GestorArc" in aux[2]:
                    target=direcciones["GestorArc"]
                    target.send(decode.encode())
             
        
        

    

def Components():
    mi_socket.listen()
    subprocess.call("start.bat")
    while True:
        conexion,addr=mi_socket.accept()
        thread = threading.Thread(target=StartKernel, args=(conexion,addr))
        thread.start()



