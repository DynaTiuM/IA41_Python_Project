import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget


class MyWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("IA41 Project")
        self.setWindowIcon(QIcon("icons/file.png"))
        self.resize(600, 600)

        # Le type QWidget représente un conteneur de widgets (et il est lui-même un widget).
        # On crée une instance que l'on va mettre au centre de la fenêtre.
        centralArea = QWidget()
        # On lui met une couleur d'arrière-plan, histoire de bien le voir.
        centralArea.setStyleSheet("background: #419eee")
        # On injecte ce widget en tant que zone centrale.
        self.setCentralWidget(centralArea)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec())