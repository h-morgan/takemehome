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
    QTabWidget,
    QMenuBar,
)
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtCore import Qt
import takemehome.database as db
from takemehome.ui.add_person import AddPersonWindow
from takemehome import inputs
from loguru import logger

# global, used for window and app icons
ICON_PATH = "takemehome/img/home.png"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Take Me Home")
        self.setGeometry(100, 100, 800, 600)

        # Set the window icon
        self.setWindowIcon(QIcon(ICON_PATH))

        self.menubar = QMenuBar()
        self.create_menu_bar()

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Tab Widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create Tabs
        self.create_tabs()

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
        column_headers = [
            "Name to Call Me",
            "First Name",
            "Middle Name",
            "Last Name",
            "DOB",
            "Age",
            "Hair",
            "Eyes",
            "Race",
            "Sex",
            "Height",
            "Weight",
            "Street",
            "City",
            "State",
            "Zipcode",
            "Special Bracelet ID",
            "Organization",
            "Record Type",
            "Picture Date",
            "Age in Picture",
            "Photo Path",
            "ID",
        ]
        self.results_table.setColumnCount(len(column_headers))
        self.results_table.setHorizontalHeaderLabels(column_headers)
        main_layout.addWidget(self.results_table)
        # Connect the cellClicked signal to a function
        self.results_table.cellClicked.connect(self.on_table_cell_clicked)

        # Connect Buttons
        self.search_button.clicked.connect(self.search_people)
        self.clear_button.clicked.connect(self.clear_search)
        self.add_button.clicked.connect(self.open_add_person_window)

        # Shortcut to reveal hidden buttons
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.reveal_hidden_buttons)

    def create_menu_bar(self):
        file_menu = self.menubar.addMenu("File")
        open_action = file_menu.addAction("Storage settings")

        util_menu = self.menubar.addMenu("Utilities")
        print_action = util_menu.addAction("Print list")
        import_action = util_menu.addAction("Import data")
        export_action = util_menu.addAction("Export data")

        help_menu = self.menubar.addMenu("More")
        about_action = help_menu.addAction("Take Me Home")

    def reveal_hidden_buttons(self, position):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier):
            self.add_button.setVisible(True)

    def create_tabs(self):
        # Demographics Tab
        demographics_tab = QWidget()
        demographics_layout = QVBoxLayout()
        demographics_tab.setLayout(demographics_layout)

        self.dob_field = QLineEdit()
        self.dob_field.setPlaceholderText("YYYY-MM-DD")
        demographics_layout.addWidget(QLabel("Date of Birth:"))
        demographics_layout.addWidget(self.dob_field)

        self.race_field = QComboBox()
        self.race_field.addItems(inputs.RACES)
        demographics_layout.addWidget(QLabel("Race:"))
        demographics_layout.addWidget(self.race_field)

        self.sex_field = QComboBox()
        self.sex_field.addItems(inputs.SEXES)
        demographics_layout.addWidget(QLabel("Sex:"))
        demographics_layout.addWidget(self.sex_field)

        self.hair_field = QComboBox()
        self.hair_field.addItems(inputs.HAIR_COLORS)
        demographics_layout.addWidget(QLabel("Hair:"))
        demographics_layout.addWidget(self.hair_field)

        self.eyes_field = QComboBox()
        self.eyes_field.addItems(inputs.EYE_COLORS)
        demographics_layout.addWidget(QLabel("Eyes:"))
        demographics_layout.addWidget(self.eyes_field)

        # Name Tab
        name_tab = QWidget()
        name_layout = QHBoxLayout()
        name_tab.setLayout(name_layout)

        self.first_name_field = QLineEdit()
        self.first_name_field.setPlaceholderText("First Name")
        name_layout.addWidget(QLabel("First Name:"))
        name_layout.addWidget(self.first_name_field)

        self.last_name_field = QLineEdit()
        self.last_name_field.setPlaceholderText("Last Name")
        name_layout.addWidget(QLabel("Last Name:"))
        name_layout.addWidget(self.last_name_field)

        self.nickname_field = QLineEdit()
        self.nickname_field.setPlaceholderText("Name to Call Me")
        name_layout.addWidget(QLabel("Name to Call Me:"))
        name_layout.addWidget(self.nickname_field)

        # Type/Organizations Tab
        type_org_tab = QWidget()
        type_org_layout = QHBoxLayout()
        type_org_tab.setLayout(type_org_layout)

        self.record_type_field = QLineEdit()
        self.record_type_field.setPlaceholderText("Record Type")
        type_org_layout.addWidget(QLabel("Record Type:"))
        type_org_layout.addWidget(self.record_type_field)

        self.organization_field = QLineEdit()
        self.organization_field.setPlaceholderText("Organization")
        type_org_layout.addWidget(QLabel("Organization:"))
        type_org_layout.addWidget(self.organization_field)

        # Contact Info Tab
        contact_tab = QWidget()
        contact_layout = QHBoxLayout()
        contact_tab.setLayout(contact_layout)

        self.phone_field = QLineEdit()
        self.phone_field.setPlaceholderText("Phone")
        contact_layout.addWidget(QLabel("Phone:"))
        contact_layout.addWidget(self.phone_field)

        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email")
        contact_layout.addWidget(QLabel("Email:"))
        contact_layout.addWidget(self.email_field)

        self.address_field = QLineEdit()
        self.address_field.setPlaceholderText("Address")
        contact_layout.addWidget(QLabel("Address:"))
        contact_layout.addWidget(self.address_field)

        # Add Tabs to TabWidget
        self.tab_widget.addTab(demographics_tab, "Demographics")
        self.tab_widget.addTab(name_tab, "Name")
        self.tab_widget.addTab(type_org_tab, "Type/Organizations")
        self.tab_widget.addTab(contact_tab, "Contact Info")

    def open_add_person_window(self):
        self.add_window = AddPersonWindow()
        self.add_window.show()

    def on_table_cell_clicked(self, row, column):

        logger.debug(f"Row {row} clicked. Opening AddPerson window with data populated")
        # Get the data of the clicked row
        name_to_call_me = self.results_table.item(row, 0)
        first_name = self.results_table.item(row, 1)
        middle_name = self.results_table.item(row, 2)
        last_name = self.results_table.item(row, 3)
        dob = self.results_table.item(row, 4)
        age = self.results_table.item(row, 5)
        hair = self.results_table.item(row, 6)
        eyes = self.results_table.item(row, 7)
        race = self.results_table.item(row, 8)
        sex = self.results_table.item(row, 9)
        height = self.results_table.item(row, 10)
        weight = self.results_table.item(row, 11)
        street = self.results_table.item(row, 12)
        city = self.results_table.item(row, 13)
        state = self.results_table.item(row, 14)
        zipcode = self.results_table.item(row, 15)
        bracelet = self.results_table.item(row, 16)
        org = self.results_table.item(row, 17)
        record_type = self.results_table.item(row, 18)
        pic_date = self.results_table.item(row, 19)
        age_in_pic = self.results_table.item(row, 20)
        photo_path = self.results_table.item(row, 21)
        db_id = self.results_table.item(row, 22)

        person_data = {
            "name_to_call_me": name_to_call_me.text(),
            "first_name": first_name.text(),
            "middle_name": middle_name.text(),
            "last_name": last_name.text(),
            "dob": dob.text(),
            "age": age.text(),
            "hair": hair.text(),
            "eyes": eyes.text(),
            "race": race.text(),
            "sex": sex.text(),
            "height": height.text(),
            "weight": weight.text(),
            "street": street.text(),
            "city": city.text(),
            "state": state.text(),
            "zipcode": zipcode.text(),
            "bracelet": bracelet.text(),
            "org": org.text() if record_type is not None else "",
            "record_type": record_type.text() if record_type is not None else "",
            "pic_date": pic_date.text() if pic_date is not None else "",
            "age_in_pic": age_in_pic.text() if age_in_pic is not None else "",
            "photo_path": photo_path.text() if photo_path is not None else "",
            "db_id": db_id.text(),  # required
        }

        # Open the AddPersonWindow and pass the selected person data
        self.add_person_window = AddPersonWindow(person_data)
        self.add_person_window.show()

    def search_people(self):

        # Get search parameters
        # demographics
        dob = self.dob_field.text()
        race = self.race_field.currentText()
        sex = self.sex_field.currentText()
        hair = self.hair_field.currentText()
        eyes = self.eyes_field.currentText()

        # name
        first_name = self.first_name_field.text()
        last_name = self.last_name_field.text()
        name_to_call = self.nickname_field.text()

        # type/org
        record_type = self.record_type_field.text()
        organization = self.organization_field.text()

        # contact info
        phone = self.phone_field.text()
        email = self.email_field.text()
        addr = self.address_field.text()

        # Fetch results
        results = db.search_people(
            dob=dob,
            race=race,
            sex=sex,
            nickname=name_to_call,
            first_name=first_name,
            last_name=last_name,
            hair=hair,
            eyes=eyes,
        )
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
    # app.setStyle("Fusion")

    # Set the application name (changes the menu bar name)
    QGuiApplication.setApplicationDisplayName("Take Me Home")
    QGuiApplication.setApplicationName("Take Me Home")
    QGuiApplication.setDesktopFileName("take-me-home")

    # Set the application icon that appears in the dock
    app.setWindowIcon(QIcon(ICON_PATH))
    window = MainWindow()
    window.show()
    app.exec()
