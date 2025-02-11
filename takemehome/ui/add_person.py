from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QGridLayout,
    QComboBox,
)
from PySide6.QtCore import Qt
import takemehome.database as db


class AddPersonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Person")
        self.setGeometry(150, 150, 600, 600)

        layout = QVBoxLayout()

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)

        # Form Fields
        self.name_to_call_me = QLineEdit()
        self.name_to_call_me.setPlaceholderText("Name to Call Me")
        form_layout.addWidget(QLabel("Name to Call Me:"), 0, 0)
        form_layout.addWidget(self.name_to_call_me, 0, 1, 1, 1)

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        form_layout.addWidget(QLabel("First Name:"), 1, 0)
        form_layout.addWidget(self.first_name, 1, 1)

        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name")
        form_layout.addWidget(QLabel("Middle Name:"), 1, 2)
        form_layout.addWidget(self.middle_name, 1, 3)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        form_layout.addWidget(QLabel("Last Name:"), 1, 4)
        form_layout.addWidget(self.last_name, 1, 5)

        self.dob = QLineEdit()
        self.dob.setPlaceholderText("Date of Birth (YYYY-MM-DD)")
        form_layout.addWidget(QLabel("Date of Birth:"), 2, 0)
        form_layout.addWidget(self.dob, 2, 1)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        form_layout.addWidget(QLabel("Age:"), 2, 2)
        form_layout.addWidget(self.age, 2, 3)

        self.hair = QComboBox()
        self.hair.addItems(
            ["", "Black", "Brown", "Blonde", "Red", "Gray", "White", "Other"]
        )
        form_layout.addWidget(QLabel("Hair:"), 3, 0)
        form_layout.addWidget(self.hair, 3, 1)

        self.eyes = QComboBox()
        self.eyes.addItems(["", "Brown", "Blue", "Green", "Hazel", "Gray", "Other"])
        form_layout.addWidget(QLabel("Eyes:"), 3, 2)
        form_layout.addWidget(self.eyes, 3, 3)

        self.race = QComboBox()
        self.race.addItems(["", "White", "Black", "Asian", "Hispanic", "Other"])
        form_layout.addWidget(QLabel("Race:"), 4, 0)
        form_layout.addWidget(self.race, 4, 1)

        self.sex = QComboBox()
        self.sex.addItems(["", "Male", "Female"])
        form_layout.addWidget(QLabel("Sex:"), 4, 2)
        form_layout.addWidget(self.sex, 4, 3)

        self.street = QLineEdit()
        self.street.setPlaceholderText("Street")
        form_layout.addWidget(QLabel("Street:"), 5, 0)
        form_layout.addWidget(self.street, 5, 1, 1, 5)

        self.city = QLineEdit()
        self.city.setPlaceholderText("City")
        form_layout.addWidget(QLabel("City:"), 6, 0)
        form_layout.addWidget(self.city, 6, 1)

        self.state = QComboBox()
        self.state.addItems(
            [
                "",
                "AL",
                "AK",
                "AZ",
                "AR",
                "CA",
                "CO",
                "CT",
                "DE",
                "FL",
                "GA",
                "HI",
                "ID",
                "IL",
                "IN",
                "IA",
                "KS",
                "KY",
                "LA",
                "ME",
                "MD",
                "MA",
                "MI",
                "MN",
                "MS",
                "MO",
                "MT",
                "NE",
                "NV",
                "NH",
                "NJ",
                "NM",
                "NY",
                "NC",
                "ND",
                "OH",
                "OK",
                "OR",
                "PA",
                "RI",
                "SC",
                "SD",
                "TN",
                "TX",
                "UT",
                "VT",
                "VA",
                "WA",
                "WV",
                "WI",
                "WY",
            ]
        )
        form_layout.addWidget(QLabel("State:"), 6, 2)
        form_layout.addWidget(self.state, 6, 3)

        self.zipcode = QLineEdit()
        self.zipcode.setPlaceholderText("Zip Code")
        form_layout.addWidget(QLabel("Zip Code:"), 6, 4)
        form_layout.addWidget(self.zipcode, 6, 5)

        self.special_bracelet_id = QLineEdit()
        self.special_bracelet_id.setPlaceholderText("Special Bracelet ID")
        form_layout.addWidget(QLabel("Special Bracelet ID:"), 7, 0)
        form_layout.addWidget(self.special_bracelet_id, 7, 1, 1, 5)

        self.organization = QLineEdit()
        self.organization.setPlaceholderText("Organization")
        form_layout.addWidget(QLabel("Organization:"), 8, 0)
        form_layout.addWidget(self.organization, 8, 1, 1, 5)

        self.record_type = QLineEdit()
        self.record_type.setPlaceholderText("Record Type")
        form_layout.addWidget(QLabel("Record Type:"), 9, 0)
        form_layout.addWidget(self.record_type, 9, 1, 1, 5)

        self.picture_date = QLineEdit()
        self.picture_date.setPlaceholderText("Picture Date (YYYY-MM-DD)")
        form_layout.addWidget(QLabel("Picture Date:"), 10, 0)
        form_layout.addWidget(self.picture_date, 10, 1)

        self.age_in_picture = QLineEdit()
        self.age_in_picture.setPlaceholderText("Age in Picture")
        form_layout.addWidget(QLabel("Age in Picture:"), 10, 2)
        form_layout.addWidget(self.age_in_picture, 10, 3)

        self.photo_path = QLineEdit()
        self.photo_path.setPlaceholderText("Photo Path")
        form_layout.addWidget(QLabel("Photo Path:"), 11, 0)
        form_layout.addWidget(self.photo_path, 11, 1, 1, 5)

        layout.addLayout(form_layout)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_person(self):

        # Collect data
        person_data = {
            "first_name": self.first_name.text(),
            "middle_name": self.middle_name.text(),
            "last_name": self.last_name.text(),
            "name_to_call_me": self.name_to_call_me.text(),
            "dob": self.dob.text(),
            "age": self.age.text(),
            "hair": self.hair.currentText(),
            "eyes": self.eyes.currentText(),
            "race": self.race.currentText(),
            "sex": self.sex.currentText(),
            "street": self.street.text(),
            "city": self.city.text(),
            "state": self.state.currentText(),
            "zipcode": self.zipcode.text(),
            "special_bracelet_id": self.special_bracelet_id.text(),
            "organization": self.organization.text(),
            "record_type": self.record_type.text(),
            "picture_date": self.picture_date.text(),
            "age_in_picture": self.age_in_picture.text(),
            "photo_path": self.photo_path.text(),
        }

        # Save to database
        try:
            db.add_person(person_data)
            QMessageBox.information(self, "Success", "Person added successfully!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add person: {e}")
