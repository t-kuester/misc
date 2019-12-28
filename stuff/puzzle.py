"""
Puzzle solver, 2019, Tobias Kuester

Made this for solving a particularly difficult wooden puzzle I had some problems
with, but also made it more generic so it can be used for similar puzzles where
differently shaped wooden blocks have to be put together to for some rectangular
shape. The first version was not finding a solution even after 2h of running
time and 170k tested combinations; later found solution after a few minutes and
18k combs (lucky run?); using sorted for deterministic results, now the solution
is reliably found after a few seconds and 2.6k combinations.

TODO
- use classes?

PERFORMANCE
- ~10% faster without debuging path and assuming infinite pieces
- ~20% faster without printing in each expansion
- ~10% faster without namedtuple
- MAX_ITER=100:  0.6 sec,  38k fits
- MAX_ITER=1000: 4.5 sec, 166k fits
"""
 
from functools import partial
from collections import namedtuple
import time

MAX_ITER = None

# representation of the "Space" available for the blocks, and current blocks
Space = namedtuple("Space", "x y z field")

# representation of a single piece, with prototype and individual blocks
Piece = namedtuple("Piece", "kind pos")


def rotations(piece):
    """Create all rotations of a given piece around all three axes; rotations
    are returnedas a set, so duplicates are removed. Rotations retain the "kind"
    attribute of the original piece. Cacheable, but actually not needed.
    """
    def rot(x,y):
        return ((x,y), (-y,x), (-x,-y), (y,-x))
    def rotate(point):
        x, y, z = point
        return ((x4, y4, z3) for y2, z2 in rot(y, z)
                             for x3, z3 in rot(x, z2)
                             for x4, y4 in rot(x3, y2))
    return [Piece(piece.kind, tuple(t)) for t in set(zip(*map(rotate, piece.pos)))]

def translations(piece, where):
    """Create all translations of a piece around a certain position `where`, 
    i.e. all translations in which the piece in some way covers that position.
    """
    wx, wy, wz = where
    return [Piece(piece.kind, tuple((wx+x-px, wy+y-py, wz+z-pz) for (x,y,z) in piece.pos))
            for (px, py, pz) in piece.pos]

def all_possibilities(space, pieces):
    """Get all possibilities (rotations and translations) of where to fit the
    given pieces into the positions in the puzzle space.
    """
    return {where: {trans for piece in pieces 
                          for rot in rotations(piece)
                          for trans in translations(rot, where)
                          if fits(space, trans)}
                    for where in empty_positions(space)}


fits_count = 0
def fits(space, piece):
    """Check whether the given piece (in a certain rotation and translation) 
    fits into the space given the space's current layout. This accounts for most
    of the work in the algorithm and thus comes with an invocation counter.
    """
    global fits_count
    fits_count += 1
    X, Y, Z, F = space # ~20% faster
    return all(0 <= x < X and  0 <= y < Y and  0 <= z < Z and 
               F[x][y][z] == 0 for (x,y,z) in piece.pos)

def place(space, piece, symbol):
    """Set the position in the space corresponding to the piece to the given
    symbol; later, the symbol shows where which piece should be. For resetting
    the space, use symbol `0`.
    """
    for (x, y, z) in piece.pos:
        space.field[x][y][z] = symbol

def num_poss(poss, x):
    """Shorthand for number of possibilities, for sorting."""
    return len(poss[x])

def get_possibilities(space, available, last_poss):
    """Determine possible piece placements for each position in the puzzle space.
    This has the greatest potential for improvement. Currently, it uses last
    turn's possibilities for restricting those further, aborting early if any
    position has no possibilities, or "fast-forwarding" if the current position
    has already more than the currently most constrained one.
    """
    possibilities = {}
    best = max(map(len, last_poss.values())) # XXX why does min not work here?
    for where in sorted(empty_positions(space), key=partial(num_poss, last_poss)):
        possibilities[where] = set()
        for piece in last_poss[where]:
            if len(possibilities[where]) > best or \
                    available[piece.kind] and fits(space, piece):
                possibilities[where].add(piece)
        best = min(best, len(possibilities[where]))
        if not possibilities[where]:
            break
    return possibilities

count = 0
def find_solution(space, pieces, available, last_poss, n=1, path=[]):
    """Simple most-constrained-first backtracking algorithm. Get possible piece
    placements for each position in the puzzle (reusing posibilities from last
    turn for fewer calculations), then testing the possibilities of the most
    restricted position one after the other, or backtracking no more possible.
    """
    global count
    count += 1
    print(count, n, *path)
    if MAX_ITER and count > MAX_ITER: return

    possibilities = get_possibilities(space, available, last_poss)

    # if none, return solution
    if not possibilities:
        return True
    else:    
        # find position with fewest possibilities
        where = min(possibilities, key=partial(num_poss, possibilities))
        # test all such possibilities (sorted for reproducibility of results)
        for i, piece in enumerate(sorted(possibilities[where]), start=1):
            # apply piece by setting the fields in space to some increasing number
            place(space, piece, n)
            available[piece.kind] -= 1
            path.append("%d/%d" % (i, len(possibilities[where])))
            # recurse
            if find_solution(space, pieces, available, possibilities, n+1, path):
                return True
            # reset fields to zero
            place(space, piece, 0)
            available[piece.kind] += 1
            path.pop()
    return False
    
    
def create_space(x, y, z):
    """Helper for initializing a new puzzle space with given dimensions."""
    return Space(x, y, z, [[[0 for _ in range(z)] for _ in range(y)] for _ in range(x)])

def empty_positions(space):
    """Helper for getting all empty positions in the given puzzle space."""
    return {(x, y, z) for x in range(space.x) 
                      for y in range(space.y)
                      for z in range(space.z)
                      if space.field[x][y][z] == 0}

def print_space(space):
    """Print the different levels of the space, one after the other."""
    for i, level in enumerate(space.field):
        print("--- %d ---" % i)
        for line in level:
            print(*map("{:2d}".format, line))


def main():
    """Main: Create representaition of the puzzle and run the algorithm.
    """
    pieces = [Piece(1, ((0,0,0),(0,0,1),(0,0,2),(0,0,3),(0,1,2)))]
    available = {1: 25}
    space = create_space(5, 5, 5)

    start = time.time()
    try:
        if find_solution(space, pieces, available, all_possibilities(space, pieces)):
            print("SOLUTION FOUND")
            print_space(space)
        else:
            print("NO SOLUTION FOUND")
    except KeyboardInterrupt:
        print("aborted")
    print("time", time.time() - start)
    print("calls to fits", fits_count)

if __name__ == "__main__":
    main()
