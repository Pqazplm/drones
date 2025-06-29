# -*- coding: utf-8 -*-
# rpcontacts/model.py

"""This module provides a model to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Model_name", "Weight", "Manufactorer", "Max_distance")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

    def _generate_hash(self, data):
        """Generate a numeric hash from the data fields."""
        combined = "".join(str(field) for field in data)
        return abs(hash(combined)) % (10 ** 4)  # 8-digit numeric hash

    def addData(self, data):
        """Add new data with generated hash ID."""
        # Generate hash ID from the data
        hash_id = self._generate_hash(data)

        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        # Set the ID first
        self.model.setData(self.model.index(rows, 0), hash_id)

        # Set the other fields
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)

        if not self.model.submitAll():
            print("SQL Error:", self.model.lastError().text())
        self.model.select()

    def deleteData(self, row):
        """Remove a data from the database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearData(self):
        """Remove all data in the database."""
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

    # Добавляем в класс ContactsModel новый метод
    def searchData(self, search_text):
        """Search data in all fields."""
        self.model.setFilter(f"""
            model_name LIKE '%{search_text}%' OR
            weight LIKE '%{search_text}%' OR
            manufactorer LIKE '%{search_text}%' OR
            max_distance LIKE '%{search_text}%'
        """)
        self.model.select()