import sys
import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QComboBox,
    QDateEdit, QFormLayout, QFileDialog, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QDate, QRegExp
from controller import Controller
from models import Contact
import json
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.basicConfig(level=logging.INFO)

class PersonalCRM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal CRM")
        self.setGeometry(100, 100, 700, 450)
        self.controller = Controller()
        self.current_contact = None
        self.init_ui()
        self.load_contacts()

    def init_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # Left panel for contacts and search
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Contacts")
        self.search_bar.textChanged.connect(self.search_contacts)
        left_layout.addWidget(self.search_bar)

        # Contact list
        self.contact_list = QListWidget()
        self.contact_list.itemClicked.connect(self.load_contact)
        left_layout.addWidget(self.contact_list)

        left_panel.setLayout(left_layout)

        # Right panel for contact details
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Name
        self.name_input = QLineEdit()
        form_layout.addRow("Name", self.name_input)

        # Email with validation
        self.email_input = QLineEdit()
        email_regex = QRegExp(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        self.email_input.setValidator(QRegExpValidator(email_regex))
        form_layout.addRow("Email", self.email_input)

        # Phone with validation
        self.phone_input = QLineEdit()
        phone_regex = QRegExp(r'^\+?\d{10,15}$')
        self.phone_input.setValidator(QRegExpValidator(phone_regex))
        form_layout.addRow("Phone", self.phone_input)

        # Birthday with date picker
        self.birthday_input = QDateEdit()
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDisplayFormat('yyyy-MM-dd')
        form_layout.addRow("Birthday", self.birthday_input)

        # Address
        self.address_input = QLineEdit()
        form_layout.addRow("Address", self.address_input)

        # Category with management
        category_layout = QHBoxLayout()
        self.category_input = QComboBox()
        self.category_input.addItems(self.controller.get_categories())
        category_layout.addWidget(self.category_input)
        manage_cat_btn = QPushButton("Manage")
        manage_cat_btn.clicked.connect(self.manage_categories)
        category_layout.addWidget(manage_cat_btn)
        form_layout.addRow("Category", category_layout)

        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setFixedHeight(100)
        form_layout.addRow("Notes", self.notes_input)

        right_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Contact")
        save_btn.clicked.connect(self.save_contact)
        delete_btn = QPushButton("Delete Contact")
        delete_btn.clicked.connect(self.delete_contact)
        export_btn = QPushButton("Export Data")
        export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(export_btn)
        right_layout.addLayout(button_layout)

        right_panel.setLayout(right_layout)

        # Assemble main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        central_widget.setLayout(main_layout)

    def load_contacts(self):
        self.contact_list.clear()
        contacts = self.controller.get_contacts()
        for contact in contacts:
            self.contact_list.addItem(contact.name)

    def load_contact(self, item):
        name = item.text()
        contact = self.controller.get_contact(name)
        if contact:
            self.current_contact = contact
            self.name_input.setText(contact.name)
            self.email_input.setText(contact.email)
            self.phone_input.setText(contact.phone)
            if contact.birthday:
                date = QDate.fromString(contact.birthday, 'yyyy-MM-dd')
                self.birthday_input.setDate(date)
            else:
                self.birthday_input.setDate(QDate.currentDate())
            self.address_input.setText(contact.address)
            self.category_input.setCurrentText(contact.category)
            self.notes_input.setPlainText(contact.notes)
            logging.info(f"Loaded contact: {contact.name}")
        else:
            logging.warning(f"Failed to load contact: {name}")

    def save_contact(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, "Input Error", "Name is required.")
            return
        email = self.email_input.text()
        phone = self.phone_input.text()
        birthday = self.birthday_input.date().toString('yyyy-MM-dd')
        address = self.address_input.text()
        category = self.category_input.currentText()
        notes = self.notes_input.toPlainText()

        contact = Contact(
            id=self.current_contact.id if self.current_contact else None,
            name=name,
            email=email,
            phone=phone,
            birthday=birthday,
            address=address,
            category=category,
            notes=notes
        )
        self.controller.save_contact(contact)
        self.load_contacts()
        QMessageBox.information(self, "Success", "Contact saved successfully.")
        logging.info(f"Saved contact: {name}")

    def delete_contact(self):
        if not self.current_contact:
            QMessageBox.warning(self, "Delete Error", "No contact selected.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {self.current_contact.name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.delete_contact(self.current_contact.id)
            self.clear_inputs()
            self.load_contacts()
            QMessageBox.information(self, "Deleted", "Contact deleted successfully.")
            logging.info(f"Deleted contact: {self.current_contact.name}")

    def clear_inputs(self):
        self.current_contact = None
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.birthday_input.setDate(QDate.currentDate())
        self.address_input.clear()
        self.notes_input.clear()

    def export_data(self):
        contacts = self.controller.get_contacts()
        data = []
        for contact in contacts:
            data.append({
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone,
                'birthday': contact.birthday,
                'address': contact.address,
                'category': contact.category,
                'notes': contact.notes
            })
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export Data",
            f"crm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    json.dump(data, f, indent=2)
                QMessageBox.information(self, "Export Successful", "Data exported successfully.")
                logging.info(f"Exported data to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"An error occurred: {e}")

    def manage_categories(self):
        category, ok = QInputDialog.getText(self, "Add Category", "Category Name:")
        if ok and category:
            self.controller.add_category(category)
            self.category_input.addItem(category)
            QMessageBox.information(self, "Category Added", f"Category '{category}' added.")
            logging.info(f"Added new category: {category}")

    def search_contacts(self, text):
        for index in range(self.contact_list.count()):
            item = self.contact_list.item(index)
            item.setHidden(text.lower() not in item.text().lower())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonalCRM()
    window.show()
    sys.exit(app.exec_())