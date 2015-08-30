#!/usr/bin/python

"""Fractal Tree Generator
by Tobias Kuester, <tobias.kuester@gmx.net>, 2011

A fractal tree is a very simple fractal structure which, with some randomness,
can look remarkably like a real tree.  Using different values for the number of
branchings, the allowed angles and the thickness of the stem, the resulting tree
can have characteristics similar to a wide range of trees and bushes.
"""

import random, cmath, math
from Tkinter import Frame, Canvas, Scale, Button, Checkbutton, IntVar

class FracTree(object):
	"""Fractal Tree Class.
	
	This class provides the logic for generating and forking the actual tree.
	"""

	def __init__(self, point=0+0j, vector=0+100j, slimness=3.0):
		"""Create new Frac Tree Object.  Point is the origin of the tree, and
		vector its direction and length.  Slimness is the thickness of the stem.
		"""
		self.p = point
		self.v = vector
		self.s = slimness
		self.b = abs(vector) / slimness
		self.left = None
		self.right = None

	def spawn(self, arc=45):
		"""Spawn left and right branches from this tree.  Arc is the angle of
		the left tree, with arc=45 being in the center.
		"""
		r = math.radians(arc)
		al = cmath.phase(self.v) + r
		ar = cmath.phase(self.v) - (cmath.pi/2 - r)
		vl = cmath.rect(abs(self.v) * math.cos(r), al)
		vr = cmath.rect(abs(self.v) * math.sin(r), ar)
		self.left  = FracTree(self.p + self.v, vl, self.s)
		self.right = FracTree(self.p + self.v, vr, self.s)
		return (self.left, self.right)
		
	def expand_random(self, levels, a_from, a_to, alternate=False, p_exp=1.0):
		"""Recursively expand the tree by given number of levels, using random
		angles in the given interval of degrees. p_exp is the probability with
		which to generate another generation (optional).  With alternate, the
		angles are swapped with each level of branching.
		"""
		if levels == 0 or random.random() > p_exp or a_from > a_to:
			return
		if self.left == None and self.right == None:
			a = random.randint(a_from, a_to)
			self.spawn(a)
			levels -= 1
		if alternate:
			a_from, a_to = 90 - a_to, 90 - a_from
		self.left.expand_random(levels, a_from, a_to, alternate, p_exp)
		self.right.expand_random(levels, a_from, a_to, alternate, p_exp)
		

# Width and Height of the Frame
WIDTH, HEIGHT = 800, 600

class FracTreeFrame(Frame):
	"""Fractal Tree Frame Class.
	
	Frames of this type can be used for configuring, creating and enjoying
	fractal trees. The frame provides a large number of controls for configuring
	every parameter of the tree and a button for quickly generating new trees.
	"""

	def __init__(self, master=None):
		"""Create instance of Fractal Tree Frame.
		"""
		Frame.__init__(self, master=master)
		self.master.title("Fractal Tree")
		self.pack()
		self.tree = None
		
		# central canvas element
		self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
		self.canvas.pack(side="top")
		
		# sliders for size, levels and angle
		self.size   = self._create_scale("Size", 10, 150, 100)
		self.slim   = self._create_scale("Slimness", 2, 15, 6)
		self.levels = self._create_scale("Levels", 1, 15, 8)
		self.a_from = self._create_scale("Angle from", 0, 90, 30)
		self.a_to   = self._create_scale("Angle to", 0, 90, 60)
		
		# button for generating a new tree and expanding existing tree
		Button(self, text="Generate Tree", command=self.new_tree).pack(side="right")
		Button(self, text="Expand", command=self.expand).pack(side="right")

		# checkbox: draw leafs
		self.leafs     = self._create_checkbox("Draw Leafs?", True)
		self.alternate = self._create_checkbox("Alternate?", False)
	
	def new_tree(self):
		"""Create and paint new Fractal Tree based on given parameters.
		"""
		self.tree = FracTree(complex(WIDTH/2, HEIGHT),
		                complex(0, - self.size.get()), self.slim.get() / 2.)
		    
		self.expand(self.levels.get())
		
	def expand(self, levels=1):
		"""Expand exiting tree with one more level and given parameters
		"""
		if self.tree != None:
			self.tree.expand_random(levels, self.a_from.get(), self.a_to.get(),
			                                     alternate=self.alternate.get())
			self.canvas.delete("all")
			self.paint_tree(self.tree, self.leafs.get())
		
	def paint_tree(self, ft, draw_leafs):
		"""Recursively paint the given tree to the canvas.
		"""
		c_trunk, c_leafs = "#483F00", "#3C631B"
		if ft != None:
			x1, y1 = ft.p.real, ft.p.imag
			x2, y2 = (ft.p + ft.v).real, (ft.p + ft.v).imag
			if draw_leafs and not (ft.left and ft.right):
				b = ft.b * 4
				self.canvas.create_oval(x2-b, y2-b, x2+b, y2+b,
				                                  outline=c_leafs, fill=c_leafs)
			else:
				self.canvas.create_line(x1, y1, x2, y2, width=ft.b, fill=c_trunk)
				self.paint_tree(ft.left, draw_leafs)
				self.paint_tree(ft.right, draw_leafs)

	# Helper Method for creating a Scale with given parameters
	def _create_scale(self, text, frm, to, val):
		scale = Scale(self, label=text, from_=frm, to=to, orient="horizontal")
		scale.pack(side="left")
		scale.set(val)
		return scale
		
	# Helper Method for creating a Checkbox
	def _create_checkbox(self, text, value):
		var = IntVar()
		var.set(1 if value else 0)
		Checkbutton(self, text=text, variable=var).pack(side="top")
		return var


# create and start FracTreeFrame
if __name__ == "__main__":
	frame = FracTreeFrame();
	frame.mainloop()
	
