
def rabin_miller(n):
	if n == 2 or n == 3: return True
	if n <= 1 or n % 2 == 0: return False
	d, r = n-1, 0
	while d % 2 == 0:
		d, r = d//2, r+1
	for a in (2, 3):
		x = a**d % n
		if x in (1, n - 1): continue
		for _ in range(r-1):
			x = x**2 % n
			if x == n - 1: break
		else:
			return False
	return True

def prime(n):
	return n >= 2 and all(n%i for i in range(2, int(n**.5)+1))

import random
for n in range(10000):
	r = rabin_miller(n)
	p = prime(n)
	if r != prime(n):
		print(n, r, p)
