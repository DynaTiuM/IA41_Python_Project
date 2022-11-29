import math

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QFont
from PySide6.examples.widgets.painting.painter import painter

import pawn
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PySide6 import QtCore, QtGui


class Grid(QMainWindow):
    pawns = []
    towers = []
    winner = "nobody"
    turn = "white"

    clicked = False
    ref = None

    # Definition of the constructor
    def __init__(self):
        # Initialisation of the pawns when launching the game
        self.temp_click_j = None
        self.temp_click_i = None
        print("New Grid!")

        # Creating the towers of white pawns
        for i in range(3):
            if i == 3:
                break
            for y in range(2):
                self.pawns.append(pawn.Pawn(0, i, 'white'))
            self.towers.append(self.pawns)
            self.pawns = []

        # Creating the towers of black pawns
        for i in range(3):
            if i == 3:
                break
            for y in range(2):
                self.pawns.append(pawn.Pawn(2, i, 'black'))
            self.towers.append(self.pawns)
            self.pawns = []

        # Should have 6 towers at the beginning of the game
        print(self.towers)

        # Defining the size of the window
        self.window_size_x = 700
        self.window_size_y = 700

        # Defining the size of the blocks
        self.block_size_x = self.block_size_y = self.window_size_x / 3.

        # Displaying the grid of the game
        app = QApplication(sys.argv)

        # Instantiation of a window
        QMainWindow.__init__(self)
        self.setWindowTitle("IA41 Project")
        # self.setWindowIcon(QIcon("icons/file.png"))
        self.setFixedSize(self.window_size_x, self.window_size_y)

        central_area = QWidget()
        self.setCentralWidget(central_area)
        self.show()

        sys.exit(app.exec())

    # Definition of the destructor
    def __del__(self):
        self.pawns.clear()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setBrush(QtGui.QColor(200, 173, 127))
        p.drawRect(0, 0, self.window_size_x, self.window_size_y)
        for i in range(4):
            p.drawLine(0, i * int(self.block_size_y), self.width(), int(i * self.block_size_y))
            p.drawLine(i * int(self.block_size_x), 0, i * int(self.block_size_x), self.height())

        for t in self.towers:
            size = 0.9

            for i in reversed(t):
                if i.color == 'white':
                    p.setBrush(QtGui.QColor(220, 220, 220))
                elif i.color == 'black':
                    p.setBrush(QtGui.QColor(30, 15, 0))

                p.drawEllipse(i.x * int(self.block_size_x) + int(self.block_size_x) * (1 - size) / 2,
                              i.y * int(self.block_size_y) + int(self.block_size_y) * (1 - size) / 2,
                              int(self.block_size_x * size),
                              int(self.block_size_y * size))
                size = size - 0.05

        if self.winner != "nobody":
            label_1 = QLabel(self.winner + " player won!", self)
            label_1.move(int(self.window_size_x / 3), int(self.window_size_y / 2))
            label_1.setFont(QFont('Arial', 60))
            label_1.setFixedHeight(100)
            label_1.setFixedWidth(400)
            label_1.show()

    def mousePressEvent(self, e):
        width = self.width() // 3
        height = self.height() // 3
        j = e.x() // width
        i = e.y() // height

        if self.winner == "nobody":
            if not self.clicked:
                for t in self.towers:
                    if j == t[0].x and i == t[0].y and t[0].color == self.turn:
                        self.ref = t
                        self.temp_click_j = j
                        self.temp_click_i = i
                        self.clicked = True
            else:
                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"
                if self.distance(self.temp_click_j, self.temp_click_i, j, i) == 1:
                    self.clicked = False
                    # Searching for if a tower already exists on the new position
                    for tower in self.towers:
                        # If this is the case,
                        if j == tower[0].x and i == tower[0].y:
                            self.move_to(1, j, i, tower, False)
                            return

                    # No tower exists, the new position is free
                    self.move_to(1, j, i, self.towers, True)

                    return

                elif self.distance(self.temp_click_j, self.temp_click_i, j, i) == 2:
                    if len(self.ref) >= 2:
                        self.clicked = False
                        # Searching for if a tower already exists on the new position
                        for tower in self.towers:
                            # If this is the case,
                            if j == tower[0].x and i == tower[0].y:
                                self.move_to(2, j, i, tower, False)
                                return

                        # No tower exists, the new position is free
                        self.move_to(2, j, i, self.towers, True)
                    else:
                        print("You don't have enough pawns!")

                elif self.distance(self.temp_click_j, self.temp_click_i, j, i) == 3:
                    if len(self.ref) >= 3:
                        self.clicked = False
                        # Searching for if a tower already exists on the new position
                        for tower in self.towers:
                            # If this is the case,
                            if j == tower[0].x and i == tower[0].y:
                                self.move_to(3, j, i, tower, False)
                                return

                        # No tower exists, the new position is free
                        self.move_to(3, j, i, self.towers, True)
                    else:
                        print("You don't have enough pawns!")
            self.check_win()

        self.repaint()

    def move_to(self, amount, x, y, tower, isFree):

        for i in range(amount):
            # New position of the pawns
            self.ref[0].x = x
            self.ref[0].y = y
            # We add to pawns list the pawns that we move

            self.pawns.append(self.ref[0])
            # We remove the pawn from the latest location
            self.ref.pop(0)

        if not isFree:
            for pawn in self.pawns:
                tower.insert(0, pawn)

        # if self.ref is NULL
        if not self.ref:
            # We remove it from the towers list
            self.towers.remove(self.ref)

        if isFree:
            self.towers.append(self.pawns)
        self.pawns = []
        self.ref = None

        print(self.towers)

        self.repaint()

        return

    def distance(self, x, y, dx, dy):

        dist = math.sqrt(math.pow((dx - x), 2) + math.pow((dy - y), 2))

        if dist == 1:
            return 1
        elif dist > 2:
            return 3
        return 2

    def check_win(self):
        count_white = 0
        count_black = 0
        for t in self.towers:
            if t[0].color == "white":
                count_white += 1
            if t[0].color == "black":
                count_black += 1

        if count_white == 0:
            self.winner = "Black"
            print("Black won!")
        elif count_black == 0:
            self.winner = "White"
            print("White won!")
