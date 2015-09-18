"""Home-brewn heap data structure. Of course, in all practical applications
the heapq module should be used. This is just for myself, for learning, etc.
"""

class Heap:
	"""Heap data structure.
	"""

	def __init__(self, verbose=False):
		"""Create empty heap. Actually, the heap contains one dummy element for
		'padding' so we have effectively a one-based array."""
		self.heap = [None]
		self.verbose = verbose
		
	def insert(self, n):
		"""Insert new element at correct position into the heap."""
		self.heap.append(n)
		i = len(self.heap)-1
		while i > 1 and self.heap[i] < self.heap[i // 2]:
			self._swap(i, i // 2)
			i = i // 2
		if self.verbose:
			self.printout()
		
	def pop(self):
		"""Pop first element from the heap and re-heapify the rest."""
		n = self.heap[1]       # the first element, to be returned
		s = len(self.heap) - 1 # the last element, to be repositioned
		self._swap(1, s)       # put last in first place
		del self.heap[s]       # remove old last
		i = 1
		while s >= i * 2:
			k = None
			if s > i * 2 + 1:
				k = i * 2 if self.heap[i * 2] <= self.heap[i * 2 + 1] else i * 2 + 1
			elif s > i * 2:
				k = i * 2
			if k and self.heap[i] > self.heap[k]:
				self._swap(i, k)
				i = k
			else:
				break
		if self.verbose:
			self.printout()
		return n
		
	def printout(self, i=1, d=0):
		"""Recursively print out the heap's tree structure."""
		print("---")
		print("%s%r" % ("  " * d, self.heap[i] if len(self.heap) > i else None))
		if i*2 < len(self.heap):
			self.printout(i * 2, d + 1)
		if i*2+1 < len(self.heap):
			self.printout(i * 2 + 1, d + 1)
			
	def _swap(self, i, k):
		self.heap[i], self.heap[k] = self.heap[k], self.heap[i]


# testing
if __name__ == "__main__":
	
	h = Heap(False)
	
	h.insert(4)
	h.insert(3)
	h.insert(2)
	h.insert(5)
	h.insert(4)
	h.insert(13)
	h.insert(5)
	h.insert(1)
	print(h.heap)
	
	print(h.pop())
	print(h.pop())
	print(h.pop())
	print(h.pop())
	print(h.pop())
	print(h.pop())
	print(h.pop())
	print(h.pop())

	print(h.heap)