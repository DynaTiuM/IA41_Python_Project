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

    # Definition of the constructor
    def __init__(self):
        # Initialisation of the pawns when launching the game
        print("New Grid!")
        for i in range(3):
            if i == 3:
                break
            self.pawns.append(pawn.Pawn(0, i, 'red'))
        for i in range(3):
            if i == 3:
                break
            self.pawns.append(pawn.Pawn(2, i, 'black'))

        # Defining the size of the window
        self.window_size_x = 800
        self.window_size_y = 800

        # Defining the size of the blocks
        self.block_size_x = self.block_size_y = self.window_size_x / 3.

        # Displaying the grid of the game
        app = QApplication(sys.argv)

        # Instantiation of a window
        QMainWindow.__init__(self)
        self.setWindowTitle("IA41 Project")
        # self.setWindowIcon(QIcon("icons/file.png"))
        self.resize(800, 800)

        central_area = QWidget()
        self.setCentralWidget(central_area)
        self.show()

        # We paint the grid
        self.paintEvent(1)
        sys.exit(app.exec())

    # Definition of the destructor
    def __del__(self):
        self.pawns.clear()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        for i in range(4):
            p.drawLine(0, i * int(self.block_size_y), self.width(), int(i * self.block_size_y))
            p.drawLine(i * int(self.block_size_x), 0, i * int(self.block_size_x), self.height())

        for i in self.pawns:
            if i.color == 'red':
                p.setBrush(QtGui.QColor(255, 0, 0))
            elif i.color == 'black':
                p.setBrush(QtGui.QColor(0, 0, 0))
            p.drawEllipse(i.x * int(self.block_size_x) + int(self.block_size_x) * 0.05,
                          i.y * int(self.block_size_y) + int(self.block_size_y) * 0.05,
                          int(self.block_size_x * 0.9),
                          int(self.block_size_y * 0.9))
