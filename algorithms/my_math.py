"""Some random mathematical helper functions.
"""

from __future__ import division, print_function
import math


# STATISTICS

def mean(L):
	"""Calculate mean of given List"""
	return sum(L) / len(L)
	
def variance(L, is_sample=0):
	"""calculate variance (or sample variance) of given List"""
	m = mean(L)
	return sum((x-m)**2 for x in L) / (len(L) - is_sample)
	
def std_dev(L, is_sample=0):
	"""calculate standard deviation of given List"""
	return math.sqrt(variance(L, is_sample))

def z_score(num, mean, std_dev):
	"""calculate z-score given sample size, mean and standard deviation"""
	return (num - mean) / std_dev


# COMBINATORICS

def fac(n):
	assert n >= 0
	return n if n <= 2 else fac(n - 1) * n

def over(n, k):
	"""n over k"""
	return fac(n) // fac(n-k)

def coin(coins, heads):
	"""Probability for given number of heads (or tails) when throwing given
	number of fair coins."""
	return Fraction(int(fac(c) / fac(c-n) / fac(n)), 2**c)

def pick_grom_group(group, other, selected):
	"""When selecting 'selected' number of individuums from 'group' and 'other',
	return probability that all are from 'group'."""
	return Faction(over(group, selected), over(group + other, selected))

def unfair_coins(num_coins, num_unfair, percent_unfair, heads_needed):
	"""Calculate probability for pulling a coin from a bag with fair and unfair
	coins and flipping it a number of times, each time coming up heads."""
	part_fair = (num_coins - num_unfair) / num_coins
	part_unfair = num_unfair / num_coins
	prob_fair = 0.5**heads_needed
	prob_unfair = (percent_unfair / 100)**heads_needed
	return part_fair * prob_fair + part_unfair * prob_unfair


# GEOMETRY

def herons_formula(a, b, c):
	"""Calculate area of triangle with sides a, b, and c."""
	print("sqrt(s*(s-a)*(s-b)*(s-c)) with s = (a + b + c)/2")
	s = (a + b + c) / 2
	return math.sqrt(s * (s-a) * (s-b) * (s-c))
	
def area_equilat(side):
	"""Area of equilateral triangle."""
	return side/2 * math.sqrt(side**2 - (side/2)**2)


# LINEAR ALGEBRA

def inv(a,b,c,d):
	"""Inverse of 2x2 matrix."""
	det = a*d-b*c
	m = lambda x: fractions.Fraction(x, det)
	return map(str, map(m, [d, -b, -c, a]))

def det2(m):
	"""Determinant of 2x2 matrix."""
	(a,b), (c,d) = m
	return a*d - b*c

def det3(m):
	"""Determinant of 3x3 matrix."""
	a, b, c = m[0]
	da = det2([ m[1][1:]        , m[2][1:]])
	db = det2([[m[1][0],m[1][2]],[m[2][0],m[2][2]]])
	dc = det2([ m[1][:2]        , m[2][:2]])
	return a*da - b*db + c*dc


# SOME COMPLEX FORMULAS I NEVER CAN QUITE REMEMBER

def series(r, n):
	"""Calculate geometric series."""
	return (1 - r**n) / (1 - r)

def quad_form(a, b, c):
	"""Quadratic Formula: calculate values of x so that ax^2+bx+c=0."""
	sq = math.sqrt(b**2 - 4 * a * c)
	x1 = (-b - sq) / (2 * a)
	x2 = (-b + sq) / (2 * a)
	return (x1, x2)

def master_method(a, b, d):
	"""Estimate Complexity using Master Method, print result."""
	if a == b**d:
		print("Case 1: a = b^d")
		print("-> O(n^%d log n)" % d)
	elif a < b**d:
		print("Case 2: a < b^d")
		print("-> O(n^%d)" % d)
	elif a > b**d:
		print("Case 3: a > b^d")
		print("-> O(n^log%d(%d))" % (b, a))
		print(" = O(n^%.2f)" % math.log(a, b))

