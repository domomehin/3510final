import numpy as np
import random

class AI1():
    
    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare, ans):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare
        self.UNPROBED = -1
        self.s = []
        self.ans = ans
        
    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    def unmarked_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
	            if self.UNPROBED == boardState[i][j]:
	                num+= 1
        return num

    def marked_neighbors(self, boardState, x, y):
        num = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
	            if self.UNPROBED == boardState[i][j]:
	                num+= 1
        return num

    def probe(self, boardState, x, y, set):
        for j in range(y-1, y+2):
            for i in range(x-1, x+2): 
                if self.UNPROBED == boardState[i][j]:
                    boardState[i][j] = self.ans
        return self.adjoin_around(boardState, x, y, self.s)

    def adjoin_around(self, boardState, x, y, set):
        for j in range(y-2, y+3):
            for i in range(x-2, x+3): 
	            if boardState[i][j] >= 0:
	                s = s.append(i, j)
        return s
    

    def mark_mines(self, boardState, x, y, sets):
        for j in range(y-1, y+2):
            for i in range(x-1, x+2): 
                if self.UNPROBED == boardState[i][j]:
                    boardState[i][j] = 9
        return self.adjoin_around(boardState, x, y, sets)

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the squiare, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm 
    # applying Single Point Strategy
    def performAI(self, boardState):
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
                        self.s = self.mark_mines(boardState, square[0], square[1], self.s)
                    elif marked == 0:
                        self.s = self.probe(boardState, square[0], square[1], self.s)
                
                
        # if empty then open a random cell
        # probe cell if all free neighbors (AFN) and all mine/mark neighbors (AMN)

        # find all the unopened squares
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
            # Otherwise, pick a random square and open it      
            if self.s:
                print("has s")
                squareToOpen = random.choice(self.s)
                print(f"Square to open is {squareToOpen}")
                return self.open_square_format(squareToOpen)
            else:
                squareToOpen = random.choice(unopenedSquares)
                print(f"Square to open is {squareToOpen}")
                return self.open_square_format(squareToOpen)
            

    
    

    
        
