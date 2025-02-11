from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt
import takemehome.database as db


class AddPersonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Person")
        self.setGeometry(150, 150, 400, 400)

        layout = QVBoxLayout()

        # Form Fields
        self.name_to_call_me = QLineEdit()
        self.name_to_call_me.setPlaceholderText("Name to Call Me")
        layout.addWidget(QLabel("Name to Call Me:"))
        layout.addWidget(self.name_to_call_me)

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.first_name)

        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name")
        layout.addWidget(QLabel("Middle Name:"))
        layout.addWidget(self.middle_name)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.last_name)

        self.dob = QLineEdit()
        self.dob.setPlaceholderText("Date of Birth (YYYY-MM-DD)")
        layout.addWidget(QLabel("Date of Birth:"))
        layout.addWidget(self.dob)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age)

        self.hair = QLineEdit()
        self.hair.setPlaceholderText("Hair")
        layout.addWidget(QLabel("Hair:"))
        layout.addWidget(self.hair)

        self.eyes = QLineEdit()
        self.eyes.setPlaceholderText("Eyes")
        layout.addWidget(QLabel("Eyes:"))
        layout.addWidget(self.eyes)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_person(self):

        # Collect data
        person_data = {
            "name_to_call_me": self.name_to_call_me.text(),
            "first_name": self.first_name.text(),
            "middle_name": self.middle_name.text(),
            "last_name": self.last_name.text(),
            "dob": self.dob.text(),
            "age": self.age.text(),
            "hair": self.hair.text(),
            "eyes": self.eyes.text(),
        }

        # Save to database
        try:
            db.add_person(person_data)
            QMessageBox.information(self, "Success", "Person added successfully!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add person: {e}")
