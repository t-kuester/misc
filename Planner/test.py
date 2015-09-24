"""Testing procedures.
2010, Tobias Kuester

This module defines a number of procedures for consistently testing the
reasoning algorithms in different scenarios.
"""

from knowledge import *
from reasoning import *
from planning  import *


def test(condition, beliefs, expected=None):
	"""Print matches for condition and compare to expected.
	"""
	matches = find_matches(condition, beliefs)
	print_all("Matches for %s:" % condition, matches)
	if expected:
		assert matches == expected


def print_all(title, collection):
	"""Print all elements of collection together with a title.
	"""
	print(title, ":")
	for item in collection:
		print("   " + str(item))
	

def reason_plan_execute(objects, rules, goal, actions, serial_decomp=False, breadth_first=True):
	"""Do a full Reason-Plan-Execute cycle on the given objects, trying to
	fulfill the given goal. First, a number of Beliefs are created from the
	given Objects. Then, further Beliefs are inferred using the given rules, if
	any. Then, a plan sequence is searched for, fulfilling the goal. If a plan
	sequence has been found, the plans elements (tuples of actions and matches)
	are executed on the original Objects, altering them in the process.
	"""
	beliefs = create_beliefs(*objects)
	if rules:
		beliefs = deduce(beliefs, *rules)
	plan = search_plan(goal, beliefs, actions, serial_decomp, breadth_first)

	if plan != None:
		print_all("Plan sequence for goal %s" % goal, [ (a.name, m) for (a, m) in plan])
		for (action, match) in plan:
			action.execute(match)
		print("Length of Plan: %d" % len(plan))
		print_all("After Plan Execution", [vars(x) for x in  objects])
		
		# test goal
		beliefs = create_beliefs(*objects)
		if rules:
			beliefs = deduce(beliefs, *rules)
		assert find_matches(goal, beliefs) != []
		
	else:
		print("No Plan Sequence found for goal %s" % goal)

