#!/usr/bin/python
import re, os, time, tools

def initPeers():
	peers=[]
        expr = re.compile(r'.*\|.*')
        for line in open("/proc/net/unix"):
        	match = expr.search(line)
                if match:
	                matchLine = match.group()
        	        matchLine = matchLine.split("@", 1)
                	matchLine = matchLine[1]
                	matchLine = matchLine.split("|", 3)
                	peers.append(matchLine[0])
	return peers

print "Broadcast message ?"
mess = raw_input()
if mess != "":
        tools.systemMessage(mess)

for peer in initPeers():
        print "Updating "+str(peer)
        os.kill(int(peer), int(10))
        time.sleep(1)

print "Done"

