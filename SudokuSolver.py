## Returns a list of all possible valid numbers for a grid position
def findPossibilities(sudokuGrid, x, y):
    pList = []
    for i in range(1,10):
        if (inRow(sudokuGrid, x, i) and inColumn(sudokuGrid, y, i) and inBox(sudokuGrid, x, y, i)):
            pList.append(i)
    return pList

## Returns a dictionary with grid position as the key and list of possibilites as the value
def constructNextTilePossibilities(sudokuGrid):
    tPossibilities = dict()
    for x, rows in enumerate(sudokuGrid):
        for y, num in enumerate(rows):
            if num == 0:
                tPossibilities[(x,y)] = findPossibilities(sudokuGrid, x, y)
                return tPossibilities
    return {}

## Backtracking algorithm to solve Sudoku
def solveSudoku(sudokuGrid):
    tile = constructNextTilePossibilities(sudokuGrid)
    for xy in tile:
        x = xy[0]
        y = xy[1]
        for i in tile[xy]:
            sudokuGrid[x][y] = i
            if (solveSudoku(sudokuGrid)):
                return True
        sudokuGrid[x][y] = 0
        return False
    return True

## Runs before backtracking algorithm to reduce the number of permutations
## Finds simple solutions where only 1 possibility exists for a grid position
## And where a specific number has only 1 possiible location is a row/column/box
## Also performs 3 validation checks while scanning for solutions which antiquated the validateGrid() function
## By checking if there are zero possibilities for a grid position,
## if a distinct number has no possible locations in the row/column/box,
## and if a distinct number had a duplicate entry in the row/column/box for the initial grid
def simplifyGrid(sudokuGrid):
    rescanQueue = []
    fullCountScanXYZ = [0,0,0]
    tPossibilities = dict()
    for x, rows in enumerate(sudokuGrid):
        for y, num in enumerate(rows):
            if num == 0:
                pList = findPossibilities(sudokuGrid, x, y)
                if len(pList) == 0:
                    return False
                    
                if len(pList) == 1:
                    sudokuGrid[x][y] = pList[0]
                    tPossibilities[(x,y)] = pList[0]
                    rescanQueue.append([(x,y), pList[0]])
                else:
                    tPossibilities[(x,y)] = pList
            else:
                tPossibilities[(x,y)] = sudokuGrid[x][y]

    while rescanQueue or fullCountScanXYZ != [1,1,1]:
        if rescanQueue:
            xy = rescanQueue[0][0]
            x = xy[0]
            y = xy[1]
            snum = rescanQueue[0][1]

            # Scan row
            numCounts = [0] * 10
            tileList = dict()
            
            for row in range(9):
                if type(tPossibilities[(row,y)]) == list:    
                    pList = tPossibilities[(row,y)]
                    try:
                        pList.remove(snum)
                    except:
                        pass
                    
                    if len(pList) == 0:
                        return False

                    if len(pList) == 1:
                        sudokuGrid[row][y] = pList[0]
                        tPossibilities[(row,y)] = pList[0]
                        rescanQueue.append([(row,y), pList[0]])
                    else:
                        tPossibilities[(row,y)] = pList

                    for pNum in pList:
                        numCounts[pNum] += 1
                        tileList[pNum] = (row, y)
                else:
                    numCounts[tPossibilities[(row,y)]] += 10

            if not (checkCountList(tileList, numCounts)):
                return False
                ''' 
            for index, count in enumerate(numCounts):
                if count == 0 and index != 0:
                    return False
                
                if count == 1:
                    tileX = tileList[index][0]
                    tileY = tileList[index][1]
                    sudokuGrid[tileX][tileY] = index
                    tPossibilities[(tileX, tileY)] = index
                    rescanQueue.append([(tileX, tileY), index])

                if count > 19:
                    return False
                    '''

            # Scan column
            numCounts = [0] * 10
            tileList = dict()
            
            for column in range(9):
                if type(tPossibilities[(x,column)]) == list:    
                    pList = tPossibilities[(x,column)]
                    try:
                        pList.remove(snum)
                    except:
                        pass
                    
                    if len(pList) == 0:
                        return False

                    if len(pList) == 1:
                        sudokuGrid[x][column] = pList[0]
                        tPossibilities[(x,column)] = pList[0]
                        rescanQueue.append([(x,column), pList[0]])
                    else:
                        tPossibilities[(x,column)] = pList

                    for pNum in pList:
                        numCounts[pNum] += 1
                        tileList[pNum] = (x, column)
                else:
                    numCounts[tPossibilities[(x,column)]] += 10

            if not (checkCountList(tileList, numCounts)):
                return False
                ''' 
            for index, count in enumerate(numCounts):
                if count == 0 and index != 0:
                    return False
                
                if count == 1:
                    tileX = tileList[index][0]
                    tileY = tileList[index][1]
                    sudokuGrid[tileX][tileY] = index
                    tPossibilities[(tileX, tileY)] = index
                    rescanQueue.append([(tileX, tileY), index])

                if count > 19:
                    return False
                    '''

            # Scan box
            numCounts = [0] * 10
            tileList = dict()
            boxX = (x // 3) * 3
            boxY = (y // 3) * 3
            for i in range(3):
                for j in range(3):
                    if type(tPossibilities[(boxX+i, boxY+j)]) == list:
                        pList = tPossibilities[(boxX+i, boxY+j)]
                        try:
                            pList.remove(snum)
                        except:
                            pass

                        if len(pList) == 0:
                            return False

                        if len(pList) == 1:
                            sudokuGrid[boxX+i][boxY+j] = pList[0]
                            tPossibilities[(boxX+i, boxY+j)] = pList[0]
                            rescanQueue.append([(boxX+i, boxY+j), pList[0]])
                        else:
                            tPossibilities[(boxX+i, boxY+j)] = pList

                        for pNum in pList:
                            numCounts[pNum] += 1
                            tileList[pNum] = (boxX+i, boxY+j)
                    else:
                        numCounts[tPossibilities[(boxX+i, boxY+j)]] += 10

            if not (checkCountList(tileList, numCounts)):
                return False
                ''' 
            for index, count in enumerate(numCounts):
                if count == 0 and index != 0:
                    return False
                    
                if count == 1:
                    tileX = tileList[index][0]
                    tileY = tileList[index][1]
                    sudokuGrid[tileX][tileY] = index
                    tPossibilities[(tileX, tileY)] = index
                    rescanQueue.append([(tileX, tileY), index])

                if count > 19:
                    return False
                    '''
            
            rescanQueue.pop(0)

        if not rescanQueue:
            for row in range(9):
                numCounts = [0] * 10
                tileList = dict()
                
                for column in range(9):
                    if type(tPossibilities[(row, column)]) == list:
                        for pNum in tPossibilities[(row, column)]:
                            numCounts[pNum] += 1
                            tileList[pNum] = (row, column)
                    else:
                        numCounts[tPossibilities[(row, column)]] += 10

                if not (checkCountList(tileList, numCounts)):
                    return False
                    ''' 
                for index, count in enumerate(numCounts):
                    if count == 0 and index != 0:
                        return False
                    
                    if count == 1:
                        tileX = tileList[index][0]
                        tileY = tileList[index][1]
                        sudokuGrid[tileX][tileY] = index
                        tPossibilities[(tileX, tileY)] = index
                        rescanQueue.append([(tileX, tileY), index])
                        if fullCountScanXYZ[0] == 1:
                            break

                    if count > 19:
                        return False
                        '''
            fullCountScanXYZ[0] = 1
            
                            
        if not rescanQueue:
            for column in range(9):
                numCounts = [0] * 10
                tileList = dict()
                
                for row in range(9):
                    if type(tPossibilities[(row, column)]) == list:
                        for pNum in tPossibilities[(row, column)]:
                            numCounts[pNum] += 1
                            tileList[pNum] = (row, column)
                    else:
                        numCounts[tPossibilities[(row, column)]] += 10

                if not (checkCountList(tileList, numCounts)):
                    return False
                    ''' 
                for index, count in enumerate(numCounts):
                    if count == 0 and index != 0:
                        return False
                        
                    if count == 1:
                        tileX = tileList[index][0]
                        tileY = tileList[index][1]
                        sudokuGrid[tileX][tileY] = index
                        tPossibilities[(tileX, tileY)] = index
                        rescanQueue.append([(tileX, tileY), index])
                        if fullCountScanXYZ[1] == 1:
                            break

                    if count > 19:
                        return False
                        '''
            fullCountScanXYZ[1] = 1

        if not rescanQueue:
            for x in range(3):
                for y in range(3):
                    numCounts = [0] * 10
                    tileList = dict()
                    
                    for i in range(3):
                        for j in range(3):
                            boxX = (x * 3) + i
                            boxY = (y * 3) + j
                            if type(tPossibilities[(boxX, boxY)]) == list:
                                for pNum in tPossibilities[(boxX, boxY)]:
                                    numCounts[pNum] += 1
                                    tileList[pNum] = (boxX, boxY)
                            else:
                                numCounts[tPossibilities[(boxX, boxY)]] += 10

                    if not (checkCountList(tileList, numCounts)):
                        return False
                        '''     
                    for index, count in enumerate(numCounts):
                        if count == 0 and index != 0:
                            return False
                        
                        if count == 1:
                            tileX = tileList[index][0]
                            tileY = tileList[index][1]
                            sudokuGrid[tileX][tileY] = index
                            tPossibilities[(tileX, tileY)] = index
                            rescanQueue.append([(tileX, tileY), index])
                            if fullCountScanXYZ[2] == 1:
                                break

                        if count > 19:
                            return False
                        '''
            fullCountScanXYZ[2] = 1

##    if not (validateGrid(tPossibilities)):
##        return False 
    return True

## Checks count list for solutions and for invalid entries
def checkCountList(tileList, numCounts):
    for index, count in enumerate(numCounts):
        if count == 0 and index != 0:
            return False
                        
        if count == 1:
            tileX = tileList[index][0]
            tileY = tileList[index][1]
            sudokuGrid[tileX][tileY] = index
            tPossibilities[(tileX, tileY)] = index
            rescanQueue.append([(tileX, tileY), index])
            if fullCountScanXYZ[2] == 1:
                break

            if count > 19:
                return False
    return True

## Validates grid by checking the number of open tiles in the row/column/box equals
## to the number of distinct possibilities still remaining
def validateGrid(tPossibilities):
    for row in range(9):
        openTileCount = 0
        openNumSet = set()

        for column in range(9):
            if type(tPossibilities[(row, column)]) == list:
                openNumSet.update(tPossibilities[(row, column)])
                openTileCount += 1

        if len(openNumSet) != openTileCount:
            return False

    for column in range(9):
        openTileCount = 0
        openNumSet = set()

        for row in range(9):
            if type(tPossibilities[(row, column)]) == list:
                openNumSet.update(tPossibilities[(row, column)])
                openTileCount += 1
                
        if len(openNumSet) != openTileCount:
            return False

    for x in range(3):
        for y in range(3):
            openTileCount = 0
            openNumSet = set()

            for i in range(3):
                for j in range(3):
                    boxX = (x * 3) + i
                    boxY = (y * 3) + j
                    if type(tPossibilities[(boxX, boxY)]) == list:
                        openNumSet.update(tPossibilities[(boxX, boxY)])
                        openTileCount += 1

            if len(openNumSet) != openTileCount:
                return False
    return True

## Checks if number is in the row
def inRow(sudokuGrid, x, num):
    for i in sudokuGrid[x]:
        if i == num:
            return False
    return True

## Checks if number is in the column
def inColumn(sudokuGrid, y, num):
    for x in range(9):
        if sudokuGrid[x][y] == num:
            return False
    return True

## Checks if number is in the box
def inBox(sudokuGrid, x, y, num):
    x = (x // 3) * 3
    y = (y // 3) * 3

    for i in range(3):
        for j in range(3):
            if sudokuGrid[x+i][y+j] == num:
                return False
    return True
