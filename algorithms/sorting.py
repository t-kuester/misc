"""Different sorting algorithms and other stuff related to sorting.
Of course, there are better, faster, and thoroughly tested algorithms in every
standard library, so this is more kind of a excercise for doing it oneself,
as inspired by different Coursera and Udacity courses.
"""

import math
import random

def mergesort(L):
	"""Perform merge sort, also count inversions.
	O_t(n) = n*log(n)	O_s(n) = n*log(n)
	"""
	inv = 0
	if len(L) > 1:
		lower, upper = L[:len(L)//2], L[len(L)//2:]
		inv = mergesort(lower) + mergesort(upper)
		l = u = 0
		for i in range(len(L)):
			if l >= len(lower) or (u < len(upper) and lower[l] > upper[u]):
				L[i] = upper[u]
				u += 1
				inv += len(lower) - l
			elif u >= len(upper) or (l < len(upper) and lower[l] <= upper[u]):
				L[i] = lower[l]
				l += 1
	return inv


def is_sorted(L):
	"""Check whether the given array is in sorted order."""
	last = 0
	for n in L:
		if n < last:
			return False
		last = n
	return True


def select_random_pivot(L, start, end):
	"""Select random pivot from List between start and end index."""
	return random.randint(start, end) if end > start else start


def quicksort(L, start=0, end=-1, select=select_random_pivot):
	"""Ugly and not very intuitive, but fast, in-place (O_space(n)) Quick Sort.
	Also count comparisons.
	O_t(n) = n*log(n)	O_s(n) = n
	"""
	if end == -1: end = len(L)
	comp = 0
	if end - start > 1:
		pivot = select(L, start, end-1)
		med = partition(L, start, end, pivot)
		comp += (end-start)-1
		comp += quicksort(L, start, med, select)
		comp += quicksort(L, med+1, end, select)
	return comp


def partition(L, start, end, pivot):
	"""Partition segment of list L from start to end using element ot position
	givne by pivot. Return new position of pivot element.
	O_t(n) = n			O_s(n) = n
	"""
	L[pivot], L[start] = L[start], L[pivot]
	cur = med = start + 1
	while cur < end:
		if L[cur] < L[start]:
			L[med], L[cur] = L[cur], L[med]
			med += 1
		cur += 1
	L[start], L[med-1] = L[med-1], L[start]
	return med-1


def random_select(L, order, start=0, end=-1, select=select_random_pivot):
	"""Select ith order statistic (ith smallest element from list L (or segment
	from start to end).
	O_t(n) = n			O_s(n) = n
	"""
	if end == -1: end = len(L)
	if end - start > 1:
		pivot = select(L, start, end-1)
		med = partition(L, start, end, pivot)
		if med+1 == order:
			return L[med]
		elif med+1 > order:
			return random_select(L, order, start, med, select)
		elif med+1 < order:
			return random_select(L, order, med+1, end, select)
	else:
		return L[start]


# testing
if __name__ == "__main__":
	# create three sets of random test data
	data = [random.randint(0, 100) for _ in range(100)]
	data2 = data[:]
	data3 = data[:]
	assert is_sorted(data) == False

	# sort test data using builtin sort and own functions
	data.sort()
	quicksort(data2)
	mergesort(data3)
	assert is_sorted(data) == True
	
	# compare sorted data
	assert data == data2 == data3
