
"""Этот модуль реализует приложение """

import sys

from PyQt5.QtWidgets import QApplication

from .database import createConnection
from .views import Window

def main():
    """Основная функция"""
    # Создание приложения
    app = QApplication(sys.argv)
    # Подключение к бд перед созданием окна приложения
    if not createConnection("data.sqlite"):
        sys.exit(1)
    # Создание главного окна приложения, если подключение прошло успешно
    win = Window()
    win.show()
    # Запуск цикла работы
    sys.exit(app.exec_())