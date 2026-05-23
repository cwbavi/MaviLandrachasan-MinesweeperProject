from board import *
from graphics import *

# Window size for the game
window_size = 600
window_height = window_size + 60

# Difficulty settings for the game. Easy = index 0, Medium = index 1, Hard = index 2
difficulties = [[8, 8, 10], [16, 16, 40], [16, 30, 99]]

# Main game class that handles the game logic and user interface
class Game:

    # Initialize the game with the selected difficulty level and set up the board and window
    def __init__(self, difficulty):
        self.rows, self.cols, self.mines = difficulties[difficulty]
        self.window = GraphWin("Minesweeper", window_size, window_height)
        self.cell_size = window_size // max(self.rows, self.cols)
        self.isFirstClick = True
        self.isOver = False
        self.flagged_cells = 0

        self.win = GraphWin("Minesweeper", window_size, window_size)
        self.win.setBackground(color_rgb(50, 50, 50))

        self.board = Board(self.rows, self.cols, self.mines, self.win, self.cell_size)
        self.board.draw()

        self.hudItems = []
        self._drawHUD()

    #Draw the heads-up display (HUD) that shows the number of mines left and game status
    def _drawHUD(self):
        # Clear existing HUD items
        for item in self.hudItems:
            item.undraw()
        self.hudItems.clear()

        hudY = self.rows * self.cellSize  # top of HUD strip

        # HUD background
        bg = Rectangle(Point(0, hudY), Point(self.window_size, self.window_height))
        bg.setFill(color_rgb(30, 30, 30))
        bg.setOutline(color_rgb(30, 30, 30))
        bg.draw(self.win)
        self.hudItems.append(bg)

        # Mine counter (remaining mines = numMines - flags placed)
        remaining = self.numMines - self.flagCount
        mineText = Text(Point(60, hudY + 30), "Mines: " + str(remaining))
        mineText.setTextColor("white")
        mineText.setSize(14)
        mineText.setStyle("bold")
        mineText.draw(self.win)
        self.hudItems.append(mineText)

        # Flag button
        flagBox = Rectangle(Point(self.window_size // 2 - 40, hudY + 10),
                            Point(self.window_size // 2 + 40, hudY + 50))
        flagBox.setFill(color_rgb(80, 80, 80))
        flagBox.draw(self.win)
        self.hudItems.append(flagBox)

        flagLabel = Text(Point(self.window_size // 2, hudY + 30), "Flag Mode")
        flagLabel.setTextColor("white")
        flagLabel.setSize(12)
        flagLabel.draw(self.win)
        self.hudItems.append(flagLabel)

        # Quit button
        quitBox = Rectangle(Point(self.window_size - 90, hudY + 10),
                            Point(self.window_size - 10, hudY + 50))
        quitBox.setFill(color_rgb(180, 50, 50))
        quitBox.draw(self.win)
        self.hudItems.append(quitBox)

        quitLabel = Text(Point(self.window_size - 50, hudY + 30), "Quit")
        quitLabel.setTextColor("white")
        quitLabel.setSize(12)
        quitLabel.setStyle("bold")
        quitLabel.draw(self.win)
        self.hudItems.append(quitLabel)

        # Store button bounds for click detection
        self.flagBoxBounds = (self.window_size // 2 - 40, hudY + 10,
                              self.window_size // 2 + 40, hudY + 50)
        self.quitBoxBounds = (self.window_size - 90, hudY + 10,
                              self.window_size - 10,  hudY + 50)
        
        def _inBounds(self, x, y, bounds):
            return bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]
        
        def _drawEndScreen(self, message):
            # Draw end game screen with message
            overlay = Rectangle(Point(0, 0), Point(self.window_size, self.window_height))
            overlay.setFill(color_rgb(0, 0, 0))
            overlay.setOutline(color_rgb(0, 0, 0))
            overlay.setFill(color_rgb(0, 0, 0, 150))  # semi-transparent
            overlay.draw(self.win)

            endText = Text(Point(self.window_size // 2, self.window_height // 2), message)
            endText.setTextColor("white")
            endText.setSize(24)
            endText.setStyle("bold")
            endText.draw(self.win)

        def start(self):
            while not self.isOver:
                click = self.win.getMouse()
                x, y = click.getX(), click.getY()

                if self._inBounds(x, y, self.flagBoxBounds):
                    self.board.toggleFlagMode()
                elif self._inBounds(x, y, self.quitBoxBounds):
                    self.isOver = True
                else:
                    cell = self.board.getCellAtPixel(x, y)
                    if cell:
                        if self.board.flagMode:
                            cell.toggleFlag()
                        else:
                            if self.isFirstClick:
                                self.board.placeMines(cell.row, cell.col)
                                self.isFirstClick = False
                            cell.reveal()
                            if cell.isMine:
                                self._drawEndScreen("Game Over!")
                                self.isOver = True
                            elif self.board.checkWin():
                                self._drawEndScreen("You Win!")
                                self.isOver = True

                self._drawHUD()