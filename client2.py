import socket
import threading #chạy đa luồn
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import json

HOST = "127.0.0.1"
PORT = 8080

CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENTSOCKET.connect((HOST, PORT))

#đăng nhập
def isLogin(user, password):
    data = {
        'username': user,
        'password': password,
        'method': 'login'
    }
    json_data = json.dumps(data)
    print(json_data)
    CLIENTSOCKET.send(json_data.encode())
    loginResponse()

def loginResponse():
    res = CLIENTSOCKET.recv(1024).decode()
    print(res)

isLogin('a', 'v')