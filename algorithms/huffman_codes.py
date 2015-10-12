"""Create letter-frequency-based 'encoding' using Huffman codes.
"""

from __future__ import division
from collections import Counter
from heapq import heappush, heappop, heapify

def get_probabilities(text):
	"""Get character probabilities from text."""
	n = len(text)
	counts = Counter(text)
	return {c: counts[c] / n for c in text}

def huffman(probabilities):
	"""Generate variable-length Huffman encoding for symbols in alphabet with 
	given probabilities or frequencies.
	"""
	# put symbols onto heap in order of probability
	# use hash as 2nd element, otherwise problem with comparison in Python 3
	heap = [(p, hash(c), c) for (c, p) in probabilities.items()]
	heapify(heap)

	# take symbols with lowest probability from heap, combine to new meta-symbol
	while len(heap) >= 2:
		p1, _, c1 = heappop(heap)
		p2, _, c2 = heappop(heap)
		heappush(heap, (p1+p2, hash((c2, c1)), (c2, c1)))

	# now, last meta-symbol on heap is the optimal encoding tree
	codes = {}
	to_code(codes, heappop(heap)[2])
	return codes

def to_code(d, tree, prefix=""):
	"""Turn the generated tree into binary codes. """
	if isinstance(tree, tuple):
		left, right = tree
		to_code(d, left, prefix+"0")
		to_code(d, right, prefix+"1")
	else:
		d[tree] = prefix

def encode(dictionary, text):
	"""Turn the text into huffman encoded binary string."""
	return "".join(dictionary[c] for c in text)
	
def decode(dictionary, binary):
	"""Turn the binary string back into readable text."""
	inverse_dict = {v: k for k, v in dictionary.items()}
	res = ""
	while binary:
		k = next(k for k in inverse_dict if binary.startswith(k))
		res += inverse_dict[k]
		binary = binary[len(k):]
	return res

def calc_avg_len(codes, probabilities):
	"""Calculate average length of codes, weighted by probabilities."""
	total = sum(probabilities.values())
	return sum(len(codes[c]) * probabilities[c] / total for c in codes)

# testing
if __name__ == "__main__":
	# probabilities = {"A": 0.6, "B": 0.25, "C": 0.10, "D": 0.05}
	# probabilities = {"A": 0.32, "B": 0.25, "C": 0.2, "D": 0.18, "E": 0.05}
	# probabilities = {"A": 0.33, "B": 0.33, "C": 0.33}
	probabilities = {"A": 0.4, "B": 0.1, "C": 0.1, "D": 0.1, "E": 0.1, "F": 0.1, "G": 0.05, "H": 0.05}
	# probabilities = {"A": 0.4, "B": 0.4, "C": 0.2}
	
	codes = huffman(probabilities)
	for c in sorted(codes, key=lambda x: probabilities[x], reverse=True):
		print("%s %.2f %s" % (c, probabilities[c], codes[c]))
	print(calc_avg_len(codes, probabilities))

	# test encoding and decoding
	text = "Hello, World! Just some text for testing encoding and decoding."
	codes = huffman(get_probabilities(text))
	print(text == decode(codes, encode(codes, text)))
	
