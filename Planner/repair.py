from knowledge import *
from reasoning import *
from planning  import *

Machine = lambda a: Belief("Machine", a)
Socket = lambda a: Belief("Socket", a)
Board = lambda a: Belief("Board", a)
Cable = lambda a: Belief("Cable", a)
Connector = lambda a: Belief("Connector", a)

has_socket = lambda a,b: Belief("has_socket", a, b)
has_board = lambda a,b: Belief("has_board", a, b)
has_connector = lambda a,b: Belief("has_connector", a, b)
has_cable = lambda a,b: Belief("has_cable", a, b)

broken = lambda a: Belief("broken", a)
locked = lambda a: Belief("locked", a)
powered = lambda a: Belief("powered", a)

fully_connected = lambda a: Belief("fully-connected", a)
not_connected = lambda a: Belief("not-connected", a)

# define shortcuts for some variables
u, v, w, x, y, z, _ = "uvwxyz*"

# rules
rule_fully_connected = Rule(pre=And(Board(x), 
                                    Not(And(Connector(y), 
                                            has_connector(x,y), 
                                            Not(has_cable(y, _))))),
							eff=fully_connected(x))
rule_not_connected   = Rule(pre=And(Board(x), 
                                    Not(And(Connector(y),
                                            has_connector(x,y), 
                                            has_cable(y, _)))),
							eff=not_connected(x))
rules = [rule_fully_connected, rule_not_connected]

# define available actions
turn_on = Action("Turn On",
				pre=And(Machine(x), 
				        Not(And(has_socket(x,y),
				                Not(locked(y))))),
				eff=powered(x))
turn_off = Action("Turn Off",
				pre=Machine(x),
				eff=Not(powered(x)))
lock = Action("Lock",
				pre=And(Socket(x), 
				        has_board(x, y),
				        Not(And(has_connector(y, z), 
				                Not(has_cable(z, _))))),
				eff=locked(x))
unlock = Action("Unlock",
				pre=And(Socket(x),
				        has_socket(y, x), 
				        Not(powered(y))),
				eff=Not(locked(x)))
insert = Action("Insert",
				pre=And(Socket(x),
				        Board(y),
				        Not(has_board(x, _)), 
				        Not(locked(x))),
				eff=has_board(x, y))
remove = Action("Remove",
				pre=And(Socket(x),
				        Board(y), 
				        has_board(x, y), 
				        Not(locked(x))),
				eff=Not(has_board(x, y)))
connect = Action("Connect",
				pre=And(Connector(x), 
				        Cable(y), 
				        Not(has_cable(x, _)), 
				        has_connector(z, x), 
				        Not(has_board(_, z))),
				eff=has_cable(x, y))
disconnect = Action("Disconnect",
				pre=And(Connector(x), 
				        Cable(y), 
				        has_cable(x, y), 
				        has_connector(z, x), 
				        Not(has_board(_, z))),
				eff=Not(has_cable(x, y)))

actions = [turn_on, turn_off, lock, unlock, insert, remove, connect, disconnect]

if __name__ == "__main__":
	from test import *

	# abbreviations for objects
	M, S, B1, B2, C1, C2, C3, C4 = "Machine Socket Board1 Board2 Cable1 Cable2 Cable3 Cable4".split()
	C11, C12, C13, C14, C21, C22, C23, C24 = ("Connector%d%d" % (i,j) for i in [1,2] for j in [1,2,3,4])

	# create initial beliefs
	beliefs = (
		# basics
		Machine(M), Socket(S), Board(B1), Board(B2), 
		has_socket(M, S), has_board(S, B1),
		powered(M), locked(S), broken(B1), 
		# cables and connectors
		# ~ Cable(C1), Cable(C2), Cable(C3), Cable(C4),
		# ~ Connector(C11), Connector(C12), Connector(C13), Connector(C14),
		# ~ Connector(C21), Connector(C22), Connector(C23), Connector(C24),
		# ~ has_connector(B1, C11), has_connector(B1, C12), has_connector(B1, C13), has_connector(B1, C14), 
		# ~ has_connector(B2, C21), has_connector(B2, C22), has_connector(B2, C23), has_connector(B2, C24), 
		# ~ has_cable(C11, C1), has_cable(C12, C1), has_cable(C13, C1), has_cable(C14, C1)
	)
	print_all("Initial Beliefs", beliefs)

	beliefs2 = deduce(beliefs, *rules)
	print_all("Deduced Beliefs", [b for b in beliefs2 if b not in beliefs])

	goal = And(powered(M), has_board(_, x), Not(broken(x)))
	
	plan = search_plan(goal, beliefs, actions, False, True)
	if plan != None:
		print_all("Plan sequence for goal %s" % goal, [ (a.name, m) for (a, m) in plan])
		for (action, match) in plan:
			beliefs = update(beliefs, action.eff, match)
		# ~ print_all("After plan execution", beliefs)
	else:
		print("No Plan Sequence found for goal %s" % goal)

