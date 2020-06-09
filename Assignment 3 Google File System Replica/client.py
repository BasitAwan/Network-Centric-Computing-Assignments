import socket 
def Main(): 
	ip='127.0.0.1' 
	port=8000 

	s = socket.socket() 
	s.connect((ip,port))
	
	print("connection established")
	s.send("Client")
	s.recv(1024)
	while True:
		string = s.recv(1024)
		print string
		query = raw_input() 
		if query=="1":
			upload(s,query,ip)
		elif query=="2":
			download(s,query,ip)
		elif query=="3":
			write(s,query,ip)



def write(s,query,ip):
	s.send(query)
	s.recv(1024)
	filename = raw_input("Enter filename to want to write:")
	option = raw_input("Enter 1 to write at the end of the file or enter 2 to select bytes offset: ")
	if option=="1":
		s.send(filename)
		s.recv(1024)
		s.send("END")
		file = s.recv(1024)
		s.send("lol")
		ports = s.recv(1024)
		chunk = socket.socket()
		port = long(ports.split('/')[0])
		print port
		chunk.connect((ip,port))
		chunk = socket.socket()
		chunk.connect((ip,long(port)))
		print port
		chunk.send(file)
		print file
		chunk.recv(1024)
		print "Download done"
		chunk.send("DOWNLOAD")
		data = chunk.recv(64000)
		if data == "Error":
			print data
			return
		chunk.send("ok")	
		chunk.close()
		addition = raw_input("Input what you want to add \n ")
		data = data + addition
		print data
		f = open("lollll.txt",'w')
		f.write(data)
		f = open("lollll.txt",'r')
		bytesToSend = f.read(64000)
		i = long(file.split('_')[1])
		while bytesToSend !="":
			for x in xrange(0,3):
				port = long(ports.split('/')[x])
				chunk = socket.socket()
				chunk.connect((ip,port))
				chunk.send(filename+ '_' + str(i))
				chunk.recv(1024)
				chunk.send("UPLOAD")
				chunk.recv(1024)
				chunk.send(bytesToSend)
				chunk.close()
			bytesToSend = f.read(64000)
			if bytesToSend == "":
				break
			i = i + 1 
			s.send(filename+ '_' + str(i))
			ports = s.recv(1024)
		s.send("STOP//")
		s.recv(1024)
		s.send("done")
		f.close()
	if option=="2":
		bytesoffset = int(raw_input("Enter the bytes offset: "))
		filenumber = (bytesoffset/64000) + 1 
		s.send(filename + '_' + str(filenumber))
		s.recv(1024)
		s.send("FIND")
		ports = s.recv(1024)
		chunk = socket.socket()
		port = long(ports.split('/')[0])
		chunk.connect((ip,port))
		chunk.send(filename+'_'+ str(filenumber))
		chunk.recv(1024)
		chunk.send("DOWNLOAD")
		data = chunk.recv(64000)
		if data == "Error":
			print data
			return
		chunk.send("ok")	
		chunk.close()
		f = open("lollll.txt",'w')
		f.write(data)
		f = open("lollll.txt",'r')
		first_half = f.read(bytesoffset%64000)
		second_half = f.read()
		insert = raw_input("Input what you want to add \n")
		data = first_half + insert + second_half
		f = open("lollll.txt",'w')
		f.write(data)
		f = open("lollll.txt",'r')
		bytesToSend = f.read(64000)
		i = filenumber
		for x in xrange(0,3):
				port = long(ports.split('/')[x])
				chunk = socket.socket()
				chunk.connect((ip,port))
				chunk.send(filename+ '_' + str(i))
				chunk.recv(1024)
				chunk.send("UPLOAD")
				chunk.recv(1024)
				chunk.send(bytesToSend)
				chunk.close()
		remaining = f.read()
		i = i+1
		while remaining!="":
			s.send(filename+ '_' + str(i))
			ports = s.recv(1024)
			chunk = socket.socket()
			port = long(ports.split('/')[0])
			chunk.connect((ip,long(port)))
			chunk.send(filename+ '_' + str(i))
			chunk.recv(1024)
			chunk.send("DOWNLOAD")
			data = chunk.recv(64000)
			if data=="Error":
				data = remaining
			else:
				data = remaining + data
			f = open("lollll.txt",'w')
			f.write(data)
			f = open("lollll.txt",'r')
			bytesToSend = f.read(64000)
			chunk.send("ok")	
			chunk.close()
			for x in xrange(0,3):
				port = long(ports.split('/')[x])
				chunk = socket.socket()
				chunk.connect((ip,port))
				chunk.send(filename+ '_' + str(i))
				chunk.recv(1024)
				chunk.send("UPLOAD")
				chunk.recv(1024)
				chunk.send(bytesToSend)
				chunk.close()
			remaining = f.read()
			i = i+1
		s.send("STOP//")





def upload(s,query,ip):
	i = 1
	s.send(query)
	s.recv(1024)
	filename = raw_input("Enter Filename of file you want to upload:")
	try:
		f = open(filename,'r')
	except:
		print "File does not exist"
		return
	bytesToSend = f.read(64000)
	while bytesToSend !="":
		s.send(filename+ '_' + str(i))
		ports = s.recv(1024)
		for x in xrange(0,3):
			port = long(ports.split('/')[x])
			chunk = socket.socket()
			chunk.connect((ip,port))
			chunk.send(filename+ '_' + str(i))
			chunk.recv(1024)
			chunk.send("UPLOAD")
			chunk.recv(1024)
			chunk.send(bytesToSend)
			chunk.close()
		bytesToSend = f.read(64000)
		i = i + 1 
	s.send("STOP//")
	s.recv(1024)
	f.close()

def download(s,query,ip):
	i = 1
	s.send(query)
	filename = raw_input("Enter Filename of file you want to download:")
	f = open(filename,'w')
	while True :
		s.send(filename+ '_' + str(i))
		port = s.recv(1024)
		if port == "STOP//":
			s.send("stop")
			break
		chunk = socket.socket()
		chunk.connect((ip,long(port)))
		chunk.send(filename+ '_' + str(i))
		chunk.recv(1024)
		chunk.send("DOWNLOAD")
		data = chunk.recv(64000)
		if data == "Error":
			print data
			return
		chunk.send("ok")	
		chunk.close()
		f.write(data)
		i= i+1

	f.close()



		


if __name__=="__main__":
	Main()
