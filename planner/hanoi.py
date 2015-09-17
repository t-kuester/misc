"""Towers of Hanoi Example.
2010, Tobias Kuester

A more complex planning problem: There are three stacks, and the goal is to move
a number of Blocks from the first Stack to the third Stack, whereas each Block
can be placed on another Block only if it is smaller than the other Block.
This problem can be solved very well with Serial Decomposition, as one subgoal
builds on the other, and with Beadth-First search, as the total Belief space is
relatively small even for large problems.
"""

from knowledge import *
from reasoning import *
from planning  import *

# define Block and Stack classes
class Block:
	
	def __init__(self, name, other):
		self._name = name
		self.is_on = other
		
	def __repr__(self):
		return self._name
		
class Stack:
	
	def __init__(self, name):
		self._name = name

	def __repr__(self):
		return self._name
		

# define shortcuts for expressing common beliefs
IsBlock = lambda subj:      Belief("Block", subj)
IsStack = lambda subj:      Belief("Stack", subj)
IsOn    = lambda subj, obj: Belief("is_on", subj, obj)
Clear   = lambda subj:      Belief("clear", subj)
Smaller = lambda subj, obj: Belief("smaller", subj, obj)


# define shortcuts for some variables
x, y, z, _ = "x", "y", "z", "*"


# define deduction rules	            
is_clear      = Rule(pre=And(Or(IsBlock(x), IsStack(x)), Not(IsOn(y, x))), eff=Clear(x))
smaller_init  = Rule(pre=And(IsBlock(x), IsBlock(y), IsOn(x, y)), eff=Smaller(x, y))
smaller_trans = Rule(pre=And(Smaller(x, y), Smaller(y, z)), eff=Smaller(x, z))
rules = [is_clear, smaller_init, smaller_trans]


# define available actions
def put_on(x, y, z):
	x.is_on = y
put_on_other = Action("Put On Other",
                      pre=And(IsBlock(x), IsBlock(y), Clear(x), Clear(y), IsOn(x, z), Smaller(x, y)), 
                      eff=And(Clear(z), IsOn(x, y), Not(And(IsOn(x, z), Clear(y)))),
                      implementation=put_on)
put_on_stack = Action("Put On Stack",
                      pre=And(IsBlock(x), IsStack(y), Clear(x), Clear(y), IsOn(x, z)), 
                      eff=And(Clear(z), IsOn(x, y), Not(And(IsOn(x, z), Clear(y)))),
                      implementation=put_on)
actions = [put_on_other, put_on_stack]


if __name__ == "__main__":

	import optparse
	parser = optparse.OptionParser("hanoi.py [Options] [Blocks]")
	parser.add_option("-s", "--serial", dest="serial", help="serial decomposition?", action="store_true")
	parser.add_option("-b", "--bfs", dest="bfs", help="breadth-first search?", action="store_true")
	(options, args) = parser.parse_args()
	
	num_blocks = int(args[0]) if args else 3
	serial = options.serial
	bfs = options.bfs
	
	# create Stacks and one Block
	S1 = Stack("Stack 1")
	S2 = Stack("Stack 2")
	S3 = Stack("Stack 3")
	B  = Block("B %d" % num_blocks, S1)
	objects = [ S1, S2, S3, B ]
	goals   = [ IsOn(B, S3) ]
	
	# create additional Blocks
	last = B
	for n in range(num_blocks - 1, 0, -1):
		B = Block("B %d" % n, last)
		objects += [ B ]
		goals   += [ IsOn(B, last) ]
		last = B
	
	# plan!
	import test
	test.reason_plan_execute(objects, rules, And(*goals), actions, serial, bfs)
	
#	RESULTS	
#	Exponential growth: Length of plan doubles with every new block; size of
#	state-space triples with every new block
#	Planning steps required for algorithms, with pruning of visited states:
#	BLOCKS	LENGTH	IDS		SD-IDS	BFS		SD-BFS
#	2		3		19		13		7		7
#	3		7		84		36		27		23
#	4		15		813		210		69		56
#	5		31		7583	1154	239		168
#	6		63				10857	657		477
#	7		127						2155	1423
#	8		255						6305	4186
#	9		511								13058

