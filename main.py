import tkinter as tk
from tkinter import ttk
from SudokuSolver import *
import threading as th

# Clears down the Sudoku grid
def reset():
    for rows in entryGrid:
        for entry in rows:
            entry.delete(0, 'end')
    errorVar.set("")

# Initializes thread for solve function
def startSolve():
    errorVar.set('')
    sudokuGrid = []
    for x, rows in enumerate(entryGrid):
        sudokuGrid.append([])
        for y, entry in enumerate(rows):
            if entry.get() == '':
                num = 0
            else:
                num = int(entry.get())
            sudokuGrid[x].append(num)

    resetButton['state'] = tk.DISABLED
    solveButton['state'] = tk.DISABLED

    sThread = th.Thread(target=solve, args=(sudokuGrid,))
    sThread.start()

# Runs solving algorithm and displays the solution
def solve(sudokuGrid):
    sSolver = SudokuSolver(sudokuGrid)
    if(sSolver.simplifyGrid()):
        if(sSolver.solveSudoku()):
            for x, rows in enumerate(entryGrid):
                for y, entry in enumerate(rows):
                    entry.delete(0, 'end')
                    entry.insert(0, sudokuGrid[x][y])
        else:
            errorVar.set('No solution exists')
    else:
        errorVar.set('No solution exists')

    resetButton['state'] = tk.NORMAL
    solveButton['state'] = tk.NORMAL
    
# Validates the input of the sudoku text boxes so only blanks or numbers 1-9 can be entered    
def validateInput(s):
    if len(s) <= 1 and s in ('', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        return True
    else:
        return False

if __name__ == '__main__':
    ui = tk.Tk()
    ui.title('Sudoku Solver')
    ui.geometry('500x450')

    borderFrame = tk.Frame(ui, bd=15)
    borderFrame.pack()

    sudokuFrame = tk.Frame(borderFrame, bd=3, bg='black')
    sudokuFrame.pack()
    vCmd = sudokuFrame.register(validateInput)

    entryGrid = []
    for i in range(9):
        entryGrid.append([])
        for j in range(9):
            entryGrid[i].append(tk.Entry(sudokuFrame, width=3, justify=tk.CENTER, font=('Times New Roman', 22), validate='key', validatecommand=(vCmd, '%P')))
            entryGrid[i][j].grid(row = i + (i // 3), column = j + (j // 3))

    hSeparator1 = ttk.Separator(sudokuFrame, orient='horizontal')
    hSeparator1.grid(row = 3, column = 0)

    hSeparator2 = ttk.Separator(sudokuFrame, orient='horizontal')
    hSeparator2.grid(row = 7, column = 0)
        
    vSeparator1 = ttk.Separator(sudokuFrame, orient='vertical')
    vSeparator1.grid(row = 0 ,column = 3)

    vSeparator2 = ttk.Separator(sudokuFrame, orient='vertical')
    vSeparator2.grid(row = 0, column = 7)

    bottomFrame = tk.Frame(ui)
    bottomFrame.pack()

    resetButton = tk.Button(bottomFrame, font=('TkTextFont', 10), text='Reset', command = reset)
    resetButton.grid(row=1, column=1, padx = 20)

    solveButton = tk.Button(bottomFrame, font=('TkTextFont', 10), text='Solve', command = startSolve)
    solveButton.grid(row=1, column=2, padx = 20)

    errorFrame = tk.Frame(ui)
    errorFrame.pack()

    errorVar = tk.StringVar()
    msgLabel = tk.Label(errorFrame, font=('TkTextFont', 10), textvariable = errorVar)
    msgLabel.pack()

    tk.mainloop()
