"""Reasoning.
2010, Tobias Kuester

This module contains a number of reasoning concepts, such as matching a given
formula to the belief base, or updating the beliefs according to some rules.
"""

from knowledge import Belief, And, Or, Not, Rule


################################################################################
#                                                                              #
#   MATCHING                                                                   #
#                                                                              #
################################################################################

def find_matches(condition, beliefs, matches=[{}], negation=False):
	"""Find matches for this condition for the given beliefs. Matches is a
	list of known partial matches (e.g. from the first term in an AND clause).
	Each match is represented by a dictionary (variable -> value).
	* If there is no match for the clause in the belief base, an empty list
	  is returned.
	* If the clause matches the belief base, but no variables are involved,
	  a list holding an empty dictionary is returned.
	* Otherwise, a list holding a dictionary for each possible match of
	  variables to values is returned.
	"""
	if isinstance(condition, Belief):
		result = []
		# for each given match...
		for match in matches:
			# substitute variables according to match
			belief = substitute_variables(condition, match)
			if negation:
				# allow only matches which do not contain the fact
				# FIXME this way, a negation can only remove matches
				if not any( do_match(belief, b) for b in beliefs):
					result += [match]
			else:
				# for all matching beliefs
				for other in [ b for b in beliefs if do_match(belief, b)]:
					# assign variables, and add match to results
					# skip if the value is already bound to another variable
					m = match.copy()
					if var(belief.subj, False):
						if other.subj in m.values(): continue
						m[belief.subj] = other.subj
					if var(belief.obj, False):
						if other.obj in m.values(): continue
						m[belief.obj] = other.obj
					result += [m]
		return result
		
	elif ((isinstance(condition, And) and not negation) or 
	      (isinstance(condition, Or)  and     negation)):
		# first match condition A, then find matches also complying condition B
		# FIXME with NOT only removing matches, AND and NOR are not commutative!
		results = matches
		for cond in condition.conditions:
			results = find_matches(cond, beliefs, results, negation)
		return results
		
	elif ((isinstance(condition, And) and     negation) or 
	      (isinstance(condition, Or)  and not negation)):
		# find matches for both conditions, then return union
		results = []
		for cond in condition.conditions:
			new_matches = find_matches(cond, beliefs, matches, negation)
			results += [m for m in new_matches if m not in results]
		return results
		
	elif isinstance(condition, Not):
		# find match for negation of condition
		return find_matches(condition.cond, beliefs, matches, not negation)



################################################################################
#                                                                              #
#   BELIEF REVISION                                                            #
#                                                                              #
################################################################################

def update(beliefs, condition, match={}, negation=False):
	"""Update the beliefs by adding and removing beliefs according to the given
	condition. If a match is given, variables in the condition are substituted
	accordingly prior to updating the beliefs. All changes are applied to a copy
	of the given beliefs.
	"""
	if match:
		condition = substitute_variables(condition, match)
	if isinstance(condition, Belief):
		beliefs = list(beliefs)
		if condition in beliefs and negation:
			# remove condition from beliefs
			# XXX if there are variables in the Belief, remove all matches?
			beliefs.remove(condition)
		elif condition not in beliefs and not negation:
			# add condition to beliefs
			# XXX what to do if there are still variables in the condition?
			beliefs.append(condition)
		return beliefs
		
	elif isinstance(condition, And) or isinstance(condition, Or):
		# update both condition
		# XXX for OR and NAND, updating one of the condition would be enough
		updated = beliefs
		for cond in condition.conditions:
			updated = update(updated, cond, {}, negation)
		return updated
		
	elif isinstance(condition, Not):
		# update condition with negation
		return update(beliefs, condition.cond, {}, not negation)


def deduce(beliefs, *rules):
	"""Apply the given Rules to the Beliefs by finding matches for their
	preconditions and updating the beliefs according to the preconditions with
	the matches. The deduction will be repeated until no new facts could be
	deduced. Like update, this method will not alter the original list of
	beliefs but create an updated copy instead.
	"""
	beliefs = list(beliefs)
	has_new_beliefs = True
	while has_new_beliefs:
		has_new_beliefs = False
		for rule in rules:
			# for each match, update beliefs with effect
			matches = find_matches(rule.pre, beliefs)
			for match in matches:
				new_beliefs = update(beliefs, rule.eff, match)
				has_new_beliefs |= beliefs != new_beliefs
				beliefs = new_beliefs
	return beliefs



################################################################################
#                                                                              #
#   HELPER FUNCTIONS                                                           #
#                                                                              #
################################################################################

def wildcard(name):
	"""Check whether a name is a wildcard. A wildcard can have any value, even
	one already assigned to another variable, and a wildcard's value is not
	stored in the match.
	"""
	return name == "*"


def var(name, allow_wildcard=True):
	"""Check whether a name is a variable. All lower-case strings are 
	considered a variable. If the respecive parameter is set, a wildcard
	is considered a variable, too (default).
	"""
	return ((type(name) == str and name.islower()) 
			or (allow_wildcard and wildcard(name)))


def has_variables(condition):
	"""Check and return whether the given condition has variable terms in it.
	"""
	if isinstance(condition, Belief):
		return var(condition.subj) or var(condition.obj)
	if isinstance(condition, And) or isinstance(condition, Or):
		return any(has_variables(cond) for cond in condition.conditions)
	if isinstance(condition, Not):
		return has_variables(condition.cond)


def do_match(belief_1, belief_2):
	"""Check whether belief_1 could match belief_2, i.e. both beliefs must have
	the same predicate, and for both subject and object, belief_1 must have a
	variable or the same value as belief_2.
	"""
	return ( belief_1.pred == belief_2.pred and 
	         ( (var(belief_1.subj) or belief_1.subj == belief_2.subj) and
	           (var(belief_1.obj ) or belief_1.obj  == belief_2.obj) ) )


def substitute_variables(condition, match):
	"""Substitute Variables in given belief according to match. The condition is
	not altered; instead a copy with the variables being replaces is created.
	"""
	if isinstance(condition, Belief):
		subj, obj = condition.subj, condition.obj
		subj = match[subj] if var(subj) and subj in match else subj
		obj  = match[obj]  if var(obj)  and obj  in match else obj
		return Belief(condition.pred, subj, obj)
		
	if isinstance(condition, And) or isinstance(condition, Or):
		conditions = (substitute_variables(cond, match) for cond in condition.conditions)
		return And(*conditions) if isinstance(condition, And) else Or(*conditions)
		
	if isinstance(condition, Not):
		return Not(substitute_variables(condition.cond, match))

