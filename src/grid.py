import pawn
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6 import QtCore, QtGui


class Grid(QMainWindow):
    pawns = []
    window_size_x = 0
    window_size_y = 0
    block_size_x = 0
    block_size_y = 0

    cursor_place = 0

    # Definition of the constructor
    def __init__(self):
        # Initialisation of the pawns when launching the game
        print("New Grid!")
        k = 0
        while k < 2:
            if k > 1:
                break
            for i in range(3):
                if i == 3:
                    break
                self.pawns.append(pawn.Pawn(0, i, k, 'white'))
            for i in range(3):
                if i == 3:
                    break
                self.pawns.append(pawn.Pawn(2, i, k, 'black'))
            k += 1

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

        for i in self.pawns:
            if i.color == 'white':
                p.setBrush(QtGui.QColor(220, 220, 220))
            elif i.color == 'black':
                p.setBrush(QtGui.QColor(30, 15, 0))

            size = 0

            if i.z == 0:
                size = 0.9
            elif i.z == 1:
                size = 0.75
            elif i.z == 2:
                size = 0.6
            p.drawEllipse(i.x * int(self.block_size_x) + int(self.block_size_x) * (1 - size) / 2,
                          i.y * int(self.block_size_y) + int(self.block_size_y) * (1 - size) / 2,
                          int(self.block_size_x * size),
                          int(self.block_size_y * size))

    def mousePressEvent(self, e):
        width = self.width() // 3
        height = self.height() // 3
        j = e.x() // width
        i = e.y() // height

        print('You clicked on : ', (i, j))

        self.cursor_place = i, j
