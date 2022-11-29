import math
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGraphicsColorizeEffect

import pawn


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
                    p.setPen(QPen(Qt.gray, 3))
                elif i.color == 'black':
                    p.setBrush(QtGui.QColor(30, 15, 0))
                    p.setPen(QPen(Qt.white, 3))

                p.drawEllipse(i.x * int(self.block_size_x) + int(self.block_size_x) * (1 - size) / 2,
                              i.y * int(self.block_size_y) + int(self.block_size_y) * (1 - size) / 2,
                              int(self.block_size_x * size),
                              int(self.block_size_y * size))
                size = size - 0.05

        if self.winner != "nobody":
            label_1 = QLabel(self.winner + " player won!", self)
            label_1.move(int(self.window_size_x / 7), int(self.window_size_y / 2.5))
            label_1.setFont(QFont('Arial', 50))
            label_1.setFixedHeight(100)
            label_1.setFixedWidth(600)
            label_1.setStyleSheet("color: #ff3b3b")
            label_1.show()

    def mousePressEvent(self, e):
        width = self.width() // 3
        height = self.height() // 3
        j = e.x() // width
        i = e.y() // height

        print("temp i : ", self.temp_click_i)
        print("temp j : ", self.temp_click_j)
        print("i : ", i)
        print("j : ", j)
        print()
        if self.winner == "nobody":
            if not self.clicked:
                for t in self.towers:
                    if j == t[0].x and i == t[0].y and t[0].color == self.turn:
                        self.ref = t
                        self.temp_click_j = j
                        self.temp_click_i = i
                        self.clicked = True
            elif j != self.temp_click_j or i != self.temp_click_i:
                self.switch_players()

                # number_of_moving corresponds to the number of pawns that we are able to move
                number_of_moving = self.distance(self.temp_click_j, self.temp_click_i, j, i)

                if len(self.ref) >= number_of_moving:
                    self.decide_type_of_moving(j, i, number_of_moving)
                else:
                    print("You don't have enough pawns! (", len(self.ref), ")")

        self.check_win()

        self.repaint()

    def decide_type_of_moving(self, j, i, number_of_moving):
        self.clicked = False
        # Searching for if a tower already exists on the new position
        for tower in self.towers:
            # If this is the case,
            if j == tower[0].x and i == tower[0].y:
                self.move_to(number_of_moving, j, i, tower, False)
                return

        # No tower exists, the new position is free
        self.move_to(number_of_moving, j, i, self.towers, True)

    def switch_players(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

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
            self.pawns += tower
            tower.clear()
            for p in self.pawns:
                tower.append(p)
            # for a_pawn in self.pawns:
            #    tower.insert(0, a_pawn)

        # if self.ref is NULL
        if not self.ref:
            # We remove it from the towers list
            self.towers.remove(self.ref)

        if isFree:
            self.towers.append(self.pawns)
        self.pawns = []
        self.ref = None

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
