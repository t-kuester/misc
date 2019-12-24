# TODO
# test again with smaller example
# run through profiler, try to make faster
# restrict placement for first corner-piece to TWO (instead of 12)
# ~10% faster without debuging path and assuming infinite pieces
# ~20% faster without printing in each expansion
# no more caching needed when reusing old positions
# use type hints
# use classes?

from functools import lru_cache, partial
from collections import namedtuple
import time

MAX_ITER = None

Space = namedtuple("Space", "x y z field")
Piece = namedtuple("Piece", "kind pos")

@lru_cache(None)
def rotations(piece):
    def rot(x,y):
        return ((x,y), (-y,x), (-x,-y), (y,-x))
    def rotate(point):
        x, y, z = point
        return ((x4, y4, z3) for y2, z2 in rot(y, z)
                             for x3, z3 in rot(x, z2)
                             for x4, y4 in rot(x3, y2))
    return set(zip(*map(rotate, piece)))

@lru_cache(None)
def translations(piece, where):
    wx, wy, wz = where
    return [tuple((wx+x-px, wy+y-py, wz+z-pz) for (x,y,z) in piece)
            for (px, py, pz) in piece]

fits_count = 0
def fits(space, piece):
    global fits_count
    fits_count += 1
    X, Y, Z, F = space # ~20% faster
    return all(0 <= x < X and 
               0 <= y < Y and 
               0 <= z < Z and 
               F[x][y][z] == 0 for (x,y,z) in piece)

def place(space, piece, symbol):
    for (x, y, z) in piece:
        space.field[x][y][z] = symbol

def num_poss(poss, x):
    return len(poss[x])

def get_possibilities_reuse(space, pieces, last_poss):
    #MAX_ITER=100:  0.75 sec,  79k fits
    #MAX_ITER=1000: 5.06 sec, 404k fits
    possibilities = {}
    for where in sorted(empty_positions(space), key=partial(num_poss, last_poss)):
        possibilities[where] = {piece
                    for piece in last_poss[where]
                    #~if pieces[piece] > 0 
                    if fits(space, piece)}
        if not possibilities[where]:
            break
    return possibilities

NOT_CALCULATED = [None] * 9999
def get_possibilities_reuse_early_abort(space, pieces, last_poss):
    # LESS THAN EARLYABORT, BUT MORE THAN PURE REUSE
    best = None
    
    def pos_new(where):
        return ((piece, rot, pos)
                 for piece in pieces if pieces[piece] > 0
                 for rot in rotations(piece)
                 for pos in rot if fits(space, rot, pos, where))
    
    def pos_old(where):
        return ((piece, rot, pos)
                 for (piece, rot, pos) in last_poss[where]
                 if pieces[piece] > 0 if fits(space, rot, pos, where))

    def poss(where, gen):
        res = set()
        for comb in gen(where):
            res.add(comb)
            if best and len(res) >= best: return NOT_CALCULATED
        return res
    
    possibilities = {}
    for where in empty_positions(space):
        possibilities[where] = poss(where, 
                (pos_old if last_poss[where] is not NOT_CALCULATED else pos_new))
        if best is None or len(possibilities[where]) < best:
            best = len(possibilities[where])
        if best == 0:
            break
    return possibilities


count = 0
def find_solution(space, pieces, last_poss, n=1, path=[]):
    global count
    count += 1
    print(count, n, *path)
    if MAX_ITER and count > MAX_ITER: return

    possibilities = get_possibilities_reuse(space, pieces, last_poss)

    # if none, return solution
    if not possibilities:
        return True
    else:    
        # find position with fewest possibilities
        where = min(possibilities, key=partial(num_poss, possibilities))
        # test all such possibilities
        # XXX using sorted to get stable result irrelevant of tuple hashing order
        #~for i, piece in enumerate(sorted(possibilities[where]), start=1):
        for i, piece in enumerate(possibilities[where], start=1):
            # apply piece by setting the fields in space to some increasing number
            place(space, piece, n)
            #~pieces[piece] -= 1
            path.append("%d/%d" % (i, len(possibilities[where])))
            # recurse
            if find_solution(space, pieces, possibilities, n+1, path):
                return True
            # reset fields to zero
            place(space, piece, 0)
            #~pieces[piece] += 1
            path.pop()
    return False
    
    
def create_space(x, y, z):
    return Space(x, y, z, [[[0 for _ in range(z)] for _ in range(y)] for _ in range(x)])

def empty_positions(space):
    return {(x, y, z) for x in range(space.x) 
                      for y in range(space.y)
                      for z in range(space.z)
                      if space.field[x][y][z] == 0}

def print_space(space):
    for i, level in enumerate(space.field):
        print("--- %d ---" % i)
        for line in level:
            print(*map("{:2d}".format, line))


def main():
    pieces = {((0,0,0),(0,0,1),(0,0,2),(0,0,3),(0,1,2)): 25}
    space = create_space(5, 5, 5)

    #~pieces = {((0,0,0),(0,0,1),(0,1,1)): 12}
    #~space = create_space(3, 3, 4)

    all_possibilities = {where: {trans for piece in pieces 
                                       for rot in rotations(piece)
                                       for trans in translations(rot, where)
                                       if fits(space, trans)}
                         for where in empty_positions(space)}

    start = time.time()
    try:
        if find_solution(space, pieces, all_possibilities):
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

# 129528 17 1/12 1/8 1/8 5/8 1/8 3/7 2/3 2/4 1/2 3/4 4/4 4/4 1/1 3/4 4/4 4/4
# ...
# 171206 12 1/12 1/8 1/8 5/8 8/8 1/8 1/7 3/4 3/4 2/4 6/6
# ...
# 18275 26 1/12 1/8 1/8 1/8 1/5 6/7 2/4 4/5 3/3 1/4 3/5 2/2 1/2 1/1 1/2 3/3 1/2 2/4 1/1 1/2 1/1 1/1 1/1 1/1 1/1
# SOLUTION FOUND
# --- 0 ---
# 17 15 15 15 15
# 17 17 15 19 12
# 17 19 19 19 19
# 17 25 18 24 14
# 18 18 18 18 20
# --- 1 ---
#  7  7  7  7  3
# 16  6  7 23 12
# 16 23 23 23 23
# 16 25 24 24 14
# 16 25 21 20 20
# --- 2 ---
#  5  5  5  5  3
#  4  6  5 12 12
# 11 11 11 11 14
# 16 25 11 24 14
# 21 21 21 21 20
# --- 3 ---
#  4  2  8  3  3
#  4  6  8  8 12
#  4  6  8 10 13
#  4 25  8 24 14
# 22 22 22 22 20
# --- 4 ---
#  2  2  2  2  3
#  1  6  9 10 13
#  1  1  9 10 13
#  1  9  9 10 13
#  1 22  9 10 13
# time 236.98839902877808
# calls to fits 7739188
