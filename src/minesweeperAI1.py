import numpy as np
import random

class AI1():

    
    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare
        self.UNPROBED = -1
        self.s = []
        self.s.append(safeSquare)

        self.openedSquares = np.full((self.numRows, self.numCols), -1)
        for row in range(self.numRows):
            for col in range(self.numCols):
                self.openedSquares[row][col] = False


    def open_square_format(self, squareToOpen):
        self.openedSquares[squareToOpen[0]][squareToOpen[1]] = True
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    def unmarked_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j):
                    continue
                if self.UNPROBED == boardState[i][j]:
	                num+= 1
        return num

    def marked_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if not self.isInBounds(i,j):
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
        return self.open_square_format(squareToOpen)

    def adjoin_around(self, boardState, x, y):
        for j in range(y-2, y+3):
            for i in range(x-2, x+3): 
                if not self.isInBounds(i,j):
                    continue
                if boardState[i][j] >= 0:
                    new = (i, j)
                    self.s.append(new)
        

    def mark_mines(self, boardState, x, y):
        for j in range(y-1, y+2):
            for i in range(x-1, x+2): 
                if not self.isInBounds(i,j):
                    continue
                if self.UNPROBED == boardState[i][j]:
                    boardState[i][j] = 9
        self.adjoin_around(boardState, x, y)

    def isInBounds(self, x=None, y=None):
        if y < 0 or y >= self.numCols or x < 0 or x >= self.numRows:
            return False
        else:
            return True

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # the boardState will contain the value (0-8 inclusive) of the squiare, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    # TODO: implement a better algorithm 
    # applying Single Point Strategy
    def performAI(self, boardState):
        print(boardState)
        print("boardstate", boardState)
        unopenedSquares = []
        bombsFoundSoFar = [] 


        # Set of safe cells to probe in this case a list
        if self.s:
            square = self.s[0]
            probed_value = boardState[square[0]][square[1]]
            if probed_value >= 0:
                unknown = self.unmarked_neighbors(boardState, square[0], square[1])
                if unknown > 0:
                    marked = probed_value - self.marked_neighbors(boardState, square[0], square[1])
                    if marked == unknown:
                        # all the unknown squares are mines
                        self.mark_mines(boardState, square[0], square[1])
                    else:
                        # all the unknown square don't have mines so we can probe them
                        self.probe(boardState, square[0], square[1])


        # if empty then open a random cell
        # probe cell if all free neighbors (AFN) and all mine/mark neighbors (AMN)

        # find all the unopened squares
        unopenedSquares = []
        bombsFoundSoFar = []
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == -1:
                    unopenedSquares.append((row, col))
                elif boardState[row][col] == 9:
                    bombsFoundSoFar.append((row, col))
                    
        if len(bombsFoundSoFar) == self.numBombs:
            # If the number of unopened squares is equal to the number of bombs, all squares must be bombs, and we can submit our answer
            print(f"List of bombs is {bombsFoundSoFar}")
            return self.submit_final_answer_format(bombsFoundSoFar)
        else:
            if self.s:
                i = 0
                while(i < len(self.s)):
                    squareToOpen = random.choice(self.s)
                    if not self.openedSquares[squareToOpen[0]][squareToOpen[1]]:
                        self.s.remove(squareToOpen)
                        break
                    i += 1
                if self.openedSquares[squareToOpen[0]][squareToOpen[1]]:
                    squareToOpen = random.choice(unopenedSquares)
                print(f"Square to open is {squareToOpen}")
                return self.open_square_format(squareToOpen)
            else:
                squareToOpen = random.choice(unopenedSquares)
                print(f"Square to open is {squareToOpen}")
                return self.open_square_format(squareToOpen)

    
    

    
        
