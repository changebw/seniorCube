import json
import os.path
import time

from algorithms.Cube import Cube
from algorithms.solver import IDA_star, build_heuristic_db
from CV.colorByFace import colorByFace

pixelDetector = colorByFace('CV/topview.jpg', 'CV/botview.jpg')
faceList = pixelDetector.allFaces()

MAX_MOVES = 7
NEW_HEURISTICS = False
HEURISTIC_FILE = 'heuristic.json'

#--------------------------------
#if we have formatted sides correctly can input into constructor like this: cube = Cube(sides)
#otherwise can do cube.input(sides)
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

solver = IDA_star(h_db)
moves = solver.run(cube.stringify())
end = time.perf_counter()