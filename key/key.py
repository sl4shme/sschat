#!/usr/bin/python
import os, re, signal, text

def cleanQuit(signum="", frame=""):
        print "\nBye !"
        quit()

signal.signal(signal.SIGINT, cleanQuit)

print "This is an alpha version, please don't attack this server."
ok=False
while ok == False :
        text.printer(text.ask)
        entry = str(raw_input())
        if entry == "help":
                os=raw_input("(l)inux / (m)ac / (a)ndroid / (w)indows ?")
                if os == "l":
                        text.printer(text.linuxHelp)
                elif os == "m":
                        text.printer(text.linuxHelp)
                elif os == "w":
                        text.printer(text.windowsHelp)
                elif os == "a":
                        text.printer(text.androidHelp)
		else:
			continue
                raw_input("Ctrl+c to quit / Enter to go back")
                continue

        if entry[0:7] == "ssh-rsa":
                entry = entry[8:]
                key = entry[:372]
                type = 1
                if len(key) != 372:
                        print "Bad key.(Bad lenght)"
                        continue

        elif entry[0:7] == "ssh-dss":
                entry = entry[8:]
                key = entry[:580]
                type = 2
                if len(key) != 580:
                        print "Bad key.(Bad lenght)"
                        continue

        else:
                print "Bad key. (Bad begining)"
                continue

        if re.match("^[A-Za-z0-9+=/]*$", key):
                line = "sudo /sschat/key/keycat.sh '"+str(type)+"' '"+key+"'"
                os.system(line)
                ok=True
        else:
                print "Bad key.(Bad characters)"
                continue

text.printer(text.congrats)
raw_input()
cleanQuit()
