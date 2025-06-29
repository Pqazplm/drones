# -*- coding: utf-8 -*-


"""This module provides views to manage the contacts table."""


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
)
# -*- coding: utf-8 -*-
# rpcontacts/views.py


from .model import ContactsModel



class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("DB Drones")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Создание таблицы для отображения виджетов
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        # Созданиие кнопок
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteData)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearData)
        self.searchButton = QPushButton("Search")
        # Реализация графического интерфейса
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)
        layout.addWidget(self.searchButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def openAddDialog(self):
        """Open the Add Data dialog."""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addData(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteData(self):
        """Delete the selected contact from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteData(row)

    def clearData(self):
        """Remove all contacts from the database."""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all data?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearData()

class AddDialog(QDialog):
    """Add Data dialog."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        """Setup the Add dialog's GUI."""
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
        """Accept the data provided through the dialog."""
        self.data = []
        for field in (self.nameField, self.weightField,
                      self.manufactorerField, self.distanceField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a data's {field.objectName()}",
                )
                self.data = None
                return
            self.data.append(field.text())
        super().accept()  # Важно: вызываем родительский accept()
