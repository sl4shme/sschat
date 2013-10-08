import socket, os, re, hashlib, threading

class SocketManager(threading.Thread):
	def __init__(self, pid, channel, hash, scr):
        	threading.Thread.__init__(self)
		self.screen=scr
		self.channel=channel
		self.channelHash=hash
		self.address='\0'+pid+'|'+self.channelHash
		self.initPeers()
	        self.sock=socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.sock.bind(self.address)

	def run(self):
        	while 1:
                	incomingMessage = self.sock.recvfrom(4096)
                	self.handlerGetComm(incomingMessage[0])

	def handlerGetComm(self, incMess):
		if incMess[0] == "/":
                        if incMess[1:4] == "add":
                                self.handlerAddPeer(incMess[5:])
                        if incMess[1:4] == "rem":
                                self.handlerRemPeer(incMess[5:])
                        if incMess[1:4] == "msg":
                                self.handlerGetMess(incMess[5:])

        def handlerAddPeer(self, mess):
		pid, name = mess.split("|")
                self.peers.append(pid)
		self.screen.setTitle(self.channel, len(self.peers))
		self.screen.printMessage(name+"("+pid+") joined.")

        def handlerRemPeer(self, mess):
		pid, name, reason = mess.split("|")
		try:
	                self.peers.remove(pid)
			self.screen.setTitle(self.channel, len(self.peers))
			self.screen.printMessage(name+"("+pid+") leaved. (Reason:"+reason+")")
		except:
			pass

        def handlerGetMess(self, message):
		self.screen.printMessage(str(message))

        def initPeers(self):
                self.peers=[]
                expr = re.compile(r'.*%s.*' % self.channelHash)
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
		self.channel=channel
		self.channelHash=hashlib.sha256(self.channel).hexdigest()
		self.nickname=nickname
		self.mySocket=SocketManager(self.pid,self.channel, self.channelHash, scr)
		self.mySocket.setDaemon(True)
		self.mySocket.start()
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
                for peerPid in self.mySocket.peers:
			self.sendMessageTo(outMessage, peerPid)
