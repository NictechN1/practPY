"""
АРХИТЕКТУРА АИС "Телефонный справочник"
"""

class Database:
    def __init__(self):
        pass
    
    def connect(self):
        print("Подключение к БД")
    
    def create_tables(self):
        print("Создание таблиц")

class ContactManager:
    def __init__(self):
        self.db = Database()
    
    def add_contact(self, name, phone):
        print(f"Добавлен контакт: {name}, {phone}")

class GUI:
    def __init__(self):
        self.manager = ContactManager()