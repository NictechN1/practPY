"""
ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
АИС "Телефонный справочник"
"""

import tkinter as tk
from tkinter import ttk, messagebox
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
        form.geometry("400x300")
        form.resizable(False, False)
        
        # Поля формы
        ttk.Label(form, text="Имя:").pack(pady=5)
        first_name_entry = ttk.Entry(form, width=30)
        first_name_entry.pack(pady=5)
        
        ttk.Label(form, text="Фамилия:").pack(pady=5)
        last_name_entry = ttk.Entry(form, width=30)
        last_name_entry.pack(pady=5)
        
        ttk.Label(form, text="Телефон:").pack(pady=5)
        phone_entry = ttk.Entry(form, width=30)
        phone_entry.pack(pady=5)
        
        ttk.Label(form, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(form, width=30)
        email_entry.pack(pady=5)
        
        ttk.Label(form, text="Организация:").pack(pady=5)
        org_entry = ttk.Entry(form, width=30)
        org_entry.pack(pady=5)
        
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
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить контакт: {e}")
        
        # Кнопки формы
        button_frame = ttk.Frame(form)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="💾 Сохранить", 
                  command=save_contact).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ Отмена", 
                  command=form.destroy).pack(side=tk.LEFT, padx=10)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()
        # При закрытии приложения закрываем соединение с БД
        self.db.close()

# Запуск приложения
if __name__ == "__main__":
    app = PhoneBookGUI()
    app.run()