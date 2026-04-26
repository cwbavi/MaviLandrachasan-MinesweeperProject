import os
import sys
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '../minesweeper'))
from graphics import *
from cell import Cell, CELL_SIZE


class Board:
    def __init__(self, rows, cols, num_mines):
        """
        Represents the minesweeper grid.

        Args:
            rows      (int): Number of rows in the grid
            cols      (int): Number of columns in the grid
            num_mines (int): Number of mines to place
        """
        self.rows      = rows
        self.cols      = cols
        self.num_mines = num_mines

        self.cells          = []   # 2D list of Cell objects
        self.mines_placed   = False
        self.revealed_count = 0    # how many safe cells have been revealed

        self._create_cells()

    # ------------------------------------------------------------------ #
    #  Setup                                                               #
    # ------------------------------------------------------------------ #

    def _create_cells(self):
        """Build the 2D grid of Cell objects."""
        self.cells = [
            [Cell(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def place_mines(self, exclude_row, exclude_col):
        """
        Randomly place mines, guaranteeing the first clicked cell is safe.

        Args:
            exclude_row (int): Row of the first click (never a mine)
            exclude_col (int): Col of the first click (never a mine)
        """
        all_positions = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) != (exclude_row, exclude_col)
        ]
        mine_positions = random.sample(all_positions, self.num_mines)

        for row, col in mine_positions:
            self.cells[row][col].set_mine()

        self._calculate_counts()
        self.mines_placed = True

    def _calculate_counts(self):
        """Set each cell's neighbor mine count."""
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.cells[row][col].is_mine:
                    count = sum(
                        1 for r, c in self._neighbors(row, col)
                        if self.cells[r][c].is_mine
                    )
                    self.cells[row][col].set_count(count)

    # ------------------------------------------------------------------ #
    #  Drawing                                                             #
    # ------------------------------------------------------------------ #

    def draw(self, win):
        """
        Draw all cells on the window.

        Args:
            win (GraphWin): The game window
        """
        for row in self.cells:
            for cell in row:
                cell.draw(win)

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #

    def reveal(self, row, col):
        """
        Reveal a cell. If it has no neighboring mines, flood-fill outward.

        Args:
            row (int): Row of the cell to reveal
            col (int): Column of the cell to reveal

        Returns:
            bool: True if a mine was revealed (game over), False otherwise
        """
        cell = self.cells[row][col]

        if cell.is_mine:
            cell.reveal()
            return True   # hit a mine

        self._flood_fill(row, col)
        return False

    def flag(self, row, col):
        """
        Toggle a flag on a cell.

        Args:
            row (int): Row of the cell
            col (int): Column of the cell
        """
        self.cells[row][col].flag()

    def reveal_all_mines(self):
        """Reveal all mines on the board (called on game over)."""
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.reveal()

    # ------------------------------------------------------------------ #
    #  Flood fill                                                          #
    # ------------------------------------------------------------------ #

    def _flood_fill(self, row, col):
        """
        Recursively reveal all connected empty cells.

        Args:
            row (int): Starting row
            col (int): Starting col
        """
        cell = self.cells[row][col]

        if cell.is_revealed or cell.is_flagged or cell.is_mine:
            return

        if cell.reveal():   # returns True if it was actually revealed
            self.revealed_count += 1

        # If this cell has no neighboring mines, spread to neighbors
        if cell.count == 0:
            for r, c in self._neighbors(row, col):
                self._flood_fill(r, c)

    # ------------------------------------------------------------------ #
    #  Click detection                                                     #
    # ------------------------------------------------------------------ #

    def get_clicked_cell(self, point):
        """
        Find which cell (if any) contains the clicked point.

        Args:
            point (Point): The point returned by GraphWin.getMouse()

        Returns:
            Cell or None: The clicked cell, or None if no cell was clicked
        """
        for row in self.cells:
            for cell in row:
                if cell.contains_click(point):
                    return cell
        return None

    # ------------------------------------------------------------------ #
    #  Win condition                                                       #
    # ------------------------------------------------------------------ #

    def is_solved(self):
        """
        Check whether the player has won.
        Win condition: every non-mine cell has been revealed.

        Returns:
            bool: True if the board is solved
        """
        total_safe = self.rows * self.cols - self.num_mines
        return self.revealed_count == total_safe

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _neighbors(self, row, col):
        """
        Return valid (row, col) pairs for all 8 neighbors of a cell.

        Args:
            row (int): Row of the cell
            col (int): Column of the cell

        Returns:
            list of (int, int): Valid neighboring positions
        """
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbors.append((r, c))
        return neighbors

    def __repr__(self):
        return (f"Board({self.rows}x{self.cols}, "
                f"mines={self.num_mines}, "
                f"revealed={self.revealed_count})")
