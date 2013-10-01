#!/usr/bin/python
import minion, screen, re, signal

class Sschat:
	def __init__(self):
		self.screen=screen.Screen()
                signal.signal(signal.SIGINT, self.cleanQuit)
                signal.signal(signal.SIGHUP, self.cleanQuit)
		self.screen.printMessage("Hi, which would you like to connect to ?")
		self.channel = self.screen.getInput()
		while not re.match("^[A-Za-z]*$", self.channel):
			self.screen.printMessage("Bad channel name.")
			self.channel = self.screen.getInput()
		self.screen.printMessage("What's your nickname ?")
		self.nickname = self.screen.getInput()
		while not re.match("^[A-Za-z]*$", self.nickname):
			self.screen.printMessage("Bad nickname.")
			self.nickname = self.screen.getInput()
		self.minion=minion.Minion(self.channel, self.screen, self.nickname)
		self.screen.clearConvers()
                self.screen.setTitle(self.channel, len(self.minion.mySocket.peers))

	def main(self):
		while 1:
			chatMessage= self.screen.getInput()
			if chatMessage[0] != "/":
				chatMessage = self.nickname+"("+str(self.minion.myPid)+") : "+chatMessage
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
			else:
				self.command(chatMessage[1:])
			

        def cleanQuit(self, signum="", frame="", reason=""):
		try:
			self.minion
		except AttributeError:
	                self.screen.stopScreen()
        	        print "Bye !"
                	quit()
		else:
			if reason == "":
				reason = "None"
               		message= "/rem "+str(self.minion.myPid)+"|"+self.nickname+"|"+reason
	                self.minion.sendMessage(message)
        	        self.screen.stopScreen()
                	print "Bye !"
               		quit()


	def command(self, mess):
		cmd = mess.split(" ")[0]
		if cmd == "clear":
			self.screen.clearConvers()
		if cmd == "quit":
			self.cleanQuit(0, 0, mess[5:])
		if cmd == "horod":
			pass
		if cmd == "nickname":
			pass
		if cmd == "join":
			pass
		if cmd == "pm":
			pass
		if cmd == "hist":
			pass
		if cmd == "help":
			pass
		else:
			pass

chat=Sschat()
chat.main()

#sigwinch
#sigdecoparcebatarddessh


