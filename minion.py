import socket, os, re, hashlib, threading

class AfkManager(threading.Thread):
	def __init__(self, minion):
        	threading.Thread.__init__(self)
		self.minion=minion
		self.afkEvent=threading.Event()

	def run(self):
		while 1:
			if self.afkEvent.wait(3600) :
				self.afkEvent.clear()
				if self.minion.afk == True :
					self.minion.afk = False
			else:
				if self.minion.afk == False :
					self.minion.afk = True

class SocketManager(threading.Thread):
	def __init__(self, minion):
        	threading.Thread.__init__(self)
		self.minion=minion
		self.address='\0'+self.minion.pid+'|'+self.minion.channelHash
		self.initPeers()
	        self.sock=socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.sock.bind(self.address)

	def run(self):
        	while 1:
                	incomingMessage = self.sock.recvfrom(4096)
                	self.handlerGetComm(incomingMessage[0])

	def handlerGetComm(self, incMess):
		if incMess[0] == "/":
                        if incMess[1:4] == "get":
                                self.handlerGetNick(incMess[5:])
                        if incMess[1:4] == "add":
                                self.handlerAddPeer(incMess[5:])
                        if incMess[1:4] == "rem":
                                self.handlerRemPeer(incMess[5:])
                        if incMess[1:4] == "msg":
                                self.handlerGetMess(incMess[5:])

        def handlerAddPeer(self, mess):
		pid, name = mess.split("|")
                self.peers.append(pid)
		self.minion.screen.setTitle(self.minion.channel, len(self.peers))
		self.minion.screen.printMessage(name+" joined.")

        def handlerRemPeer(self, mess):
		pid, name, reason = mess.split("|")
		try:
	                self.peers.remove(pid)
			self.minion.screen.setTitle(self.minion.channel, len(self.peers))
			self.minion.screen.printMessage(name+" leaved. (Reason:"+reason+")")
		except:
			pass

        def handlerGetMess(self, message):
		if self.minion.screen.doNotif == True:
			self.minion.screen.notif.flash = True
		self.minion.screen.printMessage(str(message))

        def handlerGetNick(self, pid):
		mess="/msg "+self.minion.nickname+" "+self.minion.pid
		if self.minion.afk == True :
			mess = mess+" <AFK>"
		self.minion.sendMessageTo(mess, pid)

        def initPeers(self):
                self.peers=[]
                expr = re.compile(r'.*%s.*' % self.minion.channelHash)
                for line in open("/proc/net/unix"):
                        match = expr.search(line)
                        if match:
                                matchLine = match.group()
                                matchLine = matchLine.split("@", 1)
                                matchLine = matchLine[1]
                                matchLine = matchLine.split("|", 3)
                                self.peers.append(matchLine[0])

class Minion:
	def __init__(self, channel, scr, nickname):
		self.pid=str(os.getpid())
		self.screen=scr
		self.channel=channel
		self.channelHash=hashlib.sha256(self.channel).hexdigest()
		self.nickname=nickname
		self.afk=False
		self.mySocket=SocketManager(self)
		self.mySocket.setDaemon(True)
		self.mySocket.start()
		self.myAfk=AfkManager(self)
		self.myAfk.setDaemon(True)
		self.myAfk.start()
                message="/add "+self.pid+"|"+nickname
                self.sendMessage(message)

	def sendMessageTo(self, outMessage, peerPid, failed=0):
		peerSock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                peerAddress = '\0'+str(peerPid)+'|'+self.channelHash
		try :
	                peerSock.sendto(outMessage, peerAddress)
		except :
			if failed >= 5:
				self.mySocket.handlerRemPeer(peerPid+"|Somebody("+peerPid+")|DeliveryError")
				return	
			failed += 1
			self.sendMessageTo(outMessage, peerPid, failed)

	def sendMessage(self, outMessage):
		self.myAfk.afkEvent.set()
                for peerPid in self.mySocket.peers:
			self.sendMessageTo(outMessage, peerPid)

