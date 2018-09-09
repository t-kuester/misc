"""Union-find / disjoint-set data structure.
See https://en.wikipedia.org/wiki/Disjoint-set_data_structure
"""

class UnionFind:
	"""Union Find data structure, providing operations for determining the group
	some element belongs to and for merging those groups, both in O(log N), N
	being the number of elements in the Union Find.

	For each element, a 'leader' is stored in a map (if an element has no leader,
	it is itself the leader of the group). By following from leader to leader,
	one can quickly find the leader of the entire group, and by rewiring a single
	leader, the entire group gets a new leader.
	
	This keeps also track of the merged groups in each step, as well as the sizes
	of those groups, and the largest group, whichever is relevant. This is a lot
	faster then re-computing the groups on demand.
	"""

	def __init__(self):
		"""Initialize UnionFind, using a defaultdict for leaders and additional
		dictionaries for groups and group sizes.
		"""
		self.leaders = {}
		self.groups = {}
		self.counts = {}
		self.largest = 0

	def find(self, x):
		"""Find group for given element x. Also rewires the leader for x to the
		leader's leader to speed up future lookups.
		"""
		if x not in self.leaders:
			# new element; set no leader, and add to it's own group
			self.leaders[x] = None
			self.groups[x] = set([x])
			self.counts[x] = 1

		# if already has a leader, update leader for x and all intermediates
		l = self.leaders[x]
		if l is not None:
			self.leaders[x] = self.find(l)

		return self.leaders[x] or x

	def union(self, x, y):
		"""Unite groups of x and y by rewiring x's leader to the leader of y.
		Also updates all the groups by updating the new leader's group with the
		element of the merged leader's group.
		"""
		lx, ly = self.find(x), self.find(y)
		if lx != ly:
			self.leaders[lx] = ly
			# merge groups, group sizes, and largest group
			self.groups[ly].update(self.groups.pop(lx))
			self.counts[ly] += self.counts.pop(lx)
			self.largest = max(self.largest, self.counts[ly])

	def get_groups(self):
		"""Get the disjoint sets, or groups, that were identified.
		With auto-updating groups, this is no longer necessary, just as reference.
		"""
		groups = defaultdict(set)
		for x in self.leaders:
			groups[self.find(x)].add(x)
		return groups	
