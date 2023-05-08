import threading
import socket

def handlecon(c_socket,address):
	print("Got connection from: {}".format(address))
	msg = c_socket.recv(1024).decode()
	m2 = "Hey there client!"
	while msg != 'quit':
		print(msg)
		c_socket.send(m2.encode())
		msg = c_socket.recv(1024).decode()
	c_socket.close()

ip = '127.0.0.1'
port = 4321
THREADS = []


s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind((ip, port))
s_socket.listen()
while True:
	print('connection not accepted yet')
	c_socket,address = s_socket.accept()
	print('connection accepted!')
	t = threading.Thread(target=handlecon,args=(c_socket,address))
	THREADS.append(t)
	t.start()
