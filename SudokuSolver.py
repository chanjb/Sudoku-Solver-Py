class SudokuSolver:

    def __init__(self, tSudokuGrid):
        self.sudokuGrid = tSudokuGrid
        self._fullPossibilities = dict()
        self._rescanQueue = []
        self._fullCountScanXYZ = [0,0,0]
        self._numCounts = [0] * 10
        self._tileList = dict()

    # Returns a list of all possible valid numbers for a grid position
    def _findPossibilities(self, tSudokuGrid, gridX, gridY):
        pList = []
        for i in range(1,10):
            if (self._inRow(tSudokuGrid, gridX, i) and self._inColumn(tSudokuGrid, gridY, i) and self._inBox(tSudokuGrid, gridX, gridY, i)):
                pList.append(i)
        return pList

    # Returns a dictionary with grid position as the key and list of possibilites as the value
    def _constructNextTilePossibilities(self, tSudokuGrid):
        tPossibilities = dict()
        for x, rows in enumerate(tSudokuGrid):
            for y, num in enumerate(rows):
                if num == 0:
                    tPossibilities[(x, y)] = self._findPossibilities(tSudokuGrid, x, y)
                    return tPossibilities
        return {}

    # Backtracking algorithm to solve Sudoku
    def solveSudoku(self, tSudokuGrid = None):
        if tSudokuGrid is None:
            tSudokuGrid = self.sudokuGrid
        tile = self._constructNextTilePossibilities(tSudokuGrid)
        for xy in tile:
            gridX, gridY = xy
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
                    pList = self._findPossibilities(self.sudokuGrid, x, y)
                    if len(pList) == 0:
                        return False   
                    elif len(pList) == 1:
                        self.sudokuGrid[x][y] = pList[0]
                        self._fullPossibilities[(x, y)] = pList[0]
                        self._rescanQueue.append((x, y, pList[0]))
                    else:
                        self._fullPossibilities[(x, y)] = pList
                else:
                    self._fullPossibilities[(x, y)] = self.sudokuGrid[x][y]

        while self._rescanQueue or self._fullCountScanXYZ != [1,1,1]:
            if self._rescanQueue:
                gridX, gridY, sNum = self._rescanQueue[0]

                # Scan row
                self._numCounts = [0] * 10
                self._tileList = dict()
                
                for row in range(9):
                    if not self._updateChecks(row, gridY, sNum):
                        return False
                if not self._checkCountList(self._fullCountScanXYZ[0]):
                    return False

                # Scan column
                self._numCounts = [0] * 10
                self._tileList = dict()
                
                for column in range(9):
                    if not self._updateChecks(gridX, column, sNum):
                        return False
                if not self._checkCountList(self._fullCountScanXYZ[1]):
                    return False

                # Scan box
                self._numCounts = [0] * 10
                self._tileList = dict()
                boxX = (gridX // 3) * 3
                boxY = (gridY // 3) * 3
                for i in range(3):
                    for j in range(3):
                        if not self._updateChecks(boxX+i, boxY+j, sNum):
                            return False
                if not self._checkCountList(self._fullCountScanXYZ[2]):
                    return False
                
                self._rescanQueue.pop(0)

            # Row counts
            if not self._rescanQueue:
                for row in range(9):
                    self._numCounts = [0] * 10
                    self._tileList = dict()
                    
                    for column in range(9):
                        if not self._updateChecks(row, column):
                            return False
                    if not self._checkCountList(self._fullCountScanXYZ[0]):
                        return False
                self._fullCountScanXYZ[0] = 1
                
            # Colomn counts                 
            if not self._rescanQueue:
                for column in range(9):
                    self._numCounts = [0] * 10
                    self._tileList = dict()
                    
                    for row in range(9):
                        if not self._updateChecks(row, column):
                            return False
                    if not self._checkCountList(self._fullCountScanXYZ[1]):
                        return False
                self._fullCountScanXYZ[1] = 1

            # Box counts
            if not self._rescanQueue:
                for x in range(3):
                    for y in range(3):
                        self._numCounts = [0] * 10
                        self._tileList = dict()
                        boxX = x * 3
                        boxY = y * 3
                        
                        for i in range(3):
                            for j in range(3):
                                if not self._updateChecks(boxX+i, boxY+j):
                                    return False
                        if not self._checkCountList(self._fullCountScanXYZ[2]):
                            return False
                self._fullCountScanXYZ[2] = 1

        ##if not (self.validateGrid()):
            ##return False 
        return True

    # Removes nummber from possibility list if supplied
    # Increments number count list for later check
    def _updateChecks(self, xCheck, yCheck, numCheck = None):
        if type(self._fullPossibilities[(xCheck, yCheck)]) == list:
            pList = self._fullPossibilities[(xCheck, yCheck)]
            if numCheck is not None:
                try:
                    pList.remove(numCheck)
                except:
                    pass

                if len(pList) == 0:
                    return False
                elif len(pList) == 1:
                    self.sudokuGrid[xCheck][yCheck] = pList[0]
                    self._fullPossibilities[(xCheck, yCheck)] = pList[0]
                    self._rescanQueue.append((xCheck, yCheck, pList[0]))
                else:
                    self._fullPossibilities[(xCheck, yCheck)] = pList

            for pNum in pList:
                self._numCounts[pNum] += 1
                self._tileList[pNum] = (xCheck, yCheck)
        else:
            self._numCounts[self._fullPossibilities[(xCheck, yCheck)]] += 10
        return True

    # Checks count list for solutions and for invalid entries
    def _checkCountList(self, scanXYZ):
        for index, count in enumerate(self._numCounts):
            if count == 0 and index != 0:
                return False              
            elif count == 1:
                tileX = self._tileList[index][0]
                tileY = self._tileList[index][1]
                self.sudokuGrid[tileX][tileY] = index
                self._fullPossibilities[(tileX, tileY)] = index
                self._rescanQueue.append((tileX, tileY, index))
                if self._fullCountScanXYZ[2] == scanXYZ:
                    break
            elif count > 19:
                return False
        return True

    # Validates grid by checking the number of open tiles in the row/column/box equals
    # to the number of distinct possibilities still remaining
    def _validateGrid(self):
        for row in range(9):
            openTileCount = 0
            openNumSet = set()

            for column in range(9):
                if type(self._fullPossibilities[(row, column)]) == list:
                    openNumSet.update(self._fullPossibilities[(row, column)])
                    openTileCount += 1

            if len(openNumSet) != openTileCount:
                return False

        for column in range(9):
            openTileCount = 0
            openNumSet = set()

            for row in range(9):
                if type(self._fullPossibilities[(row, column)]) == list:
                    openNumSet.update(self._fullPossibilities[(row, column)])
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
                        if type(self._fullPossibilities[(boxX+i, boxY+j)]) == list:
                            openNumSet.update(self._fullPossibilities[(boxX+i, boxY+j)])
                            openTileCount += 1

                if len(openNumSet) != openTileCount:
                    return False
        return True

    # Checks if number is in the row
    def _inRow(self, tSudokuGrid, gridX, numCheck):
        for i in tSudokuGrid[gridX]:
            if i == numCheck:
                return False
        return True

    # Checks if number is in the column
    def _inColumn(self, tSudokuGrid, gridY, numCheck):
        for x in range(9):
            if tSudokuGrid[x][gridY] == numCheck:
                return False
        return True

    # Checks if number is in the box
    def _inBox(self, tSudokuGrid, gridX, gridY, numCheck):
        boxX = (gridX // 3) * 3
        boxY = (gridY // 3) * 3

        for i in range(3):
            for j in range(3):
                if tSudokuGrid[boxX+i][boxY+j] == numCheck:
                    return False
        return True
