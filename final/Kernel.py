import socket
import threading
import sys
import pickle

class Kernel():
    """docstring for Kernel"""
    def __init__(self, host="localhost", port=4000):

        self.clientes = []

        self.msg_dst = ''

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
            cmd = input('->')
            if cmd == 'salir':
                self.sock.close()
                sys.exit()
            else:
                pass


    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clientes.remove(c)

    def msg_to(self, msg, cliente):
        try:
            cliente.send(msg)
        except:
            self.clientes.remove(cliente)

    def aceptarCon(self):
        print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
                data = conn.recv(1024)
                data = pickle.loads(data)
                
                if data:
                    #self.msg_to_all(data,c)
                    
                    if data == 'GestorArch':
                        print('Modulo Gestor de Archivos conectado')
                    elif data == 'App':
                        print('Modulo Aplicacion conectado')
                    elif data == 'GUI':
                        print('Modulo GUI conectado')
            except:
                pass

    def procesarCon(self):
        print("ProcesarCon iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        data = pickle.loads(data)
                        
                        if data:
                            data = data.split(';')
                            print(f'como queda la lista {data}')
                            #self.msg_to_all(data,c)
                            if data[1] == 'GestorArch':
                                print('soy GestorArc')
                                self.router(data)
                            elif data[1] == 'App':
                                print('soy App')
                                self.router(data)
                            elif data[1] == 'GUI':
                                print('soy GUI')
                                self.router(data)
                            
                    except:
                        pass

    def router(self, data):
        dst = data[2]
        msg = data[3]
        if dst == 'GestorArch':
            print('intentando enviar a gest')
            self.msg_to(pickle.dumps(msg), self.clientes[0])
        elif dst == 'App':
            print('intentando enviar a app')
            self.msg_to(pickle.dumps(msg), self.clientes[1])
        elif dst == 'GUI':
            print('intentando enviar a gui')
            self.msg_to(pickle.dumps(msg), self.clientes[2])

s = Kernel()