import minion, screen, signal, text, time, socket, threading, crypt, curses, tools

class Sschat:
	def __init__(self, channel="", nickname="", history=""):
		self.screen=screen.Screen()
                signal.signal(signal.SIGINT, self.screen.clearInput)
                signal.signal(signal.SIGHUP, self.cleanQuit)
	        signal.signal(signal.SIGWINCH, self.screen.handlerResize)
		self.update = False
	        signal.signal(signal.SIGUSR1, self.handlerUpdate)
		if channel == "":
			self.screen.printMessage("Hi, which channel would you like to connect to ?")
			channel = self.screen.strictInput()
		if nickname == "":
			self.screen.printMessage("What's your nickname ?")
			nickname = self.screen.strictInput()
		self.minion=minion.Minion(channel, self.screen, nickname)
		self.screen.clearConvers()
                self.screen.setTitle(channel, len(self.minion.mySocket.peers))
		if history != "":
			self.screen.history=history
			self.screen.printHistory()
		self.motd()

	def main(self):
		while 1:
			chatMessage= self.screen.getInput()
			if self.update == True :
				self.screen.printMessage("You are going to be upgraded, please wait 5 seconds")
				self.channelSwitch("Update")
				return (self.minion.channel, self.minion.nickname, self.screen.history)
			if chatMessage[0] != "/":
				chatMessage = self.minion.nickname+" : "+chatMessage
				if self.minion.encrypt == False:
					self.minion.sendMessage("/msg "+chatMessage)
				else :
					chatMessage = "<e> "+chatMessage
		                        encMessage = self.minion.crypto.encrypt(chatMessage)
		                        self.minion.sendMessage("/enc "+encMessage)
                        	self.screen.printMessage(chatMessage)
			else:
				newChannel = self.command(chatMessage[1:])
				if newChannel:
					self.channelSwitch()
					return (newChannel, self.minion.nickname, "")

				
        def channelSwitch(self, reason="ChannelSwitch"):
      		message= "/rem "+self.minion.pid+"|"+self.minion.nickname+"|"+reason
	        self.minion.sendMessage(message)
        	self.screen.stopScreen()
		self.minion.mySocket.active=False
		self.minion.mySocket.sock.shutdown(socket.SHUT_RDWR)
		self.minion.mySocket.sock.close()
		self.screen.stopNotif()
		self.minion.myAfk.active=False
		self.minion.myAfk.afkEvent.set()
		while threading.activeCount() != 1:
			time.sleep(0.2)

	def handlerUpdate(self, signum, frame):
		self.update = True
                self.screen.interruptInput=True
                curses.ungetch(curses.ascii.NL)

        def cleanQuit(self, signum="", frame="", reason=""):
		try:
			self.minion
		except AttributeError:
	                self.screen.stopScreen()
        	        print self.motBye()
                	quit()
		else:
			if reason == "":
				reason = "Deco"
               		message= "/rem "+self.minion.pid+"|"+self.minion.nickname+"|"+reason
	                self.minion.sendMessage(message)
        	        self.screen.stopScreen()
        	        print self.motBye()
               		quit()

	def motBye(self):
		f = open('motb', 'r')
		line = f.readline()
		f.close()
		return line[:-1]

        def motd(self):
                f = open('motd', 'r')
                lines = f.readlines()
                f.close()
		for line in lines :
			self.screen.printMessage(line[:-1])

        def bug(self, mess):
                line = '#'+mess+"\n"
		try :
	                f = open('bugReport', 'a')
			f.write(line)
                	f.close()
			self.screen.printMessage("Bug sent.")			
		except:
			self.screen.printMessage("Bug not sent.")

	def command(self, mess):
		cmd = mess.split(" ")[0]
		args = mess.split(" ")[1:]
		if cmd == "clear":
			self.screen.clearConvers()
		elif cmd == "help":
			self.screen.scrollPrinter(text.help)
                elif cmd == "paste":
                        longLine = self.screen.getPaste()
                        if longLine != "" :
                                chatMessage = self.minion.nickname+" : "+longLine
                                if self.minion.encrypt == False:
                                        self.minion.sendMessage("/msg "+chatMessage)
                                else :
                                        chatMessage = "<e> "+chatMessage
                                        encMessage = self.minion.crypto.encrypt(chatMessage)
                                        self.minion.sendMessage("/enc "+encMessage)
                                self.screen.printMessage(chatMessage)
		elif cmd == "encrypt" and len(args) == 1:
			if args[0] == "on" and self.minion.encrypt == False:
				self.screen.printMessage("Please enter the private key.")
				self.minion.crypto=crypt.Crypt(self.screen.getInput())
				self.minion.encrypt=True
			if args[0] == "off" and self.minion.encrypt == True:
				del self.minion.crypto
				self.minion.encrypt=False
				self.screen.printMessage("Encryption disabled.")
		elif cmd == "list":
			self.screen.printMessage("Peoples present in channel :")
			self.minion.sendMessage("/get "+self.minion.pid)
		elif cmd == "afk" and len(args) == 1:
			if args[0] == "on":
				chatMessage = self.minion.nickname+" is now AFK."
                                self.minion.sendMessage("/msg "+chatMessage)
                                self.screen.printMessage(chatMessage)
				self.minion.afk = True
			if args[0] == "off":
				chatMessage = self.minion.nickname+" is back."
                                self.minion.sendMessage("/msg "+chatMessage)
                                self.screen.printMessage(chatMessage)
				self.minion.afk = False
		elif cmd == "quit":
			reason=' '.join(args)
			if reason=="":
				reason="None"
			self.cleanQuit(0, 0, reason)
		elif cmd == "channel" and len(args) == 1:
                        channel = args[0]
                        if tools.validateName(channel):
				return channel
                        else:
                                self.screen.printMessage("Bad channel name.")
		elif cmd == "timestamp" and len(args) == 1:
			if args[0] == "on":
				self.screen.timestamp=True
			if args[0] == "off":
				self.screen.timestamp=False
		elif cmd == "notif" and len(args) == 1:
			if args[0] == "on":
				self.screen.startNotif()
				self.screen.printMessage("Visual notification enabled.")
			if args[0] == "off":
				self.screen.stopNotif()
				self.screen.printMessage("Visual notification disabled.")
		elif cmd == "nickname" and len(args) == 1:
			nick = args[0]
			if tools.validateName(nick):
				chatMessage = self.minion.nickname+"("+self.minion.pid+") is now known as "+nick
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
				self.minion.nickname=nick
			else:
				self.screen.printMessage("Bad nickname.")
		elif cmd == "bug" and len(args) >= 1:
			mess=' '.join(args)
			self.bug(mess)
                elif cmd == "me" and len(args) >= 1:
                        mess=' '.join(args)
                        chatMessage = self.minion.nickname+" "+mess
                        if self.minion.encrypt == False:
                                self.minion.sendMessage("/msg "+chatMessage)
                        else :
                                chatMessage = "<e> "+chatMessage
                                encMessage = self.minion.crypto.encrypt(chatMessage)
                                self.minion.sendMessage("/enc "+encMessage)
                        self.screen.printMessage(chatMessage)
		elif cmd == "pm" and len(args) >= 2:
			pid=args[0]
			message=' '.join(args[1:])
			outMessage="/msg PM from "+self.minion.nickname+"("+self.minion.pid+") : "+message
	        	self.minion.sendMessageTo(outMessage, pid)		
			self.screen.printMessage("PM to "+pid+" : "+message)
		elif cmd == "history"  and len(args) <= 1:
			if len(args) == 0:
				if self.screen.doHistory == 1:
					self.screen.scrollPrinter(self.screen.history)
			elif args[0] == "on":
				self.screen.doHistory=1
				self.screen.printMessage("History enabled.")
			elif args[0] == "off":
				self.screen.doHistory=0
				self.screen.history.clear()
				self.screen.printMessage("History disabled.")
			elif args[0] == "clear":
				self.screen.history.clear()
