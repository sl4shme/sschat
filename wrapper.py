#!/usr/bin/python
import sschat

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

chat=sschat.Sschat()
while 1 :
        newChannel, nickname, history = chat.main()
        del chat
	moduleUpgrade()
        chat=sschat.Sschat(newChannel, nickname, history)
