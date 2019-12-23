# TODO
# test again with smaller example
# run through profiler, try to make faster
# more caching?
# no passing of "space" and "pieces" parameters (faster or slower?)
# restrict placement for first corner-piece to TWO (instead of 12)
# ~10% faster without debuging path and assuming infinite pieces
# ~20% faster without printing in each expansion

import functools, collections, time

Space = collections.namedtuple("Space", "x y z field")

@functools.lru_cache(None)
def rotations(piece):
    def rot(x,y):
        return ((x,y), (-y,x), (-x,-y), (y,-x))
    def rotate(point):
        x, y, z = point
        for y2, z2 in rot(y, z):
            for x3, z3 in rot(x, z2):
                for x4, y4 in rot(x3, y2):
                    yield (x4, y4, z3)
    return set(zip(*map(rotate, piece)))

@functools.lru_cache(None)
def translate(piece, pos, where):
    px, py, pz = pos
    wx, wy, wz = where
    return tuple((wx+x-px, wy+y-py, wz+z-pz) for (x,y,z) in piece)

fits_count = 0
def fits(space, piece, pos, where):
    global fits_count
    fits_count += 1
    X, Y, Z, F = space # slightly faster
    return all(0 <= x < X and 
               0 <= y < Y and 
               0 <= z < Z and 
               F[x][y][z] == 0 for (x,y,z) in translate(piece, pos, where))

def place(space, piece, pos, where, symbol):
    for x, y, z in translate(piece, pos, where):
        space.field[x][y][z] = symbol

def get_possibilities_all(space, empty, pieces, last_poss):
    # MAX_ITER=100: 7.7 sec, 827k fits
    return {where: {(piece, rot, pos)
                    for piece in pieces if pieces[piece] > 0
                    for rot in rotations(piece)
                    for pos in rot if fits(space, rot, pos, where)}
            for where in empty}
    
def get_possibilities_break(space, empty, pieces, last_poss):
    # MAX_ITER=100: 6.3 sec, 662k fits
    possibilities = {}
    for where in empty:
        possibilities[where] = {(piece, rot, pos)
                    for piece in pieces if pieces[piece] > 0
                    for rot in rotations(piece)
                    for pos in rot if fits(space, rot, pos, where)}
        if not possibilities[where]:
            break
    return possibilities
    
def get_possibilities_early_abort(space, empty, pieces, last_poss):
    # MAX_ITER=100: 2.2 sec, 196k fits
    # MAX_ITER=1000: 17.8 sec, 1670k fits
    best = None
    def poss(where):
        res = set()
        for comb in ((piece, rot, pos)
                for piece in pieces if pieces[piece] > 0
                for rot in rotations(piece)
                for pos in rot if fits(space, rot, pos, where)):
            res.add(comb)
            if best and len(res) >= best: return res | {None}
        return res
    
    possibilities = {}
    for where in empty:
        possibilities[where] = poss(where)
        if best is None or len(possibilities[where]) < best:
            best = len(possibilities[where])
        if best == 0:
            break
    return possibilities

def get_possibilities_reuse(space, empty, pieces, last_poss):
    #MAX_ITER=100: 1.7 sec, 113k fits
    #MAX_ITER=1000: 16.5 sec, 930k fits
    possibilities = {}
    for where in empty:
        possibilities[where] = {(piece, rot, pos)
                    for (piece, rot, pos) in last_poss[where]
                    if pieces[piece] > 0 
                    if fits(space, rot, pos, where)}
        if not possibilities[where]:
            break
    return possibilities

NOT_CALCULATED = [None] * 9999
def get_possibilities_early_abort_reuse(space, empty, pieces, last_poss):
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
    for where in empty:
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

    empty = empty_positions(space)
    #~possibilities = get_possibilities_early_abort(space, empty, pieces, last_poss)
    possibilities = get_possibilities_reuse(space, empty, pieces, last_poss)
    #~possibilities = get_possibilities_early_abort_reuse(space, empty, pieces, last_poss)

    # if none, return solution
    if not possibilities:
        return True
    else:    
        # find position with fewest possibilities
        where = min(possibilities, key=lambda p: len(possibilities[p]))
        # test all such possibilities
        for i, (piece, rot, pos) in enumerate(possibilities[where], start=1):
            # apply piece by setting the fields in space to some increasing number
            place(space, rot, pos, where, n)
            pieces[piece] -= 1
            path.append("%d/%d" % (i, len(possibilities[where])))
            # recurse
            if find_solution(space, pieces, possibilities, n+1, path):
                return True
            # reset fields to zero
            place(space, rot, pos, where, 0)
            pieces[piece] += 1
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

    
MAX_ITER = 100

pieces = {((0,0,0),(0,0,1),(0,0,2),(0,0,3),(0,1,2)): 25}
space = create_space(5, 5, 5)

#~pieces = {((0,0,0),(0,0,1),(0,1,1)): 12}
#~space = create_space(3, 3, 4)

all_possibilities = get_possibilities_all(space, empty_positions(space), pieces, None)

start = time.time()
if find_solution(space, pieces, all_possibilities):
    print("SOLUTION FOUND")
    print_space(space)
else:
    print("NO SOLUTION FOUND")
print(time.time() - start)
print(fits_count)

# 129528 17 1/12 1/8 1/8 5/8 1/8 3/7 2/3 2/4 1/2 3/4 4/4 4/4 1/1 3/4 4/4 4/4
# 171206 12 1/12 1/8 1/8 5/8 8/8 1/8 1/7 3/4 3/4 2/4 6/6

