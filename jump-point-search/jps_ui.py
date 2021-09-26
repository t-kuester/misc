import tkinter as tk

from contextlib import suppress

from jps_algo import *


class JumpPointSearchFrame(tk.Frame):

	def __init__(self, master, width, height):
		tk.Frame.__init__(self, master)
		self.master.title("Jump Point Search")
		self.width = width
		self.height = height
		self.field = init_field(width, height)
		self.pack(fill=tk.BOTH, expand=tk.YES)
		
		self.canvas = tk.Canvas(self)
		self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
		
		self.bind_all("<KeyPress>", self.handle_key)
		self.canvas.bind("<ButtonRelease>", self.handle_mouse)
		self.bind("<Configure>", lambda _: self.draw_state())
		
	def handle_key(self, event):
		res = a_star_search(self.field)
		if res is not None:
			path, visited = res
			self.draw_path(path, visited)
		
	def handle_mouse(self, event):
		w = self.get_cellwidth()
		r, c = int(event.y // w), int(event.x // w)
		with suppress(IndexError):
			cell = self.field.cells[r][c]
		
			if event.num == 1:
				cell.free = not cell.free
				
			if event.num == 3:
				if self.field.start is not None and self.field.target is None:
					self.field.target = cell
				else:
					self.field.start = cell
					self.field.target = None
		
		self.draw_state()

	def draw_state(self,):
		self.update()
		self.canvas.delete("all")
		w = self.get_cellwidth()
		to_xy = lambda r, c: (c * w, r * w)

		# draw free / blocked cells
		for r in range(self.height):
			for c in range(self.width):
				x, y = to_xy(r, c)
				cell = self.field.cells[r][c]
				fill = "#888888" if not cell.free else "#ffffff"
				self.canvas.create_rectangle(x, y, x+w, y+w, fill=fill)
				
				if cell is self.field.start or cell is self.field.target:
					fill = "#88cc88" if cell is self.field.start else "#8888cc"
					self.canvas.create_oval(x+w/6, y+w/6, x+5*w/6, y+5*w/6, fill=fill)

		# TODO draw primary jump points
		# TODO draw numbers
		
	def draw_path(self, path, visited):
		w = self.get_cellwidth()
		to_xy = lambda r, c: (c * w, r * w)
		
		for r, c in visited:
			x, y = to_xy(r, c)
			self.canvas.create_oval(x+w/4, y+w/4, x+3*w/4, y+3*w/4, fill="#cccc88")
			
		for r, c in path:
			x, y = to_xy(r, c)
			self.canvas.create_oval(x+w/4, y+w/4, x+3*w/4, y+3*w/4, fill="#cc8888")
	
	def get_cellwidth(self):
		rows, cols = self.height, self.width
		return min(self.canvas.winfo_height() / rows, self.canvas.winfo_width() / cols)


def main():
	root = tk.Tk()
	JumpPointSearchFrame(root, 15, 10)
	root.mainloop()

	
if __name__ == "__main__":
	main()
