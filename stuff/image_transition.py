"""Different functions to transition from one PIL image to another (must have
same dimensions) and update the images in a simple Tkinter canvas accordingly.
"""

import tkinter, random
import numpy as np
from PIL import Image, ImageTk


def slide(img_a, img_b, n=10):
	"""Slide-transition from left to right"""
	arr_a = np.array(img_a.convert("RGB"))
	arr_b = np.array(img_b.convert("RGB"))
	yield img_a
	h, w, _ = arr_a.shape
	for k in range(0, w, n):
		arr_a[:,k:k+n] = arr_b[:,k:k+n]
		yield Image.fromarray(arr_a, mode="RGB")

def fade_rows(img_a, img_b, n=10):
	"""Fade random rows (10 at a time) from one image to the other."""
	arr_a = np.array(img_a.convert("RGB"))
	arr_b = np.array(img_b.convert("RGB"))
	yield img_a
	h, w, _ = arr_a.shape
	rows = random.sample(range(h), h)
	for k in range(0, len(rows), n):
		arr_a[rows[k:k+n]] = arr_b[rows[k:k+n]]
		yield Image.fromarray(arr_a, mode="RGB")

def pixelate(img_a, img_b, n=20):
	"""Replace big chunks/pixels of one pixels with those of the other."""
	arr_a = np.array(img_a.convert("RGB"))
	arr_b = np.array(img_b.convert("RGB"))
	h, w, _ = arr_a.shape
	yield img_a
	
	px = [(x,y) for x in range(0, w, n) for y in range(0, h, n)]
	random.shuffle(px)
	
	for k in range(0, len(px), 10):
		for x, y in px[k:k+10]:
			arr_a[y:y+n:,x:x+n] = arr_b[y:y+n:,x:x+n]
		yield Image.fromarray(arr_a, mode="RGB")

f = fade_rows

def update(img_gen):
	global img
	try:
		img = ImageTk.PhotoImage(next(img_gen))
		c.delete("all")
		c.create_image(0, 0, image=img, anchor="nw")
		c.after(1, update, img_gen)
	except StopIteration:
		pass

root = tkinter.Tk()
c = tkinter.Canvas(root, width=800, height=400)
c.pack()
update(f(Image.open("a.gif"), Image.open("b.gif")))
root.mainloop()
