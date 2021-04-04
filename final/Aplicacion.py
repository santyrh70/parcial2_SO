import socket
import threading
import subprocess
import sys
import pickle

class Cliente():
    """docstring for Cliente"""
    def __init__(self, host="localhost", port=4000):

        self.cerrar_bool = False
        self.p_list = []
        
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
                    do = msg.split('->')[0].split(' ')
                    if msg == 'salir':
                        self.cerrar_bool = True
                    if do[0] == 'OpenApp1':
                        pid_to_send = self.open_app()
                        self.send_pid('0', pid_to_send)
                    elif do[0] == 'OpenApp2':
                        pid_to_send = self.open_app()
                        self.send_pid('1', pid_to_send)
                    elif do[0] == 'OpenApp3':
                        pid_to_send = self.open_app()
                        self.send_pid('2', pid_to_send)
                    if do[0] == 'CloseApp1':
                        pid = do[1]
                        print(f'eliminando proceso con pid: {pid}')
                        self.close_app(pid)
                    elif do[0] == 'CloseApp2':
                        pid = do[1]
                        print(f'eliminando proceso con pid: {pid}')
                        self.close_app(pid)
                    elif do[0] == 'CloseApp3':
                        pid = do[1]
                        print(f'eliminando proceso con pid: {pid}')
                        self.close_app(pid)
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    def send_pid(self, num_app, pid):
        print(f'enviando pid: {pid} para asignar a boton: {num_app}')
        self.sock.send(pickle.dumps(f'send;App;GUI;pid {num_app} {pid}'))

    def open_app(self):
        p = subprocess.Popen('notepad.exe')
        try:    
            self.p_list.append((p.pid, p))
            return p.pid
        except:
            pass
    
    def close_app(self, pid):
        try:
            for p in self.p_list:
                if str(p[0]) == str(pid):
                    p[1].kill()
        except:
            pass

    def cerrar(self):
        if self.cerrar_bool:
            sys.exit()

c = Cliente()
    