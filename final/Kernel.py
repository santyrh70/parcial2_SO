import socket
import threading
import sys
import pickle
import time
from datetime import datetime

class Kernel():
    def __init__(self, host="localhost", port=4000):

        self.clientes = [(0,0)]

        self.cerrar_bool = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)
        
        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        while True:
            cmd = input('->').split(' ')
            if cmd[0] == 'salir' and len(cmd)>1:
                if cmd[1] == 'App':
                    for c in self.clientes:
                        if c[0] == 'App':
                            self.msg_to(pickle.dumps('salir'), c[1])
                            self.clientes.remove(c)
                elif cmd[1] == 'GestorArch':
                    for c in self.clientes:
                        if c[0] == 'GestorArch':
                            self.msg_to(pickle.dumps('salir'), c[1])
                            self.clientes.remove(c)
                elif cmd[1] == 'GUI':
                    for c in self.clientes:
                        if c[0] == 'GUI':
                            self.msg_to(pickle.dumps('salir'), c[1])
                            self.clientes.remove(c)
            elif cmd[0] == 'salir':
                self.cerrar_modulos()
    


    def msg_to_all(self, msg):
        if (0,0) in self.clientes:
            self.clientes.remove((0,0))
        for c in self.clientes:
            try:
                c[1].send(msg)
            except:
                self.clientes.remove(c)

    def msg_to(self, msg, cliente):
        try:
            cliente.send(msg)
        except:
            self.clientes.remove(cliente)

    def logs_init(self, msg):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y"+"-"+"%H:%M:%S")
        for c in self.clientes:
            if c[0] == 'GestorArch':
                self.msg_to(pickle.dumps('log ' + msg + '->' + dt_string), c[1])

    def aceptarCon(self):
        print("hilo aceptarCon iniciado")
        while True:
            self.cerrar()
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)                
                data = conn.recv(1024)
                data = pickle.loads(data)
                
                if data:
                    if data == 'GestorArch':
                        print('Modulo Gestor de Archivos conectado')
                        self.clientes.append(('GestorArch',conn))
                        time.sleep(1)
                        self.logs_init('Modulo Gestor de Archivos conectado')
                    elif data == 'App':
                        print('Modulo Aplicacion conectado')
                        self.clientes.append(('App',conn))
                        self.logs_init('Modulo Aplicacion conectado')
                    elif data == 'GUI':
                        print('Modulo GUI conectado')
                        self.clientes.append(('GUI',conn))
                        self.logs_init('Modulo GUI conectado')
                
            except:
                pass

    def procesarCon(self):
        print("hilos procesarCon iniciado")
        while True:
            self.cerrar()
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c[1].recv(1024)
                        data = pickle.loads(data)
                        
                        if data:
                            if data == 'salir':
                                self.cerrar_bool = True
                                print('cerrando todos los modulos...')
                                self.msg_to_all(pickle.dumps('salir'))
                                print('modulos cerrados.')
                                time.sleep(5)
                                self.sock.close()
                                sys.exit()
                            data = data.split(';')
                            print(data)      
                            if data[0] == 'Error':
                                print(f'Error inesperado en el proceso {data}')
                            elif data[0] == 'Ocupado':
                                print(f'Modulos ocupados... pronto se procesara el mensaje')
                                time.sleep(3)
                                if data[2] == 'GestorArch':
                                    self.router(data)
                                elif data[2] == 'App':
                                    self.router(data)
                                elif data[2] == 'GUI':
                                    self.router(data)
                            elif data[2] == 'GestorArch':
                                self.router(data)
                            elif data[2] == 'App':
                                self.router(data)
                            elif data[2] == 'GUI':
                                self.router(data)
                    except:
                        pass

    def router(self, data):
        dst = data[3]
        msg = data[4]
        if dst == 'GestorArch':
            for c in self.clientes:
                if c[0] == 'GestorArch':
                    self.msg_to(pickle.dumps(msg), c[1])
        elif dst == 'App':
            for c in self.clientes:
                if c[0] == 'App':
                    self.msg_to(pickle.dumps(msg), c[1])
                elif c[0] == 'GestorArch':
                    self.msg_to(pickle.dumps('log ' + msg), c[1])
        elif dst == 'GUI':
            for c in self.clientes:
                if c[0] == 'GUI':
                    self.msg_to(pickle.dumps(msg), c[1])
                elif c[0] == 'GestorArch':
                    self.msg_to(pickle.dumps('log ' + msg), c[1])

    def cerrar(self):
        if self.cerrar_bool:
            sys.exit()

    def cerrar_modulos(self):
        self.cerrar_bool = True
        print('cerrando todos los modulos...')
        self.msg_to_all(pickle.dumps('salir'))
        print('modulos cerrados.')
        time.sleep(5)
        self.sock.close()
        sys.exit()

s = Kernel()