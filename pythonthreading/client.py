import socket
import threading

ip = '127.0.0.1'
port = 4321

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip,port))

msg = "Hello World!"
i = 10
while (i >= 0):
	cs.send(msg.encode())
	fromserver = cs.recv(1024)
	print(fromserver.decode())
	i = i - 1
fromserver = cs.recv(1024)
print(fromserver.decode())
cs.close()