#!/usr/bin/python

import math, cmath
from operator import add, sub
from itertools import product

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


class Camera(Point):
	"""Class representing a Camera position. The camera inherits from Point,
	but also has a heading, represented by three angles.
	"""

	def __init__(self, x=0, y=0, z=0, ax=0, ay=0, az=0):
		Point.__init__(self, x, y, z)
		self.ax = ax
		self.ay = ay
		self.az = az
		
	def __repr__(self):
		return "Camera(%.1f, %.1f, %.1f, %.1f, %.1f, %.1f)" % (self.coords() + self.angles())

	def angles(self):
		"""Get (alpha, beta, gamma) angles as a tuple."""
		return (self.ax, self.ay, self.az)
		
	def move_absolute(self, dx, dy, dz, dax, day, daz):
		"""Move absolutely, directly manipulating the different degrees.
		"""
		self.x += dx
		self.y += dy
		self.z += dz
		self.ax += dax
		self.ay += day
		self.az += daz
		
	def move_quake(self, fwd, strafe, vert, yaw, pitch):
		"""Move like in Quake and other FPS; movement is always in a plane, but
		relative to heading. No roll.
		"""
		print("MOVE_QUAKE not yet implemented")
		pass
		
	def move_descent(self, fwd, strafe, vert, yaw, pitch, roll):
		"""Move like in Descent and similar games; all movement and rotation is
		relative to current heading.
		"""
		print("MOVE_descent not yet implemented")
		pass
		

def create_block(w, h, d, x=0, y=0, z=0, ax=0, ay=0, az=0):
	p1 = Point(0, 0, 0)
	p2 = Point(w, 0, 0)
	p3 = Point(w, 0, d)
	p4 = Point(0, 0, d)
	p5 = Point(0, h, 0)
	p6 = Point(w, h, 0)
	p7 = Point(w, h, d)
	p8 = Point(0, h, d)
	
	# shift and rotate
	for p in [p1, p2, p3, p4, p5, p6, p7, p8]:
		coords = map(add, p.coords(), (x-w/2., y-h/2., z-d/2.))
		coords = rotate(coords, (ax, ay, az))
		p.x, p.y, p.z = coords
	
	return [(p1, p2), (p2, p3), (p3, p4), (p4, p1),
		    (p1, p5), (p2, p6), (p3, p7), (p4, p8),
		    (p5, p6), (p6, p7), (p7, p8), (p8, p5)]


def projection(point, side):
	"""Calculate the projection "on screen" of a (normalized) point.
	Return a tuple (x-position, y-position, distance).
	"""
	x, y, z = point.coords()
	if z > 0:
		pos_x = x/z * side/2 + side/2
		pos_y = y/z * side/2 + side/2
#		pos_x = x / 1+(math.sqrt(math.exp(z))) * side/2 + side/2
#		pos_y = y / 1+(math.sqrt(math.exp(z))) * side/2 + side/2
		dist = math.sqrt(x**2 + y**2 + z**2)
		return (pos_x, pos_y, dist)
	return 0, 0, 0


def normalize(point, camera):
	"""Normalize Point w.r.t. camera position, i.e. shift and rotate so as if
	the camera were at (0,0,0) and looking straight.
	"""
	x, y, z = map(sub, point.coords(), camera.coords())
	x, y, z = rotate((x, y, z), camera.angles())
	return Point(x, y, z)


def rotate(coords, angles):
	"""Rotate point by converting the angles to complex numbers and dividing.
	"""
	x, y, z = coords
	ax, ay, az = angles
	cxy = complex(x, y)               / cmath.rect(1, az*math.pi/180)
	cxz = complex(cxy.real, z)        / cmath.rect(1, ay*math.pi/180)
	cyz = complex(cxy.imag, cxz.imag) / cmath.rect(1, ax*math.pi/180)
	return cxz.real, cyz.real, cyz.imag
	
	

from tkinter import Frame, Canvas

SIDE = 800

class ThreeDFrame(Frame):

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
		
		movement = {"mode": "ABS"}
		
		# movement
		MOVEMENT = 0.5
		if event.keysym == "d": movement["x"] = +MOVEMENT
		if event.keysym == "a": movement["x"] = -MOVEMENT
		if event.keysym == "f": movement["y"] = +MOVEMENT
		if event.keysym == "r": movement["y"] = -MOVEMENT
		if event.keysym == "w": movement["z"] = +MOVEMENT
		if event.keysym == "s": movement["z"] = -MOVEMENT
		# tilt
		TILT = 5
		if event.keysym == "Up":    movement["ax"] = +TILT
		if event.keysym == "Down":  movement["ax"] = -TILT
		if event.keysym == "Left":  movement["ay"] = +TILT
		if event.keysym == "Right": movement["ay"] = -TILT
		if event.keysym == "e":     movement["az"] = +TILT
		if event.keysym == "q":     movement["az"] = -TILT
		
		self.move(**movement)
		
		self.update()
	
	def update(self):
		self.canvas.delete("all")
		self.canvas.create_text(150, 10, text=repr(self.camera))
		for p1, p2 in self.edges:
			p1 = self.norm(p1)
			p2 = self.norm(p2)
			self.draw_point(p1)
			self.draw_point(p2)
			self.draw_line(p1, p2)

	def draw_point(self, point):
		x, y, d = projection(point, SIDE)
		s = 100 / d if d else 100
		self.canvas.create_oval(x - s, y - s, x + s, y + s)
		
	def draw_line(self, point1, point2):
		x1, y1, _ = projection(point1, SIDE)
		x2, y2, _ = projection(point2, SIDE)
		
		self.canvas.create_line(x1, y1, x2, y2)

	def norm(self, point):
		return normalize(point, self.camera)
		
	def move(self, mode, x=0, y=0, z=0, ax=0, ay=0, az=0):
		if mode == "ABS":
			self.camera.move_absolute(x, y, z, ax, ay, az)
		elif mode == "QAK":
			self.camera.move_quake(x, y, z, ax, ay)
		elif mode == "DSC":
			self.camera.move_descent(x, y, z, ax, ay, az)
		else:
			print("UNKNOWN MOVEMENT MODE: %s" % mode)


if __name__ == "__main__":

	block1 = create_block(5, 5, 5, -2, 5, 7)
	block2 = create_block(2, 5, 3, -4, 3, 1, 30, 45, 60)
	block3 = create_block(1, 1, 1, 0, 0, 0, 0, 0, 0)
	block4 = create_block(1, 1, 1, 0, 0, 0, 45, 45, 45)
	
	frame = ThreeDFrame(block1 + block2 + block3);
	frame.mainloop()
	