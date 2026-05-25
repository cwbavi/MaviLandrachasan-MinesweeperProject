from board import Board
from graphics import *
import time

HUD_HEIGHT = 60


class Game:
    def __init__(self, difficulty):
        difficulties = [
            (8, 8, 10),
            (16, 16, 40),
            (16, 30, 99)
        ]

        self.rows, self.cols, self.numMines = difficulties[difficulty]

        self.windowSize = 600
        self.cellSize = self.windowSize // max(self.rows, self.cols)

        self.win = GraphWin("Minesweeper", self.windowSize, self.windowSize + HUD_HEIGHT)
        self.win.setBackground(color_rgb(40, 40, 40))

        self.board = Board(self.rows, self.cols, self.cellSize, self.numMines, self.win)

        # State
        self.isOver = False
        self.isFirstClick = True
        self.flagMode = False
        self.flagCount = 0

        # Timer
        self.timerStarted = False
        self.startTime = 0

        # HUD objects
        self._createHUD()

    # =========================
    # HUD CREATION
    # =========================

    def _createHUD(self):

        # background
        self.hudBG = Rectangle(
            Point(0, self.windowSize),
            Point(self.windowSize, self.windowSize + HUD_HEIGHT)
        )
        self.hudBG.setFill(color_rgb(25, 25, 25))
        self.hudBG.setOutline(color_rgb(25, 25, 25))
        self.hudBG.draw(self.win)

        # FLAG ICON + COUNT
        fx, fy, s = 20, self.windowSize + 10, 30

        self.flagIcon = Polygon(
            Point(fx + s * 0.3, fy + s * 0.15),
            Point(fx + s * 0.7, fy + s * 0.35),
            Point(fx + s * 0.3, fy + s * 0.55)
        )
        self.flagIcon.setFill("red")
        self.flagIcon.setOutline("red")
        self.flagIcon.draw(self.win)

        poleX = fx + s * 0.3
        self.flagPole = Line(
            Point(poleX, fy + s * 0.15),
            Point(poleX, fy + s * 0.85)
        )
        self.flagPole.setWidth(3)
        self.flagPole.draw(self.win)

        self.mineText = Text(Point(95, self.windowSize + 30), str(self.numMines))
        self.mineText.setTextColor("white")
        self.mineText.setSize(16)
        self.mineText.setStyle("bold")
        self.mineText.draw(self.win)

        # TIMER
        self.timerText = Text(
            Point(self.windowSize // 2, self.windowSize + 30),
            "0"
        )
        self.timerText.setTextColor("white")
        self.timerText.setSize(16)
        self.timerText.setStyle("bold")
        self.timerText.draw(self.win)

        # QUIT
        self.quitText = Text(
            Point(self.windowSize - 30, self.windowSize + 30),
            "X"
        )
        self.quitText.setTextColor("white")
        self.quitText.setSize(18)
        self.quitText.setStyle("bold")
        self.quitText.draw(self.win)

    # =========================
    # TIMER
    # =========================

    def _updateTimer(self):
        if self.timerStarted:
            elapsed = int(time.time() - self.startTime)
        else:
            elapsed = 0

        self.timerText.setText(str(elapsed))

    # =========================
    # GAME LOOP
    # =========================

    def start(self):
        while not self.isOver:

            click = self.win.checkMouse()

            if click:
                self._handleClick(click)

            self._updateTimer()
            time.sleep(0.03)

        self._gameOverScreen()

    # =========================
    # INPUT HANDLING
    # =========================

    def _handleClick(self, point):

        x, y = point.getX(), point.getY()

        # quit
        if x > self.windowSize - 60 and y > self.windowSize:
            self.isOver = True
            return

        # board click
        cell = self.board.getClickedCell(point)

        if not cell:
            return

        # FIRST CLICK RULE
        if self.isFirstClick:
            self.board.initialReveal(cell)
            self.isFirstClick = False

            self.startTime = time.time()
            self.timerStarted = True

        # FLAG MODE (optional)
        if self.flagMode:
            self.board.flag(cell)
            return

        # NORMAL REVEAL
        hitMine = self.board.reveal(cell)

        if hitMine:
            self.board.revealAllMines()
            self.isOver = True

        elif self.board.isSolved():
            self.isOver = True

    # =========================
    # END SCREEN
    # =========================

    def _gameOverScreen(self):
        msg = Text(
            Point(self.windowSize // 2, self.windowSize // 2),
            "Game Over"
        )
        msg.setSize(24)
        msg.setTextColor("white")
        msg.setStyle("bold")
        msg.draw(self.win)

        self.win.getMouse()
        self.win.close()