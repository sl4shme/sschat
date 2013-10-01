#!/usr/bin/python
import curses, curses.textpad

class Screen:
	def __init__(self):
		self.mainWindow=curses.initscr()
		self.ySize, self.xSize = self.mainWindow.getmaxyx()
		self.titleWindow = curses.newwin(1, self.xSize, 0, 0)
		self.conversWindow = curses.newwin((self.ySize - 2), self.xSize, 1, 0)
                self.inputWindow = curses.newwin(1, (self.xSize - 1), (self.ySize - 1), 1)
		self.inputBox = curses.textpad.Textbox(self.inputWindow)
		self.inputBox.stripspaces=1
		self.conversWindow.scrollok(True)
		self.mainWindow.addch((self.ySize - 1),0,">")
		curses.noecho()
		self.mainWindow.refresh()
	
	def printMessage(self, message):
                self.conversWindow.addstr(message+"\n")
                self.conversWindow.refresh()

	def getInput(self):
		while 1:
			inputMessage = self.inputBox.edit()
			if inputMessage != "":
				self.inputWindow.clear()
				self.inputWindow.refresh()
				return inputMessage[:-1]
	
	def stopScreen(self):
		curses.endwin()
	
        def setTitle(self, channel, people):
                self.titleWindow.clear()
                self.titleWindow.addstr("Channel : "+channel+" / People : "+str(people))
                self.titleWindow.refresh()

	def clearConvers(self):
		self.conversWindow.clear()
		self.conversWindow.refresh()
