import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPen
from PySide6.QtWidgets import QLabel, QApplication, QMainWindow, QWidget


class View(QMainWindow):

    def __init__(self, ref_controller):

        self.ref_controller = ref_controller

        self.clicked = False

        print("new View!")

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

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setBrush(QtGui.QColor(200, 173, 127))
        p.drawRect(0, 0, self.window_size_x, self.window_size_y)
        for i in range(4):
            p.drawLine(0, i * int(self.block_size_y), self.width(), int(i * self.block_size_y))
            p.drawLine(i * int(self.block_size_x), 0, i * int(self.block_size_x), self.height())

        towers = self.ref_controller.get_towers()
        winner = self.ref_controller.get_winner()
        for t in towers:
            size = 0.9

            for i in reversed(t):
                if i.color == 'white':
                    p.setBrush(QtGui.QColor(220, 220, 220))
                    if self.ref_controller.is_selected():
                        p.setPen(QPen(Qt.red, 3))
                    p.setPen(QPen(Qt.gray, 3))
                elif i.color == 'black':
                    p.setBrush(QtGui.QColor(30, 15, 0))
                    p.setPen(QPen(Qt.white, 3))

                p.drawEllipse(i.x * int(self.block_size_x) + int(self.block_size_x) * (1 - size) / 2,
                              i.y * int(self.block_size_y) + int(self.block_size_y) * (1 - size) / 2,
                              int(self.block_size_x * size),
                              int(self.block_size_y * size))
                size = size - 0.05

        if self.ref_controller.is_winner():
            label_1 = QLabel(winner + " player won!", self)
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

        self.ref_controller.action(j, i)
        self.repaint()
