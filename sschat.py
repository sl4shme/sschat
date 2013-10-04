#!/usr/bin/python
import minion, screen, re, signal

class Sschat:
	def __init__(self):
		self.screen=screen.Screen()
                signal.signal(signal.SIGHUP, self.cleanQuit)
                signal.signal(signal.SIGINT, self.screen.clearInput)
	        signal.signal(signal.SIGWINCH, self.screen.handlerResize)
		self.screen.printMessage("Hi, which channel would you like to connect to ?")
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
		self.screen.printMessage("/help to list available commands")

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
		args = mess.split(" ")[1:]
		if cmd == "clear":
			self.screen.clearConvers()
		elif cmd == "help":
			self.screen.printMessage("Available commands : /clear /help")
			self.screen.printMessage("/quit [message]")
			self.screen.printMessage("/timestamp on|off")
			self.screen.printMessage("/nickname newNickname")
			self.screen.printMessage("/pm id message")
		elif cmd == "quit":
			reason=' '.join(args)
			self.cleanQuit(0, 0, reason)
		elif cmd == "timestamp":
			if mess.split(" ")[1] == "on":
				self.screen.timestamp=True
			if mess.split(" ")[1] == "off":
				self.screen.timestamp=False
		elif cmd == "nickname":
			nick = args[0]
			if re.match("^[A-Za-z]*$", nick):
				chatMessage = self.nickname+"("+str(self.minion.myPid)+") is now known as "+nick
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
				self.nickname=nick
			else:
				self.screen.printMessage("Bad nickname.")
		elif cmd == "pm":
			pid=args[0]
			message=' '.join(args[1:])
			outMessage="/msg PM from "+self.nickname+"("+str(self.minion.myPid)+") : "+message
		        self.minion.sendMessageTo(outMessage, pid)		
			self.screen.printMessage("PM to "+pid+" : "+message)
		elif cmd == "join":
			pass
		elif cmd == "history": #on off rien=afficher int=longueur clear=vider
			pass
		else:
			pass

chat=Sschat()
chat.main()

