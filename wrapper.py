#!/usr/bin/python
import sschat, sys, re

def moduleUpgrade():
	import crypt
	crypt = reload(crypt)
	import minion
	minion = reload(minion)
	import screen
	screen = reload(screen)
	import scroll
	scroll = reload(scroll)
	import sschat
	sschat = reload(sschat)
	import text
	text = reload(text)

channel=""
nick=""
try:
        args=sys.argv[2]
        args=args.split(" ")
        if args[0] and re.match("^[A-Za-z]*$", args[0]) and len(args[0]) <= 12:
                channel=args[0]
        if args[1] and re.match("^[A-Za-z]*$", args[1]) and len(args[1]) <= 12:
                nick=args[1]
except:
        pass

chat=sschat.Sschat(channel, nick)
while 1 :
        newChannel, nickname, history = chat.main()
        del chat
	moduleUpgrade()
        chat=sschat.Sschat(newChannel, nickname, history)
