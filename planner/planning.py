"""Planning.
2010, Tobias Kuester

This module contains a number of different searching and planning algorithms of
varying complexity, effciency, and suitability for different planning problems.

Implemented Algorithms:
- Graph Search
  - uninformed Depth-First and Breadth-First Search
  - keeping track of visited Belief states
- Iterative Deepening Search
- Serial Decomposition
  - no backtracking yet; subgoals can be undone by plans for other goals

To Do:
- Serial Decomposition w/ backtracking
- Informed Search, using the number of fulfilled subgoals as heuristics
- Regression Search / Backward Chaining
- Partial Order Planning
"""

from knowledge import *
from reasoning import *
from collections import deque

LOG_LEVEL = 2
MAX_DEPTH = 64


def search_plan(goal, beliefs, actions, serial_decomp=False, breadth_first=False):
	"""Search for a way to fulfill the goal Condition for the Beliefs using the
	given Actions. Returns a sequence of tuples of actions and variable matches
	of how the goal can be reached (which can also be an empty sequence) or None
	if no way to reach the goal has been found.
	"""
	global c, p; c, p = 0, 0
	if serial_decomp:
		plan = serial_decomposition(goal, beliefs, actions, breadth_first)
	elif breadth_first:
		plan = graph_search(goal, beliefs, actions, breadth_first)
	else:
		plan = iterative_deepening_search(goal, beliefs, actions)
	log(1, " %d planning steps until finished." % c)
	log(1, " %d pruned planning branches." % p)
	return plan



################################################################################
#                                                                              #
#   SERIAL DECOMPOSITION                                                       #
#                                                                              #
################################################################################

def serial_decomposition(goal, beliefs, actions, breadth_first=False):
	"""In Serial Decomposition Planning, a Conjunction of goals is split up into
	several subgoals which are planned for one after another. If the goal is
	stated such that the most important aspect, or what has to be done first, is
	first in the disjunction, this algorithm can perform very well, as the
	length of the plans to find (and thus the exponent of the search cost) can
	be reduced significantly.
	
	This simple form does not backtrack, so it is necessary that a solution for
	the first subgoal does always allow for a solution for the other subgoals,
	and that no solution for a later subgoal undoes a former subgoal's solution!
	"""
	if isinstance(goal, And):
		new_beliefs = beliefs
		full_plan = []
		for subgoal in goal.conditions:
			log(2, "Planning for Subgoal %s" % str(subgoal))
			plan = serial_decomposition(subgoal, new_beliefs, actions, breadth_first)
			if plan is not None:
				for (action, match) in plan:
					new_beliefs = update(new_beliefs, action.eff, match)
				full_plan += plan
			else:
				return None
		return full_plan
	else:
		if breadth_first:
			return graph_search(goal, beliefs, actions, True)
		else:
			return iterative_deepening_search(goal, beliefs, actions)



################################################################################
#                                                                              #
#   ITERATIVE DEEPENING SEARCH                                                 #
#                                                                              #
################################################################################

def iterative_deepening_search(goal, beliefs, actions):
	"""Iterative Deepening Search calls a restricted depth-first search with 
	increasing depth, until a plan is found or MAX_DEPTH is reached.
	"""
	for i in range(1, MAX_DEPTH):
		log(2, "Searching for a plan with length %d" % i)
		plan = graph_search(goal, beliefs, actions, False, i)
		if plan is not None:
			return plan
	# no plan found
	return None



################################################################################
#                                                                              #
#   GRAPH SEARCH                                                               #
#                                                                              #
################################################################################

def graph_search(goal, beliefs, actions, breadth_first=True, max_depth=MAX_DEPTH):
	"""Uninformed Restricted Depth Graph Search. Keeps track of visited Belief
	states and the length of the plans needed to go there. If a new plan reaches
	a Belief state that has already been achieved with another plan of smaller
	or equal length, that branch is aborted.

	Can be used as a Breadth-First or as a Depth-First search, both of which
	have their strengths and weaknesses. Breadth-First Search can be very fast,
	if the Belief space is limited (as in the Towers of Hanoi case). Depth-First
	Search should be used only in the form of Iterative Deepening Search.
	"""
	global c
	visited = {}
	fringe = deque()
	fringe.append(([], beliefs)) # ([(action, match)*], beliefs)
	
	last = 0
	while fringe:
		c += 1
		(plan, beliefs) = fringe.pop()
		
		# check plan length (only for DFS)
		if breadth_first and len(plan) > last:
			log(2, "Searching for a plan with length %d" % len(plan))
			last = len(plan)
		
		# test whether the goal is fulfilled
		if find_matches(goal, beliefs):
			return plan
		
		# continue search?
		if max_depth == None or len(plan) < max_depth:
		
			# expand current belief state with applicable actions
			for (action, match, new_beliefs) in expand(beliefs, actions):

				# continue search with this plan if the new beliefs are really new
				if check_visited(new_beliefs, visited, len(plan)):
					item = (plan + [(action, match)], new_beliefs)
					if breadth_first:
						fringe.appendleft(item)
					else:
						fringe.append(item)
	# nothing found 
	return None
	


################################################################################
#                                                                              #
#   HELPER FUNCTIONS                                                           #
#                                                                              #
################################################################################

def defect(goal, beliefs, negation=False):
	"""Get the defect of the goal condition in the given belief base. The defect
	for a Belief is One if the Belief is not in the Belief set. The defect of a 
	Conjunction is the sum of the defects of its conditions, and the defect of a
	Disjunction is the minimum of the defects of its conditions.
	"""
	if isinstance(goal, Belief):
		return 0 if find_matches(goal, beliefs, negation=negation) else 1
	
	elif ((isinstance(goal, And) and not negation) or 
	      (isinstance(goal, Or)  and     negation)):
		return sum(defect(cond, beliefs, negation=negation) for cond in goal.conditions)
		
	elif ((isinstance(goal, And) and     negation) or 
	      (isinstance(goal, Or)  and not negation)):
		return min(defect(cond, beliefs, negation=negation) for cond in goal.conditions)
		
	elif isinstance(goal, Not):
		return defect(goal.cond, beliefs, negation=not negation)


def expand(beliefs, actions):
	"""Apply each Action with all possible matches on the given Belief and
	return the results as a List of Tuples (action, match, new_beliefs).
	"""
	result = []
	for action in actions:
		for match in find_matches(action.pre, beliefs):
			new_beliefs = update(beliefs, action.eff, match)
			result += [ (action, match, new_beliefs) ]
	return result
	

def check_visited(beliefs, visited, length=0):
	"""Check whether the Belief state has already be visited using the map of
	visited Belief states to required plan lengths. Return True, if the given
	Belief state has _not_ already been visited.
	"""
	h = hash(frozenset(beliefs))
	if h not in visited or visited[h] > length:
		visited[h] = length
		return True
	global p; p += 1
	return False
	# For testing: Much slower, but guaranteed to be correct.
#	if any((len(v) == len(beliefs) and
#	        all(b in v for b in beliefs) and
#	        visited[v] <= length) for v in visited):
#		global p; p += 1
#		return False
#	visited[frozenset(beliefs)] = length
#	return True
		

def log(n, message):
	"""Print log message, if LOG_LEVEL is >= n."""
	if LOG_LEVEL >= n:
		print(message)

