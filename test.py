from SudokuSolver import *
import json 
import copy
import time
from datetime import datetime
from multiprocessing import Process, Queue

def solveProcess(solveQueue):
    sSolver = solveQueue.get()

    startTime = datetime.now()
    result = sSolver.solveSudoku()
    endTime = datetime.now()

    solveQueue.put((result, startTime, endTime))
    if(result):
        solveQueue.put(sSolver.sudokuGrid)

if __name__ == '__main__':
    with open('testcases.json', 'r') as read_file:
        dataFile = json.load(read_file)

    for testCase in dataFile:
        print('Test Case:', testCase)
        print('Description:', dataFile[testCase]['description'])
        sudokuGrid = copy.deepcopy(dataFile[testCase]['sudoku'])
        sSolver = SudokuSolver(sudokuGrid)
        solution = dataFile[testCase]['solution']

        # simplifyGrid() test section
        startTime = datetime.now()
        result = sSolver.simplifyGrid()
        endTime = datetime.now()
        totalStartTime = endTime - startTime
        
        if result == dataFile[testCase]['result']:
            if result == False:
                print('Simplify/Validate: Passed (' + solution + ')')
            else:
                if sudokuGrid == solution:
                    print('Simplify/Validate: Passed')
                else:
                    print('Simplify/Validate: Unfinished Solution')
                for x in sudokuGrid:
                    print(x)
        else:
            print('Simplify/Validate: Failed')

        print('Time to simplify/validate:', totalStartTime)

        # simplify -> solve test section
        if (result != False) and (sudokuGrid != solution):
            startTime = datetime.now()
            result = sSolver.solveSudoku()
            endTime = datetime.now()
            totalStartTime += endTime - startTime
            totalStartTime = str(totalStartTime)
            
            if result == dataFile[testCase]['result']:
                if result == False:
                    print('Simply/Validate/Solve: Passed (' + solution + ')')
                else:
                    if sudokuGrid == solution:
                        print('Simplify/Validate/Solve: Passed')
                    else:
                        print('Simplify/Validate/Solve: Failed (Wrong Solution)')
                    for x in sudokuGrid:
                        print(x)
            else:
                print('Simplify/Validate/Solve: Failed')

            print('Time to solve:', endTime - startTime)
            print('Total time to simplify/validate/solve:', totalStartTime)


        # solveSudoku() only test section
        sudokuGrid = copy.deepcopy(dataFile[testCase]['sudoku'])
        sSolver = SudokuSolver(sudokuGrid)

        solveQueue = Queue()
        solveQueue.put(sSolver)
        solveTask = Process(target=solveProcess, args=(solveQueue,))

        timeout = 20
        startTimeout = datetime.now()
        solveTask.start()
        endTimeout = datetime.now()
        while (endTimeout - startTimeout).seconds < timeout:
            time.sleep(.01)
            endTimeout = datetime.now()
            if not solveTask.is_alive():
                result, startTime, endTime = solveQueue.get()
                if result:
                    sudokuGrid = solveQueue.get()
                if result == dataFile[testCase]['result']:
                    if result == False:
                        print('Solve: Passed (' + solution + ')')
                    else:
                        if sudokuGrid == solution:
                            print('Solve: Passed')
                        else:
                            print('Solve: Failed (Wrong Solution)')
                        for x in sudokuGrid:
                            print(x)
                else:
                    print('Solve - Failed')
                break
        else:
            solveTask.terminate()
            solveTask.join()
            print('Solve: Failed (Timeout - 20 secs)')
            result = False
            startTime = startTimeout
            endTime = endTimeout
        
        print('Time to solve:', endTime - startTime, '\n')
