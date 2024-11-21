import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)
from takemehome.database import save_person, get_people


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Take Me Home")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        # Search section
        search_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name")
        search_layout.addWidget(self.name_input)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter age")
        search_layout.addWidget(self.age_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_people)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        # Table section for displaying results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["ID", "Name", "Age"])
        layout.addWidget(self.results_table)

        # Container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search_people(self):
        """Search for people in the database based on name or age."""
        name_query = self.name_input.text()
        age_query = self.age_input.text()

        # Query the database
        results = get_people(name=name_query, age=age_query)

        # Populate the results table
        self.results_table.setRowCount(0)  # Clear previous results
        for row_idx, (person_id, name, age, _) in enumerate(results):
            self.results_table.insertRow(row_idx)
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(str(person_id)))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(str(age)))

    def add_person(self):
        # Example of adding a person (extend with input forms as needed)
        name = "John Doe"
        age = 30
        photo_path = "path/to/photo.jpg"
        save_person(name, age, photo_path)
        self.label.setText("Person added: John Doe")


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
