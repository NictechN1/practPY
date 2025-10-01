"""
МОДУЛЬ БАЗЫ ДАННЫХ
АИС "Телефонный справочник"
"""

import sqlite3

class Database:
    def __init__(self, db_name="phonebook.db"):
        self.db_name = db_name
        self.connection = None
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("✅ База данных подключена успешно!")
            return True
        except sqlite3.Error as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            return False
    
    def create_tables(self):
        """Создание таблиц в базе данных"""
        try:
            cursor = self.connection.cursor()
            
            # Создание таблицы контактов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL, 
                    phone TEXT NOT NULL UNIQUE,
                    email TEXT,
                    organization TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.connection.commit()
            print("✅ Таблицы созданы успешно!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Ошибка создания таблиц: {e}")
            return False
    
    def close(self):
        """Закрытие соединения с БД"""
        if self.connection:
            self.connection.close()
            print("✅ Соединение с БД закрыто")

# Тестируем работу с БД
if __name__ == "__main__":
    db = Database()
    if db.connect():
        db.create_tables()
        db.close()