# models.py

from database_manager import DatabaseManager

class Contact:
    def __init__(self, id=None, name='', email='', phone='', birthday='', address='', category='', notes='', image=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.address = address
        self.category = category
        self.notes = notes
        self.image = image  # Binary data for the profile picture

class Model:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_contacts(self):
        contacts_data = self.db.fetchall("SELECT * FROM contacts")
        contacts = []
        for data in contacts_data:
            contact = Contact(*data)
            contacts.append(contact)
        return contacts

    def get_contact_by_name(self, name):
        data = self.db.fetchone("SELECT * FROM contacts WHERE name=?", (name,))
        return Contact(*data) if data else None

    def save_contact(self, contact):
        if contact.id:
            # Update existing contact
            self.db.execute('''
                UPDATE contacts SET
                    name=?, email=?, phone=?, birthday=?, address=?, category=?, notes=?, image=?
                WHERE id=?
            ''', (contact.name, contact.email, contact.phone, contact.birthday, contact.address,
                  contact.category, contact.notes, contact.image, contact.id))
        else:
            # Insert new contact
            self.db.execute('''
                INSERT INTO contacts (name, email, phone, birthday, address, category, notes, image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (contact.name, contact.email, contact.phone, contact.birthday, contact.address,
                  contact.category, contact.notes, contact.image))

    def delete_contact(self, contact_id):
        self.db.execute("DELETE FROM contacts WHERE id=?", (contact_id,))

    def get_categories(self):
        categories = self.db.fetchall("SELECT name FROM categories")
        return [category[0] for category in categories]

    def add_category(self, category_name):
        self.db.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
