"""Boating Example.
2010, Tobias Kuester

Another well-known Planning Problem. Three brothers want to pass a river, one of
which is fat, the other two are slim, and there is only one boat which can hold
only either the fat guy or both the slim ones.

This problem may require rethinking the matching of NOT conditions.
"""

from knowledge import *
from reasoning import *
from planning  import *


# define shortcuts for expressing common beliefs
Slim   = lambda subj:      Belief("Slim", subj)
Fat    = lambda subj:      Belief("Fat", subj)
Boat   = lambda subj:      Belief("Boat", subj)
Side   = lambda subj:      Belief("Side", subj)
In     = lambda subj, obj: Belief("In", subj, obj)
At     = lambda subj, obj: Belief("At", subj, obj)

# define shortcuts for some variables
x, y, z, w, v, _ = "x", "y", "z", "w", "v", "*"


# define available actions
enter  = Action("Enter",
				pre=And(Boat(y), At(y, z), At(x, z)),
				eff=And(In(x, y), Not(At(x, z))))
exit  = Action("Exit",
				pre=And(Boat(y), In(x, y), At(y, z)),
				eff=And(At(x, z), Not(In(x, y))))
ride = Action("Ride",
				pre=And(Boat(x), At(x, z), Side(w), In(y, x)),
				eff=And(At(x, w), Not(At(x, z))))

actions = [enter, exit, ride]


if __name__ == "__main__":

	from test import *

	# abbreviations for objects
	S1, S2, F, B, U1, U2 = "Slim 1", "Slim 2", "Fat", "Boat", "Side 1", "Side 2"

	# create initial beliefs
	beliefs = (
		Slim(S1), Slim(S2), Fat(F), Boat(B), Side(U1), Side(U2),
		At(S1, U1), At(S2, U1), At(F, U1), At(B, U1)
	)
	print_all("Initial Beliefs", beliefs)
	
	# Get all brothers to the other side
	goal = And(At(S1, U2), At(S2, U2), At(F, U2))
	plan = search_plan(goal, beliefs, actions, False, True)
	if plan != None:
		print_all("Plan sequence for goal %s" % goal, [ (a.name, m) for (a, m) in plan])
		for (action, match) in plan:
			beliefs = update(beliefs, action.eff, match)
		print_all("After plan execution", beliefs)
	else:
		print("No Plan Sequence found for goal %s" % goal)


