import socket
import threading
import subprocess
import sys
import pickle

class Cliente():
    """docstring for Cliente"""
    def __init__(self, host="localhost", port=4000):

        self.cerrar_bool = False
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.send_msg('App')

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
                    if msg.split('->')[0] == 'OpenApp1':
                        print(msg.split('->')[0])
                        self.open_app()
                    elif msg.split('->')[0] == 'OpenApp2':
                        print(msg.split('->')[0])
                        self.open_app()
                    elif msg.split('->')[0] == 'OpenApp3':
                        print(msg.split('->')[0])
                        self.open_app()
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    def open_app(self):
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')

    def cerrar(self):
        if self.cerrar_bool:
            sys.exit()

c = Cliente()
    