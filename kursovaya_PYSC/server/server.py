import socket
import os
import json
from threading import Thread

class User(Thread):  
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.default_dir = "/Users/nikolajudin/Desktop/kursovaya_PYSC/server/"
        self.dirr = self.default_dir
        super().__init__()
    
    
    def send(self, msg):
        return self.conn.send(msg.encode())
    
    
    def recv(self, size: int = 1024):
        return self.conn.recv(size).decode ('UTF-8')
    
    
    def mkdir(self):
        path_name = self.recv()
        if not os.path.isdir(self.dirr+path_name):
            os.mkdir(self.dirr+path_name)
            self.send(f"Папка {path_name} создана!")
            self.recv()
        else:
            self.send(f"Папка {path_name} не создана!")
            self.recv()
            
    
    
    def cd(self):
        cd = self.recv()
        try:    
            if cd == "/":
                os.chdir(self.default_dir)
                self.dirr = self.default_dir
                self.send(f"Текущая директория: {self.dirr}!")
                self.recv()
            else:
                os.chdir(self.dirr+cd)
                self.dirr = self.dirr + cd +'/'
                self.send(f"Текущая директория: {self.dirr}!")
                self.recv()
        except:
            self.send(f"Директория не изменена!")
            self.recv()

    
    
    def recv_file(self): 
        i=0  
        while True:  
            try:  
                name_f = self.recv(1024)  
                f = open(self.dirr + name_f,'wb')  
                l = self.conn.recv(1024)  
                f.write(l)  
                if not l:  
                    break  
                print(f'File {name_f} received')  
                f.close() 
                i+=1  
                if i == 2:  
                    self.send("STOP") 
                    self.recv()  
                    break 
                else:
                    self.send("OK") 
                    self.recv() 
            except:  
                break


    def autentific(self):      
        path = "/Users/nikolajudin/Desktop/kursovaya_PYSC/server/base.json"
        with open(path, "r") as database:
            users = json.load(database)
        self.send("Login: ")
        login = self.recv(1024)
        self.send("Passwd: ")
        password = self.recv(1024)
        if login in users and users[login] == password:
            self.send("OK")
            return 1
        self.send("ERR") 
        
    
    def run(self):
        while True:
            try:
                if self.autentific() == 1:
                    break
            except:
                break
        
        
        
        try:
            while True:
                self.send("Выберите действие: mkdir, cd, recv_file")
                msg = self.recv()
                
                options = {"mkdir":self.mkdir,
                        "cd":self.cd,
                        "recv_file":self.recv_file
                }
                if msg in options:
                    options[msg]()
                else:
                   pass
        except:
            pass

class Server:
    def __init__(self):
        # создаём сокет и связываем его с IP-адресом и портом
        self.sock = socket.socket()
        ip = "127.0.0.1"
        port = 33334
        self.sock.bind((ip, port))
        self.sock.listen()
        self.active_user = []
        while True:
            if len(self.active_users()) > 1:
                conn, addr = self.sock.accept()
                conn.send("Сервер переполнен".encode())
                conn.close() 
                continue
            conn, addr = self.sock.accept()
            # выводим информацию о подключении
            print('Соединение:',  addr)
            user = User(conn, addr)
            user.start() 
            self.active_user.append(user)
    
    
    def active_users(self):
        self.active_user = [user for user in self.active_user if user.is_alive()]
        return self.active_user
            
server = Server() 
