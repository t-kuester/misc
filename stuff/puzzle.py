# TODO
# test again with smaller example
# run through profiler, try to make faster
# more caching?
# no passing of "space" and "pieces" parameters (faster or slower?)

import functools, collections, string, time

SYMBOLS = string.ascii_uppercase

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
                    
def create_space(x, y, z):
    return Space(x, y, z, [[[0 for _ in range(z)] for _ in range(y)] for _ in range(x)])

def print_space(space):
    for i, level in enumerate(space.field):
        print("- - %d - -" % i)
        for line in level:
            print(*line)

@functools.lru_cache(None)
def translate(piece, pos, where):
    px, py, pz = pos
    wx, wy, wz = where
    return tuple((wx+x-px, wy+y-py, wz+z-pz) for (x,y,z) in piece)

fits_count = 0
def fits(space, piece, pos, where):
    global fits_count
    fits_count += 1
    X,Y,Z,F=space
    return all(0 <= x < X and 
               0 <= y < Y and 
               0 <= z < Z and 
               F[x][y][z] == 0 for (x,y,z) in translate(piece, pos, where))

def place(space, piece, pos, where, symbol):
    for x, y, z in translate(piece, pos, where):
        space.field[x][y][z] = symbol

def empty_positions(space):
    return {(x, y, z) for x in range(space.x) 
                      for y in range(space.y)
                      for z in range(space.z)
                      if space.field[x][y][z] == 0}

count = 0
def find_solution(space, empty, pieces, i=0):
    global count
    count += 1
    print(count, len(empty), "-"*i,i)
    if MAX_ITER and count > MAX_ITER: return

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
    
    # get valid pieces, rotations, and positions for all empty positions
    possibilities = {}
    for where in empty: #_positions(space):
        possibilities[where] = poss(where)
        if best is None or len(possibilities[where]) < best:
            best = len(possibilities[where])
        if best == 0:
            return
        
    # if none, return solution
    if not possibilities:
        return space
    else:    
        # find position with fewest possibilities
        where = min(possibilities, key=lambda p: len(possibilities[p]))
        # test all such possibilities
        for piece, rot, pos in possibilities[where]:
            # apply piece by setting the fields in space to some increasing number
            place(space, rot, pos, where, SYMBOLS[i])
            pieces[piece] -= 1
            trans = set(translate(rot, pos, where))
            empty -= trans
            # recurse
            res = find_solution(space, empty, pieces, i+1)
            if res:
                return res
            # reset fields to zero
            place(space, rot, pos, where, 0)
            pieces[piece] += 1
            empty |= trans
    
MAX_ITER = None

pieces = {((0,0,0),(0,0,1),(0,0,2),(0,0,3),(0,1,2)): 25}
space = create_space(5, 5, 5)

#~pieces = {((0,0,0),(0,0,1),(0,1,1)): 12}
#~space = create_space(3, 3, 4)

start = time.time()
res = find_solution(space, empty_positions(space), pieces)
if res:
    print("SOLUTION FOUND")
    print_space(res)
else:
    print("NO SOLUTION FOUND")
print(time.time() - start)
print(fits_count)
