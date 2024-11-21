import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)
from PySide6.QtGui import QPixmap
from takemehome.database import save_person, get_people


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Take Me Home")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        self.label = QLabel("Person Details Viewer")
        layout.addWidget(self.label)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # Load image button
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        # Add person button
        self.add_button = QPushButton("Add Person")
        self.add_button.clicked.connect(self.add_person)
        layout.addWidget(self.add_button)

        # Container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image")
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200))  # Resize for display

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
