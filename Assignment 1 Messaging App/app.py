import socket
import thread
import os

gmsgs = dict()
dict = {}
username = ""
check = True
groupcheck = True
filesize = 0
filename = ""
checkfile = True

def GMSG(string, i):

	name = ""
	user = ""
	message = ""
	newmsg = ""

	while string[i] != "/":
		name = name + string[i]
		i = i+1

	i = i + 1
	while string[i] != "/":
		user = user + string[i]
		i = i+1

	i = i + 1

	while string[i] != "/":
		message = message + string[i]
		i = i + 1
		newmsg = {user: message}
	if(gmsgs.has_key(name) == True):
		gmsgs[name].append(newmsg)
	else:
		newgrp = [newmsg]
		gmsgs.update({name: newgrp})

	i = i + 1
	return string[i:]

def FILE(string, i):
	while string[i] != "/":
			temp = temp + string[i]
			i = i + 1

	i = i + 1
	while string[i] != "/":
		filename = filename + string[i]
		i = i + 1

	filename = "client" + filename
	filesize = long(temp)
	global fileptr
	fileptr = open(filename, 'wb')
	global checkfile
	checkfile = False
	return string[i:]

def mesg(string, i):
	username = ""
	message = ""

	while string[i] != "/":
		username = username + string[i]
		i = i + 1

	i = i + 1
	while string[i] != "/":
		message = message + string[i]
		i = i + 1

	if(dict.has_key(username) == True):
		dict[username].append(message)
	else:
		newstring = [message]
		dict.update({username: newstring})

	i = i + 1	
	return string[i:] 

def keys(string, s):
	print "You have messages from: " 
	print "users:"  
	print dict.keys()
	print "groups:" 
	print gmsgs.keys()
	print "(note you can only view group messages from option 4)"
	global username

	username = raw_input("Who's messages do you want to see? enter \"**\" to go back: ")
	while not (username in dict):
		if(username == "**"):
			break;
		else:
	 		print "invalid username, try again: "
	 		print dict.keys()
	 		print gmsgs.keys()
	 		username = raw_input("Who's messages do you want to see? enter \"**\" to go back: ")			

	s.send(username)
	return ""

def keyreader(string, s):
	while string != "":
		keyword = string[0:4]
		i = 0
		if(keyword == "mesg"):
			string = mesg(string[5:], i)

		elif(keyword == "keys"):
			string = keys(string, s)

		elif(keyword == "GMSG"):
			string = GMSG(string[5:], i)
		
		elif(keyword == "FILE"):
			string = FILE(string[5:], i)

def recv(username, s):
	while check:
		if username in dict:
			for i in dict.get(username):
				print username + ": " + i
			dict.pop(username, None)


def chat(username, s):
	chatmessage = ""
	global check
	check = True
	thread.start_new_thread(recv,(username, s))

	while chatmessage != "**" and chatmessage != "*$":
		chatmessage = raw_input()
		s.send(chatmessage)

	check = False


def grouprecv(group, s):
	while groupcheck:
		if group in gmsgs:
			for mesg in gmsgs.get(group):
				print (mesg.keys())[0] + ": " + (mesg.values())[0]
			gmsgs.pop(group, None)


def groupchat(group, s):
	chatmessage = ""
	global groupcheck
	groupcheck = True
	thread.start_new_thread(grouprecv,(group, s))


	while chatmessage != "*?":
		chatmessage = raw_input()
		s.send(chatmessage)
	groupcheck = False

def filesend(path, s):
	f = open(path, 'rb')
	l = ""
	l = f.read(1024)
	while (l != ""):
		s.send(l)
		l = f.read(1024)
		print "sending.."

	print 'all done'

def Main():
	ip = '127.0.0.1'
	port = 51111
	s = socket.socket()
	s.connect((ip,port))
	path = ""
	name = ""
	print("connected \n")
	msg1 = """Welcome to the main menu, please select the appropriate option or input \"0\" at any time to go back to the previous menu.
	1)Open chat with a user.
	2)View recieved messages.
	3)Create a group.
	4)Send message in a group.
	5)Display all online users"""

	msg2 = """Enter \"*!\" to add more members 
	or \"*@\" to make other people admin
	or \"**\" to go back to main menu
	or \"*x\" to go leave group
	or just send a message.""" 

	responses = ["Do you have an account?", msg1, msg2, "Please enter your Username.", "Sorry user is already online, you can't sign in from different devices. Enter any key to go back.", "Please Choose Your Username.", "Username already exists, Please try again. If you want to go back enter \"**\".", "Who do you want to add in the group?", "The Username already in group, please re-enter Username or enter \"**\" to get done.", "The Username does not exist, please re-enter Username or enter \"**\" to get done.", "Do you want to add anyone else? If not enter \"**\".", "Who do you want to add?", "Who do you want to make admin?", "Username not in group, please enter another username or enter \"**\" to get done", "Admin added, please enter another username or enter \"**\" to get done"]
	global username
	global filesize
	global filename
	global checkfile
	global fileptr
	while True:
		if(filesize <= 0 and checkfile == False):
			filesize = 0
			filename = ""
		string = s.recv(1024)
		if(string[0:4] in ("mesg", "keys", "GMSG", "FILE")):	
			keyreader(string, s)
		elif(string[0:5] == "list/"):
			print string[5:]
		elif(string == "Who do you want to send a message to? Enter Username."):
		 	username = raw_input(string + '\n' + "Enter name: ")
			s.send(username);
		elif(string == "Username does not exist, Please re-enter Username or enter \"**\" to go back to the Main Menu"):
		 	username = raw_input(string + '\n' + "Enter name or **: ")
			s.send(username);
		elif(string == "done with file" or string == "What message do you want to send?Enter \"**\" or \"*$\"  to stop sending message and go back to the Main menu or to send a file."):
			print string + ": "
			thread.start_new_thread(chat,(username, s))
		elif(string == "What message do you want to send in the group? or enter \"*?\" for options" or string == "What message do you want to send in the group? or enter *? to go back" or string == "You're not an admin, Send a message" or string == "returning to chat"):
			print string + '\n'
			thread.start_new_thread(groupchat,(name, s))	
		elif(string == "What do you want to name the group?"):
			name = raw_input(string + '\n' + "name: ")
			s.send(name)
		elif(string == "Group already exists, please re-enter name or enter \"**\" to go back to the main menu"):
			name = raw_input(string + '\n' + "Enter name or **: ")
			s.send(name)
		elif(string == "Which group do you want to send a message in?" or string == "Group does not exist, please enter name again. To go back enter \"**\" " or string == "Sorry but you are not added in this group, please try again.  To go back enter \"**\""):
			name = raw_input(string + '\n' + "Enter name or **: ")
			s.send(name)
		elif(string == "Enter file name in directory"):
			path = raw_input("Enter file name in directory: ")
			s.send(path)
		elif(string == "SIZE/"):
			size = str(os.path.getsize(path))
			s.send(size)
		elif(string == "SEND/"):
			thread.start_new_thread(filesend, (path, s))
		elif string in responses:
			response = raw_input(string + '\n')
			s.send(response)
		else:
			if(checkfile == False):	
				fileptr.write(string)
				filesize -= len(string)

	s.close()

if __name__ == "__main__":
	Main()


#backend messages
#username to connect to