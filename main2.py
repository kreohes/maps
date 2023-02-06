import os
import sys

import requests
from PIL import Image, ImageQt
from io import BytesIO
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.scale1 = 10
        self.scale2 = 10
        self.coords = '37.530887,55.703118'
        self.getImage()
        self.initUI()

    def getImage(self):
        self.scale = f'{str(self.scale1)},{str(self.scale2)}'
        print(self.scale)
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords}&spn={self.scale}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        coeff = 0.5
        if event.key() == Qt.Key_PageUp:
            if 0 <= self.scale1 < 90 and 0 <= self.scale2 < 90:
                self.scale1 += coeff
                self.scale2 += coeff
                self.getImage()
        if event.key() == Qt.Key_PageDown:
            if 0 < self.scale1 <= 90 and 0 < self.scale2 <= 90:
                self.scale1 -= coeff
                self.scale2 -= coeff
                self.getImage()
        self.update_image()

    def update_image(self):
        pixmap = QtGui.QPixmap('map.png')
        if not pixmap.isNull():
            self.image.setPixmap(pixmap)
            self.image.adjustSize()
            self.resize(pixmap.size())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Map()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())