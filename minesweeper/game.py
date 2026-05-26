from board import *
from graphics import *
import time

# Window size for the game.
windowSize = 528
windowHeight = windowSize + 60

HUDBackgroundColor = color_rgb(74, 117, 44)

# Difficulty settings for the game. Easy = index 0, Medium = index 1, Hard = index 2.
difficulties = [[8, 8, 10], [16, 16, 40], [22, 22, 99]]
difficultyNames = ["Easy", "Medium", "Hard"]

# Main game class that handles the game logic and user interface.
class Game:

    # Initialize the game with the selected difficulty level and set up the board and window.
    def __init__(self, difficulty):
        self.rows, self.cols, self.numMines = difficulties[difficulty]
        self.windowSize = windowSize
        self.windowHeight = windowHeight
        self.cellSize = self.windowSize // max(self.rows, self.cols)
        self.isFirstClick = True
        self.isOver = False
        self.flagCount = 0
        self.endMsg = ''
        self.hoveredCell = None

        # Draws the window.
        self.win = GraphWin(difficultyNames[difficulty], self.windowSize, self.windowHeight)
        self.win.setBackground(color_rgb(50, 50, 50))

        # State
        self.isOver = False
        self.isFirstClick = True
        self.flagMode = False
        self.flagCount = 0
        self.remainingFlags = self.numMines - self.flagCount
        self.lastClickType = "left"
        
        # Timer
        self.timerStarted = False
        self.startTime = 0

        # Creates the board.
        self.board = Board(self.rows, self.cols, self.cellSize, self.numMines, self.win)

        self._createHUD()

    # Draw the heads-up display (HUD) that shows the number of mines left and game status
    def _createHUD(self):
        hudY = self.windowSize

        # HUD background
        bg = Rectangle(Point(0, 0), Point(self.windowSize, 60))
        bg.setFill(HUDBackgroundColor)
        bg.setOutline(HUDBackgroundColor)
        bg.draw(self.win)

        flagX = 20
        flagY = 48
        flagSize = 30

        # Flag icon
        self.flagIcon = Polygon(
            Point(flagX + flagSize * 0.3, 12 + flagSize * 0.15),
            Point(flagX + flagSize * 0.7, 12 + flagSize * 0.35),
            Point(flagX + flagSize * 0.3, 12 + flagSize * 0.55))
        self.flagIcon.setFill("red")
        self.flagIcon.setOutline("red")
        self.flagIcon.setWidth(2)
        self.flagIcon.draw(self.win)

        # Flagpole
        poleX = flagX + flagSize * 0.3
        pole = Line(
            Point(poleX, 12 + flagSize * 0.15),
            Point(poleX, 12 + flagSize * 0.85))
        pole.setWidth(3)
        pole.draw(self.win)

        # Mine count (Dynamic)
        self.mineText = Text(Point(90, 30), str(self.remainingFlags))
        self.mineText.setTextColor("white")
        self.mineText.setSize(16)
        self.mineText.setStyle("bold")
        self.mineText.draw(self.win)

        # Clock
        clockX = self.windowSize // 2 - 35
        clockY = 30

        # Clock outline
        self.clockCircle = Circle(Point(clockX, clockY), 12)
        self.clockCircle.setOutline("white")
        self.clockCircle.setWidth(2)
        self.clockCircle.draw(self.win)

        # Minute hand
        self.clockHand1 = Line(Point(clockX, clockY), Point(clockX, clockY - 7))
        self.clockHand1.setFill("white")
        self.clockHand1.setWidth(2)
        self.clockHand1.draw(self.win)

        # Hour hand
        self.clockHand2 = Line(Point(clockX, clockY), Point(clockX + 5, clockY))
        self.clockHand2.setFill("white")
        self.clockHand2.setWidth(2)
        self.clockHand2.draw(self.win)

        # Timer (Dynamic)
        self.timerText = Text(Point(self.windowSize // 2, 30), "0")
        self.timerText.setTextColor("white")
        self.timerText.setSize(16)
        self.timerText.setStyle("bold")
        self.timerText.draw(self.win)

        # Quit button
        self.quitLabel = Text(Point(self.windowSize - 35, 30), "X")
        self.quitLabel.setTextColor("white")
        self.quitLabel.setSize(12)
        self.quitLabel.setStyle("bold")
        self.quitLabel.draw(self.win)
        
    # Updates dynamic elements of the HUD.
    def _updateHUD(self):

        # Updates remaining flags.
        self.remainingFlags = self.numMines - self.flagCount
        self.mineText.setText(str(self.remainingFlags))

        # Updates the timer.
        if self.timerStarted:
            self.timerText.setText(str(int(time.time() - self.startTime)))

    # What to do when a click occurs.
    def _handleClick(self, click):

        # Get the coordinates of the click
        x, y = click.getX(), click.getY()

        # Update click type.
        self.lastClickType = self.win.lastClickType

        # Check if the click is on the quit button
        if 488 <= x <= 528 and 10 <= y <= 50:
            self.isOver = True
            return

        # Get the cell that was clicked
        cell = self.board.getClickedCell(click)
        
        # If the click is a right click, flag the cell.
        if self.lastClickType == "right":
            self.board.flag(cell) 
            if cell.isFlagged:
                self.flagCount += 1
            else:
                self.flagCount += -1
            return
        
        # Nothing happens.
        if cell is None or cell.isFlagged:
            return

        # If it's the first click, reveal the cell and start the timer.
        if self.isFirstClick and self.lastClickType == "left":
            self.board.initialReveal(cell)
            self.isFirstClick = False
            self.timerStarted = True
            self.startTime = time.time()
            return

        # If the click is a left click, reveal the cell.
        hitMine = self.board.reveal(cell)
        
        # If the player hits a mine, reveal all mines and end the game.
        if hitMine:
            self.board.revealAllMines()
            self.isOver = True
            self.endMsg = "Game Over! You lost."
            return

        # If the player wins the game, end the game.
        if self.board.isSolved():
            self.isOver = True
            self.endMsg = "Congratulations! You won in " + str(int(time.time() - self.startTime)) + " seconds."

    def _updateHover(self):
        # Poll the current mouse position and update highlighting
        try:
            x, y = self.win.winfo_pointerxy()
            # Convert screen coordinates to canvas coordinates
            x = x - self.win.winfo_rootx()
            y = y - self.win.winfo_rooty()
            x, y = self.win.toWorld(x, y)
            cell = self.board.getClickedCell(Point(x, y))
        except:
            cell = None

        if cell is self.hoveredCell:
            return

        if self.hoveredCell:
            self.hoveredCell.unhighlight()

        self.hoveredCell = cell
        if self.hoveredCell:
            self.hoveredCell.highlight()

    # Returns the end message.
    def start(self):
        while not self.isOver:
            self._updateHover()
            click = self.win.checkMouse()
            if click:
                self._handleClick(click)
            self._updateHUD()
            time.sleep(0.020)
        return self.endMsg
