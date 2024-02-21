from Cube import Cube

cube = Cube()
cube.printCube()
moves = ["r2","l3", "u1", "b1", "u2", "d1", "l1", "u3", "d1", "l2", "u2", "b1", "u1", "l2", "d2", "f3", "b3", "d3", "r2", "u1", "f1", "l2", "f1", "l1", "b2"]
print(len(moves))
cube.turnCube(moves)
#cube.turnCube(["r3"])
print("-----------------------------")
cube.printCube()


#5,i,2 -> 3,2-i,0
#3,2-i,2 -> 5,i,0