"""
ДИАГРАММА КОМПОНЕНТОВ
Архитектура компонентов системы
"""

class ComponentDiagram:
    def __init__(self):
        self.components = {
            "GUI Module": [
                "main_window.py",
                "contact_form.py", 
                "search_window.py"
            ],
            "Business Logic": [
                "contact_manager.py",
                "validation.py",
                "search_engine.py"
            ],
            "Data Access": [
                "database.py",
                "models.py"
            ],
            "External Dependencies": [
                "tkinter (UI)",
                "sqlite3 (Database)",
                "os (File system)"
            ]
        }
        self.connections = [
            "GUI Module → Business Logic: передача данных",
            "Business Logic → Data Access: запросы к БД",
            "Data Access → External Dependencies: использование библиотек"
        ]
    
    def display(self):
        print("ДИАГРАММА КОМПОНЕНТОВ")
        print("=" * 40)
        for component, modules in self.components.items():
            print(f"\n{component}:")
            for module in modules:
                print(f"  - {module}")
        
        print("\nСвязи между компонентами:")
        for connection in self.connections:
            print(f"- {connection}")

# Создаем и отображаем диаграмму
component_diagram = ComponentDiagram()
component_diagram.display()