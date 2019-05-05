import tkinter as tk
from tkinter import *
import socket
HOST = '127.0.0.1'
PORT = 9995
BUFFSIZE = 2
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

tk=Tk()
tk.title('Slide show')
frame =  Canvas(bg='black', height=768, width=1366)

im0 = PhotoImage(file='0.png')
im1 = PhotoImage(file='1.png')
im2 = PhotoImage(file='2.png')
im3 = PhotoImage(file='3.png')
images = [im0, im1, im2, im3]
frame.pack()
fst = 1
d = "00"
def get():
	global fst
	if fst==1:
		d = "00"
	else:
		d = client_socket.recv(BUFFSIZE).decode("utf-8")
	d = str(d)
	d = int(d)
	frame.create_image(20,20, anchor=NW, image=images[d])
	fst = 0;
	tk.after(500, get)
get()
tk.mainloop()

