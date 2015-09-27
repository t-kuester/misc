"""Algorithms to determine the difference between two strings or other sequence
types. Can be used to find the Levenshtein distance between words, but also in
the more general case of comparing any kind of sequence, with arbitrary functions
for determining whether two elements are equal (or however 'matching') and what
to use as the substitution cost.

Tobias Kuester, 2014
"""

import operator
from itertools import product

def diff(s1, s2, match=operator.eq, neutral="*", subst=1):
    """Determine difference, or minimum edit distance, between two strings,
    or arbitrary sequence objects.
    @param s1, s2: the two strings or lists to match
    @param match: function to determine whether two elements match up
    @param neutral: 'neutral' element for padding
    @param subst: substitution costs
    @return the total edit cost and the "edit path"
    """
    s1, s2 = neutral + s1, neutral + s2
    
    # setup edit matrix
    A = [[0] * len(s2) for _ in range(len(s1))]
    
    # calculate edit distance / sequence match with DP
    for i, k in product(range(len(s1)), range(len(s2))):
        if min(i, k) == 0:
            A[i][k] = max(i, k)
        else:
            diag = 0 if match(s1[i], s2[k]) else subst
            A[i][k] = min(A[i-1][k-1] + diag,
                          A[i  ][k-1] + 1,
                          A[i-1][k  ] + 1)
    
    # reconstruct path
    path, i, k = [], len(s1)-1, len(s2)-1
    while i > 0 or k > 0:
        if A[i][k] == A[i][k-1] + 1:
            path = [+1] + path
            k = k-1
        elif A[i][k] == A[i-1][k] + 1:
            path = [-1] + path
            i = i-1
        else:
            path = [0] + path
            i, k = i-1, k-1
    
    return A[-1][-1], path


def align_match(list1, list2, path):
    """Reconstruct the matching elements from the two sequences and the path.
    """
    i1, i2 = iter(list1), iter(list2)
    for p in path:
        if p == -1: print("DEL     %20r"      %  next(i1)           )
        if p ==  0: print("EQ/SUB  %20r %20r" % (next(i1), next(i2)))
        if p == +1: print("INS     %41r"      %            next(i2) )


# testing
if __name__ == "__main__":

    # with strings
    word1, word2 = "INTENTION", "EXECUTION"
    x, path = diff(word1, word2)
    print(x, path)
    align_match(word1, word2, path)

    print()

    # with lists
    list1 = [[['B', 10], 1], [['C', 15], 1], [['F', 30], 1]]
    list2 = [[['G', 20], 2], [['D', 25], 1]]
    x, path = diff(list1, list2, match=lambda x, y: x[1] == y[1], neutral=[[None, -1]])
    print(x, path)
    align_match(list1, list2, path)
