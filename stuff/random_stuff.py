"""Random bits and pieces, computational curiosities, etc.

Each of the following functions is a self-contained little useless program.
"""

def generate_pi(n=100):
	"""Generate an approximation of pi.
	"""
	import itertools, math
	def pi_gen():
		terms = 0
		for n in itertools.count(1):
			terms += 1 / n**4
			yield (terms * 90)**(1/4)

	for i, p in zip(range(n), pi_gen()):
		print(i, p)
	print("---\n", math.pi)


def print_quine():
	"""Print the exact content of this method, following GEB
	"""
	def quine(s): return '%s(%r))' % (s, s)
	print(quine("def quine(s): return '%s(%r))' % (s, s)\nprint(quine"))


def robinsonade():
	"""Do a so-called "robinsonade" from D.R. Hofstadter's "Metamagicum",
	iteratively finding a self-descriptive string telling how many of each
	digit is contained within it.
	"""
	text = "This text has " + ", ".join("{} %d" % i for i in range(10))
	last, cur = None, [0] * 10
	while last != cur:
		inserted = text.format(*cur)
		# cur, last = count_digits(text % cur), cur
		cur, last = list(map(inserted.count, "0123456789")), cur
	print(inserted)
		

def towers_of_hanoi(height, source="A", target="B", swap="C"):
	"""Solve tower of hanoi with three stakes and given height.
	"""
	def move_piece(src, tgt, hgt):
		print("%s%r to %r" % (hgt * " ", src, tgt))
	
	if height == 1:
		move_piece(source, target, height)
	else:
		towers_of_hanoi(height - 1, source, swap, target)
		move_piece(source, target, height)
		towers_of_hanoi(height - 1, swap, target, source)


def hyper_operator(x, y, op):
	"""Define hyper-operator for succ, add, mult, pow, etc., and apply it to
	the given parameters (parameters must be positive integers).
	"""
	def hypop(a, b, c):
		
		if c == 0: return a + 1
		else:      return hypop(hypop(a, b-1, c), a, c-1) \
				          if (c == 1 and b > 0) or (b > 1) else a
	print(hypop(x, y, op))


# running/testing
if __name__ == "__main__":
	# generate_pi(100)
	# print_quine()
	# robinsonade()
	# towers_of_hanoi(5)
	# hyper_operator(4, 5, 3)
	pass
