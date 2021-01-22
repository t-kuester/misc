import math, cmath


# PENDULUM MODEL

GRAVITY  = 10.0
FRICTION = 0.01

class Pendulum:
	
	def __init__(self, x, y, length, mass, angle, speed):
		self.x = x
		self.y = y
		self.length = length
		self.mass = mass
		self.angle = angle
		self.speed = speed
		self.rad = math.sqrt(self.mass)
	
	def __repr__(self):
		return f"Pendulum({self.x}, {self.y}, {self.length}, {self.mass}, {self.angle}, {self.speed})"
	
	def update(self):
		pass
		# accelerate "downwards" by gravity, amount of gravity as by sin/cos of angle
		# update angular speed
		# update angle, i.e. position
		
		# TODO looks good already, frequency stays the same even with friction
		# but have to take length and mass into account somehow, too
		# or is length implicitly handled by the way it accelerates downwards?
		# nope, short and long pendulum have same frequency, short should be faster
		acc = -GRAVITY * math.sin(math.radians(self.angle))
		# seems a little arbitrary... but entirely correct according to Wikipedia
		acc *= 1 / self.length
		self.speed += acc
		self.angle += self.speed
		# ~self.speed *= 1 - FRICTION
		
		# so why is it not correct w.r.t. different angles? just too large steps?
		
		# ~self.angle = (self.angle + 1) % 360
		# ~print(self)
		
	def get_pos(self):
		a = math.radians(self.angle)
		px = self.x + math.sin(a) * self.length
		py = self.y + math.cos(a) * self.length
		return (px, py)


# SIMPLE UI FOR TESTING / VISUALIZATION

from tkinter import Frame, Canvas

SIDE = 600

class PendulumFrame(Frame):

	def __init__(self, *pendulums):
		Frame.__init__(self, master=None)
		self.master.title("Pendulum Frame")

		self.pendulums = pendulums
	
		self.pack()
		self.canvas = Canvas(self, width=SIDE, height=SIDE, bg="white")
		self.canvas.pack(side="top")

		self.update()
	
	def update(self):
		self.canvas.delete("all")
		
		for p in self.pendulums:
			p.update()
			px, py = p.get_pos()
			self.canvas.create_oval(px-p.rad, py-p.rad, px+p.rad, py+p.rad)
			self.canvas.create_line(p.x, p.y, px, py)
		
		self.after(10, self.update)
		
# testing
if __name__ == "__main__":
	p1 = Pendulum(300, 100, 200, 100, 60, 0)
	p2 = Pendulum(300, 100, 100, 100, 60, 0)
	frame = PendulumFrame(p1, p2);
	frame.mainloop()
