import socket
import os
ip = "127.0.0.1"
port = 33334
sock = socket.socket()
sock.connect((ip,port))

    
def recv():
    msg_stat = (sock.recv(1024)).decode ('UTF-8')
    return msg_stat

    
def send(text = 'Ввод: '): 
    sock.send((bytes(text, encoding = 'UTF-8')))
    return text


def mkdir():
    name = input("Имя папки для создания: ")
    send(name)
    print(recv())
    send("OK")


def cd():
    name = input("Имя директории для перехода: ")
    if name == "":
        name = '/'
    send(name)
    print(recv())
    send("OK")


def file_send():
    # запрашиваем имя файла и отправляем серверу
    
    while True:
        f_name = input ('Файл для отправки: ')
        if os.path.isfile("/Users/nikolajudin/Desktop/kursovaya_PYSC/client/" + f_name):
            if os.stat("/Users/nikolajudin/Desktop/kursovaya_PYSC/client/" + f_name).st_size != 0:
                sock.send((bytes(f_name, encoding = 'UTF-8')))
                # открываем файл в режиме байтового чтения
                f = open ("/Users/nikolajudin/Desktop/kursovaya_PYSC/client/" + f_name, "rb")
                # читаем строку
                l = f.read(1024)
                while (l):
                    # отправляем строку на сервер
                    sock.send(l)
                    l = f.read(1024)
                f.close()
                break
            print(f"{f_name} пустой!")
            continue
        print(f"{f_name} такого файла нет!")
        pass         


def recv_files():
    a: bool = True
    while a == True:
        try:
            file_send()
            log = recv()
            send("OK")
            if log == "STOP":
                break
        except:
            break
    a = False
    print("Лимит передачи файлов")
    recv()
    q = "."
    sock.send(q.encode())
    #sock.close()

def menu():
    msg = recv()
    if msg == "Сервер переполнен":
        print(msg)
        return 1
    else:
        print(msg)
        action  = input("Введите текст: ")
        options = {"mkdir":mkdir,
        "cd":cd,
        "recv_file":recv_files
        }
        if action in options:
            send(action)
            options[action]()
        else:
            print("Такого действия нет!\n")
            send("Err")
    

def autoriz():
    while True:
        try:
            st = recv()
            if st == "Сервер переполнен":
                print(st)
                return 1
            print(st)
            msg = input("Введите: ")
            if msg == "":
                msg = '.'
            send(msg)
            print(recv())
            msg = input("Введите: ")
            if msg == "":
                msg = '.'
            send(msg)
            if recv() =="OK":
                break
        except:
            print("Связь с сервером потеряна")
            break

if autoriz() != 1:
    while True:
        try:
            if menu() == 1:
                break
        except:
            print("Связь с сервером потеряна!")
            break
else:
    pass