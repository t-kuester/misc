"""Module providing a simple Binary Search Tree
"""

class BTree:
	"""Class representing a Binary Search Tree.
	TODO: delete arbitrary nodes, getlower, getupper
	"""

	def __init__(self, value=None, left=None, right=None, count=0, d=0):
		"""Create new Binary Search Tree. If value, left, and right are supplied,
		they have to be in the correct order already. A leaf node is represented
		as BTree(X, BTree(None, None, None), BTree(None, None, None)).
		"""
		self.value = value
		self.left = left
		self.right = right
		self.count = count
		self.d = d

	def insert(self, value, count=1):
		"""Insert element into tree. Either add a new node in the correct place
		in the tree, or increment the count for an existing element.
		"""
		if self.value is None:
			self.value = value
			self.count = count
			self.left = BTree(d=self.d + 1)
			self.right = BTree(d=self.d + 1)
		elif value == self.value:
			self.count += count
		elif value < self.value:
			self.left.insert(value, count)
		else:
			self.right.insert(value, count)

	def balance(self):
		"""Balance the tree by rotating the subtrees, i.e. removing the max from
		the left tree, using it as the value, and inserting the old value into
		the right tree, or vice versa.
		"""
		if self.value is not None:
			while True:
				# balance subtrees
				self.left.balance()
				self.right.balance()
				lh, rh = self.left.height(), self.right.height()
				if lh > rh + 1:
					# rotate right
					self.right.insert(self.value, self.count)
					self.value, self.count = self.left.popmax()
				elif lh + 1 < rh:
					# rotate left
					self.left.insert(self.value, self.count)
					self.value, self.count = self.right.popmin()
				else:
					break

	def popmin(self):
		"""Remove minimum elements from tree and return value and count.
		"""
		if self.value is None:
			return None, 0
		if self.left.value is not None:
			return self.left.popmin()
		else:
			v, c = self.value, self.count
			self.value, self.count = self.right.popmin()
			return v, c

	def popmax(self):
		"""Remove maximum elements from tree and return value and count.
		"""
		if self.value is None:
			return None, 0
		if self.right.value is not None:
			return self.right.popmax()
		else:
			v, c = self.value, self.count
			self.value, self.count = self.left.popmax()
			return v, c

	def contains(self, value):
		"""Check whether the given element is contained in the tree and return
		its count, or 0 if it is not contained. Also works for boolean checks.
		"""
		if self.value is None:
			return 0
		if self.value == value:
			return self.count
		if value < self.value:
			return self.left.contains(value)
		else:
			return self.right.contains(value)

	def num(self):
		"""Get total number of elements in the tree, including duplicates."""
		if self.value is None:
			return 0
		else:
			return self.left.num() + self.count + self.right.num()

	def getmin(self):
		"""Get minimum element in the tree."""
		return self.value if self.left.value is None else self.left.getmin()

	def getmax(self):
		"""Get maximum element in the tree."""
		return self.value if self.right.value is None else self.right.getmax()

	def lower(self, value):
		"""Get portion of the tree strictly lower than the given element.
		The method does not alter the original tree, but the result reuses nodes
		of the original, so altering it may alter the original.
		"""
		if self.value is None:
			return self
		if self.value >= value:
			return self.left.lower(value)
		else:
			return BTree(self.value, self.left, self.right.lower(value), self.count, self.d)

	def upper(self, value):
		"""Get portion of the tree strictly greater than the given element.
		The method does not alter the original tree, but the result reuses nodes
		of the original, so altering it may alter the original.
		"""
		if self.value is None:
			return self
		if self.value <= value:
			return self.right.upper(value)
		else:
			return BTree(self.value, self.left.upper(value), self.right, self.count, self.d)

	def inorder(self):
		"""Return list of elements of the tree in-order, expanding duplicates.
		"""
		if self.value is None:
			return []
		else:
			return (self.left.inorder() +
			        [self.value for _ in range(self.count)] +
			        self.right.inorder())

	def height(self):
		"""Get the height of the tree."""
		return 0 if self.value is None else 1 + max(self.left.height(),
		                                            self.right.height())

	def __str__(self):
		s = "  " * self.d
		if self.value is None:
			return s + "-"
		else:
			return "%s(%r *%d\n%s\n%s)" % (s, self.value, self.count,
					                       self.left, self.right)

	def __repr__(self):
		return "BTree(%r, %r, %r)" % (self.value, self.left, self.right)


def from_list(lst):
	"""Create BTree from list."""
	tree = BTree()
	for x in lst:
		tree.insert(x)
	return tree


# TESTING
if __name__ == "__main__":
	import random
	N, M = 100, 100

	# create random numbers, put numbers into tree
	values = [random.randint(0, M) for _ in range(N)]
	tree = from_list(values)
	assert tree.num() == len(values)

	# min and max elements
	assert tree.getmin() == min(values)
	assert tree.getmax() == max(values)

	# check whether inorder is same as ordered list
	assert sorted(values) == tree.inorder()

	# check for all numbers whether they are in the tree
	pos = set(values)
	neg = [x for x in range(M) if x not in pos]
	assert all(tree.contains(x) for x in pos)
	assert all(not tree.contains(x) for x in neg)

	# lower and higher partitions
	low = tree.lower(M//2)
	high = tree.upper(M//2)
	assert low.inorder() == sorted(x for x in values if x < M//2)
	assert high.inorder() == sorted(x for x in values if x > M//2)

	# balancing
	tree.balance()
	assert sorted(values) == tree.inorder()
	print(tree)
	print("height", tree.height())
