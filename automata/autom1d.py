#!/usr/bin/env python3

""" Module for creating and printing simple 1-dimensional line-automata.
Supports different simple automata, such as the different elementary cellular
automata by Stephen Wolfram, and helper methods for creating different ones.

Tobias Kuester, 2015
"""

import random

# SOME HELPER FUNCTIONS

def random_line(width):
	""" Create line with random 0s and 1s. """
	return [random.randint(0, 1) for n in range(width)]

def single_one(width):
	""" Create line with a singe 1 and rest 0s. """
	return [0] * (width - 1) + [1]

def wrap_line(line, extra):
	""" Wrap line around at the edges with #extra chars of overlap. """
	return line[-extra:] + line + line[:extra]

def to_str(line):
	""" Convert binary line to string. """
	return ''.join(map(str, line))

def make_rule(num):
	""" Make rule #num for elementary automaton. """
	binary = "{0:08b}".format(num)
	return dict(("{0:03b}".format(i), int(x)) for i, x in enumerate(reversed(binary)))

def print_to_image(automaton, lines):
	""" Print a number of lines generated from the given automata to an image
	file in simple PGM format. Run the script as "python [filename] > img.pgm"
	to save the image. """
	first_line = next(automaton)
	print("P1")
	print("%d %d" % (len(first_line), lines))
	print(first_line)
	for line in range(lines - 1):
		print(next(automaton))


# GENERATOR FUNCTIONS FOR DIFFERENT AUTOMATONS

def wolfram(width):
	"""Not sure what this automaton was about or why I named the function 
	like that... """
	line = random_line(width)
	while True:
		last = wrap_line(line, 2)
		line = [int(sum(last[k:k+5]) in (2, 4)) for k in range(width)]
		yield to_str(line)

def elementary(width, rule_num, single1=True):
	""" Generator function for elementary cellular automatons.
	See https://en.wikipedia.org/wiki/Elementary_cellular_automaton
	"""
	rule = make_rule(rule_num)
	line = single_one(width) if single1 else random_line(width)
	while True:
		last = wrap_line(line, 1)
		line = [rule[to_str(last[k:k+3])] for k in range(len(last)-2)]
		yield to_str(line)


# TEST/RUN AUTOMATON
if __name__ == "__main__":
	print_to_image(elementary(1000, 110, True), 1000)
	