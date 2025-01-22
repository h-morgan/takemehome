# ui.py - UI Setup and Logic
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QComboBox,
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Take Me Home")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Search Area
        search_layout = QHBoxLayout()

        self.dob_field = QLineEdit()
        self.dob_field.setPlaceholderText("Date of Birth")
        search_layout.addWidget(QLabel("Date of Birth:"))
        search_layout.addWidget(self.dob_field)

        self.race_field = QComboBox()
        self.race_field.addItems(["", "White", "Black", "Asian", "Hispanic", "Other"])
        search_layout.addWidget(QLabel("Race:"))
        search_layout.addWidget(self.race_field)

        self.sex_field = QComboBox()
        self.sex_field.addItems(["", "Male", "Female"])
        search_layout.addWidget(QLabel("Sex:"))
        search_layout.addWidget(self.sex_field)

        self.hair_field = QLineEdit()
        self.hair_field.setPlaceholderText("Hair")
        search_layout.addWidget(QLabel("Hair:"))
        search_layout.addWidget(self.hair_field)

        self.eyes_field = QLineEdit()
        self.eyes_field.setPlaceholderText("Eyes")
        search_layout.addWidget(QLabel("Eyes:"))
        search_layout.addWidget(self.eyes_field)

        main_layout.addLayout(search_layout)

        # Advanced Search Checkbox
        self.advanced_search_checkbox = QCheckBox("Advanced Search Enabled")
        main_layout.addWidget(self.advanced_search_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.clear_button = QPushButton("Clear")
        self.add_button = QPushButton("Add")
        self.add_button.setVisible(False)  # Hidden by default

        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.add_button)
        main_layout.addLayout(button_layout)

        # Table for Results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setHorizontalHeaderLabels(
            [
                "First Name",
                "Middle Name",
                "Last Name",
                "Name to Call Me",
                "DOB",
                "Age",
                "Hair",
                "Eyes",
            ]
        )
        main_layout.addWidget(self.results_table)

        # Connect Buttons
        self.search_button.clicked.connect(self.search_people)
        self.clear_button.clicked.connect(self.clear_search)
        self.add_button.clicked.connect(self.open_add_person_window)

        # Shortcut to reveal hidden buttons
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.reveal_hidden_buttons)

    def reveal_hidden_buttons(self, position):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier):
            self.add_button.setVisible(True)

    def open_add_person_window(self):
        self.add_window = AddPersonWindow()
        self.add_window.show()

    def search_people(self):

        # Get search parameters
        dob = self.dob_field.text()
        hair = self.hair_field.text()
        eyes = self.eyes_field.text()

        # Fetch results
        results = db.search_people(dob=dob, hair=hair, eyes=eyes)
        print(results)

        # Populate the table
        self.results_table.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                self.results_table.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(col_data))
                )

    def clear_search(self):
        # Clear all fields and the table
        self.dob_field.clear()
        self.race_field.setCurrentIndex(0)
        self.sex_field.setCurrentIndex(0)
        self.hair_field.clear()
        self.eyes_field.clear()
        self.results_table.setRowCount(0)


# Function to run the app
def run_app():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
