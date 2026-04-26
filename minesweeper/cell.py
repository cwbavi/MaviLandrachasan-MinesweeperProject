from graphics import *

almostBlack = color_rgb(33, 33, 33)

# Represents the colors of the numbers for adjacent mines, with the index representing how many adjacent mines present.
adjacentMineColors = [None, 
                      color_rgb(0, 0, 255), 
                      color_rgb(0, 128, 0), 
                      color_rgb(255, 0, 0), 
                      color_rgb(0, 0, 128), 
                      color_rgb(128, 0, 0), 
                      color_rgb(0, 128, 128),
                      color_rgb(0, 0, 0),
                      color_rgb(128, 128, 128)]

class Cell:

    # Creates the cell with all its specs once Cell is called.
    def __init__(self, row, col, size, win):
        self.row = row
        self.col = col
        self.size = size
        self.win = win
        self.isMine = False
        self.isRevealed = False
        self.isFlagged = False
        self.adjacentMines = 0
        self.x = self.col * self.size
        self.y = self.row * self.size

        # Creates that checkered color pattern
        if (self.row + self.col) % 2 == 0:
            self.colorUnrevealed = color_rgb(170, 215, 81)
            self.colorRevealed = color_rgb(229, 194, 159)
        else:
            self.colorUnrevealed = color_rgb(162, 209, 73)
            self.colorRevealed = color_rgb(215, 184, 153)
        self._draw()

    # Changes isMine and adjacentMines. To be called after first cell is revealed.
    def fill(self, isMine, adjacentMines):
        self.isMine = isMine
        self.adjacentMines = adjacentMines

    """
    Draws cell.
    If cell is revealed, it will show if it's a mine or how many adjacent mines there are.
    To be called at initialization and whenever a cell's state changes.
    """
    def _draw(self):
        box = Rectangle(Point(self.x, self.y), Point(self.x + self.size, self.y + self.size))
        box.draw(self.win)
        if self.isRevealed:
            
            # Draws what a mine looks like.
            if self.isMine:
                box.setFill(almostBlack)
                mine = Circle(Point(self.x + self.size / 2, self.y + self.size / 2), self.size / 4)
                mine.setFill("black")
                mine.draw(self.win)

            # Revealed box
            else:
                box.setFill(self.colorRevealed)

                # Draws the number for adjacent mines.
                if self.adjacentMines > 0:
                    number = Text(Point(self.x + self.size / 2, self.y + self.size / 2), str(self.adjacentMines))
                    number.setFill(adjacentMineColors[self.adjacentMines])
                    number.setSize(min(36, max(5, self.size // 2)))
                    number.setStyle("bold")
                    number.draw(self.win)

        # Unrevealed box        
        else:
            box.setFill(self.colorUnrevealed)

            # Draws the flag.
            if self.isFlagged:
                flag = Polygon(Point(self.x + self.size * 0.3, self.y + self.size * 0.15),
                               Point(self.x + self.size * 0.7, self.y + self.size * 0.35),
                               Point(self.x + self.size * 0.3, self.y + self.size * 0.55))
                flag.setFill("red")
                flag.draw(self.win)
                pole_x = self.x + self.size * 0.3
                pole = Line(Point(pole_x, self.y + self.size * 0.15), Point(pole_x, self.y + self.size * 0.85))
                pole.setWidth(2)
                pole.draw(self.win)

    # Digs up the cell.
    def reveal(self):
        self.isRevealed = True
        self._draw()

    # Flags the cell.
    def flag(self):
        if not self.isRevealed:
            self.isFlagged = not self.isFlagged
            self._draw()

    # Checks if mouse cursor is in the cell.
    def containsClick(self, point):
        x, y = point.getX(), point.getY()
        return (x > self.x and x < self.x + self.size and y > self.y and y < self.y + self.size)