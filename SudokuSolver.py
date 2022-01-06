class SudokuSolver:

    def __init__(self, tSudokuGrid):
        self.sudokuGrid = tSudokuGrid
        self.fullPossibilities = dict()
        self.rescanQueue = []
        self.fullCountScanXYZ = [0,0,0]
        self.numCounts = [0] * 10
        self.tileList = dict()

    # Returns a list of all possible valid numbers for a grid position
    def findPossibilities(self, tSudokuGrid, gridX, gridY):
        pList = []
        for i in range(1,10):
            if (self.inRow(tSudokuGrid, gridX, i) and self.inColumn(tSudokuGrid, gridY, i) and self.inBox(tSudokuGrid, gridX, gridY, i)):
                pList.append(i)
        return pList

    # Returns a dictionary with grid position as the key and list of possibilites as the value
    def constructNextTilePossibilities(self, tSudokuGrid):
        tPossibilities = dict()
        for x, rows in enumerate(tSudokuGrid):
            for y, num in enumerate(rows):
                if num == 0:
                    tPossibilities[(x, y)] = self.findPossibilities(tSudokuGrid, x, y)
                    return tPossibilities
        return {}

    # Backtracking algorithm to solve Sudoku
    def solveSudoku(self, tSudokuGrid = None):
        if tSudokuGrid is None:
            tSudokuGrid = self.sudokuGrid
        tile = self.constructNextTilePossibilities(tSudokuGrid)
        for xy in tile:
            gridX = xy[0]
            gridY = xy[1]
            for i in tile[xy]:
                tSudokuGrid[gridX][gridY] = i
                if (self.solveSudoku(tSudokuGrid)):
                    return True
            tSudokuGrid[gridX][gridY] = 0
            return False
        return True

    # Runs before backtracking algorithm to reduce the number of permutations
    # Finds simple solutions where only 1 possibility exists for a grid position
    # And where a specific number has only 1 possiible location is a row/column/box
    # Also performs 3 validation checks while scanning for solutions which antiquated the validateGrid() function
    # By checking if there are zero possibilities for a grid position,
    # if a distinct number has no possible locations in the row/column/box,
    # and if a distinct number had a duplicate entry in the row/column/box for the initial grid
    def simplifyGrid(self):
        for x, rows in enumerate(self.sudokuGrid):
            for y, num in enumerate(rows):
                if num == 0:
                    pList = self.findPossibilities(self.sudokuGrid, x, y)
                    if len(pList) == 0:
                        return False   
                    elif len(pList) == 1:
                        self.sudokuGrid[x][y] = pList[0]
                        self.fullPossibilities[(x, y)] = pList[0]
                        self.rescanQueue.append([(x, y), pList[0]])
                    else:
                        self.fullPossibilities[(x, y)] = pList
                else:
                    self.fullPossibilities[(x, y)] = self.sudokuGrid[x][y]

        while self.rescanQueue or self.fullCountScanXYZ != [1,1,1]:
            if self.rescanQueue:
                xy = self.rescanQueue[0][0]
                gridX = xy[0]
                gridY = xy[1]
                sNum = self.rescanQueue[0][1]

                # Scan row
                self.numCounts = [0] * 10
                self.tileList = dict()
                
                for row in range(9):
                    if not self.updateChecks(row, gridY, sNum):
                        return False
                if not self.checkCountList(self.fullCountScanXYZ[0]):
                    return False

                # Scan column
                self.numCounts = [0] * 10
                self.tileList = dict()
                
                for column in range(9):
                    if not self.updateChecks(gridX, column, sNum):
                        return False
                if not self.checkCountList(self.fullCountScanXYZ[1]):
                    return False

                # Scan box
                self.numCounts = [0] * 10
                self.tileList = dict()
                boxX = (gridX // 3) * 3
                boxY = (gridY // 3) * 3
                for i in range(3):
                    for j in range(3):
                        if not self.updateChecks(boxX+i, boxY+j, sNum):
                            return False
                if not self.checkCountList(self.fullCountScanXYZ[2]):
                    return False
                
                self.rescanQueue.pop(0)

            # Row counts
            if not self.rescanQueue:
                for row in range(9):
                    self.numCounts = [0] * 10
                    self.tileList = dict()
                    
                    for column in range(9):
                        if not self.updateChecks(row, column):
                            return False
                    if not self.checkCountList(self.fullCountScanXYZ[0]):
                        return False
                self.fullCountScanXYZ[0] = 1
                
            # Colomn counts                 
            if not self.rescanQueue:
                for column in range(9):
                    self.numCounts = [0] * 10
                    self.tileList = dict()
                    
                    for row in range(9):
                        if not self.updateChecks(row, column):
                            return False
                    if not self.checkCountList(self.fullCountScanXYZ[1]):
                        return False
                self.fullCountScanXYZ[1] = 1

            # Box counts
            if not self.rescanQueue:
                for x in range(3):
                    for y in range(3):
                        self.numCounts = [0] * 10
                        self.tileList = dict()
                        boxX = x * 3
                        boxY = y * 3
                        
                        for i in range(3):
                            for j in range(3):
                                if not self.updateChecks(boxX+i, boxY+j):
                                    return False
                        if not self.checkCountList(self.fullCountScanXYZ[2]):
                            return False
                self.fullCountScanXYZ[2] = 1

        ##if not (self.validateGrid()):
            ##return False 
        return True

    # Removes nummber from possibility list if supplied
    # Increments number count list for later check
    def updateChecks(self, xCheck, yCheck, numCheck = None):
        if type(self.fullPossibilities[(xCheck, yCheck)]) == list:
            pList = self.fullPossibilities[(xCheck, yCheck)]
            if numCheck is not None:
                try:
                    pList.remove(numCheck)
                except:
                    pass

                if len(pList) == 0:
                    return False
                elif len(pList) == 1:
                    self.sudokuGrid[xCheck][yCheck] = pList[0]
                    self.fullPossibilities[(xCheck, yCheck)] = pList[0]
                    self.rescanQueue.append([(xCheck, yCheck), pList[0]])
                else:
                    self.fullPossibilities[(xCheck, yCheck)] = pList

            for pNum in pList:
                self.numCounts[pNum] += 1
                self.tileList[pNum] = (xCheck, yCheck)
        else:
            self.numCounts[self.fullPossibilities[(xCheck, yCheck)]] += 10
        return True

    # Checks count list for solutions and for invalid entries
    def checkCountList(self, scanXYZ):
        for index, count in enumerate(self.numCounts):
            if count == 0 and index != 0:
                return False              
            elif count == 1:
                tileX = self.tileList[index][0]
                tileY = self.tileList[index][1]
                self.sudokuGrid[tileX][tileY] = index
                self.fullPossibilities[(tileX, tileY)] = index
                self.rescanQueue.append([(tileX, tileY), index])
                if self.fullCountScanXYZ[2] == scanXYZ:
                    break
            elif count > 19:
                return False
        return True

    # Validates grid by checking the number of open tiles in the row/column/box equals
    # to the number of distinct possibilities still remaining
    def validateGrid(self):
        for row in range(9):
            openTileCount = 0
            openNumSet = set()

            for column in range(9):
                if type(self.fullPossibilities[(row, column)]) == list:
                    openNumSet.update(self.fullPossibilities[(row, column)])
                    openTileCount += 1

            if len(openNumSet) != openTileCount:
                return False

        for column in range(9):
            openTileCount = 0
            openNumSet = set()

            for row in range(9):
                if type(self.fullPossibilities[(row, column)]) == list:
                    openNumSet.update(self.fullPossibilities[(row, column)])
                    openTileCount += 1
                    
            if len(openNumSet) != openTileCount:
                return False

        for x in range(3):
            for y in range(3):
                openTileCount = 0
                openNumSet = set()
                boxX = (x * 3)
                boxY = (y * 3)

                for i in range(3):
                    for j in range(3):
                        if type(self.fullPossibilities[(boxX+i, boxY+j)]) == list:
                            openNumSet.update(self.fullPossibilities[(boxX+i, boxY+j)])
                            openTileCount += 1

                if len(openNumSet) != openTileCount:
                    return False
        return True

    # Checks if number is in the row
    def inRow(self, tSudokuGrid, gridX, numCheck):
        for i in tSudokuGrid[gridX]:
            if i == numCheck:
                return False
        return True

    # Checks if number is in the column
    def inColumn(self, tSudokuGrid, gridY, numCheck):
        for x in range(9):
            if tSudokuGrid[x][gridY] == numCheck:
                return False
        return True

    # Checks if number is in the box
    def inBox(self, tSudokuGrid, gridX, gridY, numCheck):
        boxX = (gridX // 3) * 3
        boxY = (gridY // 3) * 3

        for i in range(3):
            for j in range(3):
                if tSudokuGrid[boxX+i][boxY+j] == numCheck:
                    return False
        return True
