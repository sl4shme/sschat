#!/usr/bin/python
import curses, curses.textpad, time, collections

class Screen:
	def __init__(self, resize=0):
		self.resize=resize
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
		if resize == 0:
			self.timestamp=True
			self.doHistory=True
			self.historyLen=20
			self.history=collections.deque(maxlen=self.historyLen)

	def printMessage(self, message):
		if self.timestamp == True:
			message=time.strftime("[%H:%M] ")+message
		if self.doHistory == True:
			self.history.append(message)
                self.conversWindow.addstr(message+"\n")
                self.conversWindow.refresh()

	def getInput(self):
		while 1:
			inputMessage = self.inputBox.edit()
			if self.resize == 1:
				self.resize=0
				continue
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

	def handlerResize(self, signum="", frame=""):
		curses.endwin()
		self.__init__(1)
		curses.ungetch(curses.ascii.NL)
		oldH = self.doHistory
		oldT = self.timestamp
		self.doHistory = False
		self.timestamp = False
		for histLine in self.history:
			self.printMessage(histLine)
		self.doHistory = oldH
		self.timestamp = oldT

