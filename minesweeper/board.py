from cell import *
from graphics import *
from random import *
from math import *

# Sets difference to be adjacent.
var = [-1, 0, 1]

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
        self.mines = []
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

    # The first reveal works differently as the code must ensure that the reveal lands on a completely empty square.
    def initialReveal(self, row, col):

        # Creates mines until the quota of mines has been met.
        i = 0
        while i < self.numMines:
            x = randint(0, self.rows)
            y = randint(0, self.cols)

            # The mine cannot be in reach of the first reveal and it cannot be placed at the location of another mine.
            if abs(row - x) > 1 and abs(col - y) > 1 and ([x, y] not in self.mines):
                self.mines.append([x, y])
                i += 1
        
        # Changes the properties of the selected cells to become mines.
        for mine in self.mines:
            self.cells[mine[0]][mine[1]].fill(True, 9)

        # Sets adjacent mines
        for cell in self.cells:
            adjacentMines = 0
            if not cell.isMine:
                for x in var:
                    for y in var:
                        if [cell.row + x, cell.col + y] in self.mines:
                            adjacentMines += 1
                cell.fill(False, adjacentMines)
    
    # Reveals the cell. Reveals all mines if cell is a mine and flood fills if completely empty.
    def reveal(self, row, col):
        cell = self.cells[row][col]

        # Flood fill
        if cell.adjacentMines == 0:
            self._floodFill(cell)
        else:
            cell.reveal()

            # Reveals all mines.
            if cell.isMine == True:
                for mine in self.mines:
                    self.cells[mine[0]][mine[1]].reveal()