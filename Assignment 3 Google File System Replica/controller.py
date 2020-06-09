import socket 
import thread
import random

chunk_ports = []
direct = {}
busy = {}
def func(client, addr):
	i = random.randrange(1,3)
	print i
	print "connected to:  ", addr 
	option = client.recv(1024)
	client.send("ok")
	print option
	if option=="Chunk":
		Chunk(client)
	elif option=="Client":
		while True:
			print direct
			interact(client)


def Chunk(client):
	print "lol"
	port = client.recv(1024)
	chunk_ports.append(port)
	print chunk_ports

def interact(client):
	client.send("""What do you want to do? Select option:
		1. Upload File
		2. Download File
		3. Write File""")
	option = client.recv(1024)
	if option == "1":
		client.send("ok")
		uploader(client)
	elif option == "2":
		downloader(client)
	elif option =="3":
		client.send("ok")
		finder(client)

def finder(client):
	filename = client.recv(1024)
	client.send("ok")
	mode = client.recv(1024)
	if mode=="END":
		i =1
		find = filename + '_' + str(i)
		while True:
			 if find not in direct:
			 	break
			 i = i+1
			 find = filename + '_' + str(i)
		filename = filename + '_' + str(i-1)
		client.send(filename)
		client.recv(1024)
		ports = direct[filename][0] + '/' + direct[filename][1] + '/' +direct[filename][0]
		client.send(ports)
		busy[filename] = True
		uploader(client)
		client.recv(1024)
		busy[filename] = False
	if mode=="FIND":
		busy[filename] = True
		ports = direct[filename][0] + '/' + direct[filename][1] + '/' +direct[filename][0]
		client.send(ports)
		filename1 = filename
		while True:
			filename = client.recv(1024)
			busy[filename1] = False
			filename1= filename
			if filename == "STOP//":
				break
			if filename not in direct:
				array = []
				filename = client.recv(1024)
				print filename
				i = random.randrange(1,len(chunk_ports)+1)
				ports = chunk_ports[i-1]
				array.append(chunk_ports[i-1])
				if i>len(chunk_ports)-1:
					i=0
				array.append(chunk_ports[i])
				ports = ports + '/' + chunk_ports[i]
				if i+1>len(chunk_ports)-1:
					i=-1
				array.append(chunk_ports[i+1])
				ports = ports + '/' + chunk_ports[i+1]
				client.send(ports)
				direct[filename]= array
				busy[filename]=False
			else:
				while busy[filename]==True:
					x=0
				ports = direct[filename][0] + '/' + direct[filename][1] + '/' +direct[filename][0]
				busy[filename] = True
				client.send(ports)



def downloader(client):
	filename1 = ""
	while True:
		filename = client.recv(1024)
		busy[filename1] = False
		filename1= filename
		if filename not in direct:
			client.send("STOP//")
			client.recv(1024)
			break
		while busy[filename]==True:
			x=0
		port = direct[filename][0]
		busy[filename] = True
		client.send(port)	


def uploader(client):
	filename = ""
	while filename != "STOP//":
		array = []
		filename = client.recv(1024)
		print filename
		i = random.randrange(1,len(chunk_ports)+1)
		ports = chunk_ports[i-1]
		array.append(chunk_ports[i-1])
		if i>len(chunk_ports)-1:
			i=0
		array.append(chunk_ports[i])
		ports = ports + '/' + chunk_ports[i]
		if i+1>len(chunk_ports)-1:
			i=-1
		array.append(chunk_ports[i+1])
		ports = ports + '/' + chunk_ports[i+1]
		client.send(ports)
		direct[filename]= array
		busy[filename]=False




def Main():
	host='127.0.0.1'
	port=8000
	s = socket.socket()
	s.bind((host,port))
	s.listen(10) # max number of connections

	print "Waiting for new connections"
	while True:
		client, addr = s.accept()
		thread.start_new_thread(func,(client,addr))

		
if __name__=="__main__":
	Main()
