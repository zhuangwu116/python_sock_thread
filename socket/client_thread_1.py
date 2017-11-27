# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
import socket
import struct
import os
import pickle
import tarfile,tempfile
import threading


def get_files_info(path):
    if not path or not os.path.exists(path):
        return None
    files = os.walk(path)
    infos = []
    file_paths = []
    for p,ds,fs in files:
        for f in fs:
            file_name = os.path.join(p,f)
            file_size = os.stat(file_name).st_size
            file_paths.append(file_name)
            file_name = file_name[len(path)+1:]
            infos.append((file_size,file_name))
    return infos,file_paths
def send_files_infos(my_socket,infos,compress):
    fmt_str = 'Q?'
    infos_bytes = pickle.dumps(infos)
    infos_bytes_len = len(infos_bytes)
    infos_len_pack = struct.pack(fmt_str,infos_bytes_len,compress)
    my_socket.sendall(infos_len_pack)
    my_socket.sendall(infos_bytes)
def send_file(my_socke,file_path,compress):
    if not compress:
        f = open(file_path,'rb')
    else:
        f = tempfile.NamedTemporaryFile()
        tar = tarfile.open(mode='w|gz',fileobj=f)
        tar.add(file_path)
        tar.close()
        f.seek(0)
        filesize = os.stat(f.name).st_size
        filesize_bytes = struct.pack('Q',filesize)
        my_socke.sendall(filesize_bytes)
    try:
        while True:
            data = f.read(1024)
            if data:
                my_socke.sendall(data)
            else:
                break
    finally:
        f.close()
def get_bak_info(my_socke,size=7):
    info = my_socke.recv(size)
    print(info.decode('utf-8'))

def start(host,post,src,compress):
    if not os.path.exists(src):
        print("备份的目录不存在!")
        return
    s = socket.socket()

    s.connect((host,post))
    path = src
    file_infos,file_paths = get_files_info(path)
    send_files_infos(s,file_infos,compress)
    for fp in file_paths:
        send_file(s,fp,compress)
        print(fp)
        get_bak_info(s)

    s.close()

class MyFrame(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.grid()
        self.remote_ip = '127.0.0.1'
        self.remote_ports = 10888
        self.compress_var = BooleanVar()
        self.remote_ip_var = StringVar()
        self.remote_ports_var = IntVar()
        self.bak_src_var = StringVar()
        self.init_components()

    def init_components(self):
        proj_name = Label(self,text = '远程备份客户机')
        proj_name.grid(columnspan=2)
        serv_ip_label = Label(self,text = "服务地址:")
        serv_ip_label.grid(row=1)

        self.serv_ip = Entry(self,textvariable=self.remote_ip_var)
        self.remote_ports_var.set(self.remote_ip)
        self.serv_ip.grid(row=1,column=1)

        serv_port_label = Label(self,text="服务端口:")
        serv_port_label.grid(row=2)

        self.serv_port = Entry(self,textvariable=self.remote_ports_var)
        self.remote_ports_var.set(self.remote_ports)
        self.serv_port.grid(row=2,column=1)

        src_label = Label(self,text="备份的目标:")
        src_label.grid(row=3)

        self.bak_src = Entry(self,textvariable=self.bak_src_var)
        self.bak_src.grid(row=3,column=1)

        tar_label = Label(self,text="压缩备份:")
        tar_label.grid(row=4)

        self.compress_on = Checkbutton(self,text="开启压缩",variable=self.compress_var,onvalue=1,offvalue=0)
        self.compress_on.grid(row=4,column=1)

        self.start_serv_btn=Button(self,text='开始备份',command=self.start_send)
        self.start_serv_btn.grid(row=5)
        self.start_exit_btn = Button(self,text="退出程序",command=self.root.destroy)
        self.start_exit_btn.grid(row=5,column=1)

    def start_send(self):
        #print(self.remote_ip_var.get(),self.remote_ports_var.get())
        host = self.remote_ip_var.get()
        port = self.remote_ports_var.get()
        compress = self.compress_var.get()
        src = self.bak_src_var.get()
        self.bak_src_var.set('')
        t = threading.Thread(target=start,args=(host,int(port),src,compress))
        t.start()
        # start(self.remote_ip_var.get(),int(self.remote_ports_var.get()),self.bak_src_var.get())
if __name__ == '__main__':
    root = Tk()
    root.title('远程备份客户机')
    root.resizable(False,False)
    app = MyFrame(root)
    app.mainloop()




