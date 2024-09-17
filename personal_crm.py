import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QComboBox
from PyQt5.QtCore import Qt
import sqlite3
import json
from datetime import datetime

class PersonalCRM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal CRM")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()
        self.init_db()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # Left panel for contact list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        self.contact_list = QListWidget()
        self.contact_list.itemClicked.connect(self.load_contact)
        left_layout.addWidget(QLabel("Contacts"))
        left_layout.addWidget(self.contact_list)
        left_panel.setLayout(left_layout)

        # Right panel for contact details
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.birthday_input = QLineEdit()
        self.address_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Friend", "Family", "Work", "Other"])
        self.notes_input = QTextEdit()

        right_layout.addWidget(QLabel("Name"))
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(QLabel("Email"))
        right_layout.addWidget(self.email_input)
        right_layout.addWidget(QLabel("Phone"))
        right_layout.addWidget(self.phone_input)
        right_layout.addWidget(QLabel("Birthday"))
        right_layout.addWidget(self.birthday_input)
        right_layout.addWidget(QLabel("Address"))
        right_layout.addWidget(self.address_input)
        right_layout.addWidget(QLabel("Category"))
        right_layout.addWidget(self.category_input)
        right_layout.addWidget(QLabel("Notes"))
        right_layout.addWidget(self.notes_input)

        save_button = QPushButton("Save Contact")
        save_button.clicked.connect(self.save_contact)
        right_layout.addWidget(save_button)

        export_button = QPushButton("Export Data")
        export_button.clicked.connect(self.export_data)
        right_layout.addWidget(export_button)

        right_panel.setLayout(right_layout)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        central_widget.setLayout(main_layout)

    def init_db(self):
        self.conn = sqlite3.connect('personal_crm.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts
            (id INTEGER PRIMARY KEY,
             name TEXT,
             email TEXT,
             phone TEXT,
             birthday TEXT,
             address TEXT,
             category TEXT,
             notes TEXT)
        ''')
        self.conn.commit()
        self.load_contacts()

    def load_contacts(self):
        self.contact_list.clear()
        self.cursor.execute("SELECT name FROM contacts")
        contacts = self.cursor.fetchall()
        for contact in contacts:
            self.contact_list.addItem(contact[0])

    def load_contact(self, item):
        name = item.text()
        self.cursor.execute("SELECT * FROM contacts WHERE name=?", (name,))
        contact = self.cursor.fetchone()
        if contact:
            self.name_input.setText(contact[1])
            self.email_input.setText(contact[2])
            self.phone_input.setText(contact[3])
            self.birthday_input.setText(contact[4])
            self.address_input.setText(contact[5])
            self.category_input.setCurrentText(contact[6])
            self.notes_input.setPlainText(contact[7])

    def save_contact(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        birthday = self.birthday_input.text()
        address = self.address_input.text()
        category = self.category_input.currentText()
        notes = self.notes_input.toPlainText()

        self.cursor.execute('''
            INSERT OR REPLACE INTO contacts
            (name, email, phone, birthday, address, category, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, birthday, address, category, notes))
        self.conn.commit()
        self.load_contacts()

    def export_data(self):
        self.cursor.execute("SELECT * FROM contacts")
        contacts = self.cursor.fetchall()
        data = []
        for contact in contacts:
            data.append({
                "name": contact[1],
                "email": contact[2],
                "phone": contact[3],
                "birthday": contact[4],
                "address": contact[5],
                "category": contact[6],
                "notes": contact[7]
            })
        with open(f"crm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    crm = PersonalCRM()
    crm.show()
    sys.exit(app.exec_())