# controller.py

from models import Model

class Controller:
    def __init__(self):
        self.model = Model()

    def get_contacts(self):
        return self.model.get_all_contacts()

    def get_contact(self, name):
        return self.model.get_contact_by_name(name)

    def save_contact(self, contact):
        self.model.save_contact(contact)

    def delete_contact(self, contact_id):
        self.model.delete_contact(contact_id)

    def get_categories(self):
        return self.model.get_categories()

    def add_category(self, category_name):
        self.model.add_category(category_name)
