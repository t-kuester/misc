"""Blocks World Example.
2010, Tobias Kuester

For testing knowledge, planning, and reasoning in a very simple environment.
Obviously, the Blocks World is static, discrete, fully-observable, determined,
and all the other boring characteristics, but for starters this will do...
"""

from knowledge import *
from reasoning import *
from planning  import *

# define Block class
class Block:
	"""Block class.
	
	This Object is what this scenario is all about. Blocks have a name and can
	be stacked on other blocks. That's all.
	"""
	
	def __init__(self, name, other=None):
		self._name = name
		if other:
			self.is_on = other
		
	def __repr__(self):
		return self._name
		

# define shortcuts for expressing common beliefs
IsBlock = lambda subj:      Belief("Block", subj)
IsOn    = lambda subj, obj: Belief("is_on", subj, obj)
OnTable = lambda subj:      Belief("on_table", subj)
Clear   = lambda subj:      Belief("clear", subj)
Single  = lambda subj:      Belief("singleton", subj)


# define shortcuts for some variables
x, y, z, _ = "x", "y", "z", "*"


# define deduction rules	            
is_clear     = Rule(pre=And(IsBlock(x), Not(IsOn(y, x))), eff=Clear(x))
is_on_table  = Rule(pre=And(IsBlock(x), Not(IsOn(x, y))), eff=OnTable(x))
singleton    = Rule(pre=And(Clear(x), OnTable(x)),        eff=Single(x))
rules = [is_clear, is_on_table, singleton ]


# define available actions
def put_on_table(x, y):
	del x.is_on
put_on_table = Action("Put On Table", 
                      pre=And(Clear(x), IsOn(x, y)), 
                      eff=And(Not(IsOn(x, y)), OnTable(x), Clear(y)),
                      implementation=put_on_table)
def put_on_other(x, y):
	x.is_on = y
put_on_other = Action("Put On Other",
                      pre=And(Clear(x), Clear(y), OnTable(x)), 
                      eff=And(Not(OnTable(x)), Not(Clear(y)), IsOn(x, y)),
                      implementation=put_on_other)
actions = [put_on_table, put_on_other]


if __name__ == "__main__":

	from test import *

	# create Block objects
	D = Block("D")
	C = Block("C")
	B = Block("B", C)
	A = Block("A", B)
	objects = (A, B, C, D)

	# create initial beliefs from objects
	beliefs = create_beliefs(*objects)
	print_all("Initial Beliefs", beliefs)

	# apply deduction rules to initial beliefs	
	beliefs = deduce(beliefs, *rules)
	print_all("Inferred Beliefs", beliefs)

	# simple testing of facts
	test(IsBlock(A), beliefs, [{}])
	test(IsBlock(Block("F")), beliefs, [])
	test(IsOn(A, B), beliefs, [{}])

	# substituting variables
	test(IsBlock(x), beliefs, [{x: A}, {x: B}, {x: C}, {x: D}])
	test(IsOn(x, y), beliefs, [{x: A, y: B}, {x: B, y: C}])

	# disjunction
	test(Or(IsOn(x, y), Clear(x)), beliefs, [{x: A, y: B}, {x: B, y: C}, {x: A}, {x: D}])
	test(Or(OnTable(x), Clear(x)), beliefs, [{x: C}, {x: D}, {x: A}])

	# conjunction
	test(And(IsOn(x, y), Clear(x)), beliefs, [{x: A, y: B}])
	test(And(OnTable(x), Clear(x)), beliefs, [{x: D}])

	# negation
	test(And(IsBlock(x), Not(Clear(x))), beliefs, [{x: B}, {x: C}] )
	test(And(IsBlock(x), Not(And(OnTable(x), Clear(x)))), beliefs)
	test(And(IsBlock(x), Not( Or(OnTable(x), Clear(x)))), beliefs, [{x: B}])
	test(And(IsBlock(x), Not(OnTable(x)), Not(Clear(x))), beliefs, [{x: B}])

	# planning
	reason_plan_execute(objects, rules, And(IsOn(C, D), IsOn(B, A)), actions)
	reason_plan_execute(objects, rules, And(IsOn(C, D), IsOn(B, C), IsOn(A, B)), actions)
	reason_plan_execute(objects, rules, Not(IsOn(_, _)), actions)

	# planning for unsolvable goals
	reason_plan_execute(objects, rules, And(IsOn(A, B), Clear(B)), actions)
	reason_plan_execute(objects, rules, And(IsOn(A, B), IsOn(B, A)), actions)
	reason_plan_execute(objects, rules, And(IsOn(A, A)), actions)

