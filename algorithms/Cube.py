import numpy as np
import random
import copy

class Cube:
    def __init__(self) -> None:
        self.sides = np.array([[['w', 'w', 'w'],['w', 'w', 'w'],['w','w','w']], [['r', 'r', 'r'],['r', 'r', 'r'],['r','r','r']], [['b', 'b', 'b'],['b', 'b', 'b'],['b','b','b']],
                      [['o', 'o', 'o'],['o', 'o', 'o'],['o','o','o']], [['g', 'g', 'g'],['g', 'g', 'g'],['g','g','g']], [['y', 'y', 'y'],['y', 'y', 'y'],['y','y','y']]])
        self.scramble = ""
        self.moves = "rlfbduRLFBUD"

    def input(self, sides):
        self.sides = sides
    
    def printCube(self):
        for i in range(3):
            print(self.sides[0][i][:], self.sides[1][i][:], self.sides[2][i][:], self.sides[3][i][:], self.sides[4][i][:], self.sides[5][i][:])

    def turnCube(self, turns):
        self.scramble = turns
        for turn in turns:
            match turn:
                case 'r':
                    self.turnRight(3)
                case 'l':
                    self.turnLeft(3)
                case 'f':
                    self.turnFront(3)
                case 'b':
                    self.turnBack(3)
                case 'd':
                    self.turnDown(3)
                case 'u':
                    self.turnUp(3)
                case 'R':
                    self.turnRight(1)
                case 'L':
                    self.turnLeft(1)
                case 'F':
                    self.turnFront(1)
                case 'B':
                    self.turnBack(1)
                case 'D':
                    self.turnDown(1)
                case 'U':
                    self.turnUp(1)
            #self.printCube()
            
    #5,i,2 -> 3,2-i,0
    #3,2-i,2 -> 5,i,0

    def turnRight(self, num):
        self.sides[4] = np.rot90(self.sides[4], 4-int(num))
        for x in range(int(num)):
            sides = copy.deepcopy(self.sides)
            for i in range(3):
                self.sides[1][i][2] = sides[0][i][2]
                self.sides[5][i][2] = sides[1][i][2]
                self.sides[3][2-i][0] = sides[5][i][2]
                self.sides[0][i][2] = sides[3][2-i][0]

    def turnLeft(self, num):
        self.sides[2] = np.rot90(self.sides[2], 4-int(num))
        for x in range(int(num)):
            sides = copy.deepcopy(self.sides)
            for i in range(3):
                self.sides[1][i][0] = sides[5][i][0]
                self.sides[0][i][0] = sides[1][i][0]
                self.sides[3][2-i][2] = sides[0][i][0]
                self.sides[5][i][0] = sides[3][2-i][2]

    #

    def turnFront(self, num):
        self.sides[1] = np.rot90(self.sides[1], 4-int(num))
        for x in range(int(num)):
            sides = copy.deepcopy(self.sides)
            for i in range(3):
                self.sides[2][i][2] = sides[0][0][i]
                self.sides[5][2][2-i] = sides[2][i][2]
                self.sides[4][i][0] = sides[5][2][i]
                self.sides[0][0][2-i] = sides[4][i][0]

    def turnBack(self, num):
        self.sides[3] = np.rot90(self.sides[3], 4-int(num))
        for x in range(int(num)):
            sides = copy.deepcopy(self.sides)
            for i in range(3):
                self.sides[4][2-i][2] = sides[0][2][i]
                self.sides[5][0][i] = sides[4][i][2]
                self.sides[2][2-i][0] = sides[5][0][i]
                self.sides[0][2][i] = sides[2][i][0]

    def turnDown(self, num):
        self.sides[0] = np.rot90(self.sides[0], 4-int(num))
        for x in range(int(num)):
            sides = copy.deepcopy(self.sides)
            self.sides[4][2] = sides[1][2]
            self.sides[3][2] = sides[4][2]
            self.sides[2][2] = sides[3][2]
            self.sides[1][2] = sides[2][2]

    def turnUp(self, num):
        self.sides[5] = np.rot90(self.sides[5], 4-int(num))
        for x in range(int(num)):
            sides = copy.deepcopy(self.sides)
            self.sides[2][0] = sides[1][0]
            self.sides[3][0] = sides[2][0]
            self.sides[4][0] = sides[3][0]
            self.sides[1][0] = sides[4][0]

    def solve(self):
        scramble = copy.deepcopy(self.scramble)

    def randomScramble(self, moveCount):
        scramble = ""
        for x in range(moveCount):
            scramble += random.choice(self.moves)
        return scramble

    def reverseMoves(self, moves):
        return moves.swapcase()[::-1]