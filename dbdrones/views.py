

"""Этот модуль предоставляет управление таблицей"""


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QSizePolicy,

)
from .model import ContactsModel


class Window(QMainWindow):
    """Главное окно приложения для управления базой данных дронов"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("База данных дронов")

        # Устанавливаем минимальный размер окна
        self.setMinimumSize(570, 250)

        # Центральный виджет и основной макет
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)

        # Убираем отступы, чтобы таблица использовала все пространство
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Инициализация модели данных
        self.contactsModel = ContactsModel()

        # Настройка интерфейса
        self.setupUI()

    def setupUI(self):
        """Настройка графического интерфейса с правильным масштабированием"""

        # ===== ТАБЛИЦА ДАННЫХ =====
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Настройка заголовков таблицы
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)  # Растягиваем последний столбец
        header.setSectionResizeMode(QHeaderView.Interactive)  # Разрешаем изменение ширины

        # Фиксированная высота строк
        self.table.verticalHeader().setDefaultSectionSize(30)

        # Политика размеров - растягивание по обоим направлениям
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Первоначальное масштабирование столбцов
        self.table.resizeColumnsToContents()

        # ===== ПАНЕЛЬ КНОПОК =====
        # Контейнер для кнопок с фиксированной шириной
        buttonsWidget = QWidget()
        buttonsWidget.setFixedWidth(200)  # Фиксированная ширина панели кнопок

        buttonsLayout = QVBoxLayout(buttonsWidget)
        buttonsLayout.setContentsMargins(10, 10, 10, 10)  # Отступы внутри панели
        buttonsLayout.setSpacing(10)
        buttonsLayout.setAlignment(Qt.AlignTop)

        # Список кнопок
        buttons = [
            ("Добавить...", self.openAddDialog),
            ("Удалить", self.deleteData),
            ("Очистить все", self.clearData),
            ("Поиск", self.searchData),
            ("Сбросить поиск", self.resetSearch)
        ]

        # Создаем кнопки
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(handler)
            buttonsLayout.addWidget(btn)

        # Добавляем растягивающееся пространство между кнопками
        buttonsLayout.insertStretch(2)

        # ===== РАСПОЛОЖЕНИЕ ЭЛЕМЕНТОВ =====
        # Добавляем таблицу и панель кнопок в главный макет
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addWidget(buttonsWidget)

        # Устанавливаем приоритет растяжения (таблица будет растягиваться)
        self.mainLayout.setStretch(0, 1)

        # Устанавливаем фокус на таблицу
        self.table.setFocus()

    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        # При изменении размера обновляем таблицу
        self.table.resizeColumnsToContents()

    def openAddDialog(self):
        """Открытие диалогового окна (Добавить)"""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addData(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteData(self):
        """Удаление выбранной позиции из бд"""
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Вы уверены, что хотите удалить выбранную позицию?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteData(row)

    def clearData(self):
        """Очистка"""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Вы уверены, что хотите все очистить?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearData()

    def searchData(self):
        """Открытие диалогового окна (Поиск)"""
        dialog = SearchDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.searchData(dialog.search_text)

        # Добавляем кнопку сброса поиска
        self.resetSearchButton = QPushButton("Сброс поиска")
        self.resetSearchButton.clicked.connect(self.resetSearch)

    def resetSearch(self):
        """Сброс поиска"""
        self.contactsModel.model.setFilter("")
        self.contactsModel.model.select()

class AddDialog(QDialog):
    """Диалоговое окно (Добавить)"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Добавить")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        """Установка графического интерфейса диалогового окна (Добавить)"""
        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Model_name")
        self.weightField = QLineEdit()
        self.weightField.setObjectName("Weight")
        self.manufactorerField = QLineEdit()
        self.manufactorerField.setObjectName("Manufactorer")
        self.distanceField = QLineEdit()
        self.distanceField.setObjectName("Max_distance")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Model_name:", self.nameField)
        layout.addRow("Weight:", self.weightField)
        layout.addRow("Manufactorer:", self.manufactorerField)
        layout.addRow("Max_distance:", self.distanceField)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):  # <- Метод должен быть здесь, а не внутри setupUI!
        """Подтверждение изменений"""
        self.data = []
        for field in (self.nameField, self.weightField,
                      self.manufactorerField, self.distanceField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"Вы должны добавить какую-то информацию {field.objectName()}",
                )
                self.data = None
                return
            self.data.append(field.text())
        super().accept()  # Важно: вызываем родительский accept()


class SearchDialog(QDialog):
    """Диалоговое окно (Поиск)"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Search")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.search_text = None
        self.setupUI()

    def setupUI(self):
        """Установка графического интерфейса диалогового окна (Поиск)"""
        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText("Введите текст...")

        layout = QFormLayout()
        layout.addRow("Поиск:", self.searchField)
        self.layout.addLayout(layout)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Подтверждение поиска"""
        self.search_text = self.searchField.text()
        if not self.search_text:
            QMessageBox.critical(
                self,
                "Error!",
                "Вы должны ввести текст",
            )
            self.search_text = None
            return
        super().accept()