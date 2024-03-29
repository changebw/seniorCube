from Cube import Cube

moves = ""

cube = Cube()
cube.printCube()
moves = cube.randomScramble(20)
print(moves)
cube.turnCube(moves)
print("-----------------------------")
cube.printCube()

# moves = cube.reverseMoves(moves)
# print(moves)
# cube.turnCube(moves)
# print("-----------------------------")
# cube.printCube()



#5,i,2 -> 3,2-i,0
#3,2-i,2 -> 5,i,0