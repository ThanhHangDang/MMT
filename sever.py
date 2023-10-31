import socket
from os import error #xuất ra lỗi
import os
import threading #chạy đa luồn
import json

#đặt host là IP của máy
HOST = "127.0.0.1"
PORT = 8080

#Tạo server socket
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Dùng try-except để bắt sự kiện
    #Cụ thể dùng socket SERVER kết nối (bind) vào HOST, PORT
        #Thành công in ra thông báo...
        #Lỗi in ra mã lỗi
try:
    SERVER.bind((HOST,PORT))
    print(f'* Running on http://{HOST}:{PORT}')
except socket.error as e:
    print(f'socket error: {e}')
    print('socket error: %s' %(e))


def _start():
    SERVER.listen() #lắng nghe yêu cầu từ phía client
    while True:
        conn, addr = SERVER.accept() #giá trị trả về accept là kết nối và địa chỉ
        #Khai báo thread để nhận dữ liệu đa luồng
        thread = threading.Thread(target=_handle, args=(conn, addr))
        thread.start()

#nhận dữ liệu khi server chấp nhận kết nối socket
def _handle(conn, addr):
    while True:
        #Dữ liệu nhận được dạng bytes nên decode về string
        data = conn.recv(1024).decode()
        #nếu không có data thì thoát khỏi vòng lặp để chạy hàm handle khác
        if not data: break

        data_dict = json.loads(data)  # Convert JSON string to dictionary
        res = []

        if data_dict['method'] == 'download':
            with open('database.json', 'r') as file:
                database =json.load(file)
                res = []
                for item in database:
                    if item['filename'] == data_dict['filename']:
                        res.append(item)
            file.close()

        elif data_dict['method'] == 'upload':
            with open('database.json', 'r') as file:
                database = json.load(file)
                found = False
                for item in database:
                    if item['filename'] == data_dict['filename'] :
                        item['path'] = data_dict['path']
                        found = True
                        res = 'Database is updated Successfull!!!'
                
                if not found:
                    new_item = {
                        "filename" : data_dict['filename'],
                        "ipaddress" : addr,
                        'path' : data_dict['path']
                    }
                    database.append(new_item)
                    res = 'Database is added Successfull!!!'
                        
            with open('database.json','w') as file:
                json.dump(database, file)        
            file.close()                    

        elif data_dict['method'] == 'login':
            print(data_dict)
            with open('login.json', 'r') as file:
                user = json.load(file)
                foundUser = False
                for item in user:
                    print(item['username'])
                    if item['username'] == data_dict['username'] and item['password'] == data_dict['password']:
                        res = 'OK'
                        foundUser = True
                
                if not foundUser:
                    res = 'Not user'
            file.close()

        else:
            print('dkuyum')

        if not isinstance(res, str):
            res_dict = json.dumps(res)
        else:
            res_dict = res
        #nhận được dữ liệu thì phản hồi về phía client, encode() về lại dạng bytes
        conn.send(res_dict.encode())
        #conn.close() # đóng kết nối
        #break #thoát khỏi vòng lặp để nhận handle khắc

if __name__ == '__main__':
    _start()