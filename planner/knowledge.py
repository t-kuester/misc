"""Knowledge
2010, Tobias Kuester

This module contains basic knowledge representation concepts for a simple AI 
framework.
"""


class Belief:
	"""Belief class.
	
	A Belief is a tuple of Subject, Predicate, Object.
	Examples: Belief("is_block", "block_A"), Belief("is_on", "block_A", "block_B")
	"""

	def __init__(self, pred, subj, obj=None):
		"""Create new Fact with predicate, subject and (optional) object."""
		self.pred = pred
		self.subj = subj
		self.obj = obj
		
	def __repr__(self):
		"""Print Belief as 'pred(subj[, obj])'."""
		if self.obj == None:
			return "%s(%s)" % (self.pred, self.subj)
		else:
			return "%s(%s, %s)" % (self.pred, self.subj, self.obj)
			
	def __eq__(self, other):
		"""Beliefs are equal, if pred, subj, and obj are equal."""
		return (type(self) == type(other) 
				and (self.pred, self.subj, self.obj) == (other.pred, other.subj, other.obj))
	
	def __hash__(self):
		"""return Belief's hash as a combination of the hashes of its parts."""
		return hash(self.pred) + (2 * hash(self.subj)) + (4 * hash(self.obj))


class And:
	"""Conjunction class.
	
	A Conjunction is True, if all its conditions are True.
	"""
	
	def __init__(self, *conditions):
		self.conditions = conditions

	def __repr__(self):
		return "(AND %s)" % str(self.conditions)

	def __eq__(self, other):
		return (type(self) == type(other) 
				and other.conditions == self.conditions)


class Or:
	"""Disjunction class.
	
	A Disjunction is True, if at least one of its conditions is True.
	"""

	def __init__(self, *conditions):
		self.conditions = conditions

	def __repr__(self):
		return "(OR %s)" % str(self.conditions)

	def __eq__(self, other):
		return (type(self) == type(other) 
				and other.conditions == self.conditions)


class Not:
	"""Negation class.
	
	A Negation is True, if its condition is not True.
	"""
	
	def __init__(self, cond):
		self.cond = cond

	def __repr__(self):
		return "(NOT %s)" % self.cond

	def __eq__(self, other):
		return (type(self) == type(other) 
				and other.cond == self.cond)


class Rule:
	"""Rule class.
	
	A Rule can represent many IF-THEN-like concepts: A Reasoning Rule, such as
	"if A is a bird, then A can fly", or an Action, such as "if you bump in a
	wall, go in another direction".
	"""

	def __init__(self, pre, eff):
		self.pre = pre
		self.eff = eff
		
	def __repr__(self):
		return "%s -> %s" % (self.pre, self.eff)

	def __eq__(self, other):
		return (type(self) == type(other) 
				and (self.pre, self.eff) == (other.pre, other.eff))


class Action(Rule):
	"""Action class.
	
	An Action is a special kind of Rule. Other than a normal Rule, an Action
	also has a name and an implementation. Further, while a Rule automatically
	applies, an Action has to be applied explicitly. When applied, the action's
	implementation is executed, which should yield the stated effect.
	
	When executed, the match found for the actions precondition will be used as
	keyword-parameters for the implementation, so the precondition's variables
	have to match the implementation's parameter names!
	"""

	def __init__(self, name, pre, eff, implementation=None):
		Rule.__init__(self, pre, eff)
		self.name = name
		self.impl = implementation
		
	def __repr__(self):
		return "%s: %s" % (self.name, Rule.__repr__(self))

	def __eq__(self, other):
		return (Rule.__eq__(self, other)
				and (self.name, self.impl) == (other.name, other.impl))
	
	def execute(self, match):
		"""Execute the Action's implementation with the given match for the 
		precondition's variables.
		"""
		if callable(self.impl):
			self.impl(**match)



def create_beliefs(*objects):
	"""Create a number of Beliefs representing the given list of objects. First,
	for each object, a Belief is created in the form "Belief(<class>, <obj>)".
	Second, for each attribute (i.e. non-callable member not starting with '_')
	a Belief is created in the form "Belief(<attribute>, <obj>, <value>)".
	If the value is iterable, than one Belief is created for each item.
	"""
	beliefs = []
	for obj in objects:
		beliefs += [Belief(obj.__class__.__name__, obj) ]
		for field in dir(obj):
			value = getattr(obj, field)
			if field[0] != "_" and not callable(value):
				if hasattr(value, "__iter__"):
					beliefs += [ Belief(field, obj, v) for v in value ]
				else:
					beliefs += [ Belief(field, obj, value) ]
	return beliefs


# callable was temporarily removed in Python 3.1... ugly hack to restore it
try:
	callable
except NameError:
	def callable(obj):
		try:
			obj.__call__
			return True
		except AttributeError:
			return False