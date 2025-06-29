

"""Этот модуль обеспечивает подключение к базе данных"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
    """Создает таблицу для базы данных"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            model_name VARCHAR(40) NOT NULL,
            weight VARCHAR(50) NOT NULL,
            manufactorer VARCHAR(40) NOT NULL,
            max_distance VARCHAR(50) NOT NULL
        )
        """
    )

def createConnection(databaseName):
    """создает и подключается к бд"""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    """обработка ошибки"""
    if not connection.open():
        QMessageBox.warning(
            None,
            "DB Drones",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    _createContactsTable()
    return True