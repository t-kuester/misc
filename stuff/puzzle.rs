use std::collections::HashMap;

struct Space {
    x: i8,
    y: i8,
    z: i8,
    field: [[[u8;5];5];5],
}

#[derive(Debug)]
struct Piece {
    points: Vec<Point>
}

#[derive(Hash,Eq,PartialEq,Debug)]
struct Point(i8, i8, i8);

fn translate(piece: &Piece, pos: &Point, whr: &Point) -> Piece {
    let Point(px, py, pz) = pos;
    let Point(wx, wy, wz) = whr;
    let points = piece.points.iter().map( |Point(x,y,z)|
                    Point(wx+x-px, wy+y-py, wz+z-pz))
            .collect::<Vec<Point>>();
    return Piece {points: points};
}

fn around(piece: &Piece, whr: &Point) -> Vec<Piece> {
    piece.points.iter()
            .map( |pos| translate(&piece, &pos,&whr))
            .collect::<Vec<Piece>>()
}

fn get(space: &Space, pos: &Point) -> u8 {
    let Point(x, y, z) = pos;
    return space.field[*x as usize][*y as usize][*z as usize];
}

fn fits(space: &Space, piece: &Piece) -> bool {
    return piece.points.iter().all( |Point(x,y,z)|
                    0 <= *x && *x < space.x &&
                    0 <= *y && *y < space.y &&
                    0 <= *z && *z < space.z &&
                    get(&space, &Point(*x,*y,*z)) == 0);
}

fn place(space: &mut Space, piece: &Piece, symbol: u8) {
    for p in piece.points.iter() {
        let Point(x, y, z) = p;
        space.field[*x as usize][*y as usize][*z as usize] = symbol;
    }
}

fn empty_positions(space: &Space) -> Vec<Point> {
    let mut res = vec![];
    for x in 0..space.x {
        for y in 0..space.y {
            for z in 0..space.z {
                let p = Point(x, y, z);
                if get(&space, &p) == 0 {
                    res.push(p);
                }
            }
        }
    }
    return res;
}

fn print_space(space: &Space) {
    for x in 0..space.x {
        println!("--- {} ---", x);
        for y in 0..space.y {
            for z in 0..space.z {
                print!("{} ", get(&space, &Point(x,y,z)));
            }
            println!();
        }
    }
}

fn get_possibilities<'a>(space: &Space, pieces: Vec<Piece>, 
                     last_poss: HashMap<Point, Vec<&'a Piece>>) -> HashMap<Point, Vec<&'a Piece>> {
    let mut possibilities = HashMap::new();
    for point in empty_positions(&space) {
        let pieces = last_poss.get(&point).iter()
                .filter( |piece| fits(&space, &piece))
                .collect::<Vec<&'a Piece>>();
        possibilities.insert(point, pieces);
        if pieces.len() == 0 {
            break;
        }
    }
    possibilities
 }

//~def get_possibilities_reuse(space, empty, pieces, last_poss):
//~    possibilities = {}
//~    for where in empty:
//~        possibilities[where] = {(piece, rot, pos)
//~                    for (piece, rot, pos) in last_poss[where]
//~                    if pieces[piece] > 0 
//~                    if fits(space, rot, pos, where)}
//~        if not possibilities[where]:
//~            break
//~    return possibilities


fn main() {
    println!("Hello World");
    
    let mut space = Space {x: 5, y: 5, z: 5, field: [[[0; 5];5];5]};
    let piece = Piece {points: vec![Point(0,0,0),Point(0,0,1),Point(0,0,2),Point(0,0,3),Point(0,1,2)]};
    
    place(&mut space, &piece, 4);
    print_space(&space);
}


/*

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


count = 0
def find_solution(space, pieces, last_poss, n=1, path=[]):
    global count
    count += 1
    print(count, n, *path)
    if MAX_ITER and count > MAX_ITER: return

    empty = empty_positions(space)
    possibilities = get_possibilities_reuse(space, empty, pieces, last_poss)

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
*/
