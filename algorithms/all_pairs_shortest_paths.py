"""Algorithms for computing all pairs' shortest paths.
- Bellman-Ford Algorithm
- Floyd-Warshall Algorithm
- Johnson's Algorithm
- Dijkstra's Algorithm
"""

from itertools import product
from heapq import heappop, heappush

INF = 10**9
NEAR_INF = 10**8


def bellman_ford(graph, source):
	"""Bellman-Ford algorithm for finding minimum path length from source to all
	other nodes (allowing for negative edge length). Graph is a dictionary mapping
	nodes of the graph to dictionaries of their successor-nodes and their costs.
	"""
	# invert graph, so we can easily find incoming edges from newly added nodes
	incoming = swap_graph(graph)
	
	# initialize subproblem matrix (only for direct predecessor layer)
	A = {node: (0 if node == source else INF) for node in incoming}
	B = A.copy() # backup holding the previous iteration
	
	# solve subproblems
	for i in range(len(graph)):
		# swap current and backup
		A, B = B, A
		
		# compute next iteration
		for node in incoming:
			case1 = B[node]
			case2 = min(B[e] + ce for (e, ce) in incoming[node].items()) \
					if incoming[node] else INF
			A[node] = min(case1, case2)
			
	# detect negative cycles!
	if sum(A.values()) != sum(B.values()):
		raise Exception("Negative Cycle Detected")
	
	return A
	

def floyd_warshall(graph):
	"""Floyd-Warshall's All-pairs shortest path algorithm.
	Graph is dict(node -> dict(node -> cost)) which can have negative edge
	length.  Negative cycles are detected and result in an Exception.
	Slow for large graphs! O(n^3)
	"""
	# set up subproblem matrix (for one step only) and base cases
	# simple dict of tuples would work, too, but this way the result is more readable
	A = {}
	for i in graph:
		A[i] = {j: (0 if i == j else graph[i][j] if j in graph[i] else INF) 
		        for j in graph}
	B = {n: A[n].copy() for n in A} # backup holding the previous iteration

	for k in graph:
		# swap current and backup
		A, B = B, A

		# build new matrix A based on last iteration (B)
		for i, j in product(graph, graph):
			case1 = B[i][j]            # path from i to j w/o k
			case2 = B[i][k] + B[k][j]  # path from i to j via k
			A[i][j] = min(case1, case2)
			
	# detect negative cycles!
	if any(A[i][i] < 0 for i in graph):
		raise Exception("Negative Cycle Detected")
		
	return A


def johnson(graph):
	"""Johnson's Graph-Reweighting Algorithm. Modifies directed graphs with 
	negative edge length so that Dijkstra's Algorithm can be applied.
	"""
	# neuer knoten mit edge mit cost 0 zu jedem anderen knoten
	dummy = "JOHNSON"
	graph_johnson = graph.copy()
	graph_johnson[dummy] = {n: 0 for n in graph}
	
	# einmal bellman-ford laufen lassen
	P = bellman_ford(graph_johnson, dummy)
	del P[dummy]
	
	# edge-weights anpassen
	graph_dijkstra = {i: {j: graph[i][j] + P[i] - P[j] for j in graph[i]} 
	                  for i in graph}
	
	# n mal dijkstra laufen lassen, ergebnis zusammenbauen
	shortest_paths = {}
	for i in graph:
		res = dijkstra(graph_dijkstra, i)
		shortest_paths[i] = {j: c-P[i]+P[j] for (j, c) in res.items()}
		
	return shortest_paths
	

def dijkstra(graph, source):
	"""Simplified version of Dijskstra's Agorithm for application in Johnson's
	Algorithm. This version does not return the actual path, but only the minimum
	path cost from source to each other node in graph.
	"""
	heap = [(0, source)]
	best = {source: 0}
	while heap:
		(b, i) = heappop(heap)
		for (j, c) in graph[i].items():
			if j not in best or best[j] > b+c:
				heappush(heap, (b+c, j))
				best[j] = b+c
	return best
	

def swap_graph(graph):
	"""Helper-function for swapping a directed graph."""
	incoming = {}
	for i in graph:
		incoming[i] = {}
	for i in graph:
		for j in graph[i]:
			incoming[j][i] = graph[i][j]
	return incoming


def print_graph(graph):
	"""Helper-function for pretty-printing graph."""
	for node in graph:
		print(node, sorted(graph[node].items()))


def filter_inf(graph):
	"""Filter out pseudo-inifinite values from result matrix."""
	return {i: {j: c for (j, c) in graph[i].items() if c < NEAR_INF}
	        for i in graph}

# testing
if __name__ == "__main__":
	graph = {"a": {"b": -2},
	         "b": {"c": -1},
	         "c": {"a": 4, "x": 2, "y": -3},
	         "x": {},
	         "y": {},
	         "z": {"x": 1, "y": -4}}
 
	print("\nBELLMAN-FORD")
	res = bellman_ford(graph, "a")
	print(res)

	print("\nFLOYD-WARShALL")
	res = floyd_warshall(graph)
	print_graph(filter_inf(res))
	
	print("\nJOHNSON")
	res = johnson(graph)
	print_graph(res)
	print("Shortest shortest path:", min(min(r.values()) for r in res.values()))
