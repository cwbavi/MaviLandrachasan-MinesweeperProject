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

        self.win = GraphWin(
            "Minesweeper",
            self.windowSize,
            self.windowSize + HUD_HEIGHT
        )
        self.win.setBackground(color_rgb(35, 35, 35))

        self.board = Board(self.rows, self.cols, self.cellSize, self.numMines, self.win)

        # =========================
        # STATE
        # =========================
        self.isOver = False
        self.isFirstClick = True

        self.flagCount = 0

        # click system
        self.lastClickType = "left"

        # timer
        self.timerStarted = False
        self.startTime = 0

        # hover (optional hook)
        self.hoveredCell = None

        # HUD
        self._createHUD()

    # =========================
    # HUD
    # =========================

    def _createHUD(self):

        self.mineText = Text(
            Point(80, self.windowSize + 30),
            str(self.numMines)
        )
        self.mineText.setTextColor("white")
        self.mineText.setSize(16)
        self.mineText.setStyle("bold")
        self.mineText.draw(self.win)

        self.timerText = Text(
            Point(self.windowSize // 2, self.windowSize + 30),
            "0"
        )
        self.timerText.setTextColor("white")
        self.timerText.setSize(16)
        self.timerText.setStyle("bold")
        self.timerText.draw(self.win)

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

    def _startTimer(self):
        if not self.timerStarted:
            self.startTime = time.time()
            self.timerStarted = True

    def _updateTimer(self):
        if self.timerStarted:
            elapsed = int(time.time() - self.startTime)
        else:
            elapsed = 0

        self.timerText.setText(str(elapsed))

    # =========================
    # MAIN LOOP
    # =========================

    def start(self):

        while not self.isOver:

            self._handleHover()

            click = self.win.checkMouse()

            if click:
                self._handleClick(click)

            self._updateTimer()
            time.sleep(0.02)

        self._gameOverScreen()

    # =========================
    # INPUT
    # =========================

    def _handleClick(self, point):

        x, y = point.getX(), point.getY()

        # quit
        if x > self.windowSize - 60 and y > self.windowSize:
            self.isOver = True
            return

        cell = self.board.getClickedCell(point)

        if not cell:
            return

        # update click type
        self.lastClickType = self.win.lastClickType

        # FIRST CLICK
        if self.isFirstClick:
            self.board.initialReveal(cell)
            self.isFirstClick = False
            self._startTimer()

        # RIGHT CLICK = FLAG
        if self.lastClickType == "right":
            self.board.flag(cell)
            return

        # LEFT CLICK = REVEAL
        hitMine = self.board.reveal(cell)

        if hitMine:
            self.board.revealAllMines()
            self.isOver = True
            return

        if self.board.isSolved():
            self.isOver = True

    # =========================
    # HOVER (optional)
    # =========================

    def _handleHover(self):

        mouse = self.win.checkMouse()

        if not mouse:
            return

        cell = self.board.getClickedCell(mouse)

        if cell != self.hoveredCell:

            if self.hoveredCell:
                self.hoveredCell.unhighlight()

            self.hoveredCell = cell

            if self.hoveredCell:
                self.hoveredCell.highlight()

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