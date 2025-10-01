"""
ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
АИС "Телефонный справочник"
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import Database

class PhoneBookGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Телефонный справочник")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Подключаем базу данных
        self.db = Database()
        self.db.connect()
        self.db.create_tables()
        
        # Создаем интерфейс
        self.create_widgets()
        self.load_contacts()
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_label = ttk.Label(self.root, text="📞 ТЕЛЕФОННЫЙ СПРАВОЧНИК", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Панель поиска
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_contacts)
        
        search_btn = ttk.Button(search_frame, text="Найти", command=self.search_contacts)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="➕ Добавить контакт", 
                  command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✏️ Редактировать", 
                  command=self.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Удалить", 
                  command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Обновить", 
                  command=self.load_contacts).pack(side=tk.LEFT, padx=5)
        
        # Таблица контактов
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Создаем Treeview для отображения контактов
        columns = ("ID", "Имя", "Фамилия", "Телефон", "Email", "Организация")
        self.contacts_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настраиваем заголовки колонок
        for col in columns:
            self.contacts_tree.heading(col, text=col)
            self.contacts_tree.column(col, width=100)
        
        # Scrollbar для таблицы
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=scrollbar.set)
        
        self.contacts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Привязываем двойной клик для редактирования
        self.contacts_tree.bind("<Double-1>", self.on_double_click)
    
    def load_contacts(self):
        """Загрузка контактов из базы данных"""
        # Очищаем таблицу
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT * FROM contacts ORDER BY first_name, last_name")
            contacts = cursor.fetchall()
            
            for contact in contacts:
                self.contacts_tree.insert("", tk.END, values=contact)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить контакты: {e}")
    
    def search_contacts(self, event=None):
        """Поиск контактов"""
        query = self.search_entry.get().strip()
        
        if not query:
            self.load_contacts()
            return
        
        # Очищаем таблицу
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        
        try:
            cursor = self.db.connection.cursor()
            cursor.execute('''
                SELECT * FROM contacts 
                WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY first_name, last_name
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
            
            contacts = cursor.fetchall()
            
            for contact in contacts:
                self.contacts_tree.insert("", tk.END, values=contact)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
    
    def add_contact(self):
        """Добавление нового контакта"""
        self.show_contact_form()
    
    def edit_contact(self):
        """Редактирование выбранного контакта"""
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите контакт для редактирования")
            return
        
        item = selected[0]
        contact_data = self.contacts_tree.item(item)['values']
        self.show_contact_form(contact_data)
    
    def delete_contact(self):
        """Удаление выбранного контакта"""
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите контакт для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить контакт?"):
            item = selected[0]
            contact_id = self.contacts_tree.item(item)['values'][0]
            
            try:
                cursor = self.db.connection.cursor()
                cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
                self.db.connection.commit()
                self.load_contacts()
                messagebox.showinfo("Успех", "Контакт удален")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить контакт: {e}")
    
    def on_double_click(self, event):
        """Обработка двойного клика по контакту"""
        self.edit_contact()
    
    def show_contact_form(self, contact_data=None):
        """Показать форму для добавления/редактирования контакта"""
        form = tk.Toplevel(self.root)
        form.title("Добавить контакт" if not contact_data else "Редактировать контакт")
        form.geometry("450x350")
        form.resizable(False, False)
        
        # Основной фрейм для отступов
        main_frame = ttk.Frame(form, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Поля формы
        ttk.Label(main_frame, text="Имя:*", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        first_name_entry = ttk.Entry(main_frame, width=30, font=("Arial", 10))
        first_name_entry.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        
        ttk.Label(main_frame, text="Фамилия:*", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        last_name_entry = ttk.Entry(main_frame, width=30, font=("Arial", 10))
        last_name_entry.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
        
        ttk.Label(main_frame, text="Телефон:*", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(main_frame, width=30, font=("Arial", 10))
        phone_entry.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)
        
        ttk.Label(main_frame, text="Email:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(main_frame, width=30, font=("Arial", 10))
        email_entry.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)
        
        ttk.Label(main_frame, text="Организация:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        org_entry = ttk.Entry(main_frame, width=30, font=("Arial", 10))
        org_entry.grid(row=4, column=1, pady=5, padx=10, sticky=tk.W)
        
        # Подсказка об обязательных полях
        help_label = ttk.Label(main_frame, text="* - обязательные поля", font=("Arial", 8), foreground="gray")
        help_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Если редактируем, заполняем поля
        if contact_data:
            first_name_entry.insert(0, contact_data[1])
            last_name_entry.insert(0, contact_data[2])
            phone_entry.insert(0, contact_data[3])
            email_entry.insert(0, contact_data[4] if contact_data[4] else "")
            org_entry.insert(0, contact_data[5] if contact_data[5] else "")
        
        def save_contact():
            """Сохранение контакта"""
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            organization = org_entry.get().strip()
            
            if not first_name or not last_name or not phone:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля (Имя, Фамилия, Телефон)")
                return
            
            try:
                cursor = self.db.connection.cursor()
                
                if contact_data:  # Редактирование
                    cursor.execute('''
                        UPDATE contacts 
                        SET first_name=?, last_name=?, phone=?, email=?, organization=?
                        WHERE id=?
                    ''', (first_name, last_name, phone, email, organization, contact_data[0]))
                else:  # Добавление
                    cursor.execute('''
                        INSERT INTO contacts (first_name, last_name, phone, email, organization)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (first_name, last_name, phone, email, organization))
                
                self.db.connection.commit()
                form.destroy()
                self.load_contacts()
                messagebox.showinfo("Успех", "Контакт сохранен")
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Контакт с таким номером телефона уже существует")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить контакт: {e}")
        
        # Фрейм для кнопок внизу формы
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # КНОПКИ СОХРАНИТЬ И ОТМЕНА (теперь они точно видны!)
        save_btn = ttk.Button(button_frame, text="💾 Сохранить", 
                             command=save_contact)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(button_frame, text="❌ Отмена", 
                               command=form.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Фокус на первом поле
        first_name_entry.focus()
        
        # Обработка нажатия Enter для сохранения
        form.bind('<Return>', lambda event: save_contact())
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()
        # При закрытии приложения закрываем соединение с БД
        self.db.close()

# Запуск приложения
if __name__ == "__main__":
    app = PhoneBookGUI()
    app.run()