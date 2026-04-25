import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../minesweeper'))
from graphics import *

# Cell size in pixels
CELL_SIZE = 40

# Colors
COLOR_UNREVEALED = color_rgb(180, 180, 180)  # grey
COLOR_REVEALED   = color_rgb(220, 220, 220)  # light grey
COLOR_MINE       = color_rgb(255, 60,  60)   # red
COLOR_FLAG       = color_rgb(255, 165, 0)    # orange
COLOR_OUTLINE    = color_rgb(100, 100, 100)  # dark grey

# Number colors (classic minesweeper colors)
NUMBER_COLORS = {
    1: color_rgb(0,   0,   255),  # blue
    2: color_rgb(0,   128, 0),    # green
    3: color_rgb(255, 0,   0),    # red
    4: color_rgb(0,   0,   128),  # dark blue
    5: color_rgb(128, 0,   0),    # dark red
    6: color_rgb(0,   128, 128),  # teal
    7: color_rgb(0,   0,   0),    # black
    8: color_rgb(128, 128, 128),  # grey
}


class Cell:
    def __init__(self, row, col):
        """
        Represents a single cell on the minesweeper board.

        Args:
            row (int): Row index of the cell on the grid
            col (int): Column index of the cell on the grid
        """
        self.row = row
        self.col = col

        # State
        self.is_mine     = False
        self.is_revealed = False
        self.is_flagged  = False
        self.count       = 0       # number of neighboring mines

        # Graphics objects (set when drawn)
        self.rect   = None
        self.label  = None

        # Pixel position of top-left corner
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE

    # ------------------------------------------------------------------ #
    #  State setters                                                       #
    # ------------------------------------------------------------------ #

    def set_mine(self):
        """Mark this cell as containing a mine."""
        self.is_mine = True

    def set_count(self, n):
        """
        Set the number of mines in neighboring cells.

        Args:
            n (int): Neighbor mine count (0-8)
        """
        self.count = n

    # ------------------------------------------------------------------ #
    #  Drawing                                                             #
    # ------------------------------------------------------------------ #

    def draw(self, win):
        """
        Draw the cell on the GraphWin for the first time.

        Args:
            win (GraphWin): The game window to draw on
        """
        x1 = self.x
        y1 = self.y
        x2 = self.x + CELL_SIZE
        y2 = self.y + CELL_SIZE

        self.rect = Rectangle(Point(x1, y1), Point(x2, y2))
        self.rect.setFill(COLOR_UNREVEALED)
        self.rect.setOutline(COLOR_OUTLINE)
        self.rect.draw(win)

    def _redraw(self):
        """Redraw the cell after a state change."""
        if self.is_revealed:
            if self.is_mine:
                self.rect.setFill(COLOR_MINE)
                # Draw a simple 'M' to represent a mine
                self._set_label('M', color_rgb(0, 0, 0))
            else:
                self.rect.setFill(COLOR_REVEALED)
                if self.count > 0:
                    color = NUMBER_COLORS.get(self.count, color_rgb(0, 0, 0))
                    self._set_label(str(self.count), color)
                else:
                    self._clear_label()
        elif self.is_flagged:
            self.rect.setFill(COLOR_FLAG)
            self._set_label('F', color_rgb(255, 255, 255))
        else:
            self.rect.setFill(COLOR_UNREVEALED)
            self._clear_label()

    def _set_label(self, text, color):
        """
        Display a text label in the center of the cell.

        Args:
            text  (str): Text to display
            color (str): Color string for the text
        """
        cx = self.x + CELL_SIZE // 2
        cy = self.y + CELL_SIZE // 2
        if self.label:
            self.label.setText(text)
            self.label.setTextColor(color)
        else:
            self.label = Text(Point(cx, cy), text)
            self.label.setTextColor(color)
            self.label.setSize(14)
            self.label.setStyle('bold')
            self.label.draw(self.rect.canvas)  # draw on the same canvas

    def _clear_label(self):
        """Remove any text label from the cell."""
        if self.label:
            self.label.undraw()
            self.label = None

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #

    def reveal(self):
        """
        Reveal the cell. Has no effect if already revealed or flagged.

        Returns:
            bool: True if the cell was successfully revealed, False otherwise
        """
        if self.is_revealed or self.is_flagged:
            return False
        self.is_revealed = True
        self._redraw()
        return True

    def flag(self):
        """
        Toggle the flag on this cell. Cannot flag a revealed cell.

        Returns:
            bool: True if the flag was toggled, False if cell is already revealed
        """
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        self._redraw()
        return True

    # ------------------------------------------------------------------ #
    #  Click detection                                                     #
    # ------------------------------------------------------------------ #

    def contains_click(self, point):
        """
        Check whether a clicked point falls inside this cell.

        Args:
            point (Point): The point returned by GraphWin.getMouse()

        Returns:
            bool: True if the point is within the cell boundaries
        """
        x, y = point.getX(), point.getY()
        return (self.x <= x <= self.x + CELL_SIZE and
                self.y <= y <= self.y + CELL_SIZE)

    # ------------------------------------------------------------------ #
    #  Utility                                                             #
    # ------------------------------------------------------------------ #

    def __repr__(self):
        return (f"Cell(row={self.row}, col={self.col}, "
                f"mine={self.is_mine}, revealed={self.is_revealed}, "
                f"flagged={self.is_flagged}, count={self.count})")