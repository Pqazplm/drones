

"""Этот модуль реализует модель для управления таблицей """

from PyQt5.QtCore import Qt

from PyQt5.QtSql import QSqlTableModel, QSqlQuery

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
        headers = ("ID", "Модель", "Вес (г)", "Производитель", "Макс. дистанция (м)")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

    def _generate_hash(self, data):
        """Генерирование числового хэша из полей данных (нужно для присваивания ID)"""
        combined = "".join(str(field) for field in data)
        return abs(hash(combined)) % (10 ** 4)  # 8-digit numeric hash

    def addData(self, data):

        # Генерация хэш-идентификатора на основе полученных данных
        hash_id = self._generate_hash(data)

        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        # Установка 1-го ID
        self.model.setData(self.model.index(rows, 0), hash_id)

        # Установка остальных полей
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        # Обработка ошибки
        if not self.model.submitAll():
            print("SQL Error:", self.model.lastError().text())
        self.model.select()

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