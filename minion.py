import socket, os, re, hashlib, time, threading

class SocketManager(threading.Thread):
	def __init__(self, pid, name, hash, aff):
        	threading.Thread.__init__(self)
		self.screen=aff
		self.workspace=name
		self.hash=hash
		self.myAddress='\0sschat|'+str(pid)+'|'+self.hash
		self.initPeers()
	        self.mySock=socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.mySock.bind(self.myAddress)

	def run(self):
        	while 1:
                	incomingMessage = self.mySock.recvfrom(4096)
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
		self.screen.setTitle(self.workspace, len(self.peers))
		self.screen.printMessage(name+"("+pid+") joined.")

        def handlerRemPeer(self, mess):
		pid, name, reason = mess.split("|")
		try:
	                self.peers.remove(pid)
			self.screen.setTitle(self.workspace, len(self.peers))
			self.screen.printMessage(name+"("+pid+") leaved. (Reason:"+reason+")")
		except: #This doesn't belong here
			self.screen.printMessage("message not delivered!")

        def handlerGetMess(self, message):
		self.screen.printMessage(str(message))

        def initPeers(self):
	#je preferrerais aller les demander a un random peer
                self.peers=[]
                expr = re.compile(r'.*%s.*' % self.hash)
                for line in open("/proc/net/unix"):
                        match = expr.search(line)
                        if match:
                                matchLine = match.group()
                                matchLine = matchLine.split("@", 1)
                                matchLine = matchLine[1]
                                matchLine = matchLine.split("|", 3)
                                self.peers.append(matchLine[1])
	

class Minion:
	def __init__(self, workspaceName, aff, nickname):
		self.myPid=os.getpid()
		self.workspace=workspaceName
		self.hashWorkspace=hashlib.sha256(self.workspace).hexdigest()
		self.nickname=nickname
		self.mySocket=SocketManager(self.myPid,self.workspace, self.hashWorkspace, aff)
		self.mySocket.setDaemon(True)
		self.mySocket.start()
                message="/add "+str(self.myPid)+"|"+nickname
                self.sendMessage(message)

	def sendMessageTo(self, outMessage, peerPid, failed=0):
		peerSock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                peerAddress = '\0sschat|'+str(peerPid)+'|'+self.hashWorkspace
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
