#!/usr/bin/python

""" Very simple "3D engine", purely for playing around with perspective and
stuff and generally for "doing it myself", not for productive use of any kind.

Tobias Kuester, 2014
"""

import math, cmath

### BASIC 3D MODEL STUFF ###

class Point:
	"""Class representing a point in space. Each point is represented by three
	coordinates: x, y, and z. Also comes with the usual magic methods and some
	helper methods.
	"""
	
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		
	def __repr__(self):
		return "Point(%.1f, %.1f, %.1f)" % self.coords()
		
	def __eq__(self, other):
		return other.__class__ == self.__class__ and self.coords() == other.coords()
				
	def __hash__(self):
		return hash(self.coords())
		
	def coords(self):
		"""Get (x, y, z) coordinates as a tuple."""
		return (self.x, self.y, self.z)
		
	def move(self, d_x, d_y, d_z):
		"""Move point by given deltas and return self."""
		self.x += d_x
		self.y += d_y
		self.z += d_z


class Camera(Point):
	"""Class representing a Camera position. The camera inherits from Point, but
	also has a heading, represented by two angles: yaw and pitch. A "roll" angle
	is not implemented, but might added in a sub-class, once this is working.
	"""

	def __init__(self, x=0, y=0, z=0, yaw=0, pitch=0, roll=0):
		Point.__init__(self, x, y, z)
		self.yaw = yaw
		self.pitch = pitch
		self.roll = roll
		
	def __repr__(self):
		return "Camera(%.1f, %.1f, %.1f, %.1f, %.1f, %.1f)" % (self.coords() + self.angles())

	def angles(self):
		"""Get yaw and pitch (and roll=0) angles as a tuple."""
		return (self.yaw, self.pitch, self.roll)
		
	def turn(self, d_yaw, d_pitch, d_roll):
		"""Turn camera by given angles and return self."""
		self.yaw = (self.yaw + d_yaw) % 360
		self.pitch = min(max(self.pitch + d_pitch, -90), 90)
		
	def move_rel(self, forward, right, up):
		"""Move relative to the camera's heading, but still in a plane, 
		i.e. using only yaw but ignoring pitch and roll."""
		d_x, d_y, d_z = rotate(right, up, forward, -self.yaw, 0, 0)
		self.move(d_x, d_y, d_z)


def normalize(point, camera):
	"""Normalize Point w.r.t. camera position, i.e. shift and rotate so as if
	the camera were at (0,0,0) and looking straight.
	"""
	x, y, z = [p - c for p, c in zip(point.coords(), camera.coords())]
	x, y, z = rotate(x, y, z, *camera.angles())
	return Point(x, y, z)

def rotate(x, y, z, yaw, pitch, roll):
	"""Rotate point by converting the angles to complex numbers and dividing.
	
	TODO order of operations is now: roll, yaw, pitch... is this the best way?
	"""
	cxy = complex(x, y)               / cmath.rect(1, math.radians(roll))
	cxz = complex(cxy.real, z)        / cmath.rect(1, math.radians(yaw))
	cyz = complex(cxy.imag, cxz.imag) / cmath.rect(1, math.radians(pitch))
	return cxz.real, cyz.real, cyz.imag
	

### SIMPLE 3D FRAME STUFF ###	

from tkinter import Frame, Canvas

SIDE = 600

class Simple3DFrame(Frame):
	"""Simple Frame class for showing objects and moving around within 3D space.
	"""

	def __init__(self, edges):
		Frame.__init__(self, master=None)
		self.master.title("Simple 3D Frame")
	
		self.bind_all("<KeyPress-space>", lambda event: self.quit())
		self.bind_all("<KeyPress>", self.shift)

		self.pack()
		self.canvas = Canvas(self, width=SIDE, height=SIDE, bg="white")
		self.canvas.pack(side="top")

		self.canvas.create_line(0, SIDE/2, SIDE, SIDE/2, fill="gray")
		self.canvas.create_line(SIDE/2, 0, SIDE/2, SIDE, fill="gray")

		self.camera = Camera()
		self.edges = edges
		self.update()
	
	def shift(self, event):
		key = event.keysym
		MOVEMENT, TILT = 0.5, 5.0
		
		d_fwd = ((key == "w") - (key == "s")) * MOVEMENT
		d_rgt = ((key == "d") - (key == "a")) * MOVEMENT
		d_up  = ((key == "r") - (key == "f")) * MOVEMENT
		
		d_pitch = ((key == "Up")   - (key == "Down"))  * TILT
		d_yaw =   ((key == "Left") - (key == "Right")) * TILT
		d_roll =  ((key == "e")    - (key == "q"))     * TILT
		
		# self.camera.move(d_rgt, d_up, d_fwd)
		self.camera.move_rel(d_fwd, d_rgt, d_up)
		self.camera.turn(d_yaw, d_pitch, d_roll)
		self.update()
	
	def update(self):
		self.canvas.delete("line", "point", "text")
		self.canvas.create_text(150, 10, text=repr(self.camera), tags="text")
		for p1, p2 in self.edges:
			p1 = normalize(p1, self.camera)
			p2 = normalize(p2, self.camera)
			# self.draw_point(p1)
			# self.draw_point(p2)
			self.draw_line(p1, p2)

	def draw_point(self, point):
		x, y, d = self.project(point)
		s = 100 / d if d else 100
		self.canvas.create_oval(x - s, y - s, x + s, y + s, tags="point")
		
	def draw_line(self, point1, point2):
		x1, y1, _ = self.project(point1)
		x2, y2, _ = self.project(point2)
		self.canvas.create_line(x1, y1, x2, y2, tags="line")

	def project(self, point):
		"""Calculate the projection "on screen" of a (normalized) point.
		Return a tuple (x-position, y-position, distance).
		
		TODO problem with lines with one end outside of screen / behind camera
		"""
		x, y, z = point.coords()
		if z > 0:
			pos_x = (1 + x / z) * SIDE/2
			pos_y = (1 - y / z) * SIDE/2
			# pos_x = (1 + x / 1+(math.sqrt(math.exp(z)))) * SIDE/2
			# pos_y = (1 - y / 1+(math.sqrt(math.exp(z)))) * SIDE/2
			dist = math.sqrt(x**2 + y**2 + z**2)
			return (pos_x, pos_y, dist)
		return 0, 0, 0

### TESTING AND TEST MODEL CREATION STUFF ###

def create_block(w, h, d, x=0, y=0, z=0, ax=0, ay=0, az=0):
	"""Helper method for creating a "block" of points, being pairwise connected
	with lines."""
	p1 = Point(0, 0, 0)
	p2 = Point(w, 0, 0)
	p3 = Point(w, 0, d)
	p4 = Point(0, 0, d)
	p5 = Point(0, h, 0)
	p6 = Point(w, h, 0)
	p7 = Point(w, h, d)
	p8 = Point(0, h, d)
	
	# shift and rotate
	for p in (p1, p2, p3, p4, p5, p6, p7, p8):
		coords = [p + c for p, c in zip(p.coords(), (x-w/2, y-h/2, z-d/2))]
		coords = rotate(*(coords + [ax, ay, az]))
		p.x, p.y, p.z = coords
	
	return [(p1, p2), (p2, p3), (p3, p4), (p4, p1),
		    (p1, p5), (p2, p6), (p3, p7), (p4, p8),
		    (p5, p6), (p6, p7), (p7, p8), (p8, p5)]

# testing
if __name__ == "__main__":

	block1 = create_block(5, 5, 5, -2, 5, 7)
	block2 = create_block(2, 5, 3, -4, 3, 1, 30, 45, 60)
	block3 = create_block(1, 1, 1, 0, 0, 0, 0, 0, 0)
	block4 = create_block(1, 1, 1, 2, 2, 2, 45, 45, 45)
	
	frame = Simple3DFrame(block1 + block2 + block3 + block4);
	frame.mainloop()
	