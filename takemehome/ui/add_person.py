import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QGridLayout,
    QComboBox,
    QHBoxLayout,
    QFileDialog,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import takemehome.database as db
import shutil


class AddPersonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Person")
        self.setGeometry(150, 150, 600, 600)

        layout = QVBoxLayout()

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(15)

        # Form Fields
        self.name_to_call_me = QLineEdit()
        form_layout.addWidget(QLabel("Name to Call Me:"), 0, 0)
        form_layout.addWidget(self.name_to_call_me, 0, 1, 1, 1)

        self.first_name = QLineEdit()
        form_layout.addWidget(QLabel("First Name:"), 1, 0)
        form_layout.addWidget(self.first_name, 1, 1)

        self.middle_name = QLineEdit()
        form_layout.addWidget(QLabel("Middle Name:"), 1, 2)
        form_layout.addWidget(self.middle_name, 1, 3)

        self.last_name = QLineEdit()
        form_layout.addWidget(QLabel("Last Name:"), 1, 4)
        form_layout.addWidget(self.last_name, 1, 5)

        self.dob = QLineEdit()
        self.dob.setPlaceholderText("YYYY-MM-DD")
        form_layout.addWidget(QLabel("Date of Birth:"), 2, 0)
        form_layout.addWidget(self.dob, 2, 1)

        self.age = QLineEdit()
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

        self.height = QLineEdit()
        self.height.setPlaceholderText("Inches")
        form_layout.addWidget(QLabel("Height:"), 5, 0)
        form_layout.addWidget(self.height, 5, 1)

        self.weight = QLineEdit()
        self.weight.setPlaceholderText("Pounds")
        form_layout.addWidget(QLabel("Weight:"), 5, 2)
        form_layout.addWidget(self.weight, 5, 3)

        self.street = QLineEdit()
        self.street.setPlaceholderText("Street address")
        form_layout.addWidget(QLabel("Address:"), 6, 0)
        form_layout.addWidget(self.street, 6, 1, 1, 5)

        self.city = QLineEdit()
        form_layout.addWidget(QLabel("City:"), 7, 0)
        form_layout.addWidget(self.city, 7, 1)

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
        form_layout.addWidget(QLabel("State:"), 7, 2)
        form_layout.addWidget(self.state, 7, 3)

        self.zipcode = QLineEdit()
        form_layout.addWidget(QLabel("Zip Code:"), 7, 4)
        form_layout.addWidget(self.zipcode, 7, 5)

        self.special_bracelet_id = QLineEdit()
        self.special_bracelet_id.setPlaceholderText("Special Bracelet ID")
        form_layout.addWidget(QLabel("Special Bracelet ID:"), 8, 0)
        form_layout.addWidget(self.special_bracelet_id, 8, 1, 1, 5)

        self.organization = QLineEdit()
        self.organization.setPlaceholderText("Organization")
        form_layout.addWidget(QLabel("Organization:"), 9, 0)
        form_layout.addWidget(self.organization, 9, 1, 1, 5)

        self.record_type = QLineEdit()
        self.record_type.setPlaceholderText("Record Type")
        form_layout.addWidget(QLabel("Record Type:"), 10, 0)
        form_layout.addWidget(self.record_type, 10, 1, 1, 5)

        self.picture_date = QLineEdit()
        self.picture_date.setPlaceholderText("YYYY-MM-DD")
        form_layout.addWidget(QLabel("Picture Date:"), 11, 0)
        form_layout.addWidget(self.picture_date, 11, 1)

        self.age_in_picture = QLineEdit()
        form_layout.addWidget(QLabel("Age in Picture:"), 11, 2)
        form_layout.addWidget(self.age_in_picture, 11, 3)

        self.photo_path = QLineEdit()
        self.photo_path.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.upload_photo)

        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.browse_button)
        form_layout.addWidget(QLabel("Photo:"), 12, 0)
        form_layout.addLayout(photo_layout, 12, 1, 1, 2)

        self.photo_path = QLineEdit()
        self.photo_path.setPlaceholderText("Photo Path")
        form_layout.addWidget(QLabel("Photo Path:"), 13, 0)
        form_layout.addWidget(self.photo_path, 13, 1, 1, 5)

        # Thumbnail Display
        self.photo_thumbnail = QLabel(self)
        self.photo_thumbnail.setFixedSize(100, 100)  # Set size for thumbnail
        form_layout.addWidget(self.photo_thumbnail, 14, 2, 2, 2)

        layout.addLayout(form_layout)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            # Define storage directory
            save_dir = "photos"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Save the file in the app's directory
            file_name = os.path.basename(file_path)
            new_path = os.path.join(save_dir, file_name)
            shutil.copy(file_path, new_path)

            self.photo_path.setText(new_path)

            # Display the image as a thumbnail
            pixmap = QPixmap(new_path)
            self.photo_thumbnail.setPixmap(
                pixmap.scaled(100, 100)
            )  # Scale image to fit the QLabel

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
