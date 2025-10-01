"""
ГЛАВНЫЙ ФАЙЛ ПРИЛОЖЕНИЯ
АИС "Телефонный справочник"

Запускает графический интерфейс приложения
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Добавляем путь к текущей директории для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import PhoneBookGUI
    from database import Database
    
    def check_dependencies():
        """Проверка наличия всех зависимостей"""
        try:
            # Проверяем подключение к БД
            db = Database()
            if db.connect():
                db.create_tables()
                db.close()
                return True
            return False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка инициализации БД: {e}")
            return False
    
    def main():
        """Основная функция запуска приложения"""
        print("=" * 50)
        print("🚀 ЗАПУСК АИС 'ТЕЛЕФОННЫЙ СПРАВОЧНИК'")
        print("=" * 50)
        
        # Проверяем зависимости
        if not check_dependencies():
            print("❌ Не удалось инициализировать приложение")
            return
        
        print("✅ Все зависимости загружены успешно!")
        print("✅ База данных инициализирована!")
        print("✅ Графический интерфейс готов к запуску!")
        print("-" * 50)
        
        try:
            # Создаем и запускаем приложение
            app = PhoneBookGUI()
            print("🎯 Приложение запущено успешно!")
            print("💡 Подсказка: Используйте интерфейс для управления контактами")
            print("-" * 50)
            
            # Запускаем главный цикл
            app.run()
            
        except Exception as e:
            error_msg = f"Критическая ошибка при запуске: {e}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Ошибка запуска", error_msg)
        
        print("=" * 50)
        print("👋 Приложение завершило работу")
        print("=" * 50)
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    # Если импорт не удался, показываем информационное окно
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно
    
    error_message = f"""
Не удалось запустить приложение!

Отсутствуют необходимые модули:
{e}

Убедитесь, что в папке проекта находятся файлы:
- database.py
- gui.py

Также убедитесь, что установлен Python 3.6+
"""
    
    messagebox.showerror("Ошибка запуска", error_message)
    print("❌ Ошибка импорта модулей:")
    print(f"   {e}")
    sys.exit(1)

except Exception as e:
    # Обработка любых других ошибок
    root = tk.Tk()
    root.withdraw()
    
    messagebox.showerror("Неизвестная ошибка", 
                        f"Произошла непредвиденная ошибка:\n{e}")
    print(f"❌ Неизвестная ошибка: {e}")
    sys.exit(1)