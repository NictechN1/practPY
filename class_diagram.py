"""
ДИАГРАММА КЛАССОВ
АИС "Телефонный справочник"

Классы и их атрибуты:
"""

class ClassDiagram:
    def __init__(self):
        self.classes = {
            "Contact": [
                "- contact_id: int",
                "- first_name: str", 
                "- last_name: str",
                "- phone: str",
                "- email: str",
                "- organization: str",
                "+ add_contact()",
                "+ update_contact()",
                "+ delete_contact()"
            ],
            "PhoneBook": [
                "- contacts: List[Contact]",
                "- db_connection: Connection",
                "+ search_contacts()",
                "+ export_contacts()",
                "+ import_contacts()"
            ],
            "Database": [
                "- db_path: str",
                "+ connect()",
                "+ create_tables()",
                "+ execute_query()"
            ],
            "GUI": [
                "- phone_book: PhoneBook",
                "+ show_main_window()",
                "+ show_add_contact_form()",
                "+ show_search_results()"
            ]
        }
    
    def display(self):
        print("ДИАГРАММА КЛАССОВ - АИС 'Телефонный справочник'")
        print("=" * 50)
        for class_name, attributes in self.classes.items():
            print(f"\n{class_name}:")
            for attr in attributes:
                print(f"  {attr}")

# Создаем и отображаем диаграмму
class_diagram = ClassDiagram()
class_diagram.display()