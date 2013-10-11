#!/usr/bin/python
import os, re, signal

def cleanQuit(signum, frame):
	quit()

signal.signal(signal.SIGINT, cleanQuit)

print "This isn't even the pre-pre-alpha phase, please don't attack this server."

ok=False
while ok == False :
        print "Paste your one-line ssh publikey (RSA 2048 bits or DSA):"
	print "Something like ssh-rsa AAAAB3N... or ssh-dss AAAAB3N..."
        entry = str(raw_input())
        if entry[0:7] == "ssh-rsa":
                entry = entry[8:]
                key = entry[:372]
                type = 1
                if len(key) != 372:
                        print "Bad key."
                        continue
        elif entry[0:7] == "ssh-dss":
                entry = entry[8:]
                key = entry[:580]
                type = 2
                if len(key) != 580:
                        print "Bad key."
                        continue
        else:
                print "Bad key."
                continue

        if re.match("^[A-Za-z0-9+/]*$", key):
                line = "sudo /sschat/key/keycat.sh '"+str(type)+"' '"+key+"'"
                os.system(line)
                ok=True
        else:
                print "Bad key."
                continue

print "\n\nCongratulations!"
print "You can now connect to the user sschat."
print "For now, you'll most likely find people in the channel : plop "
print "\n\nPlease note that this server will not keep any trace of anything but your publikey."
print "Please remember that this service comes with NO FUCKING GUARANTEE"
print "\nEnter to quit."
raw_input()
quit()
