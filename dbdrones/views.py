

"""Этот модуль предоставляет управление таблицей"""


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QStyledItemDelegate,
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
from PyQt5.QtWidgets import QComboBox, QInputDialog
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap

class Window(QMainWindow):
    """Главное окно приложения для управления базой данных дронов"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("База данных дронов")

        # Устанавливаем минимальный размер окна
        self.setMinimumSize(800, 250)

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
        self.table.setItemDelegate(ImageDelegate(self.table))

        # Настройка столбцов (изображение в 5-м столбце)
        self.table.setColumnWidth(5, 200)  # Ширина столбца с изображениями
        self.table.verticalHeader().setDefaultSectionSize(150)  # Высота строк

        # Настройка заголовков таблицы
        headers = ("ID", "Модель", "Вес (г)", "Производитель", "Макс. дистанция (м)", "Спектр")
        for col, header in enumerate(headers):
            self.table.model().setHeaderData(col, Qt.Horizontal, header)
        self.table.setModel(self.contactsModel.model)


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
        dialog = AddDialog(self)  # Передаем self как родителя
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


from PyQt5.QtCore import Qt, QSize  # Добавляем QSize в импорты

class ImageDelegate(QStyledItemDelegate):
    """Делегат для отображения изображений в таблице"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_size = QSize(200, 150)  # Фиксированный размер для изображений

    def paint(self, painter, option, index):
        """Отрисовывает изображение в ячейке"""
        if index.column() == 5:  # Столбец с изображениями
            path = index.data()
            if path:  # Если есть путь к изображению
                try:
                    pixmap = QPixmap(path)
                    if not pixmap.isNull():
                        # Масштабируем изображение с сохранением пропорций
                        scaled = pixmap.scaled(
                            option.rect.width() - 10,  # -10 для отступов
                            option.rect.height() - 10,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                        # Выравниваем по центру
                        x = option.rect.x() + (option.rect.width() - scaled.width()) // 2
                        y = option.rect.y() + (option.rect.height() - scaled.height()) // 2
                        painter.drawPixmap(x, y, scaled)
                        return
                except Exception as e:
                    print(f"Error loading image: {e}")

        # Если нет изображения или это другой столбец - стандартная отрисовка
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        """Задает размер ячейки для изображений"""
        if index.column() == 5:
            return self.image_size
        return super().sizeHint(option, index)


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Добавить дрон")
        self.main_layout = QVBoxLayout()  # Используем только один layout
        self.setLayout(self.main_layout)
        self.data = None
        self.image_path = ""
        self.setupUI()
        self.setupImageUI()

    def setupUI(self):
        # Создаем выпадающие списки
        self.modelCombo = QComboBox()
        self.manufacturerCombo = QComboBox()

        # Настраиваем списки
        self.setupComboBox(self.modelCombo, "модель", self.getModels)
        self.setupComboBox(self.manufacturerCombo, "производителя", self.getManufacturers)

        # Остальные поля
        self.weightField = QLineEdit()
        self.distanceField = QLineEdit()

        # Форма для основных полей
        form_layout = QFormLayout()
        form_layout.addRow("Модель:", self.modelCombo)
        form_layout.addRow("Производитель:", self.manufacturerCombo)
        form_layout.addRow("Вес (г):", self.weightField)
        form_layout.addRow("Макс. дистанция (м):", self.distanceField)


        # Добавляем форму в главный layout
        self.main_layout.addLayout(form_layout)

        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.main_layout.addWidget(buttons)

    def setupImageUI(self):
        """Элементы для работы с изображением"""
        self.btn_load = QPushButton("Загрузить фото дрона")
        self.btn_load.clicked.connect(self.loadImage)

        self.lbl_preview = QLabel()
        self.lbl_preview.setFixedSize(200, 200)
        self.lbl_preview.setStyleSheet("border: 1px solid #ccc;")
        self.lbl_preview.setAlignment(Qt.AlignCenter)

        # Layout для изображения
        image_layout = QVBoxLayout()
        image_layout.addWidget(QLabel("Фото дрона:"))
        image_layout.addWidget(self.btn_load)
        image_layout.addWidget(self.lbl_preview)

        # Вставляем layout с изображением перед кнопками
        self.main_layout.insertLayout(self.main_layout.count() - 1, image_layout)




    def setupComboBox(self, combo, item_type, data_func):
        """Настраивает выпадающий список"""
        combo.clear()
        combo.addItems(data_func())
        combo.insertItem(0, "")  # Пустая строка в начале
        combo.addItem(f"+ Добавить {item_type}", "add_item")
        combo.setCurrentIndex(0)  # Выбираем пустую строку по умолчанию

        combo.currentIndexChanged.connect(
            lambda: self.handleComboSelection(combo, item_type, data_func)
        )

    def handleComboSelection(self, combo, item_type, data_func):
        """Обрабатывает выбор элемента"""
        if combo.currentData() == "add_item":
            # Запоминаем текущий индекс перед открытием диалога
            prev_index = combo.currentIndex()

            if item_type == "модель":
                new_item, ok = QInputDialog.getText(
                    self, f"Добавить {item_type}", f"Введите название {item_type}:")

                if ok and new_item:
                    if self.parent().contactsModel.addModel(new_item):
                        self.refreshCombo(combo, item_type, data_func, new_item)
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось добавить")
                        combo.setCurrentIndex(0)
                else:
                    # При отмене возвращаем выбор на первый элемент
                    combo.setCurrentIndex(0)
            else:
                manufacturer, ok = QInputDialog.getText(
                    self, "Добавить производителя", "Введите название производителя:")

                if ok and manufacturer:
                    country, ok = QInputDialog.getText(
                        self, "Страна производителя", "Введите страну производителя:")

                    if ok and country:
                        if self.parent().contactsModel.addManufacturer(manufacturer, country):
                            self.refreshCombo(combo, item_type, data_func, manufacturer)
                        else:
                            QMessageBox.warning(self, "Ошибка", "Не удалось добавить")
                            combo.setCurrentIndex(0)
                    else:
                        combo.setCurrentIndex(0)
                else:
                    combo.setCurrentIndex(0)

    def refreshCombo(self, combo, item_type, data_func, select_item=None):
        """Обновляет содержимое комбобокса"""
        current_text = combo.currentText()
        combo.clear()
        combo.addItems(data_func())
        combo.insertItem(0, "")
        combo.addItem(f"+ Добавить {item_type}", "add_item")

        if select_item:
            index = combo.findText(select_item)
            if index >= 0:
                combo.setCurrentIndex(index)
        else:
            combo.setCurrentIndex(0)

    def getModels(self):
        return self.parent().contactsModel.getModels()

    def getManufacturers(self):
        return self.parent().contactsModel.getManufacturers()


    def loadImage(self):
        """Диалог выбора изображения"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение дрона",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )

        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path).scaled(
                200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_preview.setPixmap(pixmap)

    def accept(self):
        """Проверка данных перед сохранением"""
        model = self.modelCombo.currentText()
        manufacturer = self.manufacturerCombo.currentText()
        weight = self.weightField.text()
        distance = self.distanceField.text()

        # Проверка заполненности полей
        if not all([model, manufacturer, weight, distance]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        # Проверка, что выбраны существующие значения (не пустая строка и не "+ Добавить")
        if model == "" or self.modelCombo.currentData() == "add_item":
            QMessageBox.warning(self, "Ошибка", "Выберите модель из списка")
            return

        if manufacturer == "" or self.manufacturerCombo.currentData() == "add_item":
            QMessageBox.warning(self, "Ошибка", "Выберите производителя из списка")
            return

        self.data = [model, weight, manufacturer, distance, self.image_path]
        super().accept()


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