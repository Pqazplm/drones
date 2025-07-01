

"""Этот модуль обеспечивает подключение к базе данных"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import os
from pathlib import Path


def _createContactsTable():
    """Создает таблицу для базы данных"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            model_name VARCHAR(40) NOT NULL,
            weight VARCHAR(50) NOT NULL,
            manufacture VARCHAR(40) NOT NULL,
            max_distance VARCHAR(50) NOT NULL
        )
        """
    )


def _createManufacturerTable():
    """Создает таблицу производителей"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS manufacture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(40) UNIQUE NOT NULL,
            country VARCHAR(50) NOT NULL
        )
        """
    )


def _createModelTable():
    """Создает таблицу моделей"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(40) UNIQUE NOT NULL
        )
        """
    )


def createConnection(databaseName):
    """Создает все таблицы при подключении"""

    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "DB Drones",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    _createContactsTable()
    _createManufacturerTable()
    _createModelTable()
    return True