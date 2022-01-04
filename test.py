from SudokuSolver import *
import json 
import copy
import time
from datetime import datetime
from multiprocessing import Process, Queue

def solveProcess(solveQueue):
    sudokuGrid = solveQueue.get()
   
    if(solveSudoku(sudokuGrid)):
        solveQueue.put(True)
        solveQueue.put(sudokuGrid)
    else:
        solveQueue.put(False)

if __name__ == '__main__':
    with open('testcases.json', 'r') as read_file:
        dataFile = json.load(read_file)

    for testCase in dataFile:
        print('Test Case:', testCase)
        print('Description:', dataFile[testCase]['description'])
        sudokuGrid = copy.deepcopy(dataFile[testCase]['sudoku'])
        solution = dataFile[testCase]['solution']

        ##simplifyGrid() test section
        startTime = datetime.now()
        result = simplifyGrid(sudokuGrid)
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

        ##simplify -> solve test section
        if (result != False) and (sudokuGrid != solution):
            startTime = datetime.now()
            result = solveSudoku(sudokuGrid)
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


        ##solveSudoku() only test section
        sudokuGrid = copy.deepcopy(dataFile[testCase]['sudoku'])

        solveQueue = Queue()
        solveQueue.put(sudokuGrid)
        solveTask = Process(target=solveProcess, args=(solveQueue,))

        timeout = 20
        startTime = datetime.now()
        solveTask.start()
        endTime = datetime.now()
        while (endTime - startTime).seconds < timeout:
            time.sleep(.01)
            endTime = datetime.now()
            if not solveTask.is_alive():
                result = solveQueue.get()
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
        
        print('Time to solve:', endTime - startTime, '\n')


