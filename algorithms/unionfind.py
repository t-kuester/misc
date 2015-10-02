"""Union-find / disjoint-set data structure.
See https://en.wikipedia.org/wiki/Disjoint-set_data_structure
"""

from collections import defaultdict

class UnionFind:
	"""Union Find data structure, providing operations for determining the group
	some element belongs to and for merging those groups, both in O(log N), N
	being the number of elements in the Union Find.

	For each element, a 'leader' is stored in a map (if an element has no leader,
	it is itself the leader of the group). By following from leader to leader,
	one can quickly find the leader of the entire group, and by rewiring a single
	leader, the entire group gets a new leader.
	"""

	def __init__(self):
		"""Initialize UnionFind, using a defaultdict.
		"""
		self.leaders = defaultdict(lambda: None)

	def find(self, x):
		"""Find group for given element x. Also rewires the leader for x to the
		leader's leader to speed up future lookups.
		"""
		l = self.leaders[x]
		if l is not None:
			l = self.find(l)
			self.leaders[x] = l
			return l
		return x

	def union(self, x, y):
		"""Unite groups of x and y by rewiring x's leader to the leader of y.
		"""
		lx, ly = self.find(x), self.find(y)
		if lx != ly:
			self.leaders[lx] = ly

	def get_groups(self):
		"""Get the disjoint sets, or groups, that were identified .
		"""
		groups = defaultdict(set)
		for x in self.leaders:
			groups[self.find(x)].add(x)
		return groups
	
