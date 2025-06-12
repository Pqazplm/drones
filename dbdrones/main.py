# -*- coding: utf-8 -*-


"""This module provides DB drones application."""

import sys

from PyQt5.QtWidgets import QApplication

from .views import Window

def main():
    """DB drones main function."""
    # Создание приложения
    app = QApplication(sys.argv)
    # Создание главного окна
    win = Window()
    win.show()
    # Запуск цикла
    sys.exit(app.exec())