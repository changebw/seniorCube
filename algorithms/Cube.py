import numpy as np
import random
import copy

#f/b - z
#r/l - x
#u/d - y

class Cube:
    def __init__(self, state = None) -> None:
        self.colors = ['w', 'g', 'r', 'b', 'o', 'y']
        if state == None:
            self.unscrambled()
            self.moves = "rlfbduRLFBUD"
        else:
            self.cube = [[[]]]
            for i, s in enumerate(state):
                self.cube[-1][-1].append(s)
                if len(self.cube[-1][-1]) == 3 and len(self.cube[-1]) < 3:
                    self.cube[-1].append([])
                elif len(self.cube[-1][-1]) == 3 and len(self.cube[-1]) == 3 and i < len(state) - 1:
                    self.cube.append([[]])

    def input(self, sides):
        self.cube = sides

    def unscrambled(self):
        self.cube = [[[s for x in range(3)] for y in range(3)] for s in self.colors]
        print(self.cube)
        self.scramble = ""

    def printCube(self):
        for i in range(3):
            print(self.cube[0][i][:], self.cube[1][i][:], self.cube[2][i][:], self.cube[3][i][:], self.cube[4][i][:], self.cube[5][i][:])

    def stringify(self):
        return ''.join([i for r in self.cube for s in r for i in s])

    def turnCube(self, turns):
        self.scramble = turns
        for turn in turns:
            match turn:
                case 'r':
                    self.xRotation(2, 0)
                case 'l':
                    self.xRotation(0, 1)
                case 'f':
                    self.zRotation(2, 0)
                case 'b':
                    self.zRotation(0, 1)
                case 'd':
                    self.yRotation(2, 0)
                case 'u':
                    self.yRotation(0, 1)
                case 'R':
                    self.xRotation(2, 1)
                case 'L':
                    self.xRotation(0, 0)
                case 'F':
                    self.zRotation(2, 1)
                case 'B':
                    self.zRotation(0, 0)
                case 'D':
                    self.yRotation(2, 1)
                case 'U':
                    self.yRotation(0, 0)
            print(turn)
            self.printCube()
            
    #5,i,2 -> 3,2-i,0
    #3,2-i,2 -> 5,i,0

    #U or D
    def yRotation(self, row, dir):
        cube = copy.deepcopy(self.cube)
        if dir == 0:
            self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (cube[2][row],
                                                                                        cube[3][row],
                                                                                        cube[4][row],
                                                                                        cube[1][row])
            if row == 0:
                #self.cube[0] = np.rot90(self.cube[0], axes=(1,0))
                self.cube[0] = [list(x) for x in zip(*reversed(cube[0]))]

            elif row == 2:
                #self.cube[5] = np.rot90(self.cube[5], axes=(0,1))
                self.cube[5] = [list(x) for x in zip(*cube[5])][::-1]

        else: #Twist right
            self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (cube[4][row],
                                                                                            cube[1][row],
                                                                                            cube[2][row],
                                                                                            cube[3][row])
            if row == 0:
                #self.cube[0] = np.rot90(self.cube[0], axes=(0,1))
                self.cube[0] = [list(x) for x in zip(*cube[0])][::-1]
            elif row == 2:
                #self.cube[5] = np.rot90(self.cube[5], axes=(1,0))
                self.cube[5] = [list(x) for x in zip(*reversed(cube[5]))]        

    #R or L
    def xRotation(self, col, dir):
        cube = copy.deepcopy(self.cube)
        for i in range(3):
            if dir == 0:
                self.cube[0][i][col], self.cube[2][i][col], self.cube[4][-i-1][-col-1], self.cube[5][i][col] = (cube[4][-i-1][-col-1],
                                                                                                                cube[0][i][col],
                                                                                                                cube[5][i][col],
                                                                                                                cube[2][i][col])
            else: #Twist right
                self.cube[0][i][col], self.cube[2][i][col], self.cube[4][-i-1][-col-1], self.cube[5][i][col] = (cube[2][i][col],
                                                                                                                cube[5][i][col],
                                                                                                                cube[0][i][col],
                                                                                                                cube[4][-i-1][-col-1])
                
        if dir == 0:
            if col == 0:
                #self.cube[1] = np.rot90(self.cube[1], axes=(1,0))
                self.cube[1] = [list(x) for x in zip(*reversed(cube[1]))]
            elif col == 2:
                #self.cube[3] = np.rot90(self.cube[3], axes=(0,1))
                self.cube[3] = [list(x) for x in zip(*cube[3])][::-1] 
        else:
            if col == 0:
                #self.cube[1] = np.rot90(self.cube[1], axes=(0,1))
                self.cube[1] = [list(x) for x in zip(*cube[1])][::-1]
            elif col == 2:
                #self.cube[3] = np.rot90(self.cube[3], axes=(1,0))
                self.cube[3] = [list(x) for x in zip(*reversed(cube[3]))]             

    #F or B
    def zRotation(self, col, dir):
        cube = copy.deepcopy(self.cube)
        for i in range(3):
            if dir == 0:
                self.cube[0][col][i], self.cube[1][-i-1][col], self.cube[3][i][-col-1], self.cube[5][-col-1][-1-i] = (cube[3][i][-col-1],
                                                                                                                    cube[0][col][i],
                                                                                                                    cube[5][-col-1][-1-i],
                                                                                                                    cube[1][-i-1][col])
            else: #Twist right
                self.cube[0][col][i], self.cube[1][-i-1][col], self.cube[3][i][-col-1], self.cube[5][-col-1][-1-i] = (cube[1][-i-1][col],
                                                                                                                    cube[5][-col-1][-1-i],
                                                                                                                    cube[0][col][i],
                                                                                                                    cube[3][i][-col-1])
                
        if dir == 0:
            if col == 0:
                #self.cube[4] = np.rot90(self.cube[4], axes=(1,0))
                self.cube[4] = [list(x) for x in zip(*reversed(cube[4]))]
            elif col == 2:
                #self.cube[2] = np.rot90(self.cube[2], axes=(0,1))
                self.cube[2] = [list(x) for x in zip(*cube[2])][::-1] 
        else:
            if col == 0:
                #self.cube[4] = np.rot90(self.cube[4], axes=(0,1))
                self.cube[4] = [list(x) for x in zip(*cube[4])][::-1]
            elif col == 2:
                #self.cube[2] = np.rot90(self.cube[2], axes=(1,0))
                self.cube[2] = [list(x) for x in zip(*reversed(cube[2]))] 

    def solve(self):
        scramble = copy.deepcopy(self.scramble)

    def printMoves(self, moves):
        solve = ""
        for x in moves:
            if x[0] == 'v':
                if x[1] == 0:
                    if x[2] == 0:
                        solve += 'L'
                    else:
                        solve += 'l'
                else:
                    if x[2] == 0:
                        solve += 'r'
                    else:
                        solve += 'R'
            elif x[0] == 'h':
                if x[1] == 0:
                    if x[2] == 0:
                        solve += 'U'
                    else:
                        solve += 'u'
                else:
                    if x[2] == 0:
                        solve += 'd'
                    else:
                        solve += 'D'
            else:
                if x[1] == 0:
                    if x[2] == 0:
                        solve += 'B'
                    else:
                        solve += 'b'
                else:
                    if x[2] == 0:
                        solve += 'f'
                    else:
                        solve += 'F'
        print(solve)
        

    def randomScramble(self, moveCount):
        scramble = ""
        for x in range(moveCount):
            scramble += random.choice(self.moves)
        print(scramble)
        self.turnCube(scramble)

    def reverseMoves(self, moves):
        return moves.swapcase()[::-1]
    
    def solved(self):
        for side in self.cube:
            hold = []
            check = True
            for row in side:
                if len(set(row)) == 1:
                    hold.append(row[0])
                else:
                    check = False
                    break
            if not(check):
                break
            if len(set(hold)) > 1:
                check = False
                break
        return check