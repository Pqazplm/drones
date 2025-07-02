

"""Этот модуль реализует модель для управления таблицей """

from PyQt5.QtCore import Qt
import os
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtGui import QPixmap

class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Создание и настройка модели"""
        tableModel = QSqlTableModel()
        tableModel.setTable("data")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Модель", "Вес (г)", "Производитель", "Макс. дистанция (м)", "Изображение")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

    def _generate_hash(self, data):
        """Генерирование числового хэша из полей данных (нужно для присваивания ID)"""
        combined = "".join(str(field) for field in data)
        return abs(hash(combined)) % (10 ** 4)  # 8-digit numeric hash

    def addData(self, data):
        """Добавляет данные с изображением"""
        hash_id = self._generate_hash(data)
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        # Устанавливаем значения для всех полей
        self.model.setData(self.model.index(rows, 0), hash_id)  # ID
        self.model.setData(self.model.index(rows, 1), data[0])  # model_name
        self.model.setData(self.model.index(rows, 2), data[1])  # weight
        self.model.setData(self.model.index(rows, 3), data[2])  # manufacture
        self.model.setData(self.model.index(rows, 4), data[3])  # max_distance

        # Сохраняем путь к изображению (5-й столбец)
        if len(data) > 4 and data[4]:
            self.model.setData(self.model.index(rows, 5), data[4])  # image_path

        if not self.model.submitAll():
            print("SQL Error:", self.model.lastError().text())
        self.model.select()

    def _store_image(self, row, image_path):
        """Сохраняет изображение в БД"""
        if os.path.exists(image_path):
            # Вариант 1: Сохраняем путь к файлу
            self.model.setData(self.model.index(row, 6), image_path)

            # Вариант 2: Сохраняем бинарные данные (раскомментировать)
             #with open(image_path, 'rb') as f:
                # image_data = f.read()
             #self.model.setData(self.model.index(row, 5), image_data)

    def getManufacturers(self):
        """Получение списка производителей"""
        query = QSqlQuery()
        query.exec("SELECT name FROM manufacture")
        manufacturers = []
        while query.next():
            manufacturers.append(query.value(0))
        return manufacturers

    def getModels(self):
        """Получение списка моделей"""
        query = QSqlQuery()
        query.exec("SELECT name FROM model")
        models = []
        while query.next():
            models.append(query.value(0))
        return models

    def addManufacturer(self, name, country):
        """Добавление нового производителя"""
        query = QSqlQuery()
        query.prepare("INSERT INTO manufacture (name, country) VALUES (?, ?)")
        query.addBindValue(name)
        query.addBindValue(country)
        return query.exec()

    def addModel(self, name):
        """Добавление новой модели"""
        query = QSqlQuery()
        query.prepare("INSERT INTO model (name) VALUES (?)")
        query.addBindValue(name)
        return query.exec()

    def deleteData(self, row):
        """Удаление выбранных данных из бд"""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearData(self):
        """Удаление всех данных из бд"."""
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

    # Добавляем в класс ContactsModel новый метод
    def searchData(self, search_text):
        """Поиск по всем полям"""
        self.model.setFilter(f"""
            model_name LIKE '%{search_text}%' OR
            weight LIKE '%{search_text}%' OR
            manufactorer LIKE '%{search_text}%' OR
            max_distance LIKE '%{search_text}%'
        """)
        self.model.select()