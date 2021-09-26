from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import sqrt
from typing import Dict, List, Optional, Tuple


DIRECTIONS = [(-1, -1), (-1, 0), (-1, +1),
              ( 0, -1),          ( 0, +1),
              (+1, -1), (+1, 0), (+1, +1)]


@dataclass
class Pos:
	r: int
	c: int
	
	def dist(self, other) -> float:
		dr, dc = abs(self.r - other.r), abs(self.c - other.c)
		return min(dr, dc) * sqrt(2) + max(dr, dc) - min(dr, dc)
	
	def pos(self):
		return (self.r, self.c)


@dataclass
class Cell(Pos):
	free: bool
	# neighbors


@dataclass
class Field:
	width: int
	height: int
	cells: List[List[Cell]]
	start: Optional[Cell]
	target: Optional[Cell]
	
	def free(self, r: int, c: int):
		return 0 <= r < self.height and 0 <= c < self.width and self.cells[r][c].free


def init_field(width: int, height: int) -> Field:
	cells = [[Cell(r, c, True) for c in range(width)] for r in range(height)]
	return Field(width, height, cells, None, None)


def a_star_search(field) -> Optional[Tuple[List[Pos], Dict[Tuple[int, int], float]]]:
	
	ids = count()
	heap = [(field.start.dist(field.target), 0, next(ids), field.start, [field.start.pos()])]
	visited = {}
	while heap:
		heur, cost, _, cell, path = heappop(heap)
		if cell is field.target:
			return (path, visited)
			
		if cell.pos() not in visited:
			visited[cell.pos()] = cost
			
			r, c = cell.r, cell.c
			for dr, dc in DIRECTIONS:
				if field.free(r+dr, c+dc) and field.free(r+dr, c) and field.free(r, c+dc):
					d = sqrt(dr**2 + dc**2)
					dest = field.cells[r+dr][c+dc]
					heappush(heap, (dest.dist(field.target), cost + d, next(ids), dest, path + [dest.pos()]))
			
	return None
