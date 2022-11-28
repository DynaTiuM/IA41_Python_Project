import pawn
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6 import QtCore, QtGui


class Grid(QMainWindow):
    pawns = []
    towers = []

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

            for i in t:
                if i.color == 'white':
                    p.setBrush(QtGui.QColor(220, 220, 220))
                elif i.color == 'black':
                    p.setBrush(QtGui.QColor(30, 15, 0))

                p.drawEllipse(i.x * int(self.block_size_x) + int(self.block_size_x) * (1 - size) / 2,
                              i.y * int(self.block_size_y) + int(self.block_size_y) * (1 - size) / 2,
                              int(self.block_size_x * size),
                              int(self.block_size_y * size))
                size = size - 0.2

    def mousePressEvent(self, e):
        width = self.width() // 3
        height = self.height() // 3
        j = e.x() // width
        i = e.y() // height

        if not self.clicked:
            for t in self.towers:
                if j == t[0].x and i == t[0].y:
                    print(t)
                    self.ref = t
                    self.temp_click_j = j
                    self.temp_click_i = i
                    self.clicked = True
        else:
            if self.distance(self.temp_click_j, self.temp_click_i, j, i) == 1:
                self.clicked = False
                # Searching for if a tower already exists on the new position
                for t in self.towers:
                    # If this is the case,
                    if j == t[0].x and i == t[0].y:
                        self.ref[0].x = j
                        self.ref[0].y = i
                        # We add the pawn into the pawns list
                        self.pawns.append(self.ref[0])
                        # We add it to the tower list
                        t.append(self.pawns)
                        self.pawns = []
                        # We remove it from the previous list
                        self.ref[0].pop()
                        if not self.ref:
                            del self.ref
                        # Need to verify if really need this :
                        self.ref = None
                        return

                # No tower exists, the new position is free
                self.ref[0].x = j
                self.ref[0].y = i
                self.pawns.append(self.ref[0])
                self.towers.append(self.pawns)
                self.ref.pop(0)
                if not self.ref:
                    self.towers.remove(self.ref)
                self.pawns = []
                # Need to verify if really need this :
                self.ref = None
                print(self.towers)

                self.repaint()

                return

            elif self.distance(self.temp_click_j, self.temp_click_i, j, i) == 2:
                if len(self.ref) == 2:
                    return
                else:
                    print("You don't have enough pawns!")

            elif self.distance(self.temp_click_j, self.temp_click_i, j, i) == 3:
                print("soon")

            print(self.distance(self.temp_click_j, self.temp_click_i, j, i))

            return

    def distance(self, x, y, dx, dy):

        # 1 place moving
        if (dx == x + 1 or dx == x - 1) and dy == y:
            return 1
        if (dy == y + 1 or dy == y - 1) and dx == x:
            return 1

        # 2 places moving
        if dx == x + 1 or dx == x - 1 and dy != y:
            return 2
        if dy == y + 1 or dy == y - 1 and dx != x:
            return 2
        if dy == y + 2 and dx == x:
            return 2
        if dx == x + 2 and dy == y:
            return 2

        # 3 places moving
        if dy != y + 2 and dx != x + 2 and dy != y - 2 and dx != x - 2:
            return 3

        return -1
