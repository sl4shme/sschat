#!/usr/bin/python
import os, re

print "This isn't even the pre-pre-alpha phase, please don't attack this server."
print "Provide your ssh publikey (RSA 2048 bits):"

entry = str(raw_input())

if entry[0:7] == "ssh-rsa":
        entry = entry[8:]
key = entry[:372]

if len(key) != 372:
        print "Bad key."
        quit()

if re.match("^[A-Za-z0-9+/]*$", key):
	line = "sudo /sschat/key/keycat.sh '"+key+"'"
	os.system(line)
else:
        print "Bad key."
	quit()

print "\n\n Congratulation!"
print "You can now connect with the user sschat."

