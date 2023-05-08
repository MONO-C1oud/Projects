import socket
import threading

ip = '127.0.0.1'
port = 4321

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind((ip, port))

s_socket.listen()
c_socket,address = s_socket.accept()

print("Got connection from: {}, {}".format(c_socket, address))

m2 = "Hey there client!"
while True:
	msg = c_socket.recv(1024)
	print(msg.decode())
	c_socket.send(m2.encode())

c_socket.close()
s_socket.close()