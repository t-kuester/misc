"""Family Example.
2010, Tobias Kuester

The usual family example, featuring lots of Deduction Rules.
"""

from knowledge import *
from reasoning import *
from planning  import *

# define Person class
class Person:
	"""Person class.
	
	This Object is what this scenario is all about. Persons have a name, a 
	gender, and (optionally) a number of parents (should be no more than two).
	"""
	
	def __init__(self, name, gender, *parents):
		self._name = name
		self.gender = gender
		self.parents = parents
		
	def __repr__(self):
		# return "Person(%r, %r, %r)" % (self._name, self.gender, self.parents)
		return self._name
	

# define shortcuts for core beliefs, derived directly from objects
IsPerson = lambda subj:      Belief("Person", subj)
Parent   = lambda subj, obj: Belief("parents", obj, subj) # swap subj and obj for readability
Name     = lambda subj, obj: Belief("name", subj, obj)
Gender   = lambda subj, obj: Belief("gender", subj, obj)

# define shortcuts for additional beliefs
Mother    = lambda subj, obj: Belief("mother", subj, obj)
Father    = lambda subj, obj: Belief("father", subj, obj)
Sibling   = lambda subj, obj: Belief("sibling", subj, obj)
OnlyChild = lambda subj:      Belief("only_child", subj)
Brother   = lambda subj, obj: Belief("brother", subj, obj)
Sister    = lambda subj, obj: Belief("sister", subj, obj)
Uncle     = lambda subj, obj: Belief("uncle", subj, obj)
Aunt      = lambda subj, obj: Belief("aunt", subj, obj)
Gramps    = lambda subj, obj: Belief("gramps", subj, obj)
Granny    = lambda subj, obj: Belief("granny", subj, obj)


# define shortcuts for variables and constants
x, y, z, _ = "x", "y", "z", "*"
M, W = "Male", "Female"

# define deduction rules	            
rules = []
rules += [ Rule(pre=And(Parent(x, y), Gender(x, M)),      eff=Father(x, y))  ]
rules += [ Rule(pre=And(Gender(x, W), Parent(x, y)),      eff=Mother(x, y))  ]
rules += [ Rule(pre=And(Parent(z, x), Parent(z, y)),      eff=Sibling(x, y)) ]
rules += [ Rule(pre=And(IsPerson(x), Not(Sibling(x, y))), eff=OnlyChild(x))  ]
rules += [ Rule(pre=And(Sibling(x, y), Gender(x, M)),     eff=Brother(x, y)) ]
rules += [ Rule(pre=And(Sibling(x, y), Gender(x, W)),     eff=Sister(x, y))  ]
rules += [ Rule(pre=And(Brother(x, z), Parent(z, y)),     eff=Uncle(x, y))   ]
rules += [ Rule(pre=And(Sister(x, z), Parent(z, y)),      eff=Aunt(x, y))    ]
rules += [ Rule(pre=And(Father(x, z), Parent(z, y)),      eff=Gramps(x, y))  ]
rules += [ Rule(pre=And(Mother(x, z), Parent(z, y)),      eff=Granny(x, y))  ]


# testing
if __name__ == "__main__":
	from test import *

	# create Person objects
	abe       = Person("Abraham Simpson", M)
	mona      = Person("Mona Simpson", W)
	homer     = Person("Homer Simpson", M, abe, mona)
	herbert   = Person("Herbert Simpson", M, abe, mona)
	jaqueline = Person("Jaqueline Bouvier", W)
	marge     = Person("Marge Simpson", W, jaqueline)
	patty     = Person("Patty Bouvier", W, jaqueline)
	selma     = Person("Selma Bouvier", W, jaqueline)
	bart      = Person("Bart Simpson", M, homer, marge)
	lisa      = Person("Lisa Simpson", W, homer, marge)
	maggie    = Person("Maggie Simpson", W, homer, marge)

	persons = (abe, mona, homer, herbert, jaqueline, marge, patty, selma, bart, lisa, maggie)

	# create initial beliefs from objects
	core_beliefs = create_beliefs(*persons)
	print_all("Initial Beliefs", core_beliefs)

	# apply deduction rules to initial beliefs	
	beliefs = deduce(core_beliefs, *rules)
	print_all("Inferred Beliefs", [b for b in beliefs if b not in core_beliefs])

	# test some predicates
	test(Uncle(x, y), beliefs)
	test(And(IsPerson(x), Not(Uncle(_, x))), beliefs)
	test(Father(x, y), beliefs)
	test(Sibling(bart, x), beliefs)
