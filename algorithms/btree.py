"""Module providing a simple Binary Search Tree
"""

class BTree:
	"""Class representing a Binary Search Tree.
	TODO: delete, balance, rotateleft, rotateright, popmin, popmax
	"""

	def __init__(self, value=None, left=None, right=None, count=0, d=0):
		self.value = value
		self.left = left
		self.right = right
		self.count = count
		self.d = d

	def insert(self, value):
		if self.value is None:
			self.value = value
			self.count = 1
			self.left = BTree(d=self.d + 1)
			self.right = BTree(d=self.d + 1)
		elif value == self.value:
			self.count += 1
		elif value < self.value:
			self.left.insert(value)
		else:
			self.right.insert(value)

	def contains(self, value):
		if self.value is None:
			return 0
		if self.value == value:
			return self.count
		if value < self.value:
			return self.left.contains(value)
		else:
			return self.right.contains(value)

	def num(self):
		if self.value is None:
			return 0
		else:
			return self.left.num() + self.count + self.right.num()

	def getmin(self):
		return self.value if self.left.value is None else self.left.getmin()

	def getmax(self):
		return self.value if self.right.value is None else self.right.getmax()

	def lower(self, value):
		if self.value is None:
			return self
		if self.value >= value:
			return self.left.lower(value)
		else:
			return BTree(self.value, self.left, self.right.lower(value), self.count, self.d)

	def upper(self, value):
		if self.value is None:
			return self
		if self.value <= value:
			return self.right.upper(value)
		else:
			return BTree(self.value, self.left.upper(value), self.right, self.count, self.d)

	def inorder(self):
		if self.value is None:
			return []
		else:
			return (self.left.inorder() +
			        [self.value for _ in range(self.count)] +
			        self.right.inorder())

	def height(self):
		return self.d if self.value is None else max(self.left.height(), self.right.height())

	def __str__(self):
		s = "  " * self.d
		if self.value is None:
			return s + "-"
		else:
			return "%s(%r *%d\n%s\n%s)" % (s, self.value, self.count, self.left, self.right)

	def __repr__(self):
		return "BTree(%r, %r, %r)" % (self.value, self.left, self.right)


def from_list(lst):
	tree = BTree()
	for x in lst:
		tree.insert(x)
	return tree


# TESTING
if __name__ == "__main__":
	import random
	N, M = 100, 20

	# create random numbers, put numbers into tree
	values = [random.randint(0, M) for _ in range(N)]
	tree = from_list(values)
	print(tree)
	print(tree.height())
	print(tree.num())

	# min and max elements
	print(tree.getmin(), tree.getmax())
	print(tree.getmin() == min(values))
	print(tree.getmax() == max(values))

	# check whether inorder is same as ordered list
	print(sorted(values) == tree.inorder())

	# check for all numbers whether they are in the tree
	pos = set(values)
	neg = [x for x in range(M) if x not in pos]
	print(all(tree.contains(x) for x in pos))
	print(all(not tree.contains(x) for x in neg))

	# lower and higher partitions
	low = tree.lower(M//2)
	high = tree.upper(M//2)
	print(low.inorder() == sorted(x for x in values if x < M//2))
	print(high.inorder() == sorted(x for x in values if x > M//2))
