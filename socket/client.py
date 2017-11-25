# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
import socket
import struct

def start(host,post):
    pass

class MyFrame(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.grid()
        self.remote_ip = '127.0.0.1'
        self.remote_ports = 10888
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

        self.start_serv_btn=Button(self,text='开始备份',command=self.start_send)
        self.start_serv_btn.grid(row=4)
        self.start_exit_btn = Button(self,text="退出程序",command=self.root.destroy)
        self.start_exit_btn.grid(row=4,column=1)

    def start_send(self):
        print(self.remote_ip_var.get(),self.remote_ports_var.get())
        start(self.remote_ip_var.get(),int(self.remote_ports_var.get()))
if __name__ == '__main__':
    root = Tk()
    root.title('远程备份客户机')
    root.resizable(False,False)
    app = MyFrame(root)
    app.mainloop()




