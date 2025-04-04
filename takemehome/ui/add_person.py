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
from takemehome import inputs
import shutil
from loguru import logger


class AddPersonWindow(QWidget):
    def __init__(self, person_data=None):
        super().__init__()

        self.setWindowTitle("Add New Person")
        self.setGeometry(150, 150, 600, 600)

        layout = QVBoxLayout()

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(15)

        # Form Fields
        ## Row 0
        self.name_to_call_me = QLineEdit()
        form_layout.addWidget(QLabel("Name to Call Me:"), 0, 0)
        form_layout.addWidget(self.name_to_call_me, 0, 1, 1, 2)

        self.first_name = QLineEdit()
        form_layout.addWidget(QLabel("First Name:"), 0, 3, alignment=Qt.AlignRight)
        form_layout.addWidget(self.first_name, 0, 4, 1, 2)

        ## Row 1
        self.middle_name = QLineEdit()
        form_layout.addWidget(QLabel("Middle Name:"), 1, 0)
        form_layout.addWidget(self.middle_name, 1, 1, 1, 2)

        self.last_name = QLineEdit()
        form_layout.addWidget(QLabel("Last Name:"), 1, 3, alignment=Qt.AlignRight)
        form_layout.addWidget(self.last_name, 1, 4, 1, 2)

        ## Row 2
        self.dob = QLineEdit()
        self.dob.setPlaceholderText("YYYY-MM-DD")
        form_layout.addWidget(QLabel("Date of Birth:"), 2, 0)
        form_layout.addWidget(self.dob, 2, 1, 1, 2)

        self.age = QLineEdit()
        form_layout.addWidget(QLabel("Age:"), 2, 3, alignment=Qt.AlignRight)
        form_layout.addWidget(self.age, 2, 4, 1, 2)

        self.hair = QComboBox()
        self.hair.addItems(inputs.HAIR_COLORS)
        form_layout.addWidget(QLabel("Hair:"), 3, 0)
        form_layout.addWidget(self.hair, 3, 1)

        self.eyes = QComboBox()
        self.eyes.addItems(inputs.EYE_COLORS)
        form_layout.addWidget(QLabel("Eyes:"), 3, 2)
        form_layout.addWidget(self.eyes, 3, 3)

        self.race = QComboBox()
        self.race.addItems(inputs.RACES)
        form_layout.addWidget(QLabel("Race:"), 4, 0)
        form_layout.addWidget(self.race, 4, 1)

        self.sex = QComboBox()
        self.sex.addItems(inputs.SEXES)
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
        self.state.addItems(inputs.STATE_CODES)
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

        if person_data:
            self.populate_existing_data(person_data)

        layout.addLayout(form_layout)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def populate_existing_data(self, person_data):
        logger.debug(f"Populating existing person data: {person_data}")

        # setting existing data - straight text fields use 'setText' method
        # dropdown fields use 'setCurrentText' method
        self.name_to_call_me.setText(person_data.get("name_to_call_me"))
        self.first_name.setText(person_data.get("first_name"))
        self.middle_name.setText(person_data.get("middle_name"))
        self.last_name.setText(person_data.get("last_name"))
        self.dob.setText(person_data.get("dob"))
        self.age.setText(person_data.get("age"))
        self.hair.setCurrentText(person_data.get("hair"))
        self.eyes.setCurrentText(person_data.get("eyes"))
        self.race.setCurrentText(person_data.get("race"))
        self.sex.setCurrentText(person_data.get("sex"))
        self.height.setText(person_data.get("height"))
        self.weight.setText(person_data.get("weight"))
        self.street.setText(person_data.get("street"))
        self.city.setText(person_data.get("city"))
        self.state.setCurrentText(person_data.get("state"))
        self.zipcode.setText(person_data.get("zipcode"))
        self.special_bracelet_id.setText(person_data.get("bracelet"))
        self.organization.setText(person_data.get("org"))
        self.record_type.setText(person_data.get("record_type"))
        self.picture_date.setText(person_data.get("pic_date"))
        self.age_in_picture.setText(person_data.get("age_in_pic"))
        self.photo_path.setText(person_data.get("photo_path"))

        # display thumbnail with photo path
        self.display_thumbnail(person_data.get("photo_path"))

        # TODO - make "save" button turn into "update" button if we're here
        # "save" will trigger a new record to get written to the db
        logger.debug(f"DB ID {person_data.get('db_id')}")

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
            self.display_thumbnail(new_path)

    def display_thumbnail(self, photo_path):
        # Display the image as a thumbnail
        pixmap = QPixmap(photo_path)
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
            "height": self.height.text(),
            "weight": self.weight.text(),
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
