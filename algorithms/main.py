import json
import os.path
import time

from Cube import Cube
from solver import IDA_star, build_heuristic_db

MAX_MOVES = 5
NEW_HEURISTICS = True
HEURISTIC_FILE = 'heuristic.json'

#--------------------------------
cube = Cube()
cube.printCube()
print('-----------')
#--------------------------------

if os.path.exists(HEURISTIC_FILE):
    with open(HEURISTIC_FILE) as f:
        h_db = json.load(f)
else:
    h_db = None

if h_db is None or NEW_HEURISTICS is True:
    actions = [(r, n, d) for r in ['h', 'v', 's'] for d in [0, 1] for n in [0,2]]
    h_db = build_heuristic_db(
        cube.stringify(),
        actions,
        max_moves = MAX_MOVES,
        heuristic = h_db
    )

    with open(HEURISTIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            h_db,
            f,
            ensure_ascii=False,
            indent=4
        )
#--------------------------------
cube.randomScramble(12)
#l_rot = MAX_MOVES if MAX_MOVES < 5 else 5,
#u_rot = MAX_MOVES

print('----------')
cube.printCube()
print('----------')
start = time.perf_counter()
#--------------------------------
solver = IDA_star(h_db)
moves = solver.run(cube.stringify())
end = time.perf_counter()

print("Moves: ")
cube.printMoves(moves)
print('----------')

for m in moves:
    if m[0] == 'h':
        cube.yRotation(m[1], m[2])
    elif m[0] == 'v':
        cube.xRotation(m[1], m[2])
    elif m[0] == 's':
        cube.zRotation(m[1], m[2])
cube.printCube()
print("Time: ", end - start, "s")