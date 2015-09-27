"""Monkey and Banana Example.
2010, Tobias Kuester

A Planning Problem with a (relatively) large number of different actions to
choose from. Monkey wants Banana. Ook!
"""

from knowledge import *
from reasoning import *
from planning  import *


# define shortcuts for expressing common beliefs
Monkey = lambda subj:      Belief("Monkey", subj)
Banana = lambda subj:      Belief("Banana", subj)
Crate  = lambda subj:      Belief("Crate", subj)
Room   = lambda subj:      Belief("Room", subj)
At     = lambda subj, obj: Belief("at", subj, obj)
Has    = lambda subj, obj: Belief("has", subj, obj)
Low    = lambda subj:      Belief("low", subj)
High   = lambda subj:      Belief("high", subj)
Happy  = lambda subj:      Belief("happy", subj)


# define shortcuts for some variables
x, y, z, _ = "x", "y", "z", "*"


# define available actions
go_to      = Action("Go To",
					pre=And(Monkey(x), At(x, y), Low(x), Room(z)),
					eff=And(At(x, z), Not(At(x, y))))
take       = Action("Take",
					pre=And(Monkey(x), At(x, y), At(z, y), 
					        Or(And(Low(x), Low(z)), And(High(x), High(z)))),
					eff=And(Has(x, z), Not(And(At(z, y), High(z), Low(z)))))
drop       = Action("Drop",
					pre=And(Monkey(x), At(x, y), Has(x, z)),
					eff=And(At(z, y), Low(z), Not(Has(x, z))))
climb_up   = Action("Climb Up",
					pre=And(Monkey(x), Crate(z), At(x, y), At(z, y), Low(x)),
					eff=And(High(x), Not(Low(x))))
climb_down = Action("Climb Down",
					pre=And(Monkey(x), Crate(z), At(x, y), At(z, y), High(x)),
					eff=And(Low(x), Not(High(x))))
eat        = Action("Eat",
					pre=And(Monkey(x), Banana(y), Has(x, y)),
					eff=And(Happy(x), Not(Has(x, y))))
actions = [go_to, take, drop, climb_up, climb_down, eat]


if __name__ == "__main__":

	from test import *

	# abbreviations for objects
	M, B, C, R1, R2, R3 = "Monkey", "Banana", "Crate", "Room 1", "Room 2", "Room 3"

	# create initial beliefs
	beliefs = (
		Monkey(M), Banana(B), Crate(C),
		Low(M), Low(C), High(B),
		Room(R1), Room(R2), Room(R3),
		At(M, R1), At(B, R2), At(C, R3)
	)
	print_all("Initial Beliefs", beliefs)
	
	# Monkey wants Banana. Plan length 9
	# Iterative Deepening: 13498 steps, w/ pruning 289
	# Serial Decomposition: 1775 steps, w/ pruning 259
	# Breadth-First Search:    ? steps, w/ pruning  30
	# SD-Breadth-First Search: ? steps, w/ pruning  23
	goal = And(Happy(M), At(M, R1))
	plan = search_plan(goal, beliefs, actions, False, True)
	if plan != None:
		print_all("Plan sequence for goal %s" % goal, [ (a.name, m) for (a, m) in plan])
		for (action, match) in plan:
			beliefs = update(beliefs, action.eff, match)
		print_all("After plan execution", beliefs)
	else:
		print("No Plan Sequence found for goal %s" % goal)

