from board import *
from graphics import *
from time import *

# Window size for the game.
windowSize = 600
windowHeight = windowSize + 60

HUDBackgroundColor = color_rgb(74, 117, 44)

# Difficulty settings for the game. Easy = index 0, Medium = index 1, Hard = index 2.
difficulties = [[9, 9, 10], [16, 16, 40], [22, 22, 99]]
difficultyNames = ["Easy", "Medium", "Hard"]

# Main game class that handles the game logic and user interface.
class Game:

    # Initialize the game with the selected difficulty level and set up the board and window.
    def __init__(self, difficulty):
        self.rows, self.cols, self.mines = difficulties[difficulty]

        # Draws the window.
        self.win = GraphWin(difficultyNames[difficulty], windowSize, windowHeight)
        self.cellSize = windowSize // max(self.rows, self.cols)
        self.isFirstClick = True
        self.isOver = False
        self.flagged_cells = 0
        self.win.setBackground(color_rgb(50, 50, 50))

        # Creates the board.
        self.board = Board(self.rows, self.cols, self.cellSize, self.mines, self.win)

        # Mine count remaining
        self.remaining = self.numMines - self.flagCount

        self._createHUD()

    # Draw the heads-up display (HUD) that shows the number of mines left and game status
    def _createHUD(self):

        hudY = self.rows * self.cellSize  # top of HUD strip

        # HUD background
        bg = Rectangle(Point(0, 0), Point(self.windowSize, 60))
        bg.setFill(HUDBackgroundColor)
        bg.setOutline(HUDBackgroundColor)
        bg.draw(self.win)

        flagX = 20
        flagY = 12
        flagSize = 30

        # Flag
        flag = Polygon(
            Point(flagX + flagSize * 0.3, flagY + flagSize * 0.15),
            Point(flagX + flagSize * 0.7, flagY + flagSize * 0.35),
            Point(flagX + flagSize * 0.3, flagY + flagSize * 0.55))
        flag.setFill("red")
        flag.setOutline("red")
        flag.draw(self.win)

        # Flagpole
        poleX = flagX + flagSize * 0.3

        pole = Line(
            Point(poleX, flagY + flagSize * 0.15),
            Point(poleX, flagY + flagSize * 0.85))
        pole.setWidth(3)
        pole.draw(self.win)

        # Mine count (Dynamic)
        self.mineText = Text(
            Point(90, 30),
            str(self.remaining))
        self.mineText.setTextColor("white")
        self.mineText.setSize(16)
        self.mineText.setStyle("bold")
        self.mineText.draw(self.win)

        # Clock icon
        clockX = self.windowSize // 2 - 35
        clockY = 30

        # Clock outline
        self.clockCircle = Circle(
            Point(clockX, clockY),
            12)
        self.clockCircle.setOutline("white")
        self.clockCircle.setWidth(2)
        self.clockCircle.draw(self.win)

        # Minute hand
        self.clockHand1 = Line(
            Point(clockX, clockY),
            Point(clockX, clockY - 7))
        self.clockHand1.setFill("white")
        self.clockHand1.setWidth(2)
        self.clockHand1.draw(self.win)

        # Hour hand
        self.clockHand2 = Line(
            Point(clockX, clockY),
            Point(clockX + 5, clockY))
        self.clockHand2.setFill("white")
        self.clockHand2.setWidth(2)
        self.clockHand2.draw(self.win)

        # Timer (Dynamic)
        self.timerText = Text(
            Point(self.windowSize // 2, 30),
            "0")
        self.timerText.setTextColor("white")
        self.timerText.setSize(16)
        self.timerText.setStyle("bold")
        self.timerText.draw(self.win)


        # Quit button
        quitLabel = Text(Point(self.windowSize - 35, 30), "X")
        quitLabel.setTextColor("white")
        quitLabel.setSize(12)
        quitLabel.setStyle("bold")
        quitLabel.draw(self.win)

        # Store button bounds for click detection
        self.quitBoxBounds = [self.windowSize - 60,  # left
                              10,                    # top
                              self.windowSize - 10,  # right
                              50                     # bottom
        ]
        
    # Updates dynamic elements of the HUD.

    def _inBounds(self, x, y, bounds):
        return bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]
        
    def _drawEndScreen(self, message):
        # Draw end game screen with message
        overlay = Rectangle(Point(0, 0), Point(self.windowSize, self.windowHeight))
        overlay.setFill(color_rgb(0, 0, 0))
        overlay.setOutline(color_rgb(0, 0, 0))
        overlay.setFill(color_rgb(0, 0, 0, 150))  # semi-transparent
        overlay.draw(self.win)

        endText = Text(Point(self.windowSize // 2, self.windowHeight // 2), message)
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