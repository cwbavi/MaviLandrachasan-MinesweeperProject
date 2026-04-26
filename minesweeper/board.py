from cell import *
from graphics import *
from random import *

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
        
        """
        Creates cells and puts them into a list
        Note: when these cells are created, they are also drawn, so there is no need for a _draw method for the board.
        """
        self.cells = [[Cell(row, col, cellSize, win) for col in range(self.cols)] for row in range(self.rows)]
        self.mines = []
    
    # Returns the cell from the row and col if there isn't an index error. Otherwise, it returne None.
    def _cells(self, row, col):

        # Python actually allows negative indexing, so if the row or col is negative, it returns None instead of a cell from the end of the list.
        if row < 0 or col < 0:
            return None
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
    def initialReveal(self, cell0):


        # Creates mines until the quota of mines has been met.
        i = 0
        while i < self.numMines:
            x = randint(0, self.rows - 1)
            y = randint(0, self.cols - 1)

            # The mine cannot be in reach of the first reveal and it cannot be placed at the location of another mine.
            if abs(cell0.row - x) > 1 and abs(cell0.col - y) > 1 and ([x, y] not in self.mines):
                self.mines.append([x, y])
                i += 1
        
        # Changes the properties of the selected cells to become mines.
        for mine in self.mines:
            """
            A mine is represented by adjacentMines = 9.
            This is because the maximum number of adjacent mines is 8, so 9 can be used to represent a mine without confusion.
            """
            self.cells[mine[0]][mine[1]].fill(True, 9)

        # Sets adjacent mines
        for i in self.cells:
            for cell1 in i:
                adjacentMines = 0
                if not cell1.isMine:
                    for x in var:
                        for y in var:
                            if [cell1.row + x, cell1.col + y] in self.mines:
                                adjacentMines += 1
                    cell1.fill(False, adjacentMines)
        self._floodFill(cell0)
    
    # Reveals the cell. Flood fills if completely empty. Returns True if a mine is revealed, False otherwise.
    def reveal(self, cell):

        # Flood fill
        if cell.adjacentMines == 0:
            self._floodFill(cell)
        else:
            cell.reveal()

        # Return statement for game over if a mine is revealed.
        return cell.isMine
    
    # Flags the cell.
    def flag(self, cell):
        cell.flag()

    # Reveals all mines on the board (called on game over).
    def revealAllMines(self):
        for mine in self.mines:
            self.cells[mine[0]][mine[1]].reveal()

    # Returns the cell that is clicked on. If the click is outside of the board, it returns None.
    def getClickedCell(self, clickPoint):
        
        # Looks through every cell to see if the click is within the cell's area. If it is, it returns that cell.
        for row in self.cells:
            for cell in row:
                if cell.containsClick(clickPoint):
                    return cell
        
        # If the click is outside of the board, it returns None.
        return None
    
    # Looks through every cell to see if all non-mine cells are revealed. If they are, it returns True. Otherwise, it returns False.
    def isSolved(self):
        
        # Looks through every cell.
        for row in self.cells:
            for cell in row:

                # If the cell is not a mine and it is not revealed, then the board is not solved, so it returns False.
                if (not cell.isMine) and not (cell.isRevealed):
                    return False

        # If all non-mine cells are revealed, the board is solved.
        return True