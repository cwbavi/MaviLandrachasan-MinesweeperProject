from cell import *
from graphics import *
from random import *

class Board:

    # Creates the board with all its specs once Board is called.
    def __init__(self, rows, cols, cellSize, numMines, win):
        self.rows = rows
        self.cols = cols
        self.cellSize = cellSize
        self.numMines = numMines
        self.win = win
        
        # Creates cells and puts them into a list
        self.cells = [[Cell(row, col, cellSize, win) for col in range(self.cols)] for row in range(self.rows)]
        self.mines = [[0] * self.cols] * self.rows
        self.revealedMines = 0
        self._draw(win)
    
    # Draws the board
    def _draw(self):

        # Draws every cell
        for row in self.cells:
            for cell in row:
                cell.draw()
    
    # Returns the cell from the row and col if there isn't an index error. Otherwise, it returne None.
    def _cells(self, row, col):
        try:
            return self.cells[row][col]
        except IndexError:
            return None
    
    # When a completely empty cell is revealed, the other surrounding completely empty cells shoud be revealed too.
    def _floodFill(self, cell0):

        # Code only functions when initial cell is completely empty.
        if not cell0.isMine:
            cell0.reveal()
            if cell0.adjacentMines == 0:

                # For cells up, down, left, and right from the cell, it repeats the floodFill.
                for cell1 in [self._cells(cell0.row, cell0.col - 1),
                              self._cells(cell0.row, cell0.col + 1), 
                              self._cells(cell0.row - 1, cell0.col), 
                              self._cells(cell0.row + 1, cell0.col)]:
                    if (cell1 is not None) and (not cell1.isRevealed):
                        self._floodFill(cell1)