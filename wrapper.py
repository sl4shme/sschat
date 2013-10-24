#!/usr/bin/python
import sschat, sys, tools

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
	import tools
	tools = reload(tools)

channel=""
nick=""
try:
        args=sys.argv[2]
        args=args.split(" ")
        if tools.validateName(args[0]):
                channel=args[0]
        if tools.validateName(args[1]):
                nick=args[1]
except:
        pass

chat=sschat.Sschat(channel, nick)
while 1 :
        newChannel, nickname, history = chat.main()
        del chat
	moduleUpgrade()
        chat=sschat.Sschat(newChannel, nickname, history)
