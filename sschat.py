#!/usr/bin/python
import minion, screen, signal, help, re, time, socket, threading

class Sschat:
	def __init__(self, channel="", nickname=""):
		self.screen=screen.Screen()
                signal.signal(signal.SIGINT, self.screen.clearInput)
                signal.signal(signal.SIGHUP, self.cleanQuit)
	        signal.signal(signal.SIGWINCH, self.screen.handlerResize)
		if channel == "":
			self.screen.printMessage("Hi, which channel would you like to connect to ?")
			channel = self.screen.strictInput()
		if nickname == "":
			self.screen.printMessage("What's your nickname ?")
			nickname = self.screen.strictInput()
		self.minion=minion.Minion(channel, self.screen, nickname)
		self.screen.clearConvers()
                self.screen.setTitle(channel, len(self.minion.mySocket.peers))
		self.motd()

	def main(self):
		while 1:
			chatMessage= self.screen.getInput()
			if chatMessage[0] != "/":
				chatMessage = self.minion.nickname+" : "+chatMessage
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
			else:
				newChannel = self.command(chatMessage[1:])
				if newChannel:
					self.channelSwitch()
					return (newChannel, self.minion.nickname)
										
        def channelSwitch(self):
      		message= "/rem "+self.minion.pid+"|"+self.minion.nickname+"|ChannelSwitch"
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
		elif cmd == "channel":
                        channel = args[0]
                        if re.match("^[A-Za-z]*$", channel) and len(channel) <= 12:
				return channel
                        else:
                                self.screen.printMessage("Bad channel name.")
		elif cmd == "help":
			self.screen.scrollPrinter(help.help)
		elif cmd == "list":
			self.screen.printMessage("Peoples present in channel :")
			self.minion.sendMessage("/get "+self.minion.pid)
		elif cmd == "quit":
			reason=' '.join(args)
			if reason=="":
				reason="None"
			self.cleanQuit(0, 0, reason)
		elif cmd == "timestamp":
			if args[0] == "on":
				self.screen.timestamp=True
			if args[0] == "off":
				self.screen.timestamp=False
		elif cmd == "notif":
			if args[0] == "on":
				self.screen.startNotif()
			if args[0] == "off":
				self.screen.stopNotif()
		elif cmd == "afk":
			if self.minion.afk == False :
				chatMessage = self.minion.nickname+" is now AFK."
                                self.minion.sendMessage("/msg "+chatMessage)
                                self.screen.printMessage(chatMessage)
				self.minion.afk = True
			else :
				self.minion.afk = False
		elif cmd == "nickname":
			nick = args[0]
			if re.match("^[A-Za-z]*$", nick) and len(nick) <= 12:
				chatMessage = self.minion.nickname+"("+self.minion.pid+") is now known as "+nick
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
				self.minion.nickname=nick
			else:
				self.screen.printMessage("Bad nickname.")
		elif cmd == "bug":
			mess=' '.join(args)
			self.bug(mess)
		elif cmd == "pm":
			if len(args) >= 2:
				pid=args[0]
				message=' '.join(args[1:])
				outMessage="/msg PM from "+self.minion.nickname+"("+self.minion.pid+") : "+message
		        	self.minion.sendMessageTo(outMessage, pid)		
				self.screen.printMessage("PM to "+pid+" : "+message)
		elif cmd == "history":
			if len(args) == 0:
				if self.screen.doHistory == 1:
					self.screen.scrollPrinter(self.screen.history)
			elif args[0] == "on":
				self.screen.doHistory=1
			elif args[0] == "off":
				self.screen.doHistory=0
				self.screen.history.clear()
			elif args[0] == "clear":
				self.screen.history.clear()
		else:
			self.screen.printMessage("/"+mess)

chat=Sschat()
while 1 :
	newChannel, nickname = chat.main()
	chat=None
	chat=Sschat(newChannel, nickname)
