import tkinter as tk
from tkinter import ttk

class PhoneBook:
    def __init__(self):
        self.root = tk.Tk()  # <- исправлено
        self.root.title("Телефонный справочник")
        self.root.geometry("600x400")
        
        # Здесь будем добавлять элементы интерфейса
        label = ttk.Label(self.root, text="Добро пожаловать в телефонный справочник!")  # <- исправлено
        label.pack(pady=10)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PhoneBook()
    app.run()