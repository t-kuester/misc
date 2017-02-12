#!/usr/bin/env python3

"""Fractal Mountain Generator
by Tobias Kuester, <tobias.kuester@gmx.net>, 2017

This creates and draws fractal "mountains" by starting with a single
triangle and subdividing that triangle into four smaller triangles, plus
a little bit of random noise, repeatedly.

Sometimes the result looks awful, but sometimes very mountainlike, too.

TODO: Add some more elaborate controls, e.g. for size and randomization.
TODO: Make a 3D-version of this...
"""

import random
import tkinter

# factor for randomization as fraction of triangle side length
FACTOR = 0.07

# Width and Height of the Frame
WIDTH, HEIGHT = 800, 600

class Line(object):
	"""Each triangle is made up of three lines. When the triangle is
	split, the lines have to split, too, and they have to keep references
	to their respective segments, or otherwise gaps will form between
	adjacent triangles.	
	"""
	
	def __init__(self, s, t):
		"""Create Line instance. s and t are expected as complex.
		"""
		self.s = s
		self.t = t
		self.left = self.right = None
	
	def split(self):
		"""Split line into two segments. The split happens roughly in
		the middle, but with some noise applied determined by FACTOR.
		The segments are lazily created and then reused.
		"""
		if self.left is None and self.right is None:
			length = abs(self.s - self.t)
			midpoint = (self.s + self.t) / 2
			p = complex(random.gauss(midpoint.real, length * FACTOR),
	                    random.gauss(midpoint.imag, length * FACTOR))
			self.left = Line(self.s, p)
			self.right = Line(p, self.t)
		return self.left, self.right


class FractalTriangle(object):
	"""The "mountain" is made up of triangles, each being split into four
	smaller triangles and so on, by splitting the lines and connecting
	the midpoints.
	"""

	def __init__(self, ab, bc, ca):
		"""Create Triangle instance. ab,bc, and ca are expected as Lines.
		"""
		self.sides = ab, bc, ca
		self.children = None
		
	def expand(self):
		"""Expand this triangle by splitting the Lines and connecting
		the corners and the midpoints to four new, smaller triangles.
		The order of the sides of the smaller triangles is important,
		or they will end up all scramble up.
		"""
		if self.children:
			# this triangle has already been expanded -> expand children
			for child in self.children:
				child.expand()
		else:
			# split all sides (if not already split)
			ab, bc, ca = self.sides
			ab1, ab2 = ab.split()
			bc1, bc2 = bc.split()
			ca1, ca2 = ca.split()
			
			# new inner lines connecting the midpoints
			a = Line(ab1.t, ca2.s)
			b = Line(bc1.t, ab2.s)
			c = Line(ca1.t, bc2.s)
			
			# create four smaller triangles (order is important!)
			triplets = ((a, ca2, ab1), (b, ab2, bc1), (c, bc2, ca1), (c, b, a))
			self.children = [FractalTriangle(*sides) for sides in triplets]
			
	def get_leafs(self):
		"""Create and return iterator/generator of all the sub-triangles.
		"""
		if self.children:
			return (leaf for child in self.children for leaf in child.get_leafs())
		return iter([self])


class FractalMountainFrame(tkinter.Frame):
	"""Very minimalistic UI for rendering new, random fractal mountains.
	Controls: Enter -> Expand next level; r -> Reset; q -> Quit.
	"""

	def __init__(self, master=None):
		"""Create new FractalMountainFrame. The frame only contains a
		canvas for drawing the mountain, as well as a few key bindings.
		"""
		tkinter.Frame.__init__(self, master=master)
		self.master.title("Fractal Mountain")
		self.pack()
		self.mountain = None
		
		# central canvas element
		self.canvas = tkinter.Canvas(self, width=WIDTH, height=HEIGHT)
		self.canvas.pack(side="top")
		
		# key bindings
		self.bind_all("<KeyPress-Return>", lambda event: self.expand())
		self.bind_all("<KeyPress-r>", lambda event: self.reset())
		self.bind_all("<KeyPress-q>", lambda event: self.quit())
		
		# create initial mountain
		self.reset()
		
	def reset(self):
		"""Start over, create and paint new mountain (just a triangle).
		"""
		a = complex(WIDTH * .1, HEIGHT * .8)
		b = complex(WIDTH * .50, HEIGHT * .2)
		c = complex(WIDTH * .9, HEIGHT * .8)
		self.mountain = FractalTriangle(Line(a, b), Line(b, c), Line(c, a))
		self.paint_mountain()
		    
	def expand(self):
		"""Expand another level of the fractal mountain and re-draw.
		"""
		if self.mountain is not None:
			self.mountain.expand()
			self.paint_mountain()
	
	def paint_mountain(self):
		"""Draw the mountain by drawing each line of each of triangle,
		keeping track of already drawn shared lines. For the next level,
		all existing lines are deleted (their midpoint has changed).
		"""
		self.canvas.delete("all")
		if self.mountain:
			drawn = set()
			for leaf in self.mountain.get_leafs():
				for side in leaf.sides:
					if side not in drawn:
						src, tgt = side.s, side.t
						self.canvas.create_line(src.real, src.imag, tgt.real, tgt.imag)
						drawn.add(side)


# create and start Fractal Mountain Frame
if __name__ == "__main__":
	frame = FractalMountainFrame();
	frame.mainloop()
