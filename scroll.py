import curses

class Scroll:
	def __init__(self, scr, content):
		self.scr = scr
		self.scr.clear()
		self.scr.refresh()
		self.content=content
		self.count=len(self.content)+1
		self.firstLine = 0
		curses.curs_set(0)
		self.maxyx = self.scr.getmaxyx()
		self.initPad()
		self.keyHandler()

	def initPad(self):
		self.pad = curses.newpad(self.count, self.maxyx[1])
		for i, line in enumerate(self.content):
                       self.pad.addstr(i, 0, line[0:self.maxyx[1]])
		self.refreshPad()

	def refreshPad(self):
		self.pad.refresh(self.firstLine, 0, 0, 0, self.maxyx[0]-1, self.maxyx[1]-1)

	def keyHandler(self):
		while True:
			ch = self.pad.getch()
			if ch == ord('j'):
				self.scrollDown()
				self.refreshPad()
			elif ch == ord('k'):
				self.scrollUp()
				self.refreshPad()
			elif ch == ord('q'):
				break

	def scrollDown(self):
		if self.maxyx[0] + self.firstLine < self.count:
			self.firstLine += 1

	def scrollUp(self):
		if self.firstLine > 0:
			self.firstLine -= 1
