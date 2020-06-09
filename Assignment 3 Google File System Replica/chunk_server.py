import socket 
import random
import thread
import hashlib
port = 8001

checksums = {}

def func(client,addr):
	filename = client.recv(1024)
	print filename
	client.send("ok")
	option = client.recv(1024)

	if option == "UPLOAD":
		upload(client,filename)

	elif option == "DOWNLOAD":
		download(client,filename)


def upload(client,filename):
	client.send("ok")
	f = open(filename,'w')
	data = client.recv(64000)
	checksums[filename] = int(hashlib.sha1(data).hexdigest(),16)
	f.write(data)
	f.close()

def download(client,filename):
	try:
		f = open(filename,'r')
	except:
		client.send("Error")
		print "LOL"
		return
	bytestosend = f.read(64000)
	check = int(hashlib.sha1(bytestosend).hexdigest(),16)
	if check!= checksums[filename]:
		client.send("Error" + filename)
		return
	client.send(bytestosend)
	client.recv(1024)
	f.close()



def listener(recieve):
	ip='127.0.0.1' 
	global port
	port = random.randrange(8001,60000)
	try:
		recieve.bind((ip,port))
		return port
	except:
		return listener(s)
def Main(): 
	ip='127.0.0.1' 
	controller=8000 

	s = socket.socket() 
	s.connect((ip,controller))
	print("connection established")
	s.send("Chunk")
	s.recv(1024)
	recieve = socket.socket()
	port = listener(recieve)
	s.send(str(port))
	recieve.listen(10)

	while True:
		client, addr = recieve.accept()
		thread.start_new_thread(func,(client,addr))
		

	s.close()

if __name__=="__main__":
	Main()
