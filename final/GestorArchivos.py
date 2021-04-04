import socket
import threading
import sys
import os
import pickle
import errno
from datetime import datetime

class GestorArchivos():
    """docstring for GestorArchivos""" 
    def __init__(self, host="localhost", port=4000):

        self.cerrar_bool = False
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.send_msg('GestorArch')

        msg_recv = threading.Thread(target=self.msg_recv)

        msg_recv.daemon = True
        msg_recv.start()

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
                if data:
                    msg = pickle.loads(data)
                    print(msg)
                    if msg == 'salir':
                        self.cerrar_bool = True
                    self.procesar(msg)
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    def procesar(self, msg):
        do = msg.split('->')[0].split(' ')[0]
        name = msg.split('->')[0].split(' ')[1]
        if do == 'Create':
            try:
                os.mkdir(name)
                self.write_log(msg)
                print(f'carpeta {name} creada')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        elif do == 'Delete':
            try:
                path = os.getcwd()
                os.rmdir(name)
                self.write_log(msg)
                print(f'carpeta {name} eliminada')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        elif do == 'log':
            try:
                self.write_log(' '.join(msg.split(' ')[1:]))
            except:
                pass

    def write_log(self, log):
        archivo = open('logs.txt','a')
        archivo.write(log + '\n')
        archivo.close()

    def cerrar(self):
        if self.cerrar_bool:
            self.send_msg('Modulo Gestor de Archivos cerrado')
            sys.exit()

c = GestorArchivos()
    