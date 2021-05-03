import numpy as np
import random

class AI2():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare
        self.numBombsFound = 0
        self.firstMove = True
        self.openedSquares = set()
        self.UNPROBED = -1
        self.s = []
        self.s.append(safeSquare)
        self.probMatrix = []
        self.lastOpened = safeSquare
        #initialize the probabilities
        
        for x in range(0, self.numRows):
            new = []
            for y in range(0, self.numCols):
                new.append(-1)
            self.probMatrix.append(new)

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    def unmarked_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j) or (x == 0 and y == 0):
                    continue
                if self.UNPROBED == boardState[i][j]:
	                num+= 1
        return num

    def get_unmarked_neighbors(self, boardState, x, y):
        neighbors = []
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j) or (x == 0 and y == 0):
                    continue
                if self.UNPROBED == boardState[i][j]:
	                neighbors.append((i,j))
        return neighbors

    def mine_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j) or (x == 0 and y == 0):
                    continue
                if boardState[i][j] == 9:
	                num+= 1
        return num

    def marked_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j) or (x == 0 and y == 0):
                    continue
                if self.UNPROBED != boardState[i][j]:
	                num+= 1
        return num

    def probe(self, boardState, x, y):
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j):
                    continue 
                # all these cells should be safe so you can add to the list of safe cells and chose a random cell to probe
                if self.UNPROBED == boardState[i][j]:
                    self.s.append((i,j))
        squareToOpen = random.choice(self.s)
        self.s.remove(squareToOpen)
        #return self.open_square_format(squareToOpen)

    """
    def adjoin_around(self, boardState, x, y):
        for j in range(y-2, y+3):
            for i in range(x-2, x+3): 
                if not self.isInBounds(i,j):
                    continue
                if boardState[i][j] >= 0:
                    new = (i, j)
                    self.s.append(new)
    """
    def mark_safe(self, boardState, x, y):
        for j in range(y-1, y+2):
            for i in range(x-1, x+2): 
                if not self.isInBounds(i,j):
                    continue
                if self.probMatrix[i][j] == 0:
                    boardState[i][j] = 0
    
    #marks that square as a mine. changes it from being unprobed without triggering bomb
    def mark_mines(self, boardState, x, y):
        for j in range(y-1, y+2):
            for i in range(x-1, x+2): 
                if not self.isInBounds(i,j):
                    continue
                if self.UNPROBED == boardState[i][j]:
                    boardState[i][j] = 9
        #self.adjoin_around(boardState, x, y)

    def isInBounds(self, x=None, y=None):
        if y < 0 or y >= self.numCols or x < 0 or x >= self.numRows:
            return False
        else:
            return True

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    def performAI(self, boardState):
        #print(boardState)

        # find all the unopened squares
        unopenedSquares = []
        bombsFoundSoFar = []
        openedSquares = []
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == -1:
                    unopenedSquares.append((row, col))
                elif boardState[row][col] == 9:
                    bombsFoundSoFar.append((row, col))
                    self.probMatrix[row][col] = 1
                else:
                    openedSquares.append((row, col))
                    self.probMatrix[row][col] = 0

        if len(bombsFoundSoFar) == self.numBombs:
            # If the number of unopened squares is equal to the number of bombs, all squares must be bombs, and we can submit our answer
            #print(f"List of bombs is {bombsFoundSoFar}")
            return self.submit_final_answer_format(bombsFoundSoFar)
        else:
            lowestProb = float("INF")
            lowestProbValues = []
            #update the probability of neighbors of the last opened square
            i, j = self.lastOpened
            probSurrOfLast = (boardState[i][j] - self.mine_neighbors(boardState, i, j)) / self.unmarked_neighbors(boardState, i, j)
            for x, y in self.get_unmarked_neighbors(boardState, i, j):
                self.probMatrix[x][y] = max(self.probMatrix[x][y], probSurrOfLast)
            if probSurrOfLast == 1:
                for (a, b) in self.get_unmarked_neighbors(boardState, i, j):
                    self.mark_mines(boardState, a, b)
            print(self.probMatrix)

            for x in range(0, len(self.probMatrix)):
                for y in range(0, len(self.probMatrix[0])):
                    if self.unmarked_neighbors(boardState, x, y) == 0 or (x,y) in openedSquares:
                        continue
                    probSquare = self.probMatrix[x][y]
                    if probSquare == -1:
                        continue
                    if probSquare > lowestProb:
                        continue
                    elif probSquare < lowestProb:
                        lowestProbValues = []
                        lowestProbValues.append((x,y))
                        lowestProb = probSquare
                        #print(f"x, y is {(x, y)}")
                        #print(f"lowest prob = {lowestProb}")
                    else:
                        lowestProbValues.append((x,y))
                    
        """    
        if self.firstMove:
            self.firstMove = False
            print("this is the first move")
            return self.open_square_format(self.safeSquare)
        """
        self.lastOpened = random.choice(lowestProbValues)
        return self.open_square_format(self.lastOpened)

