import curses

class Scroll:
	def __init__(self, scr, content):
		self.scr = scr
		self.content=content
		self.count=len(self.content)+1
		self.first_line = 0
		curses.curs_set(0)
		self.maxyx = self.scr.getmaxyx()
		self.init_pad()
		self.key_handler()

	def init_pad(self):
		self.pad = curses.newpad(self.count, self.maxyx[1])
		for i, line in enumerate(self.content):
			self.pad.addstr(i, 0, line)
		self.refresh_pad()

	def refresh_pad(self):
		self.pad.refresh(self.first_line, 0, 0, 0, self.maxyx[0]-1, self.maxyx[1]-1)

	def key_handler(self):
		while True:
			ch = self.pad.getch()
			if ch == ord('j'):
				self.scroll_down()
				self.refresh_pad()
			elif ch == ord('k'):
				self.scroll_up()
				self.refresh_pad()
			elif ch == ord('q'):
				break

	def scroll_down(self):
		if self.maxyx[0] + self.first_line < self.count:
			self.first_line += 1

	def scroll_up(self):
		if self.first_line > 0:
			self.first_line -= 1
