#!/usr/bin/env python3

"""Fractal Mountain Generator
by Tobias Kuester, <tobias.kuester@gmx.net>, 2017

"""

import random, cmath, math
import tkinter


def randomize(point, magnitude):
	return complex(random.gauss(point.real, magnitude),
	               random.gauss(point.imag, magnitude))


class FractalMountain(object):

	def __init__(self, f, a, b, c):
		self.points = a, b, c
		self.factor = f
		self.children = []
		
	def expand(self):
		if self.children:
			for child in self.children:
				child.expand()
		else:
			a, b, c = self.points
			ab = (a + b) / 2
			bc = (b + c) / 2
			ca = (c + a) / 2
			factor = self.factor * (abs(a-b) + abs(b-c) + abs(c-a)) / 3
			ab, bc, ca = (randomize(x, factor) for x in (ab, bc, ca))
			
			for points in ((a, ab, ca), (b, bc, ab), (c, bc, ca), (ab, bc, ca)):
				self.children.append(FractalMountain(self.factor, *points))
				
	def get_leafs(self):
		if self.children:
			return [leaf for child in self.children for leaf in child.get_leafs()]
		return [self]


# Width and Height of the Frame
WIDTH, HEIGHT = 800, 600

class FractalMountainFrame(tkinter.Frame):

	def __init__(self, master=None):
		tkinter.Frame.__init__(self, master=master)
		self.master.title("Fractal Mountain")
		self.pack()
		self.mountain = None
		
		# central canvas element
		self.canvas = tkinter.Canvas(self, width=WIDTH, height=HEIGHT)
		self.canvas.pack(side="top")
		
		self.bind_all("<KeyPress-Escape>", lambda event: self.reset())
		self.bind_all("<KeyPress-Return>", lambda event: self.expand())
		self.bind_all("<KeyPress-q>", lambda event: self.quit())
		
		self.reset()
		
	def reset(self):
		a = complex(WIDTH * .25, HEIGHT * .75)
		b = complex(WIDTH * .50, HEIGHT * .25)
		c = complex(WIDTH * .75, HEIGHT * .75)
		self.mountain = FractalMountain(0.05, a, b, c)
		self.paint_mountain()
		    
	def expand(self):
		if self.mountain is not None:
			self.mountain.expand()
			self.paint_mountain()
		
	def paint_mountain(self):
		self.canvas.delete("all")
		if self.mountain:
			for leaf in self.mountain.get_leafs():
				a, b, c = leaf.points
				points = [p for x in (a, b, c, a) for p in (x.real, x.imag)]
				self.canvas.create_line(points)
				

# create and start FracTreeFrame
if __name__ == "__main__":
	frame = FractalMountainFrame();
	frame.mainloop()
	
