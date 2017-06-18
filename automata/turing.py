#!/usr/bin/env python3

"""
Very simple implementation of a Turing Machine.

Tobias Kuster, 2017
"""

import collections
Head = collections.namedtuple("Head", ("state", "symbol"))
Body = collections.namedtuple("Body", ("write", "move", "state"))

R = RIGHT = 1
L = LEFT = -1

class Tape:
	"""Class representing a tape in a turing machine. It consists of two
	lists, one for the 'forward' and one for the 'backward' half of the
	tape. Both lists are automatically appended to as needed.
	"""
	
	def __init__(self, initial_state=None, position=0, default_symbol=0):
		self.default_symbol = default_symbol
		self.position = position
		self.forward = list(initial_state or [default_symbol])
		self.backward = []
	
	def read(self):
		"""Read symbol at head position."""
		lst, pos = self._get_cell()
		return lst[pos]
		
	def write(self, value):
		"""Write symbol to head position."""
		lst, pos = self._get_cell()
		lst[pos] = value
		
	def move(self, direction):
		"""Move head #direction amount to right/left."""
		self.position += direction
		lst, pos = self._get_cell()
		if pos >= len(lst):
			lst.append(self.default_symbol)
		
	def _get_cell(self):
		"""Get part of tape and position therein."""
		if self.position >= 0:
			return self.forward, self.position
		else:
			return self.backward, ~ self.position
			
	def __str__(self):
		return "%r %r %r" % (self.backward[::-1], self.forward, self.position)

	
class TuringMachine:
	"""Class representing a simple Turing Machine with a single tape.
	Transition rules are represented as a dict mapping Head to Body
	tuples. Use step method to advance to next state.
	"""
	
	def __init__(self, rules, state, tape=None):
		self.rules = rules
		self.state = state
		self.tape = tape or Tape()
	
	def step(self):
		"""Read symbol, get matching rule, advance to next state."""
		symbol = self.tape.read()
		rule = Head(self.state, symbol)
		if rule in self.rules:
			body = self.rules[rule]
			self.tape.write(body.write)
			self.tape.move(body.move)
			self.state = body.state
			return True
		else:
			return False
	
	def __str__(self):
		return "%r %s" % (self.state, self.tape)


def tm_increment(n):
	"""TM to increment a number in binary.
	"""
	rules = {Head('inc', 1): Body(0, R, 'inc'),
			 Head('inc', 0): Body(1, L, 'end')}
	binary = [int(x) for x in reversed(format(n, 'b'))]
	return TuringMachine(rules, 'inc', Tape(binary))

def tm_busybeaver():
	"""Two-state Busy Beaver TM.
	"""
	rules = {Head('A', 0): Body(1, R, 'B'),
			 Head('A', 1): Body(1, L, 'B'),
			 Head('B', 0): Body(1, L, 'A'),
			 Head('B', 1): Body(1, 0, 'C')}
	return TuringMachine(rules, 'A')

import time
#~ tm = tm_increment(15)
tm = tm_busybeaver()
print(tm)
while tm.step():
	print(tm)
	time.sleep(.5)
