#!/usr/bin/python
import re, os, time

def initPeers():
	peers=[]
#        expr = re.compile(r'.*9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08.*')
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

for peer in initPeers():
	os.kill(int(peer), int(10))
	time.sleep(1)
