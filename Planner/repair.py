from knowledge import *
from reasoning import *
from planning  import *

Machine = lambda a: Belief("Machine", a)
Socket = lambda a: Belief("Socket", a)
Board = lambda a: Belief("Board", a)
Cable = lambda a: Belief("Cable", a)

has_socket = lambda a,b: Belief("has_socket", a, b)
connected = lambda a,b: Belief("connected", a, b)
in_socket = lambda a,b: Belief("in_socket", a, b)

broken = lambda a: Belief("broken", a)
locked = lambda a: Belief("locked", a)
powered = lambda a: Belief("powered", a)

# define shortcuts for some variables
x, y, z, _ = "x", "y", "z", "*"

# define available actions
# TODO handle cables

turn_on = Action("Turn On",
				pre=And(Machine(x), Socket(y), Not(And(has_socket(x,y), Not(locked(y))))),
				eff=powered(x))
turn_off = Action("Turn Off",
				pre=And(Machine(x), powered(x)),
				eff=Not(powered(x)))
lock = Action("Lock",
				pre=And(Socket(x), Not(locked(x))),
				eff=locked(x))
unlock = Action("Unlock",
				pre=And(Socket(x), locked(x), Machine(y), Not(powered(y))),
				eff=Not(locked(x)))
insert = Action("Insert",
				pre=And(Socket(x), Board(y), Not(in_socket(_, x)), Not(locked(x))),
				eff=in_socket(y, x))
remove = Action("Remove",
				pre=And(Socket(x), Board(y), in_socket(y, x), Not(locked(x))),
				eff=Not(in_socket(y, x)))

actions = [turn_on, turn_off, lock, unlock, insert, remove]

if __name__ == "__main__":
	from test import *

	# abbreviations for objects
	M, S, B, B2, C1, C2, C3, C4 = "Machine Socket Board1 Board2 Cable1 Cable2 Cable3 Cable4".split()

	# create initial beliefs
	beliefs = (
		Machine(M), Socket(S), Board(B), Board(B2), 
		# ~ Cable(C1), Cable(C2), Cable(C3), Cable(C4),
		has_socket(M, S), in_socket(B, S),
		powered(M), locked(S), broken(B), 
		# ~ connected(C1, B), connected(C2, B), connected(C3, B), connected(C4, B)
	)
	print_all("Initial Beliefs", beliefs)

	goal = And(powered(M), in_socket(x, _), Not(broken(x)))
	plan = search_plan(goal, beliefs, actions, False, True)
	if plan != None:
		print_all("Plan sequence for goal %s" % goal, [ (a.name, m) for (a, m) in plan])
		for (action, match) in plan:
			beliefs = update(beliefs, action.eff, match)
		print_all("After plan execution", beliefs)
	else:
		print("No Plan Sequence found for goal %s" % goal)

