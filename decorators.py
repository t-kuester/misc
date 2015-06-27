"""A Collection of Function Decorators.

by Tobias Kuester

This module provides a number of useful function decorators for e.g. caching
values, for creating debugging stack traces, or even for type-checking.

See also: http://wiki.python.org/moin/PythonDecoratorLibrary
"""

import copy

def decorator(deco):
	"""Meta-Decorator, having the effect that decorated functions retain their
	original function name (plus decorators), doc, and attributes."""
	def _deco(f):
		f_new = deco(f)
		f_new.__name__ = "%s(%s)" % (deco.__name__, f.__name__)
		f_new.__doc__ = f.__doc__
		f_new.__dict__.update(f.__dict__)
		return f_new
	return _deco

@decorator
def memo(f):
	"""Function Decorator for momoizing results for certain parameters. Once a
	function has been called with some parameters, the result value is stored
	in a map and future calls with the same parameters can use that value."""
	f.cache = {}
	def _f(*args, **kwargs):
		if args not in f.cache:
			f.cache[args] = f(*args, **kwargs)
		return f.cache[args]
	return _f

@decorator
def trace(f):
	"""Function Decorator for tracing call hierarchies. When a function with
	this decorator is called, a line is printed telling the function name and the
	parameters, and when the function returns a similar line is printed showing
	the results. Lines are indented to show the depth in the call hierarchy."""
	trace.depth = 0
	def _f(*args, **kwargs):
		print "  " * trace.depth, ">", f.__name__, args, kwargs if kwargs else ""
		trace.depth += 1
		res = f(*args, **kwargs)
		trace.depth -= 1
		print "  " * trace.depth, "<", res
		return res
	return _f

@decorator
def varargs(f):
	"""Function Decorator that makes every two-parameter-function a varargs
	function by using reduce."""
	def _f(*args):
		return reduce(f, args)
	return _f
	
@decorator
def deprecated(f):
	"""Function Decorator, printing a warning when a function with this decorator
	is called."""
	def _f(*args, **kwargs):
		print "WARNING: Call to deprecated function", f.__name__, args
		return f(*args, **kwargs)
	return _f

#@decorator # meta-decorator not working here
def typecheck(*types, **kwtypes):
	"""Function Decorator providing limited type checking. Parameters to the 
	function will be checked to comply to the types given in the decorator."""
	def __f(f):
		def _f(*args, **kwargs):
			for a, t in zip(args, types):
				if not isinstance(a, t):
					print "WARNING: Expected", t, "got", a
			for k, a in kwargs.items():
				if k in kwtypes and not isinstance(a, kwtypes[k]):
					print "WARNING: Expected", kwtypes[k], "got", a
			return f(*args, **kwargs)
		return _f
	return __f

@decorator
def pass_by_value(f):
	"""Function decorator creating another version of the function first
	deep-copying all the parameters.
	"""
	def _f(*args, **kwargs):
		args_copied = copy.deepcopy(args)
		kwargs_copied = copy.deepcopy(kwargs)
		return f(*args_copied, **kwargs_copied)
	return _f

@decorator
def keep_trying(f):
	def _f(*args, **kwargs):
		while True:
			try:
				return f(*args, **kwargs)
			except Exception as e:
				print e, "trying again..."
	return _f
	
# TODO other ideas:
# synchronized function calls
# invocation counter
# timing
# currying


# Testing

if __name__ == "__main__":

	@trace
	@memo
	def fib(n):
		"""Simple Fibonacci function, for testing."""
		if n == 3: return fib2(n)
		return fib(n-1) + fib(n-2) if n > 1 else n

	@trace
	def fib2(n):
		print "FOOOO"
		return fib(n-1) + fib(n-2) if n > 1 else n
		
	fib(10)

	print fib.__name__
	print fib.__doc__
	print fib.cache

	@trace
	@memo
	def a(n):
		return "A"
		
	@trace
	@memo
	@deprecated
	def b(n):
		return "B"

	a(42)
	b(42)
	
	@trace
	@varargs
	def add(a, b):
		return a + b
		
	add(1, 2)
	add(*range(10))
	
	@typecheck(int, str, c=int)
	def foo(a, b, c):
		pass	
	
	foo(42, "bar", 0)
	foo(42., None, c="blub")
	
