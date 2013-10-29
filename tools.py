import re, hashlib, socket

def sendOnlyOneToChan(chann, nick, mess):
        mess="/msg "+nick+" : "+mess
        channelHash=hashlib.sha256(chann).hexdigest()
        peers=[]
        expr = re.compile(r'.*%s.*' % channelHash)
        for line in open("/proc/net/unix"):
                match = expr.search(line)
                if match:
                        matchLine = match.group()
                        matchLine = matchLine.split("@", 1)
                        matchLine = matchLine[1]
                        matchLine = matchLine.split("|", 3)
                        peers.append(matchLine[0])
        for peerPid in peers:
                peerSock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                peerAddress = '\0'+str(peerPid)+'|'+channelHash
                peerSock.sendto(mess, peerAddress)

def systemMessage(mess):
        mess="/msg SYSTEM MESSAGE : "+mess
        peers=[]
        expr = re.compile(r'.*\|.*')
        for line in open("/proc/net/unix"):
                match = expr.search(line)
                if match:
                        matchLine = match.group()
                        matchLine = matchLine.split("@", 1)
                        matchLine = matchLine[1]
                        peers.append(matchLine)
        for peerPid in peers:
                peerSock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                peerAddress = '\0'+str(peerPid)
                peerSock.sendto(mess, peerAddress)

def validateName(input):
	if re.match("^\d*[a-zA-Z][a-zA-Z\d]*$", input) and len(input) <= 12:
        	return True
	else :
		return False

def getSpawnLock():
        while 1:
                if "OK" in open("lock"):
                        f = open("lock", 'w')
                        f.write("KO")
                        f.close()
                        return

def releaseSpawnLock():
        f = open("lock", 'w')
        f.write("OK")
        f.close()

