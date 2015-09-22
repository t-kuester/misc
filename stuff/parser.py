"""Parser for simple mathematical expressions in prefix or postfix notation.
"""

def parse(stack):
	"""Parse the given list of arguments and operations, return result.
	"""
	token = stack.pop()
	if token == "add":
		return parse(stack) + parse(stack)
	if token == "sub":
		return parse(stack) - parse(stack)
	if token == "mul":
		return parse(stack) * parse(stack)
	if token == "div":
		return parse(stack) / parse(stack)
	return float(token)


# testing
if __name__ == "__main__":
	MODE = ("postfix", "prefix")
	prefix = True
	while True:
		
		# read inputs
		stack = input("Enter expression in %s form: " % MODE[prefix]).split()
		
		# reversed: prefix; default: postfix
		if prefix:
			stack.reverse()

		# parse and present result
		print("Result: ", parse(stack))
