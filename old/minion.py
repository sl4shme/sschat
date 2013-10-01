#!/usr/bin/python
import signal, socket, os, re, hashlib, time, posix_ipc, random
    ##
#   ####
##########  Le pb viens des kill qui baisent les sleep et les wait
#   ####
    ##
class Minion:
#A minion worker

	def __init__(self):
		self.myPid= os.getpid()

	def __str__(self):
	#Method called when print instance is executed 
        	return "I'm a minion in workspace %s with pid %s" % (self.workspace,self.myPid)

	def init(self, workspaceName):
	#We need a different method than __init__ cause you might want to instanciate minion before giving him a workspace
		startSemaphore=posix_ipc.Semaphore("/stfare", posix_ipc.O_CREAT, 0600, 1)
		startSemaphore.acquire()
		self.workspace=workspaceName
		self.hashWorkspace=hashlib.sha256(self.workspace).hexdigest()
		self.chanSemaphore=posix_ipc.Semaphore("/chffaelle", posix_ipc.O_CREAT, 0600, 1)
		self.initPeers()
		self.initSocket()
		self.initSignals()
		startSemaphore.release()

	def initSocket(self):
	#Personnal socket initialisation
                self.myAddress = '\0sschat|'+str(self.myPid)+'|'+self.hashWorkspace
                self.mySock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                self.mySock.bind(self.myAddress)

	def initSemaphore(self):
	#Personnal semaphore initialisation
	#Doit etre bloquant pendant l'initialisation
		self.mySemaphore=posix_ipc.Semaphore("/sschat_"+str(self.myPid), posix_ipc.O_CREAT, 0600, 1)

	def initPeers(self):
	#Getting the list of all peers in our channel
		self.peers=[]
		expr = re.compile(r'.*%s.*' % self.hashWorkspace)
		for line in open("/proc/net/unix"):
		        match = expr.search(line)
			if match:
				matchLine = match.group()
		        	matchLine = matchLine.split("@", 1)
        			matchLine = matchLine[1]
        			matchLine = matchLine.split("|", 3)
        			self.peers.append(matchLine[1])
		#send hi to all other minions
		message="/add "+str(self.myPid)
		self.sendMessage(message)

        def initSignals(self):
	#Init for signals handlers
                signal.signal(signal.SIGUSR1, self.handlerGetMessage)
                signal.signal(signal.SIGINT, self.handlerQuitKeyboard)

	def sendMessage(self, outMessage):
	#Send Message to all minion in workspace
		try :
			self.chanSemaphore.acquire()
		except :
			self.sendMessage(outMessage)
			time.sleep(1)
		for peerPid in self.peers:
                        peerSock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                        peerAddress = '\0sschat|'+str(peerPid)+'|'+self.hashWorkspace
         	        os.kill(int(peerPid),10)
	                peerSock.sendto(outMessage, peerAddress)
		self.chanSemaphore.release()

	def handlerQuitKeyboard(self, signum, frame):
	#Called when Ctrl+C
		self.cleanQuit()
		quit()

	def handlerGetMessage(self, signum, frame):
	#Called when a message needs to be received on personal socket
		incomingMessage = self.mySock.recvfrom(4096)
                incomingMessage = incomingMessage[0]
                if incomingMessage[0] == "/":
		#If Minion message "/"
                        if incomingMessage[1:4] == "add":
               			self.handlerAddMinion(incomingMessage[5:])
                        if incomingMessage[1:4] == "rem":
               			self.handlerRemMinion(incomingMessage[5:])
                        if incomingMessage[1:4] == "msg":
              			self.handlerMessage(incomingMessage[5:])

	def handlerAddMinion(self, pid):
	#Called when a minion registers in the workspace
		self.peers.append(pid)

	def handlerRemMinion(self, pid):
	#Called when a minion leaves the workspace
		self.peers.remove(pid)

	def handlerMessage(self, message):
	#Need to be redefine in instanciation
		print message
	
	def cleanQuit(self):
	#Clean exit
		#send bye to all other minions
		message= "/rem "+str(self.myPid)
                self.sendMessage(message)
		
		
	def main(self):
	#Work to do for the minion
		num = 0
		while 1:
			time.sleep(5)
			self.sendMessage("/msg plop"+str(num))
			time.sleep(5)
			num += 1

#jaune = Minion()
#jaune.init("plop")
#jaune.main()
