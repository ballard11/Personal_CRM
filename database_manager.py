# database_manager.py

import sqlite3

class DatabaseManager:
    def __init__(self, db_name='personal_crm.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        # Create contacts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                email TEXT,
                phone TEXT,
                birthday TEXT,
                address TEXT,
                category TEXT,
                notes TEXT,
                image BLOB
            )
        ''')
        # Create categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        # Insert default categories if they don't exist
        default_categories = ['Friend', 'Family', 'Work', 'Other']
        for category in default_categories:
            self.cursor.execute('''
                INSERT OR IGNORE INTO categories (name) VALUES (?)
            ''', (category,))
        self.conn.commit()

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
