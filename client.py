import socket
import threading #chạy đa luồn
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import json

HOST = "127.0.0.1"
PORT = 8080

# Define global variables to hold the entry fields
e1 = None
e2 = None
entry_filenameDownload = None
entry_filenameUpload = None
entry_file_path = None

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
    if res == 'OK':
        chooseLayout()
    else:
        CLIENTSOCKET.close()
        print("Login failed. Please try again.")

    

#Gửi filename lên server để tìm address client
def sendFilenameToServerToFind(filename):
    #lấy tên file name từ trường nhập liệu
    data = {
        'filename' : filename,
        'method' : 'download',  
    }
    json_data = json.dumps(data)  # Convert dictionary to JSON string
    CLIENTSOCKET.send(json_data.encode())

    receiveAddressFromServer()

#nhận respon
def receiveAddressFromServer():
    address = CLIENTSOCKET.recv(1024).decode() #nhận về địa chỉ chưa file từ server
    if address != "False":
        print("File found at: ", address)
        #Thực hiện p2p với client(address) chưa file

    else:
        print(text="Cannot find client having this file")

#gửi data để cập nhật, sửa
def sendInformationOfFileToServerToSaveToDatabase(filename, path):
    data = {
        'filename' : filename,
        'path' : path,
        'method' : 'upload',
    }
    json_data = json.dumps(data) 
    CLIENTSOCKET.send(json_data.encode())

    receiveUpLoadResponseFromServer()

#nhận và show kết quả
def receiveUpLoadResponseFromServer():
    res = CLIENTSOCKET.recv(1024).decode()
    res_window = tk.Toplevel()
    res_window.title("Upload Response")
    
    label = tk.Label(res_window, text=res)
    label.pack()
    
    res_window.mainloop()   

def searchButtonClicked(entry_filenameDownload):
    filename = entry_filenameDownload.get() # Lấy giá trị từ trường nhập liệu
    sendFilenameToServerToFind(filename)

def uploadButtonClicked(entry_filenameUpload, entry_file_path):
    filename = entry_filenameUpload.get()
    path = entry_file_path.get()
    sendInformationOfFileToServerToSaveToDatabase(filename, path)

def openDownloadWindow(root):
    root.destroy() #Đóng cửa sổ hiện tại
    #tạo cửa sổ cho phần download
    download_window = tk.Tk()
    download_window.title("Download")
    download_window.geometry('300x150')
    #các thành phần và layout cho phần download
    label_name = tk.Label(download_window, text="Filename to download:",bg='#eb85de')
    label_name.pack()
    # Tạo trường nhập liệu
    entry_filenameDownload = tk.Entry(download_window)
    entry_filenameDownload.pack()
    # Tạo nút "Search"
    search_button = tk.Button(download_window, text="Search File to DownLoad", command=lambda: searchButtonClicked(entry_filenameDownload))
    search_button.pack()
    download_window.mainloop()

def openUploadWindow(root):
    root.destroy()
    #Tạo cửa sổ cho Upload
    upload_window = tk.Tk()
    upload_window.title("Upload")
    upload_window.geometry('300x150')
    #Các thành phần và layout cho phần upload
    label_name_upload = tk.Label(upload_window, text="Filename to upload:",bg='#eb85de')
    label_name_upload.pack()
    # Tạo trường nhập liệu
    entry_filenameUpload = tk.Entry(upload_window)
    entry_filenameUpload.pack()
    # Khung chọn file
    def browse_file():
        file_path = filedialog.askopenfilename()
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(tk.END, file_path)

    label_file_path = tk.Label(upload_window, text="File Path:")
    label_file_path.pack()

    entry_file_path = tk.Entry(upload_window)
    entry_file_path.pack()

    button_browse = tk.Button(upload_window, text="Choose FIle", command=browse_file)
    button_browse.pack()

    upload_button = tk.Button(upload_window, text="File to Upload", command=lambda: uploadButtonClicked(entry_filenameUpload, entry_file_path))
    upload_button.pack()
    
    upload_window.mainloop()

def openDownloadOrUploadWindow(choice):
    if choice == "download":
        openDownloadWindow()
    elif choice == "upload":
        openUploadWindow()


def chooseLayout():
    # Tạo giao diện tkinter
    root = tk.Tk()
    root.title("File Upload/Download Example")
    root.geometry('300x150')

    # Tạo nút "Download"
    download_button = tk.Button(root, text="Download", command=lambda: openDownloadOrUploadWindow("download"))
    download_button.pack()

    # Tạo nút "Upload"
    upload_button = tk.Button(root, text="Upload", command=lambda: openDownloadOrUploadWindow("upload"))
    upload_button.pack()
    root.mainloop()

def login(e1, e2):
    username = e1.get()
    password = e2.get()
    print(username, password)
    isLogin(username, password)
    login_window.destroy()


#Tạo giao diện login
login_window = tk.Tk()
login_window.title("Please Login")
login_window.geometry('300x150')
name = tk.Label(login_window, text = "Name").grid(row = 0, column = 0)
e1 = tk.Entry(login_window)
e1.grid(row = 0, column = 1)
password = tk.Label(login_window, text = "Password").grid(row = 1, column = 0)
e2 = tk.Entry(login_window)
e2.grid(row = 1, column = 1)
submit = Button(login_window, text = "Submit", command=lambda:login(e1, e2)).grid(row = 4, column = 0)
login_window.mainloop()



