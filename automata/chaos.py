import tkinter as tk
import math
from collections import namedtuple

R = 5
F = 4.669

def f(r, x=0.5):
	while True:
		yield round(x, R)
		x = r * x * (1 - x)

def g(gen, k=10000):
	d = {}
	a = []
	for i, x in enumerate(gen):
		if i >= k:
			return a
		if x in d:
			return a[d[x]:]
		d[x] = i
		a.append(x)


Pos = namedtuple("Pos", "x y")

W = H = 500

class FractalZoom(tk.Frame):
	# TODO add stack and move up on right-click
	# TODO conveniene methods for position-conversion
	# TODO allow drawing frame in all directions
	
	def __init__(self, root):
		self.start = None
		self.end = None
		self.pos = Pos(0.0, 0.0)
		self.size = Pos(4.0, 1.0)
		
		self.canvas = tk.Canvas(root, width=W, height=H)
		self.canvas.pack()
		
		self.canvas.bind("<ButtonPress>", self.press)
		self.canvas.bind("<Motion>", self.move)
		self.canvas.bind("<ButtonRelease>", self.release)
		self.draw()
		
	def press(self, event):
		self.start = self.end = Pos(event.x, event.y)
		
	def move(self, event):
		if self.start is not None:
			p1 = self.start
			p2 = self.end = Pos(event.x, event.y)
			self.canvas.delete("zoom")
			self.canvas.create_rectangle(p1.x, p1.y, p2.x, p2.y, tags="zoom")
	
	def release(self, event):
		p1, p2 = self.start, self.end
		p, d = self.pos, self.size
		self.pos = Pos(p.x + p1.x / W * d.x, p.y + p1.y / H * d.y)
		self.size = Pos(d.x * (p2.x - p1.x) / W, d.y * (p2.y - p1.y) / H)
		self.draw()
		self.start = self.end = None

class BifurcationFrame(FractalZoom):

	def draw(self):
		(X, Y), (DX, DY) = self.pos, self.size
		self.canvas.delete("all")
		r = X
		while r <= X + DX:
			res = g(f(r))
			print(r, len(res))
			for x in res:
				x, y = W * (r - X) / DX, H * (x - Y) / DY
				self.canvas.create_oval(x, y, x+1, y+1)
			r += DX / 500


def m(cx, cy, max_square=4, max_iter=100):
	z, c, i = 0+0j, complex(cx, cy), 0
	while abs(z) < max_square and i < max_iter:
		z = z**2 + c
		i += 1
	return max_iter - i
	
		
class MandelbrotFrame(FractalZoom):
	
	def __init__(self, master):
		FractalZoom.__init__(self, master)
		self.pos = Pos(-1.0, -1.0)
		self.size = Pos(2.0, 2.0)
	
	def draw(self):
		(X, Y), (DX, DY) = self.pos, self.size
		self.canvas.delete("all")
		
		cy = Y
		while cy < Y + DY:
			cx = X
			while cx < X + DX:
				z = m(cx, cy)
				self.canvas.create_rectangle(cx, cy, cx+1, cy+1)
				cx += DX / 500
			cy += DY / 500
			print(cx, cy, z)
		

def plot_tkinter():
	root = tk.Tk()
	# ~BifurcationFrame(root)
	MandelbrotFrame(root)
	root.mainloop()
	
	
def plot_pyplot():
	from matplotlib import pyplot as plt

	pts = []
	r = 0
	while r <= 4:
		res = g(f(r))
		print(r, len(res))
		pts += ((r, x) for x in res)
		r += 0.001

	x, y = zip(*pts)
	plt.plot(x, y, "b.", linewidth=0, markersize=1)
	plt.show()


if __name__ == "__main__":
	# ~plot_pyplot()
	plot_tkinter()
