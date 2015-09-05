#!/usr/bin/python

""" This is a simple UI for drawing different kinds of fractal shapes, like
the Koch Snowflake and some others. The fractals are given using some basic
measurements and kind of a recursive formula, similar to / inspired by
Lindenmayer System (https://en.wikipedia.org/wiki/L-system).

Tobias Kuester, 2014
"""

from tkinter import Frame, Canvas, Listbox, StringVar, Label, Button, Entry, Text
from math import sqrt, pi, sin, cos

# Width and Height of the Frame
WIDTH, HEIGHT = 600, 600

# predefined fractals
FRACTALS = {
	"Snowflake"      : ( 3, 200, 60, 3, "F", {"F": "RF+++R--" * 6, "R": "RRR"}),
	"Koch Snowflake" : ( 4, 400, 60, 3, "F--F--F--", {"F": "F+F--F+F"}),
	"Dragon Curve"   : (10, 500, 45, sqrt(2), "R", {"R": "+R--L+", "L": "-R++L-"}),
	"Levy's C-Curve" : ( 8, 400, 45, sqrt(2), "F", {"F": "+F--F+"}),
	"Triangle"       : ( 6, 400, 60, 2, "R", {"R": "+L-R-L+", "L": "-R+L+R-"}),
	"Sierpinski Triangle" : ( 4, 500, 60, 2, "F++F++F++", {"F": "F++F++F++ff", "f": "ff"}),
	"Blocks-Blocks"  : ( 3, 400, 90, 3, "F+F+F+F", {"F": "F+F-F-F+F"}),
	"Carpet"         : ( 3, 400, 90, 3, "F", {"F": "F+F-F-FF-F-F-fF", "f": "fff"}),
	"Zacken-Stern"   : ( 3, 300, 36, (sqrt(5)+1)**2/4, "F+++" * 10, {"F": "F++F----F++F"}),
	"Hilbert-Kurve"  : ( 3, 100, 90, 2, "X", {"X": "-YF+XFX+FY-", "Y": "+XF-YFY-FX+", "F": "F"}),
	"Gosper-Kurve"   : ( 4, 400, 60, sqrt(7), "R", {"R": "R+L++L-R--RR-L+", "L": "-R+LL++L+R--R-L"}),
	"Peano-Kurve 1"  : ( 4, 400, 90, 3, "F", {"F": "F+F-F-F-F+F+F+F-F"}),
	"Peano-Kurve 2"  : ( 2, 400, 90, 5, "X", {"X": "XfYfX+f+YfXfY-f-XfYfX", "Y": "YfXfY-f-XfYfX+f+YfXfY", "f": "f"}),
}

class FracFrame(Frame):
	"""Simple Frame for configuring and drawing fractals. Similar to fractals2.py
	but drawing with Tkinter Canvas instead of turtle and with controls for quickly
	adjusting the parameters of the fractal. Much quicker to try new fractals than
	using turtle, but not as accurate w.r.t. scaling the fractal.
	"""

	def __init__(self, master=None):
		"""Create new Fractal Frame instance.
		"""
		Frame.__init__(self, master=master)
		self.master.title("Fractal GUI")
		self.pack()
		self.x = 100
		self.y = 300
		self.a = 0
		
		# main canvas element
		self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
		self.canvas.pack(side="left")
		
		# configuration widgets
		def create_entry(name, value=""):
			var = StringVar()
			var.set(value)
			Label(self, text=name).pack(side='top')
			Entry(self, textvariable=var, width=18).pack(side='top')
			return var

		# liste
		self.listbox = Listbox(self, height=5, bg='white', activestyle='dotbox')
		for i, f in enumerate(FRACTALS):
			self.listbox.insert(i, f)
		self.listbox.bind('<ButtonRelease-1>', self.clicked)
		self.listbox.pack(side='top')
	
		self.xVar   = create_entry("X", "200")
		self.yVar   = create_entry("Y", "200")
		self.lvlVar = create_entry("Levels", "4")
		self.lenVar = create_entry("Size", "400")
		self.angVar = create_entry("Angle", "60")
		self.relVar = create_entry("Relation", "3")
		self.startVar = create_entry("Start Rule", "F--F--F--")
		
		# rules
		Label(self, text='Rules').pack(side='top')
		self.rules = Text(self, width=20, height=10)
		self.rules.pack(side='top')
		self.rules.insert("0.0", "F:F+F--F+F")

		# button for drawing the fractal
		Button(self, text="Draw Fractal", command=self.draw_new_fractal).pack(side='bottom')
		self.bind_all("<Control-KeyPress-Return>", lambda event: self.draw_new_fractal())
		self.bind_all("<Control-KeyPress-q>", lambda event: self.quit())

	def clicked(self, event):
		"""Push values for the selected fractal into the entry fields.
		"""
		i = self.listbox.curselection()
		if i:
			fractal = FRACTALS[self.listbox.get(i)]
			print(fractal)
			lvl, length, ang, rel, start, rules = fractal
			self.lvlVar.set(lvl)
			self.lenVar.set(length)
			self.angVar.set(ang)
			self.relVar.set(rel)
			self.startVar.set(start)
			self.rules.delete("0.0", "end")
			self.rules.insert("0.0", "\n".join("%s:%s" % (key, val) for key, val in rules.items()))

	def draw_new_fractal(self):
		"""Get values from entry fields, determinate the points of the polyline
		and finally draw the line to the canvas.
		"""
		self.x = int(self.xVar.get())
		self.y = int(self.yVar.get())
		self.a = 0
		
		lvl = int(self.lvlVar.get())
		length = int(self.lenVar.get())
		ang = float(self.angVar.get())
		rel = float(self.relVar.get())
		start = self.startVar.get()
		
		rules = dict(line.split(":") for line in self.rules.get('0.0', "end").splitlines())
		print(lvl, length, ang, rel, start, rules)

		self.canvas.delete("all")
		self.points = [(self.x, self.y)]
		self.draw_fractal(lvl, length, ang, rel, start, rules)
		print(len(self.points))
		
		self.canvas.create_line(self.points)
			
		
	def draw_fractal(self, level, size, angle, divisor, start, rules):
		"""Recursively draw the fractal by modifying the angle and adding
		points to the list that's later used for drawing the polyline.
		"""
		if level >= 0:
			for c in start:
				if c == "+": self.a += angle # turn left
				if c == "-": self.a -= angle # turn right
				if c in rules:
					self.draw_fractal(level - 1, size / divisor, angle, divisor, rules[c], rules)
		else:
			# move forward
			x2 = self.x + cos(pi * self.a / 180) * (size * divisor)
			y2 = self.y - sin(pi * self.a / 180) * (size * divisor)
			self.x, self.y = x2, y2
			self.points.append((self.x, self.y))


# create and start FracTreeFrame
if __name__ == "__main__":
	frame = FracFrame();
	frame.mainloop()
