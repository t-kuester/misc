#!/usr/bin/env python3

""" Module for creating different kinds of 2D cellular automata, such as the 
"Game of Life", and others. Each automata has some functions for creating the 
initial state and the follow-up states, and the automata can be visualized and 
advanced in a very simple UI.

Currently, the state of each cell is determined by the number of 'alive' 
neighbors, but this could also be extended to allow more complex automata.

Tobias Kuester, 2014
"""

from random import randint
from time import time
from operator import add
from tkinter import Frame, Canvas, Button
	

class TwoDimAutomata:
	"""Abstract super-class for the actual automata, providing basic 
	initialization and stuff."""
		
	def __init__(self, x, y, prnt=False, profile=False):
		"""Initialize the different variables: size, current bitmap, and backup.
		"""
		self.X, self.Y = x, y
		self._print = prnt
		self._profile = profile
		self._last = time()
		self.bitmap = [[0 for x in range(self.X)] for y in range(self.Y)]
		self.backup = [[0 for x in range(self.X)] for y in range(self.Y)]

	def initialize(self):
		"""Create initial matrix. (to be implemented in sub-class)
		"""
		pass
	
	def next_step(self):
		"""Trigger the calcualtion of the next step for each cell.
		"""
		# swap bitmap and backup
		self.bitmap, self.backup = self.backup, self.bitmap
		for (x,y) in [ (n,m) for n in range(self.X) for m in range(self.Y)]:
			this = self.backup[y][x]
			alive = -this
			for dx in range(x-1, x+2):
				for dy in range(y-1, y+2):
					if 0 <= dx < self.X and 0 <= dy < self.Y:
						alive += self.backup[dy][dx]
			self.bitmap[y][x] = self.next_state(this, alive)
		if self._print:
			self.print_matrix(self.bitmap)
		if self._profile:
			self.print_time()

	def next_state(self, this, alive):
		"""Calculate next state for some cell. this is state of the cell itself,
		alive is number of alive cells around. (to be implemented in sub-class)
		"""
		pass

	def print_matrix(self, matrix):
		"""Print the current state of the automaton."""
		print('\n'.join(''.join(('# ' if cell else '. ') for cell in line)
								for line in matrix))
	
	def print_time(self):
		"""Print the time it took to calculate the current step."""
		t=time()
		print(t - self._last)
		self._last = t


class Copier(TwoDimAutomata):
	"""Automaton copying its content after a few iterations.
	"""

	def next_state(self, this, alive):
		return alive % 2 == 1	

	def initialize(self):
		s, e, f = 4, 5, 9
		for (x,y) in ((n,m) for n in range(s*self.X/f, e*self.X/f) 
							for m in range(s*self.Y/f, e*self.Y/f)):
			self.bitmap[y][x] = 1 if x % 3 ==0 and y % 3 == 0 else 0


class GameOfLife(TwoDimAutomata):
	"""Automaton implementing the rules of Conway's "Game of Life.
	"""
	
	def next_state(self, this, alive):
		return (this and (1 < alive < 4)) or (not this and alive == 3)
	
	def initialize(self):
		for (x,y) in [(n,m) for n in range(self.X) for m in range(self.Y)]:
			self.bitmap[y][x] = randint(0, 1)



class Application(Frame):
	"""This simple UI is used for visualizing and advancin the current state
	of the automata.
	"""
	
	def __init__(self, x, zoom, engine, master=None, profile=False):
		Frame.__init__(self, master)
		self.x = self.y = x
		self.z = zoom
		self.master.title(engine.__name__)
		self.pack()
		self.create_field()
		self.create_buttons()
		self.engine = engine(self.x, self.y, prnt=False, profile=profile)
		self.running = False
		
	def create_field(self):
		X, Y, Z = self.x, self.y, self.z
		self.canvas = Canvas(self, width=X*Z, height=Y*Z, bg="white")
		self.canvas.bind("<Button-1>", self.next_step)
		self.canvas.pack(side='bottom')
		self.ids = {}
		for (x,y) in [(n,m) for n in range(X) for m in range(Y)]:
			self.ids[(x,y)] = self.canvas.create_rectangle(x*Z, y*Z, (x+1)*Z, (y+1)*Z, 
														   outline='white', fill='white')

	def create_buttons(self):
		Button(self, text="Initialize", command=self.new_game).pack(side='left')
		Button(self, text="Next Step", command=self.next_step).pack(side='left')
		Button(self, text="Auto On/Off", command=self.autorun).pack(side='left')
		Button(self, text="Quit", command=self.quit).pack(side='right')
	
	def new_game(self):
		self.engine.initialize()
		self.update_canvas()
		
	def next_step(self, event=None):
		self.engine.next_step()
		self.update_canvas()
		if self.running:
			self.after(100, self.next_step)
		
	def autorun(self):
		self.running = not self.running
		if self.running:
			self.next_step()
		
	def update_canvas(self):
		for (x,y) in ((n,m) for n in range(self.x) for m in range(self.y)):
			if self.engine.bitmap[x][y] != self.engine.backup[x][y]:
				color = "black" if self.engine.bitmap[x][y] else "white"
				self.canvas.itemconfigure(self.ids[(x, y)], fill=color, outline=color)

# start application
if __name__ == "__main__":
	
	try:
		import psyco
		psyco.full()
	except ImportError:
		print("Failed to load psyco")

	# engine = Copier
	engine = GameOfLife
	app = Application(100, 5, engine, profile=True)
	app.new_game()
	app.mainloop()
