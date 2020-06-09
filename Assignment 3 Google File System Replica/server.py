import socket 
import thread
offline = dict()
online = dict()
def func(client, addr):
	print "connected to:  ", addr 
	while True:
		accountDet(client)
		

def accountDet(client):
	client.send("Do you have an account?")
	exist = client.recv(1024)
	if exist in ("No","n","no","N"):
		newAccount(client)
	else:
		existAccount(client)
def existAccount(client):
	userName = ""
	while not(userName in offline):
		client.send("Please enter your Username.")
		userName = client.recv(1024)
		if userName in offline:
			if userName in online:
				client.send("Sorry user is already online, you can't sign in from different devices. Enter any key to go back.")
				userName = client.recv(1024)
				accountDet(client)
				return
			else:
				online[userName]=client	
				mainMenu(client,userName)
		else:
			client.send("Username does not exist please try again with another userName")
def newAccount(client):
	client.send("Please Choose Your Username.")
	userName = client.recv(1024)
	while userName in offline:
		client.send("Username already exists, Please try again. If you want to go back enter \"**\".")
		if userName=="**":
			accountDet(client)
			return
		userName = client.recv(1024)
	offline[userName]=client
	online[userName]=client
	mainMenu(client,userName)
	
def mainMenu (client,userName):
	msg= """Welcome to the main menu, please select the appropriate option or input \"0\" at any time to go back to the previous menu.
	1)Open chat with a user.
	2)View recieved messages.
	3)Create a group."""
	client.send(msg)
	option = client.recv(1024)
	if not option:
		del online[userName]
	if option == "1":
		client.send("Who do you want to send a message to? Enter Username.")
		interact(client,userName)
	elif option == "0":
		accountDet(client)
		


def interact(client, userName):
	reciever= client.recv(1024)
	if reciever in offline:
		client.send("What message do you want to send?Enter \"**\" to stop sending message and go back to the previous menu.")
		msg =client.recv(1024)
		while msg != "**":
			client.send("----------------------------------")
			friend = online[reciever]
			friend.send("mesg/" + userName +"/"+msg + "/")
			msg =client.recv(1024)
		mainMenu(client, userName)
	else:
		client.send("Username does not exist, Please re-enter Username.")
		interact(client,userName)





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
