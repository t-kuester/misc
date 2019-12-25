"""Convert integer number to corresponding English expression.
"""

# primitives for digits and curiously-spelled numbers smaller than twenty
PRIMITIVES = ("", "one", "two", "three", "four", "five",
			  "six", "seven", "eight", "nine", "ten",
			  "eleven", "twelve", "thirteen", "fourteen", "fifteen",
			  "sixteen", "seventeen", "eighteen", "nineteen")

# primitives for multiples of ten              
TENS = ("", "ten", "twenty", "thirty", "forty", "fifty",
		"sixty", "seventy", "eighty", "ninety")

# some potencies; higher ones are given in exponential form
POTENCIES = ("", "thousand", "million", "billion", "trillion")


def saynumber(number):
	"""Spell out number. Convert a number into a natural-english string.
	"""
	words, potencies = [], potencies_gen()
	while number:
		words = saynumber_1000(number) + [next(potencies)] + words
		number = number // 1000
	return " ".join(filter(None, words)) if words else "zero"

def saynumber_1000(number):
	"""Spell last three digits of number, ignore the rest.
	"""
	number = number % 1000
	words = [PRIMITIVES[number // 100], "hundred"] if number > 99 else []
	number = number % 100
	if number < 20:
		words.append(PRIMITIVES[number])
	else:
		words.append(TENS[number // 10])
		number = number % 10
		if number:
			words.append(PRIMITIVES[number])
	return words

def potencies_gen():
	"""Generator for spelling out various potencies, like 'thousand' 
	or 'million', one after another.
	"""
	for potency in POTENCIES:
		yield potency
	exponent = len(POTENCIES)
	while True:
		exponent += 1
		yield "10^%d" % (exponent * 3)


# testing
if __name__ == "__main__":
	import random
	for e in range(1, 12):
		n = random.randint(0, 10**e)
		num = saynumber(n)
		print("%15d %s" % (n, num))
