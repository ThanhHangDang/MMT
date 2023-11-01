import socket
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import json

HOST = "127.0.0.1"
PORT = 8080

CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENTSOCKET.connect((HOST, PORT))

# Define a global variable to hold the main window
main_window = None

# Đăng nhập
def isLogin(user, password):
    data = {
        'username': user,
        'password': password,
        'method': 'login'
    }
    json_data = json.dumps(data)
    CLIENTSOCKET.send(json_data.encode())
    loginResponse()

def loginResponse():
    res = CLIENTSOCKET.recv(1024).decode()
    print(res)
    if res == 'OK':
        # Đóng cửa sổ đăng nhập
        login_window.destroy()
        # Mở cửa sổ chọn layout
        chooseLayout()
    else:
        CLIENTSOCKET.close()
        login_window.destroy()
        res_window = tk.Tk()
        res_window.title("Upload Response")

        label = tk.Label(res_window, text="Login Fail")
        label.pack()

        res_window.mainloop()
        print("Login failed. Please try again.")

# Mở cửa sổ download
def openDownloadWindow():
    global main_window
    main_window.destroy()
    download_window = tk.Tk()
    download_window.title("Download")
    download_window.geometry('300x150')
    # Các thành phần và layout cho phần download
    label_name = tk.Label(download_window, text="Filename to download:", bg='#eb85de')
    label_name.pack()
    # Tạo trường nhập liệu
    entry_filenameDownload = tk.Entry(download_window)
    entry_filenameDownload.pack()
    # Tạo nút "Search"
    search_button = tk.Button(download_window, text="Search File to Download", command=lambda: searchButtonClicked(entry_filenameDownload))
    search_button.pack()
    download_window.mainloop()

# Mở cửa sổ upload
def openUploadWindow():
    global main_window
    main_window.destroy()
    upload_window = tk.Tk()
    upload_window.title("Upload")
    upload_window.geometry('300x150')
    # Các thành phần và layout cho phần upload
    label_name_upload = tk.Label(upload_window, text="Filename to upload:", bg='#eb85de')
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

    button_browse = tk.Button(upload_window, text="Choose File", command=browse_file)
    button_browse.pack()

    upload_button = tk.Button(upload_window, text="File to Upload", command=lambda: uploadButtonClicked(entry_filenameUpload, entry_file_path))
    upload_button.pack()
    upload_window.mainloop()

# Mở cửa sổ chọn layout
def chooseLayout():
    global main_window
    main_window = tk.Tk()
    main_window.title("File Upload/Download Example")
    main_window.geometry('300x150')

    # Tạo nút "Download" và "Upload" và gán cho các hàm tương ứng
    download_button = tk.Button(main_window, text="Download", command=openDownloadWindow)
    download_button.pack()

    upload_button = tk.Button(main_window, text="Upload", command=openUploadWindow)
    upload_button.pack()
    main_window.mainloop()

# Hàm gửi filename lên server để tìm địa chỉ client
def sendFilenameToServerToFind(filename):
    data = {
        'filename' : filename,
        'method' : 'download',
    }
    json_data = json.dumps(data)
    CLIENTSOCKET.send(json_data.encode())
    receiveAddressFromServer()

# Nhận respon
def receiveAddressFromServer():
    address = CLIENTSOCKET.recv(1024).decode()
    if address != "False":
        print("File found at: ", address)
        # Thực hiện p2p với client(address) chứa file
    else:
        print("Cannot find a client having this file")

# Gửi data để cập nhật, sửa
def sendInformationOfFileToServerToSaveToDatabase(filename, path):
    data = {
        'filename' : filename,
        'path' : path,
        'method' : 'upload',
    }
    json_data = json.dumps(data)
    CLIENTSOCKET.send(json_data.encode())
    receiveUploadResponseFromServer()

# Nhận và show kết quả
def receiveUploadResponseFromServer():
    res = CLIENTSOCKET.recv(1024).decode()
    res_window = tk.Toplevel()
    res_window.title("Upload Response")

    label = tk.Label(res_window, text=res)
    label.pack()

    res_window.mainloop()

# Hàm xử lý nút "Search File to Download"
def searchButtonClicked(entry_filenameDownload):
    filename = entry_filenameDownload.get()
    sendFilenameToServerToFind(filename)

# Hàm xử lý nút "File to Upload"
def uploadButtonClicked(entry_filenameUpload, entry_file_path):
    filename = entry_filenameUpload.get()
    path = entry_file_path.get()
    sendInformationOfFileToServerToSaveToDatabase(filename, path)

# Hàm xử lý nút "Submit" trong cửa sổ đăng nhập
def login(e1, e2):
    username = e1.get()
    password = e2.get()
    print(username, password)
    isLogin(username, password)

# Tạo giao diện đăng nhập
login_window = tk.Tk()
login_window.title("Please Login")
login_window.geometry('300x150')
name = tk.Label(login_window, text="Name").grid(row=0, column=0)
e1 = tk.Entry(login_window)
e1.grid(row=0, column=1)
password = tk.Label(login_window, text="Password").grid(row=1, column=0)
e2 = tk.Entry(login_window)
e2.grid(row=1, column=1)
submit = Button(login_window, text="Submit", command=lambda: login(e1, e2))
submit.grid(row=4, column=0)
login_window.mainloop()
