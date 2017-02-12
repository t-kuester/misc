#!/usr/bin/env python3

"""Fractal Mountain Generator
by Tobias Kuester, <tobias.kuester@gmx.net>, 2017
"""

import random, cmath, math
import tkinter

# factor for randomization as fraction of triangle side length
FACTOR = 0.075

class Line(object):
	
	def __init__(self, s, t, left=None, right=None):
		self.s = s
		self.t = t
		self.left = left
		self.right = right
	
	def __repr__(self):
		return "Line(%r, %r, %r, %r)" % (self.s, self.t, self.left, self.right)
		
	def split(self):
		if self.left is None and self.right is None:
			length = abs(self.s - self.t)
			midpoint = (self.s + self.t) / 2
			p = complex(random.gauss(midpoint.real, length * FACTOR),
	                    random.gauss(midpoint.imag, length * FACTOR))
			self.left = Line(self.s, p)
			self.right = Line(p, self.t)
		return self.left, self.right


class FractalTriangle(object):

	def __init__(self, ab, bc, ca, children=None):
		self.sides = ab, bc, ca
		self.children = children
		
	def __repr__(self):
		s1, s2, s3 = self.sides
		return "FractalTriangle(%r, %r, %r, %r)" % (s1, s2, s3, self.children)
		
	def expand(self):
		if self.children:
			for child in self.children:
				child.expand()
		else:
			ab, bc, ca = self.sides
			ab1, ab2 = ab.split()
			bc1, bc2 = bc.split()
			ca1, ca2 = ca.split()
			
			a = Line(ab1.t, ca2.s)
			b = Line(bc1.t, ab2.s)
			c = Line(ca1.t, bc2.s)
			
			triplets = ((a, ca2, ab1), (b, ab2, bc1), (c, bc2, ca1), (c, b, a))
			self.children = [FractalTriangle(*sides) for sides in triplets]
			
	def get_leafs(self):
		if self.children:
			return (leaf for child in self.children for leaf in child.get_leafs())
		return [self]


# Width and Height of the Frame
WIDTH, HEIGHT = 800, 600

import time

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
		a = complex(WIDTH * .1, HEIGHT * .8)
		b = complex(WIDTH * .50, HEIGHT * .2)
		c = complex(WIDTH * .9, HEIGHT * .8)
		self.mountain = FractalTriangle(Line(a, b), Line(b, c), Line(c, a))
		self.paint_mountain()
		    
	def expand(self):
		if self.mountain is not None:
			self.mountain.expand()
			self.paint_mountain()
	
	def paint_mountain(self):
		self.canvas.delete("all")
		if self.mountain:
			for leaf in self.mountain.get_leafs():
				for side in leaf.sides:
					self.canvas.create_line(side.s.real, side.s.imag, side.t.real, side.t.imag)

# create and start FracTreeFrame
if __name__ == "__main__":
	frame = FractalMountainFrame();
	frame.mainloop()
