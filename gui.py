from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox, QMessageBox
from PyQt6 import QtGui
from litscholar import LitScholar
import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title, size, and icon
        self.setWindowTitle("Search Results")
        self.setGeometry(200, 200, 500, 300)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        # Create query label
        self.query_label = QLabel("Query:", self)
        self.query_label.move(50, 50)

        # Create query textbox
        self.query_textbox = QLineEdit(self)
        self.query_textbox.setGeometry(120, 50, 200, 25)

        # Create num results label
        self.num_results_label = QLabel("Number of Results:", self)
        self.num_results_label.move(50, 100)

        # Create num results dropdown
        self.num_results_dropdown = QComboBox(self)
        self.num_results_dropdown.setGeometry(250, 100, 70, 25)
        for i in range(1, 1001):
            self.num_results_dropdown.addItem(str(i))

        # Create cited by checkbox
        self.cited_by_checkbox = QCheckBox("Cited By", self)
        self.cited_by_checkbox.setGeometry(50, 150, 150, 25)

        # Add warning label
        self.warning_label = QLabel("Warning: checking this could increase the chance Google blocks your IP.", self)
        self.warning_label.move(50, 175)
        self.warning_label.setStyleSheet("color: red")
        self.warning_label.adjustSize()

        # Create search button
        self.search_button = QPushButton("Search", self)
        self.search_button.setGeometry(50, 200, 100, 30)
        self.search_button.clicked.connect(self.search_results)



    def search_results(self):
        # Get search query
        query = self.query_textbox.text()

        # Get number of results
        num_results = int(self.num_results_dropdown.currentText())

        # Check if cited by checkbox is checked
        if self.cited_by_checkbox.isChecked():
            cited_by = True
        else:
            cited_by = False

        # run original code here
        lit_scholar = LitScholar(
            num_papers=num_results, 
            enable_cited_by=cited_by
        )

        lit_scholar.search(query)
        file_path = lit_scholar.export()

        # Show message box to confirm search completed and Excel file saved
        msg = QMessageBox()
        msg.setWindowTitle("Search Results")
        msg.setText(f"Search completed. Results saved to {file_path} and will be automatically opened.")
        msg.exec()

        # Open Excel at file_path
        os.system(f"start excel.exe {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
